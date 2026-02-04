#!/usr/bin/env python3
"""
Crownwell Press EPUB Builder
Converts DOCX manuscripts to professional EPUB3 files
"""

import os
import sys
import yaml
import subprocess
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import zipfile
import xml.etree.ElementTree as ET


class EPUBBuilder:
    """Orchestrates EPUB3 generation from DOCX"""
    
    def __init__(self, book_dir: Path):
        self.book_dir = book_dir
        self.input_dir = book_dir / "input"
        self.output_dir = book_dir / "output"
        self.working_dir = book_dir / "working"
        self.metadata_file = book_dir / "metadata.yaml"
        
        self.metadata: Dict = {}
        self.log_entries: List[str] = []
        
    def log(self, message: str, level: str = "INFO"):
        """Add entry to build log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(entry)
        print(entry)
        
    def load_metadata(self) -> None:
        """Load book metadata from YAML"""
        self.log(f"Loading metadata from {self.metadata_file}")
        
        if not self.metadata_file.exists():
            self.log(f"ERROR: metadata.yaml not found in {self.book_dir}", "ERROR")
            sys.exit(1)
            
        with open(self.metadata_file, 'r', encoding='utf-8') as f:
            self.metadata = yaml.safe_load(f) or {}
            
        # Validate required fields
        required = ['title', 'author', 'publisher']
        missing = [f for f in required if not self.metadata.get(f)]
        if missing:
            self.log(f"ERROR: Missing required metadata: {', '.join(missing)}", "ERROR")
            sys.exit(1)
            
        self.log(f"Loaded metadata for: {self.metadata['title']}")
        
    def find_input_docx(self) -> Path:
        """Locate input DOCX file"""
        self.log("Searching for input DOCX")
        
        # Look for original.docx or any .docx file
        docx_files = list(self.input_dir.glob("*.docx"))
        
        if not docx_files:
            self.log("ERROR: No DOCX file found in input directory", "ERROR")
            sys.exit(1)
            
        # Prefer original.docx, otherwise take first
        for docx in docx_files:
            if docx.name == "original.docx":
                self.log(f"Found input: {docx.name}")
                return docx
                
        self.log(f"Found input: {docx_files[0].name}")
        return docx_files[0]
        
    def clean_docx(self, input_docx: Path) -> Path:
        """
        Remove old publisher references from DOCX
        Returns path to cleaned DOCX
        """
        self.log("Cleaning DOCX (removing old publisher references)")
        
        # For now, copy as-is. Full implementation requires python-docx
        # to parse and modify document content
        
        cleaned_path = self.working_dir / "cleaned.docx"
        shutil.copy2(input_docx, cleaned_path)
        
        # TODO: Implement actual cleaning with python-docx
        # - Remove "Delmarva Publications" text
        # - Remove old copyright pages
        # - Remove old title page elements
        
        self.log("DOCX cleaning: basic copy complete (TODO: implement full cleaning)")
        return cleaned_path
        
    def generate_metadata_yaml(self) -> Path:
        """Generate Pandoc metadata YAML"""
        self.log("Generating Pandoc metadata")
        
        metadata_content = f"""---
