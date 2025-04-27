"""
ObsidianLatexSectionConverter - A tool to convert Obsidian markdown to LaTeX sections

This module provides a class-based solution to convert Obsidian markdown files 
with mathematical content, images, and various markdown elements to properly 
formatted LaTeX section files compatible with a multi-file LaTeX project structure.
"""

import re
import os
import sys
import argparse
import shutil
from pathlib import Path
import logging

class ObsidianLatexSectionConverter:
    """
    A class to convert Obsidian markdown to LaTeX sections for integration with existing projects
    """
    
    def __init__(self, input_file=None, output_file=None, figures_dir=None, verbose=False):
        """
        Initialize the converter with input and output files
        
        Args:
            input_file (str): Path to the input Obsidian markdown file
            output_file (str): Path to the output LaTeX section file
            figures_dir (str): Path to the figures directory (default: figures/)
            verbose (bool): Enable verbose logging
        """
        self.input_file = input_file
        self.output_file = output_file
        self.figures_dir = figures_dir or "figures"
        
        # Set up logging
        self.logger = logging.getLogger('ObsidianLatexSectionConverter')
        logging_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=logging_level, 
                           format='%(levelname)s: %(message)s')
        
        # Document metadata from frontmatter
        self.metadata = {
            'title': '',
            'tags': []
        }
        
        # Store image file extensions
        self.image_extensions = ['.png', '.jpg', '.jpeg', '.pdf', '.svg', '.excalidraw.png']

    def extract_frontmatter(self, content):
        """
        Extract and parse YAML frontmatter from the content
        
        Args:
            content (str): The markdown content
            
        Returns:
            dict: Extracted metadata
        """
        frontmatter = {}
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        
        if match:
            yaml_text = match.group(1)
            for line in yaml_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Process lists in YAML (like tags)
                    if value.startswith('-'):
                        frontmatter[key] = [item.strip('- ') for item in value.split('\n')]
                    else:
                        frontmatter[key] = value
        
        # Update metadata with extracted frontmatter
        for key, value in frontmatter.items():
            if key in self.metadata:
                self.metadata[key] = value
        
        self.logger.debug(f"Extracted frontmatter: {frontmatter}")
        return frontmatter

    def remove_frontmatter(self, content):
        """
        Remove YAML frontmatter from the content
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content without frontmatter
        """
        return re.sub(r'^---\s*\n(.*?)\n---\s*\n', '', content, flags=re.DOTALL)

    def convert_headers(self, content, level_adjustment=0):
        """
        Convert markdown headers to LaTeX sections with level adjustment
        
        Args:
            content (str): The markdown content
            level_adjustment (int): Number of levels to adjust headers by
            
        Returns:
            str: Content with headers converted
        """
        # Define the LaTeX section commands by level
        section_commands = [
            '\\section',
            '\\subsection',
            '\\subsubsection',
            '\\paragraph',
            '\\subparagraph'
        ]
        
        # Convert headers based on the adjusted level
        for i in range(5):
            md_level = i + 1  # Markdown level (# = 1, ## = 2, etc.)
            latex_level = i + level_adjustment
            
            # Ensure we don't go out of bounds
            if latex_level < 0:
                latex_level = 0
            if latex_level >= len(section_commands):
                latex_level = len(section_commands) - 1
                
            # Create the regex pattern for this header level
            hashes = '#' * md_level
            pattern = f'^{hashes} (.*?)$'
            
            # Replace with the appropriate LaTeX section command
            content = re.sub(pattern, f'{section_commands[latex_level]}{{{1}}}', content, flags=re.MULTILINE)
        
        return content

    def convert_lists(self, content):
        """
        Convert markdown lists to LaTeX itemize environment
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with lists converted
        """
        # Convert list items
        content = re.sub(r'^- (.*?)$', r'\\item \1', content, flags=re.MULTILINE)
        
        # Find all sequences of \item lines
        item_blocks = re.findall(r'((?:^\\item .*\n)+)', content, re.MULTILINE)
        
        # Replace each block with an itemize environment
        for block in item_blocks:
            content = content.replace(block, f"\\begin{{itemize}}\n{block}\\end{{itemize}}\n")
        
        return content

    def convert_images(self, content):
        """
        Convert Obsidian image links to LaTeX figures
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with images converted
        """
        def replace_image(match):
            # Extract image path and options
            image_path = match.group(1).split('|')[0].strip()
            
            # Extract image options like width
            size_info = ""
            if '|' in match.group(1):
                size = match.group(1).split('|')[1].strip()
                if size.isdigit():
                    size_info = f"[width={size}pt]"
            
            # Get just the filename without path
            filename = os.path.basename(image_path)
            clean_filename = re.sub(r'[^\w\.-]', '_', filename)
            
            # Create a proper caption and label
            caption = filename.replace('_', ' ').split('.')[0]
            label = f"fig:{clean_filename.replace('.', '_')}"
            
            return f"""
\\begin{{figure}}[htbp]
    \\centering
    \\includegraphics{size_info}{{{self.figures_dir}/{clean_filename}}}
    \\caption{{{caption}}}
    \\label{{{label}}}
\\end{{figure}}
"""
        
        # Standard Obsidian image syntax: ![[image.png]]
        content = re.sub(r'!\[\[(.*?)\]\]', replace_image, content)
        
        # Standard Markdown image syntax: ![alt text](image.png)
        content = re.sub(r'!\[(.*?)\]\((.*?)\)', 
                       lambda m: f"""
\\begin{{figure}}[htbp]
    \\centering
    \\includegraphics{{{self.figures_dir}/{os.path.basename(m.group(2))}}}
    \\caption{{{m.group(1)}}}
    \\label{{fig:{os.path.basename(m.group(2)).replace('.', '_')}}}
\\end{{figure}}
""", content)
        
        return content

    def convert_internal_links(self, content):
        """
        Convert Obsidian internal links to LaTeX references or text
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with internal links converted
        """
        # Handle links with display text: [[actual|display]]
        content = re.sub(r'\[\[(.*?)\|(.*?)\]\]', r'\\textit{\2}', content)
        
        # Handle regular internal links
        content = re.sub(r'\[\[(.*?)\]\]', r'\\textit{\1}', content)
        
        # Handle markdown links
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', content)
        
        return content

    def remove_comments(self, content):
        """
        Remove Obsidian comments from the content
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content without comments
        """
        return re.sub(r'%%.*?%%', '', content, flags=re.DOTALL)

    def convert_emphasis(self, content):
        """
        Convert markdown text formatting to LaTeX
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with text formatting converted
        """
        # Handle bold text
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        
        # Handle italic text
        content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)
        
        # Handle strikethrough
        content = re.sub(r'~~(.*?)~~', r'\\sout{\1}', content)
        
        return content

    def convert_code_blocks(self, content):
        """
        Convert markdown code blocks to LaTeX environments
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with code blocks converted
        """
        def replace_code_block(match):
            language = match.group(1).strip()
            code = match.group(2)
            
            # Skip math blocks that use $ delimiters (they're handled elsewhere)
            if code.strip().startswith('$') and code.strip().endswith('$'):
                return match.group(0)
                
            if language == "":
                return f"\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}"
            else:
                return f"\\begin{{lstlisting}}[language={language}]\n{code}\n\\end{{lstlisting}}"
        
        content = re.sub(r'```(.*?)\n(.*?)```', replace_code_block, content, flags=re.DOTALL)
        
        # Handle inline code
        content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', content)
        
        return content

    def preserve_math(self, content):
        """
        Preserve and process math environments in the document
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with math properly handled
        """
        # Handle aligned environment properly
        content = re.sub(r'\\begin{aligned}(.*?)\\end{aligned}', 
                       r'\\begin{aligned}\1\\end{aligned}', 
                       content, flags=re.DOTALL)
        
        # Keep display math blocks as is - they're already in LaTeX format
        # In a multi-file LaTeX project, we might want to use equation environments
        # but it's safer to keep the original format to avoid numbering issues
        
        return content

    def process_images(self):
        """
        Copy images from Obsidian attachments to the project's figures directory
        """
        if not self.input_file or not self.output_file:
            return
            
        # Target figures directory (use the provided one or a default)
        figures_dir = os.path.abspath(self.figures_dir)
        if not os.path.exists(figures_dir):
            try:
                os.makedirs(figures_dir)
                self.logger.info(f"Created figures directory at '{figures_dir}'")
            except Exception as e:
                self.logger.warning(f"Failed to create figures directory: {e}")
                return
        
        # Try to find Obsidian attachments
        input_dir = os.path.dirname(os.path.abspath(self.input_file))
        possible_attachment_dirs = [
            os.path.join(input_dir, "attachments"),
            os.path.join(input_dir, "assets"),
            os.path.join(input_dir, "images"),
            os.path.join(os.path.dirname(input_dir), "attachments"),
        ]
        
        # Track whether we found any attachments
        found_attachments = False
        
        for attachment_dir in possible_attachment_dirs:
            if os.path.exists(attachment_dir):
                self.logger.info(f"Found attachments in: {attachment_dir}")
                found_attachments = True
                
                # Copy all image files to figures directory
                for file in os.listdir(attachment_dir):
                    file_path = os.path.join(attachment_dir, file)
                    if (os.path.isfile(file_path) and 
                        any(file.lower().endswith(ext) for ext in self.image_extensions)):
                        try:
                            shutil.copy2(file_path, figures_dir)
                            self.logger.debug(f"Copied {file} to figures directory")
                        except Exception as e:
                            self.logger.warning(f"Failed to copy {file}: {e}")
                
                self.logger.info(f"Copied available images to {figures_dir}")
        
        if not found_attachments:
            self.logger.warning("No attachments directory found. You may need to manually copy images.")

    def add_section_comment(self, content):
        """
        Add a comment at the top of the file indicating it was auto-generated
        
        Args:
            content (str): The LaTeX content
            
        Returns:
            str: Content with comment added
        """
        comment = "% Auto-generated from Obsidian markdown\n"
        comment += f"% Source: {os.path.basename(self.input_file)}\n"
        if self.metadata['title']:
            comment += f"% Title: {self.metadata['title']}\n"
        if self.metadata['tags']:
            tags_str = ', '.join(self.metadata['tags'])
            comment += f"% Tags: {tags_str}\n"
        comment += "%\n\n"
        
        return comment + content

    def convert(self, level_adjustment=0):
        """
        Convert an Obsidian markdown file to a LaTeX section
        
        Returns:
            str: The converted LaTeX content
        """
        # Check if input file exists
        if not os.path.exists(self.input_file):
            self.logger.error(f"Input file '{self.input_file}' not found.")
            return None
        
        # Read the content
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from frontmatter
        self.extract_frontmatter(content)
        
        # Conversion process - apply each conversion step
        content = self.remove_frontmatter(content)
        content = self.remove_comments(content)
        content = self.convert_headers(content)
        content = self.convert_lists(content)
        content = self.convert_images(content)
        content = self.convert_internal_links(content)
        content = self.convert_emphasis(content)
        content = self.convert_code_blocks(content)
        content = self.preserve_math(content)
        
        # Add section comment
        content = self.add_section_comment(content)
        
        self.logger.info("Conversion completed successfully")
        return content

    def save(self, latex_content):
        """
        Save the LaTeX content to the output file
        
        Args:
            latex_content (str): The LaTeX content to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not latex_content:
            return False
            
        try:
            # Ensure the output directory exists
            output_dir = os.path.dirname(self.output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            self.logger.info(f"LaTeX content saved to '{self.output_file}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save output: {e}")
            return False

    def convert_and_save(self):
        """
        Convert the Obsidian markdown file and save the result
        
        Returns:
            bool: True if conversion and saving completed successfully
        """
        latex_content = self.convert()
        if latex_content:
            success = self.save(latex_content)
            if success:
                self.process_images()
            return success
        return False
