# AI Image Captioner

An intelligent image captioning tool using Azure OpenAI's GPT-4V model, specifically designed for training diffusion models. This tool preprocesses images and generates high-quality captions optimized for AI training.

## Features

- **Image Preprocessing**
  - Automatic resizing to 1024x1024
  - Aspect ratio preservation with padding
  - RGB conversion (alpha channel removal)
  - Standardized JPEG output
  - Sequential naming (image0.jpg, image1.jpg, etc.)

- **Caption Generation**
  - Intelligent captioning using GPT-4V
  - Gender and attribute detection
  - Consistent formatting
  - No introductory phrases
  - Focus on main subjects
  - Comma-separated elements

- **Batch Processing**
  - Multiple file format support
  - Progress tracking
  - Error handling
  - Retry mechanism for API failures

- **Output Options**
  - Individual caption files (.txt)
  - Dataset JSON file
  - CSV export
  - Customizable prefix/suffix

## Prerequisites

- Python 3.8+
- Azure OpenAI API access with GPT-4V deployment
- Required Python packages (see requirements.txt)

## Installation

1.Clone the repository:

```bash
git clone https://github.com/CroissanStudioDev/ai-image-captioner.git
cd ai-image-captioner
```

2.Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

3.Install the package in development mode:

```bash
pip install -e .
```

4.Create a `.env` file with your Azure OpenAI credentials:

```ini
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

## Usage

### Basic Usage

Process images with default settings:

```bash
# Using the module
python -m ai_image_captioner.cli --input-folder input --output-folder output

# Using the installed script
ai-image-captioner --input-folder input --output-folder output
```

### Advanced Usage

Add style prefix and quality suffix:

```bash
python -m ai_image_captioner.cli \
    --input-folder input \
    --output-folder output \
    --prefix "in the style of TOK" \
    --suffix "high quality"
```

Disable JSON dataset creation:

```bash
python -m ai_image_captioner.cli \
    --input-folder input \
    --output-folder output \
    --no-json
```

### Output Structure

```text
output/
├── image0.jpg          # Preprocessed image
├── image0.txt          # Caption file
├── image1.jpg
├── image1.txt
├── ...
├── captions.csv        # All captions in CSV format
└── dataset.json        # Complete dataset information
```

### Caption Format

The tool generates captions following these rules:

- No introductory phrases
- Direct descriptions
- Comma-separated elements
- Gender-specific descriptions
- No ending punctuation

Example captions:

```text
woman with pink hair wearing orange sunglasses, gray jumpsuit with orange accents
man in blue shirt and jeans standing with arms crossed
young girl holding a red balloon, wearing a white dress
```

## Development

### Project Structure

```text
ai-image-captioner/
├── src/
│   └── ai_image_captioner/
│       ├── __init__.py
│       ├── cli.py
│       ├── image_captioner.py
│       └── preprocessor.py
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

### Code Style

The project follows PEP 8 guidelines. Run the following checks:

```bash
# Format code with black
black src/ai_image_captioner

# Check with flake8
flake8 src/ai_image_captioner
```

## Troubleshooting

### Common Issues

1.**ModuleNotFoundError**: Make sure you've installed the package in development mode:

```bash
pip install -e .
```

2.**Import Error**: Verify you're using the correct Python from virtual environment:

```bash
which python  # Should point to .venv/bin/python
```

3.**API Errors**: Check your `.env` file and Azure OpenAI credentials

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Azure OpenAI team for providing the GPT-4V API
- Inspired by [oCaption](https://github.com/ghostofpokemon/oCaption)
- Contributors to the Python Pillow library

## Support

For support:

- Open an issue in the [GitHub repository](https://github.com/CroissanStudioDev/ai-image-captioner/issues)
- Contact: <serge@croissanstudio.ru>
