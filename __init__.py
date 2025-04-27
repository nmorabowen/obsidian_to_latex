"""
obsidian2latex - A package to convert Obsidian markdown to LaTeX

This package provides tools to convert Obsidian markdown files with 
mathematical content to LaTeX, with a focus on preserving equations and formatting.
"""

__version__ = '0.1.0'
__author__ = 'nmorabowen.com'

# Export the main classes for easy import
from .obsidian_to_latex import ObsidianLatexConverter
from .section_converter import ObsidianLatexSectionConverter

# Make it easy to access version information
__all__ = ['ObsidianLatexConverter', 'ObsidianLatexSectionConverter', '__version__', '__author__']