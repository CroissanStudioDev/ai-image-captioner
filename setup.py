from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="ai-image-captioner",
    version="0.1.0",
    author="Croissan Studio",
    author_email="serge@croissanstudio.ru",
    description="An intelligent image captioning tool using Azure OpenAI's GPT-4V model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CroissanStudioDev/ai-image-captioner",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-image-captioner=ai_image_captioner.cli:main",
        ],
    },
)
