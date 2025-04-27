# Obsidian to LaTeX Converter

A tool to convert Obsidian markdown files to LaTeX format for integration with existing LaTeX projects.

## Features

- Converts Obsidian markdown to LaTeX sections for multi-file projects
- Preserves mathematical expressions and formatting
- Handles Obsidian-specific syntax like internal links and image embeds
- Processes images from attachments folder to figures directory
- Adjusts header levels to fit into existing LaTeX document structure
- Command-line interface for easy integration with build systems

## Installation

```bash
pip install obsidian2latex
```

Or install from source:

```bash
git clone https://github.com/nmorabowen/obsidian_to_latex_.git
cd obsidian_to_latex
pip install -e .
```

## Usage

### Command Line

```bash
# Basic conversion
obsidian_to_latex my_note.md -o sections/my_section.tex

# Specify figures directory
obsidian_to_latex my_note.md -o sections/my_section.tex -f custom_figures

# Adjust header levels (e.g., make # in markdown become \subsection in LaTeX)
obsidian_to_latex my_note.md -o sections/my_section.tex -l 1
```

### Python API

```python
from obsidian_to_latex import ObsidianLatexSectionConverter

# Create a converter instance
converter = ObsidianLatexSectionConverter(
    input_file="my_note.md",
    output_file="sections/my_section.tex",
    figures_dir="figures"
)

# Convert the file
latex_content = converter.convert(level_adjustment=1)
converter.save(latex_content)
converter.process_images()
```

## Jupyter Notebook Interface

The package includes a Jupyter notebook interface with file selection widgets.
See the `examples/jupyter_interface.ipynb` file for details.

## License

MIT

## Author

Nicolas Mora Bowen