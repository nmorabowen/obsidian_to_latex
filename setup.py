from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obsidian_to_latex",
    version="0.1.0",
    author="Nicolas Mora Bowen",
    author_email="nmorabowen@gmail.com",
    description="A tool to convert Obsidian markdown to LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nmorabowen/obsidian_to_latex",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=8.0.0",  # For image processing
    ],
    entry_points={
        "console_scripts": [
            "obsidian_to_latex=obsidian_to_latex.CLI:main",
        ],
    },
)