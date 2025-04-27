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
import traceback  # Add this import for better error tracing
import datetime

class ObsidianLatexSectionConverter:
    """
    A class to convert Obsidian markdown to LaTeX sections for integration with existing projects
    """
    
    def __init__(self, input_file=None, output_file=None, figures_dir=None, verbose=False, log_file="obsidian2latex.log"):
        """
        Initialize the converter with input and output files
        
        Args:
            input_file (str): Path to the input Obsidian markdown file
            output_file (str): Path to the output LaTeX section file
            figures_dir (str): Path to the figures directory (default: figures/)
            verbose (bool): Enable verbose logging
            log_file (str): Path to the log file
        """
        self.input_file = input_file
        self.output_file = output_file
        self.figures_dir = figures_dir or "figures"
        self.log_file = log_file
        
        # Set up logging to both file and console
        self.logger = logging.getLogger('ObsidianLatexSectionConverter')
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        
        # Clear any existing handlers
        self.logger.handlers = []
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # File handler
        try:
            file_handler = logging.FileHandler(log_file, mode='w')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)  # Always log everything to file
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not set up log file: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        self.logger.addHandler(console_handler)
        
        # Don't propagate to root logger
        self.logger.propagate = False
        
        self.logger.info(f"Initializing converter: input={input_file}, output={output_file}")
        
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
        try:
            self.logger.debug("Attempting to extract frontmatter")
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            
            if match:
                yaml_text = match.group(1)
                self.logger.debug(f"Found frontmatter: {yaml_text}")
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
        except Exception as e:
            self.logger.error(f"Error extracting frontmatter: {e}")
            self.logger.error(traceback.format_exc())
            return {}

    def remove_frontmatter(self, content):
        """
        Remove YAML frontmatter from the content
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content without frontmatter
        """
        try:
            self.logger.debug("Removing frontmatter")
            result = re.sub(r'^---\s*\n(.*?)\n---\s*\n', '', content, flags=re.DOTALL)
            self.logger.debug(f"First 50 chars after frontmatter removal: {repr(result[:50])}")
            return result
        except Exception as e:
            self.logger.error(f"Error removing frontmatter: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def convert_headers(self, content, level_adjustment=0):
        """
        Convert markdown headers to LaTeX sections with level adjustment
        
        Args:
            content (str): The markdown content
            level_adjustment (int): Number of levels to adjust headers by
            
        Returns:
            str: Content with headers converted
        """
        try:
            self.logger.debug("Converting headers")
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
                pattern = r'^' + re.escape(hashes) + r' (.*?)$'
                
                # Replace with the appropriate LaTeX section command
                self.logger.debug(f"Converting level {md_level} headers to {section_commands[latex_level]}")
                replacement = fr'{section_commands[latex_level]}{{\1}}'
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            return content
        except Exception as e:
            self.logger.error(f"Error converting headers: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def convert_lists(self, content):
        """
        Convert markdown lists to LaTeX itemize environment
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with lists converted
        """
        try:
            self.logger.debug("Converting lists")
            # Convert list items
            content = re.sub(r'^- (.*?)$', r'\\item \1', content, flags=re.MULTILINE)
            
            # Find all sequences of \item lines
            item_blocks = re.findall(r'((?:^\\item .*\n)+)', content, re.MULTILINE)
            
            # Replace each block with an itemize environment
            for i, block in enumerate(item_blocks):
                self.logger.debug(f"Processing list block {i+1} of {len(item_blocks)}")
                content = content.replace(block, fr"\begin{{itemize}}\n{block}\end{{itemize}}\n")
            
            return content
        except Exception as e:
            self.logger.error(f"Error converting lists: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def convert_images(self, content):
        """
        Convert Obsidian image links to LaTeX figures
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with images converted
        """
        try:
            self.logger.debug("Converting images")
            
            def replace_image(match):
                try:
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
                    
                    self.logger.debug(f"Processing image: {image_path} -> {clean_filename}")
                    
                    # Use raw f-string (fr) to properly handle backslashes
                    return fr"""
\begin{{figure}}[htbp]
    \centering
    \includegraphics{size_info}{{{self.figures_dir}/{clean_filename}}}
    \caption{{{caption}}}
    \label{{{label}}}
\end{{figure}}
"""
                except Exception as e:
                    self.logger.error(f"Error in replace_image: {e}")
                    self.logger.error(traceback.format_exc())
                    return match.group(0)  # Return original text on error
            
            # Standard Obsidian image syntax: ![[image.png]]
            self.logger.debug("Processing Obsidian image syntax")
            content = re.sub(r'!\[\[(.*?)\]\]', replace_image, content)
            
            # Standard Markdown image syntax: ![alt text](image.png)
            self.logger.debug("Processing standard Markdown image syntax")
            content = re.sub(
                r'!\[(.*?)\]\((.*?)\)', 
                lambda m: self._process_md_image(m), 
                content
            )
            
            return content
        except Exception as e:
            self.logger.error(f"Error converting images: {e}")
            self.logger.error(traceback.format_exc())
            return content
    
    def _process_md_image(self, match):
        """Helper method to process standard Markdown images"""
        try:
            alt_text = match.group(1)
            image_path = match.group(2)
            filename = os.path.basename(image_path)
            
            self.logger.debug(f"Processing Markdown image: {image_path}")
            
            # Use raw f-string for proper backslash handling
            return fr"""
\begin{{figure}}[htbp]
    \centering
    \includegraphics{{{self.figures_dir}/{filename}}}
    \caption{{{alt_text}}}
    \label{{fig:{filename.replace('.', '_')}}}
\end{{figure}}
"""
        except Exception as e:
            self.logger.error(f"Error processing Markdown image: {e}")
            self.logger.error(traceback.format_exc())
            return match.group(0)  # Return original text on error

    def convert_internal_links(self, content):
        """
        Convert Obsidian internal links to LaTeX references or text
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with internal links converted
        """
        try:
            self.logger.debug("Converting internal links")
            # Handle links with display text: [[actual|display]]
            content = re.sub(r'\[\[(.*?)\|(.*?)\]\]', r'\\textit{\2}', content)
            
            # Handle regular internal links
            content = re.sub(r'\[\[(.*?)\]\]', r'\\textit{\1}', content)
            
            # Handle markdown links
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'\\href{\2}{\1}', content)
            
            return content
        except Exception as e:
            self.logger.error(f"Error converting internal links: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def remove_comments(self, content):
        """
        Remove Obsidian comments from the content
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content without comments
        """
        try:
            self.logger.debug("Removing comments")
            return re.sub(r'%%.*?%%', '', content, flags=re.DOTALL)
        except Exception as e:
            self.logger.error(f"Error removing comments: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def convert_emphasis(self, content):
        """
        Convert markdown text formatting to LaTeX
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with text formatting converted
        """
        try:
            self.logger.debug("Converting emphasis")
            # Handle bold text
            content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
            
            # Handle italic text
            content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)
            
            # Handle strikethrough
            content = re.sub(r'~~(.*?)~~', r'\\sout{\1}', content)
            
            return content
        except Exception as e:
            self.logger.error(f"Error converting emphasis: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def convert_code_blocks(self, content):
        """
        Convert markdown code blocks to LaTeX environments
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with code blocks converted
        """
        try:
            self.logger.debug("Converting code blocks")
            def replace_code_block(match):
                try:
                    language = match.group(1).strip()
                    code = match.group(2)
                    
                    # Skip math blocks that use $ delimiters (they're handled elsewhere)
                    if code.strip().startswith('$') and code.strip().endswith('$'):
                        return match.group(0)
                    
                    self.logger.debug(f"Processing code block with language: {language}")    
                    if language == "":
                        return fr"\begin{{verbatim}}\n{code}\n\end{{verbatim}}"
                    else:
                        return fr"\begin{{lstlisting}}[language={language}]\n{code}\n\end{{lstlisting}}"
                except Exception as e:
                    self.logger.error(f"Error in replace_code_block: {e}")
                    self.logger.error(traceback.format_exc())
                    return match.group(0)
            
            content = re.sub(r'```(.*?)\n(.*?)```', replace_code_block, content, flags=re.DOTALL)
            
            # Handle inline code
            content = re.sub(r'`([^`]+)`', r'\\texttt{\1}', content)
            
            return content
        except Exception as e:
            self.logger.error(f"Error converting code blocks: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def preserve_math(self, content):
        """
        Preserve and process math environments in the document
        
        Args:
            content (str): The markdown content
            
        Returns:
            str: Content with math properly handled
        """
        try:
            self.logger.debug("Preserving math environments")
            # Handle aligned environment properly
            content = re.sub(r'\\begin{aligned}(.*?)\\end{aligned}', 
                          r'\\begin{aligned}\1\\end{aligned}', 
                          content, flags=re.DOTALL)
            
            # Keep display math blocks as is - they're already in LaTeX format
            # In a multi-file LaTeX project, we might want to use equation environments
            # but it's safer to keep the original format to avoid numbering issues
            
            return content
        except Exception as e:
            self.logger.error(f"Error preserving math: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def process_images(self):
        """
        Copy images from Obsidian attachments to the project's figures directory
        """
        try:
            self.logger.debug("Processing images")
            if not self.input_file or not self.output_file:
                self.logger.warning("Input or output file not specified, skipping image processing")
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
        except Exception as e:
            self.logger.error(f"Error processing images: {e}")
            self.logger.error(traceback.format_exc())

    def add_section_comment(self, content):
        """
        Add a comment at the top of the file indicating it was auto-generated
        
        Args:
            content (str): The LaTeX content
            
        Returns:
            str: Content with comment added
        """
        try:
            self.logger.debug("Adding section comment")
            comment = "% Auto-generated from Obsidian markdown\n"
            comment += f"% Source: {os.path.basename(self.input_file)}\n"
            if self.metadata['title']:
                comment += f"% Title: {self.metadata['title']}\n"
            if self.metadata['tags']:
                if isinstance(self.metadata['tags'], list):
                    tags_str = ', '.join(self.metadata['tags'])
                else:
                    tags_str = str(self.metadata['tags'])
                comment += f"% Tags: {tags_str}\n"
            comment += "%\n\n"
            
            return comment + content
        except Exception as e:
            self.logger.error(f"Error adding section comment: {e}")
            self.logger.error(traceback.format_exc())
            return content

    def convert(self, level_adjustment=0):
        """
        Convert an Obsidian markdown file to a LaTeX section
        
        Returns:
            str: The converted LaTeX content
        """
        try:
            self.logger.info(f"Starting conversion of {self.input_file}")
            
            # Normalize path
            normalized_path = os.path.normpath(self.input_file)
            self.logger.debug(f"Normalized input path: {normalized_path}")
            
            # Check if input file exists
            if not os.path.exists(normalized_path):
                self.logger.error(f"Input file '{normalized_path}' not found.")
                return None
            
            self.input_file = normalized_path  # Use normalized path
            
            # Read the content
            self.logger.debug(f"Reading content from {self.input_file}")
            try:
                with open(self.input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.logger.debug(f"Successfully read {len(content)} characters")
                self.logger.debug(f"First 100 characters: {repr(content[:100])}")
            except UnicodeDecodeError:
                # Try with another encoding if UTF-8 fails
                self.logger.warning("UTF-8 decoding failed, trying with latin-1")
                with open(self.input_file, 'r', encoding='latin-1') as f:
                    content = f.read()
                self.logger.debug(f"Successfully read {len(content)} characters with latin-1 encoding")
            
            # Extract metadata from frontmatter
            self.logger.debug("Extracting frontmatter")
            self.extract_frontmatter(content)
            
            # Conversion process - apply each conversion step
            self.logger.debug("Starting conversion process")
            
            self.logger.debug("Step 1: Removing frontmatter")
            content = self.remove_frontmatter(content)
            
            self.logger.debug("Step 2: Removing comments")
            content = self.remove_comments(content)
            
            self.logger.debug("Step 3: Converting headers")
            content = self.convert_headers(content, level_adjustment)
            
            self.logger.debug("Step 4: Converting lists")
            content = self.convert_lists(content)
            
            self.logger.debug("Step 5: Converting images")
            content = self.convert_images(content)
            
            self.logger.debug("Step 6: Converting internal links")
            content = self.convert_internal_links(content)
            
            self.logger.debug("Step 7: Converting emphasis")
            content = self.convert_emphasis(content)
            
            self.logger.debug("Step 8: Converting code blocks")
            content = self.convert_code_blocks(content)
            
            self.logger.debug("Step 9: Preserving math")
            content = self.preserve_math(content)
            
            # Add section comment
            self.logger.debug("Step 10: Adding section comment")
            content = self.add_section_comment(content)
            
            self.logger.info("Conversion completed successfully")
            self.logger.debug(f"Final content length: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Error during conversion: {e}")
            self.logger.error(traceback.format_exc())
            return None

    def save(self, latex_content, overwrite_mode='overwrite'):
        """
        Save the LaTeX content to the output file
        
        Args:
            latex_content (str): The LaTeX content to save
            overwrite_mode (str): How to handle existing files: 'overwrite', 'backup', or 'skip'
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            self.logger.debug(f"Saving content to {self.output_file} (mode: {overwrite_mode})")
            if not latex_content:
                self.logger.error("No content to save")
                return False
            
            # Ensure the output directory exists
            output_dir = os.path.dirname(self.output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.logger.debug(f"Created output directory: {output_dir}")
            
            # Check if file already exists
            if os.path.exists(self.output_file):
                self.logger.debug(f"Output file already exists: {self.output_file}")
                
                if overwrite_mode == 'skip':
                    self.logger.info(f"Skipping existing file '{self.output_file}'")
                    return True
                
                elif overwrite_mode == 'backup':
                    # Create backup with timestamp
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_file = f"{self.output_file}.{timestamp}.bak"
                    try:
                        shutil.copy2(self.output_file, backup_file)
                        self.logger.info(f"Created backup of existing file: {backup_file}")
                    except Exception as e:
                        self.logger.warning(f"Failed to create backup: {e}")
                        self.logger.error(traceback.format_exc())
            
            # Save the file
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            self.logger.info(f"LaTeX content saved to '{self.output_file}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save output: {e}")
            self.logger.error(traceback.format_exc())
            return False

    def convert_and_save(self):
        """
        Convert the Obsidian markdown file and save the result
        
        Returns:
            bool: True if conversion and saving completed successfully
        """
        try:
            self.logger.info("Starting convert_and_save")
            latex_content = self.convert()
            if latex_content:
                success = self.save(latex_content)
                if success:
                    self.process_images()
                return success
            return False
        except Exception as e:
            self.logger.error(f"Error in convert_and_save: {e}")
            self.logger.error(traceback.format_exc())
            return False