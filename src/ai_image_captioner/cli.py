"""Command line interface for AI Image Captioner."""

import argparse
from dotenv import load_dotenv
import os
from .image_captioner import ImageCaptioner


def main():
    """Main entry point for the CLI."""
    load_dotenv(override=True)

    parser = argparse.ArgumentParser(
        description="Generate image captions for training diffusion models"
    )
    parser.add_argument(
        "--input-folder", default="input", help="Input folder containing images"
    )
    parser.add_argument(
        "--output-folder", default="output", help="Output folder for caption files"
    )
    parser.add_argument("--prefix", default="", help="Prefix for each caption")
    parser.add_argument("--suffix", default="", help="Suffix for each caption")
    parser.add_argument(
        "--no-json", action="store_true", help="Disable JSON dataset creation"
    )

    args = parser.parse_args()

    # Get Azure OpenAI credentials
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not all([api_key, endpoint, deployment_name]):
        print("Please set the required environment variables:")
        print("AZURE_OPENAI_API_KEY")
        print("AZURE_OPENAI_ENDPOINT")
        print("AZURE_OPENAI_DEPLOYMENT_NAME")
        return

    # Initialize and run captioner
    captioner = ImageCaptioner(api_key, endpoint, deployment_name)
    captioner.process_folder(
        args.input_folder,
        args.output_folder,
        args.prefix,
        args.suffix,
        not args.no_json,
        True,
    )


if __name__ == "__main__":
    main()
