from openai import AzureOpenAI
import base64
from typing import Optional, Dict, Any, List
import os
from pathlib import Path
import json
import csv
from tqdm import tqdm
import time
from .preprocessor import ImagePreprocessor


class ImageCaptioner:
    """Handles image captioning using Azure OpenAI's GPT-4V model."""

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        deployment_name: str,
        api_version: str = "2024-02-15-preview",
    ) -> None:
        """Initialize the ImageCaptioner."""
        self.deployment_name = deployment_name
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            base_url=f"{endpoint}/openai/deployments/{deployment_name}",
        )
        self.preprocessor = ImagePreprocessor()

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _get_system_prompt(self) -> str:
        """Get the system prompt for image captioning."""
        return (
            "Directly describe the scene or characters with brevity and "
            "precision. Follow these rules:\n"
            "1. DO NOT use introductory phrases\n"
            "2. Start describing immediately\n"
            "3. Use commas to separate elements\n"
            "4. Refer to animated characters as regular humans\n"
            "5. Make no reference to specific franchises\n"
            "6. Focus on main subjects and actions\n"
            "7. Detect gender and describe accordingly\n"
            "8. DO NOT end with a period\n"
            "9. ALWAYS IDENTIFY THE GENDER OF THE MAIN SUBJECT\n"
            "10. DO NOT mention background or environment\n"
            "11. DO NOT use word 'character'\n"
        )

    def get_caption(
        self,
        image_path: str,
        prefix: Optional[str] = "",
        suffix: Optional[str] = "",
        max_retries: int = 3,
        retry_delay: int = 5,
    ) -> str:
        """Generate caption for a single image with retry logic."""
        base64_image = self._encode_image(image_path)

        for attempt in range(max_retries):
            try:
                response = self._make_api_call(base64_image)
                return self._format_caption(response, prefix, suffix)

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"All attempts failed for {image_path}: {str(e)}")
                    return ""

    def _make_api_call(self, base64_image: str) -> Dict[str, Any]:
        """Make the API call to Azure OpenAI."""
        return self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe this image directly and concisely:",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=100,
            temperature=0.5,
            timeout=30,
        )

    def _format_caption(
        self, response: Dict[str, Any], prefix: Optional[str], suffix: Optional[str]
    ) -> str:
        """Format the caption with optional prefix and suffix."""
        caption = response.choices[0].message.content.replace('"', "").strip()
        if suffix:
            caption = f"{caption}, {suffix}"
        if prefix:
            caption = f"{prefix}, {caption}"
        return caption

    def process_folder(
        self,
        input_folder: str,
        output_folder: str,
        prefix: Optional[str] = "",
        suffix: Optional[str] = "",
        save_json: bool = True,
        save_csv: bool = True,
    ) -> None:
        """Process all images in a folder and save captions."""
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        # Get list of image files
        image_files = self._get_image_files(input_folder)
        dataset = self._initialize_dataset()
        # Initialize CSV if needed
        if save_csv:
            self._initialize_csv(output_folder)
        # Process each image
        for idx, filename in enumerate(tqdm(image_files, desc="Processing images")):
            input_path = os.path.join(input_folder, filename)
            # Preprocess image
            processed_filename = self.preprocessor.preprocess_image(
                input_path, output_folder, idx
            )
            if not processed_filename:
                print(f"✗ Failed to preprocess: {filename}")
                continue
            # Generate caption
            processed_path = os.path.join(output_folder, processed_filename)
            caption = self.get_caption(processed_path, prefix, suffix)
            if caption:
                self._save_caption_files(
                    caption, processed_filename, output_folder, dataset, save_csv
                )
                print(f"✓ Processed: {filename} -> {processed_filename}")
            else:
                print(f"✗ Failed to caption: {processed_filename}")
        # Save dataset JSON
        if save_json:
            self._save_dataset_json(dataset, output_folder)

    def _get_image_files(self, input_folder: str) -> List[str]:
        """Get list of image files from input folder."""
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
        return [
            f
            for f in os.listdir(input_folder)
            if Path(f).suffix.lower() in image_extensions
        ]

    def _initialize_dataset(self) -> Dict[str, Any]:
        """Initialize the dataset dictionary."""
        return {
            "info": {
                "description": "Image-Caption Dataset for Diffusion Model Training",
                "version": "1.0",
                "date_created": "",
                "image_size": self.preprocessor.target_size,
                "format": "JPEG",
            },
            "images": [],
        }

    def _initialize_csv(self, output_folder: str) -> None:
        """Initialize the CSV file."""
        csv_path = os.path.join(output_folder, "captions.csv")
        with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["caption", "image_file"])

    def _save_caption_files(
        self,
        caption: str,
        processed_filename: str,
        output_folder: str,
        dataset: Dict[str, Any],
        save_csv: bool,
    ) -> None:
        """Save caption to all required output formats."""
        # Save caption text file
        caption_filename = f"{os.path.splitext(processed_filename)[0]}.txt"
        caption_path = os.path.join(output_folder, caption_filename)
        with open(caption_path, "w", encoding="utf-8") as f:
            f.write(caption)

        # Add to dataset
        dataset["images"].append({"file_name": processed_filename, "caption": caption})

        # Add to CSV if enabled
        if save_csv:
            csv_path = os.path.join(output_folder, "captions.csv")
            with open(csv_path, mode="a", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([caption, processed_filename])

    def _save_dataset_json(self, dataset: Dict[str, Any], output_folder: str) -> None:
        """Save the dataset JSON file."""
        json_path = os.path.join(output_folder, "dataset.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        print(f"\nDataset saved to {json_path}")
