"""
Example usage of AI Image Captioner.
This script demonstrates different ways to use the image captioning tool.
"""

import os
from dotenv import load_dotenv
from src.ai_image_captioner import ImageCaptioner


def basic_example():
    """Basic usage example with default settings."""
    print("\n=== Basic Example ===")
    captioner = ImageCaptioner(api_key, endpoint, deployment_name)
    captioner.process_folder(input_folder="input", output_folder="output/basic")


def style_transfer_example():
    """Example with style transfer prefix."""
    print("\n=== Style Transfer Example ===")
    captioner = ImageCaptioner(api_key, endpoint, deployment_name)
    captioner.process_folder(
        input_folder="input",
        output_folder="output/style",
        prefix="in the style of TOK",
        suffix="high quality",
    )


def single_image_example():
    """Example of processing a single image."""
    print("\n=== Single Image Example ===")
    captioner = ImageCaptioner(api_key, endpoint, deployment_name)

    # Process single image
    image_path = "input/example.jpg"
    caption = captioner.get_caption(
        image_path=image_path, prefix="a photo of", suffix="detailed"
    )
    print(f"Caption for {image_path}: {caption}")


def custom_size_example():
    """Example with custom image size."""
    print("\n=== Custom Size Example ===")
    from src.ai_image_captioner import ImagePreprocessor

    # Create captioner with custom preprocessor
    captioner = ImageCaptioner(api_key, endpoint, deployment_name)
    captioner.preprocessor = ImagePreprocessor(
        target_size=(512, 512), output_format="JPEG"  # Smaller size
    )

    captioner.process_folder(input_folder="input", output_folder="output/small")


def batch_processing_example():
    """Example of batch processing with different settings."""
    print("\n=== Batch Processing Example ===")
    captioner = ImageCaptioner(api_key, endpoint, deployment_name)

    # Process different styles
    styles = [
        ("anime", "in anime style", "vibrant colors"),
        ("realistic", "realistic photo of", "high detail"),
        ("painting", "oil painting of", "artistic"),
    ]

    for style_name, prefix, suffix in styles:
        output_dir = f"output/batch/{style_name}"
        print(f"\nProcessing {style_name} style...")

        captioner.process_folder(
            input_folder="input", output_folder=output_dir, prefix=prefix, suffix=suffix
        )


def main():
    """Run all examples."""
    # Create output directories
    os.makedirs("output/basic", exist_ok=True)
    os.makedirs("output/style", exist_ok=True)
    os.makedirs("output/small", exist_ok=True)
    os.makedirs("output/batch", exist_ok=True)

    try:
        # Basic example
        basic_example()

        # Style transfer example
        style_transfer_example()

        # Single image example
        single_image_example()

        # Custom size example
        custom_size_example()

        # Batch processing example
        batch_processing_example()

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Get Azure OpenAI credentials
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not all([api_key, endpoint, deployment_name]):
        print("Please set the required environment variables in .env file")
        exit(1)

    main()
