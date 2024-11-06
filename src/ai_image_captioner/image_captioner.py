from openai import AzureOpenAI
import base64
from typing import Optional, Dict, Any
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
            "8. DO NOT end with a period"
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