title: "{self.metadata['title']}"
author: "{self.metadata['author']}"
publisher: "{self.metadata.get('publisher', 'Crownwell Press')}"
date: "{self.metadata.get('copyright_year', datetime.now().year)}"
lang: "{self.metadata.get('language', 'en-US')}"
"""
        
        if self.metadata.get('subtitle'):
            metadata_content += f'subtitle: "{self.metadata["subtitle"]}"\n'
            
        if self.metadata.get('isbn'):
            metadata_content += f'identifier: "urn:isbn:{self.metadata["isbn"]}"\n'
            
        if self.metadata.get('description'):
            desc = self.metadata['description'].replace('"', '\\"')
            metadata_content += f'description: "{desc}"\n'
            
        if self.metadata.get('subjects'):
            metadata_content += "subject:\n"
            for subject in self.metadata['subjects']:
                metadata_content += f'  - "{subject}"\n'
                
        metadata_content += "---\n"
        
        pandoc_metadata = self.working_dir / "pandoc-metadata.yaml"
        pandoc_metadata.write_text(metadata_content, encoding='utf-8')
        
        self.log(f"Wrote Pandoc metadata to {pandoc_metadata}")
        return pandoc_metadata
        
    def run_pandoc(self, input_docx: Path, metadata_yaml: Path) -> Path:
        """Execute Pandoc to create EPUB"""
        self.log("Running Pandoc: DOCX → EPUB3")
        
        epub_output = self.working_dir / f"{self.metadata.get('slug', 'book')}.epub"
        
        # Build Pandoc command
        cmd = [
            "pandoc",
            str(input_docx),
            "-o", str(epub_output),
            "--metadata-file", str(metadata_yaml),
            "--toc",
            "--toc-depth=3",
            "--epub-cover-image", str(self.find_cover()) if self.find_cover() else "",
            "--css", str(Path(__file__).parent.parent / "templates" / "epub-styles.css"),
            "--standalone",
            "--self-contained"
        ]
        
        # Remove empty cover arg if no cover found
        cmd = [c for c in cmd if c]
        
        self.log(f"Pandoc command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            self.log("Pandoc conversion successful")
            
            if result.stdout:
                self.log(f"Pandoc stdout: {result.stdout}")
            if result.stderr:
                self.log(f"Pandoc stderr: {result.stderr}", "WARN")
                
            return epub_output
            
        except subprocess.CalledProcessError as e:
            self.log(f"ERROR: Pandoc conversion failed: {e}", "ERROR")
            self.log(f"Pandoc stderr: {e.stderr}", "ERROR")
            sys.exit(1)
            
        except FileNotFoundError:
            self.log("ERROR: Pandoc not found. Install with: sudo apt install pandoc", "ERROR")
            sys.exit(1)
            
    def find_cover(self) -> Optional[Path]:
        """Locate cover image"""
        for ext in ['jpg', 'jpeg', 'png']:
            cover = self.book_dir / f"cover.{ext}"
            if cover.exists():
                self.log(f"Found cover: {cover.name}")
                return cover
        
        self.log("No cover image found (looking for cover.jpg/png)", "WARN")
        return None
        
    def validate_epub(self, epub_path: Path) -> bool:
        """Validate EPUB with epubcheck"""
        self.log("Validating EPUB with epubcheck")
        
        try:
            # Try epubcheck command
            result = subprocess.run(
                ["epubcheck", str(epub_path)],
                capture_output=True,
                text=True
            )
            
            validation_report = self.output_dir / "validation-report.txt"
            validation_report.write_text(
                f"EPUBCHECK VALIDATION\n{'='*50}\n\n{result.stdout}\n{result.stderr}",
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.log("EPUB validation: PASSED")
                return True
            else:
                self.log("EPUB validation: FAILED (see validation-report.txt)", "WARN")
                return False
                
        except FileNotFoundError:
            self.log("epubcheck not found (optional validation skipped)", "WARN")
            self.log("Install: wget https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip", "WARN")
            return False
            
    def finalize_output(self, epub_path: Path) -> None:
        """Copy EPUB to output directory with proper naming"""
        self.log("Finalizing output")
        
        # Determine output filename
        slug = self.metadata.get('slug')
        if not slug:
            # Generate slug from title
            slug = re.sub(r'[^a-z0-9]+', '-', self.metadata['title'].lower()).strip('-')
            
        final_epub = self.output_dir / f"{slug}.epub"
        shutil.copy2(epub_path, final_epub)
        
        self.log(f"EPUB written to: {final_epub}")
        
        # Write build log
        log_path = self.output_dir / "build-log.md"
        log_content = f"""# Build Log
## {self.metadata['title']}

**Build Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### Metadata
- Title: {self.metadata['title']}
- Author: {self.metadata['author']}
- Publisher: {self.metadata.get('publisher', 'Crownwell Press')}

### Build Log

```
{"".join([f"{e}\n" for e in self.log_entries])}
```

### Output Files
- EPUB: {final_epub.name}
- Validation: validation-report.txt (if generated)
"""
        
        log_path.write_text(log_content, encoding='utf-8')
        self.log(f"Build log written to: {log_path}")
        
    def build(self) -> None:
        """Main build orchestration"""
        self.log("=== Crownwell Press EPUB Builder ===")
        self.log(f"Book directory: {self.book_dir}")
        
        # Setup
        self.working_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load metadata
        self.load_metadata()
        
        # Find input
        input_docx = self.find_input_docx()
        
        # Clean DOCX
        cleaned_docx = self.clean_docx(input_docx)
        
        # Generate Pandoc metadata
        pandoc_metadata = self.generate_metadata_yaml()
        
        # Run Pandoc
        epub_path = self.run_pandoc(cleaned_docx, pandoc_metadata)
        
        # Validate
        self.validate_epub(epub_path)
        
        # Finalize
        self.finalize_output(epub_path)
        
        self.log("=== Build Complete ===")


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python build-epub.py <book-directory>")
        print("Example: python build-epub.py books/cartwright-autobiography")
        sys.exit(1)
        
    book_dir = Path(sys.argv[1])
    
    if not book_dir.exists():
        print(f"ERROR: Directory not found: {book_dir}")
        sys.exit(1)
        
    builder = EPUBBuilder(book_dir)
    builder.build()


if __name__ == "__main__":
    main()
