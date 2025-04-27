"""
Command-line interface for obsidian_to_latex
Focused on converting Obsidian markdown to LaTeX sections for multi-file projects
"""

import sys
import argparse
import logging
from pathlib import Path

# Update import to match the class name in converter.py
from .converter import ObsidianLatexSectionConverter


def setup_logging(verbose=False):
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )
    return logging.getLogger('obsidian2latex-cli')


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description='Convert Obsidian markdown to LaTeX sections for multi-file projects',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic conversion:
    obsidian2latex my_note.md -o sections/my_section.tex
  
  Specify figures directory:
    obsidian2latex my_note.md -o sections/my_section.tex -f custom_figures
  
  Adjust header levels:
    obsidian2latex my_note.md -o sections/my_section.tex -l 1
        """
    )
    
    parser.add_argument('input_file', help='Input Obsidian markdown file')
    parser.add_argument('-o', '--output', required=True, help='Output LaTeX section file')
    parser.add_argument('-f', '--figures', default='figures', help='Figures directory (default: figures)')
    parser.add_argument('-l', '--level-adjust', type=int, default=0, 
                        help='Adjust header levels by this amount (default: 0)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    
    try:
        # Create the converter
        converter = ObsidianLatexSectionConverter(
            input_file=args.input_file,
            output_file=args.output,
            figures_dir=args.figures,
            verbose=args.verbose
        )
        
        # Perform the conversion with level adjustment
        latex_content = converter.convert(level_adjustment=args.level_adjust)
        if latex_content:
            success = converter.save(latex_content)
            if success:
                converter.process_images()
                logger.info(f"Conversion completed successfully: {args.output}")
                
                # Provide helpful next steps
                logger.info(f"To include this section in your main LaTeX document, add:")
                relative_path = Path(args.output).relative_to(Path.cwd())
                logger.info(f"\\input{{{relative_path}}}")
                
                return 0
        
        logger.error("Conversion failed")
        return 1
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())