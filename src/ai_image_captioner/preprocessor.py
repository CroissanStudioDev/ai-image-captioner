"""Image preprocessing module."""

from PIL import Image
import os
from typing import Tuple


class ImagePreprocessor:
    """Handles image preprocessing tasks like resizing and format conversion."""

    def __init__(
        self, target_size: Tuple[int, int] = (1024, 1024), output_format: str = "JPEG"
    ) -> None:
        """
        Initialize image preprocessor.

        Args:
            target_size: Tuple of (width, height) for output images
            output_format: Output image format (e.g., "JPEG", "PNG")
        """
        self.target_size = target_size
        self.output_format = output_format

    def preprocess_image(self, input_path: str, output_path: str, index: int) -> str:
        """
        Preprocess image with standardized formatting.

        Args:
            input_path: Path to input image
            output_path: Directory for output
            index: Image index for naming

        Returns:
            str: Output filename or empty string on failure
        """
        try:
            # Open and convert to RGB
            image = Image.open(input_path).convert("RGB")

            # Calculate new size
            width, height = image.size
            ratio = min(self.target_size[0] / width, self.target_size[1] / height)
            new_size = (int(width * ratio), int(height * ratio))

            # Resize image
            image = image.resize(new_size, Image.Resampling.LANCZOS)

            # Add padding
            new_image = Image.new("RGB", self.target_size, (0, 0, 0))
            paste_pos = (
                (self.target_size[0] - new_size[0]) // 2,
                (self.target_size[1] - new_size[1]) // 2,
            )
            new_image.paste(image, paste_pos)

            return self._save_image(new_image, output_path, index)

        except Exception as e:
            print(f"Error preprocessing {input_path}: {str(e)}")
            return ""

    def _save_image(self, image: Image.Image, output_path: str, index: int) -> str:
        """Save processed image with standardized naming."""
        output_filename = f"image{index}.jpg"
        output_filepath = os.path.join(output_path, output_filename)
        image.save(output_filepath, self.output_format, quality=95)
        return output_filename
