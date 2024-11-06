# AI Image Captioner

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/CroissanStudioDev/ai-image-captioner)
![Code Style](https://img.shields.io/badge/code%20style-black-black)

⭐ Star us on GitHub — it motivates us a lot!

An intelligent image captioning tool using Azure OpenAI's GPT-4V model, specifically designed for training diffusion models. This tool preprocesses images and generates high-quality captions optimized for AI training.

## 📋 Table of Contents

- [About](#about-section)
- [Features](#features-section)
- [Prerequisites](#prerequisites-section)
- [Installation](#installation-section)
- [Usage](#usage-section)
- [Development](#development-section)
- [Troubleshooting](#troubleshooting-section)
- [Contributing](#contributing-section)
- [License](#license-section)
- [Support](#support-section)

## 🎯 About {#about-section}

**AI Image Captioner** is a Python library designed to provide comprehensive support for image captioning using Azure OpenAI's GPT-4V model. It adheres to high standards of:

- **Modularity**: Different components can function independently
- **Testability**: Improved separation of concerns
- **Maintainability**: Clear structure and organization
- **Reliability**: Robust error handling and retry mechanisms

## ✨ Features {#features-section}

### Image Preprocessing

- Automatic resizing to 1024x1024
- Aspect ratio preservation with padding
- RGB conversion (alpha channel removal)
- Standardized JPEG output
- Sequential naming (image0.jpg, image1.jpg, etc.)

### Caption Generation

- Intelligent captioning using GPT-4V
- Gender and attribute detection
- Consistent formatting
- No introductory phrases
- Focus on main subjects
- Comma-separated elements

### Batch Processing

- Multiple file format support
- Progress tracking
- Error handling
- Retry mechanism for API failures

### Output Options

- Individual caption files (.txt)
- Dataset JSON file
- CSV export
- Customizable prefix/suffix

## 📦 Prerequisites {#prerequisites-section}

- Python 3.8+
- Azure OpenAI API access with GPT-4V deployment
- Required Python packages (see requirements.txt)

## 🚀 Installation {#installation-section}

1. Clone the repository:

```bash
git clone https://github.com/CroissanStudioDev/ai-image-captioner.git
cd ai-image-captioner
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate on Linux/macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

4. Create a `.env` file with your Azure OpenAI credentials:

```ini
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

## 💡 Usage {#usage-section}

### Basic Usage

Process images with default settings:

```bash
python -m ai_image_captioner.cli --input-folder input --output-folder output
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

### Output Format

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

### Caption Examples

```text
woman with pink hair wearing orange sunglasses, gray jumpsuit with orange accents
man in blue shirt and jeans standing with arms crossed
young girl holding a red balloon, wearing a white dress
```

## 🛠️ Development {#development-section}

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

The project follows PEP 8 guidelines and uses Black for formatting:

```bash
# Format code
black src/ai_image_captioner

# Check style
flake8 src/ai_image_captioner
```

## ❗ Troubleshooting {#troubleshooting-section}

### Common Issues

1. **ModuleNotFoundError**: Ensure proper installation:

```bash
pip install -e .
```

2. **Import Error**: Verify virtual environment:

```bash
which python  # Should point to .venv/bin/python
```

3. **API Errors**: Check `.env` configuration

## 🤝 Contributing {#contributing-section}

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License {#license-section}

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support {#support-section}

For support:

- Open an issue in the [GitHub repository](https://github.com/CroissanStudioDev/ai-image-captioner/issues)
- Contact: <serge@croissanstudio.ru>

---

Made with ❤️ by [Croissan Studio](https://github.com/CroissanStudioDev)
