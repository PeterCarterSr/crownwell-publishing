# Crownwell Press Publishing System

Professional EPUB3 publishing pipeline for transforming DOCX manuscripts into Big Five quality e-books.

## Overview

This system converts DOCX manuscripts from previous publishers into professional EPUB3 files with:
- Industry-standard formatting and typography
- Automated front matter generation (title page, copyright)
- Table of contents generation
- EPUB3 validation
- GitHub Actions automation

## Quick Start

### Prerequisites

**Local development**:
- Python 3.11+
- Pandoc 3.x: `sudo apt install pandoc` (Linux) or `brew install pandoc` (macOS)
- epubcheck (optional): Download from https://github.com/w3c/epubcheck/releases

**GitHub Actions**: All dependencies installed automatically

### Building Your First Book

1. **Create book directory**:
```bash
mkdir -p books/my-book/input
```

2. **Add your DOCX**:
```bash
cp your-manuscript.docx books/my-book/input/original.docx
```

3. **Create metadata.yaml**:
```bash
cp books/cartwright-autobiography/metadata.yaml books/my-book/metadata.yaml
# Edit with your book details
```

4. **Build EPUB**:
```bash
python tools/build-epub.py books/my-book
```

5. **Find output**:
```
books/my-book/output/my-book.epub
books/my-book/output/build-log.md
books/my-book/output/validation-report.txt
```

## Directory Structure

```
crownwell-publishing/
├── books/                          # One directory per book
│   ├── cartwright-autobiography/
│   │   ├── input/
│   │   │   └── original.docx       # Source manuscript
│   │   ├── metadata.yaml           # Book metadata
│   │   ├── cover.jpg               # Cover image (1600x2560px min)
│   │   ├── working/                # Temporary files (git-ignored)
│   │   └── output/
│   │       ├── book.epub           # Final EPUB3
│   │       ├── build-log.md        # Build process log
│   │       └── validation-report.txt
│   └── _example/                   # Template for new books
├── templates/
│   └── epub-styles.css             # EPUB typography
├── tools/
│   └── build-epub.py               # Main build script
├── .github/workflows/
│   └── build-epub.yml              # GitHub Actions automation
└── README.md
```

## Metadata File Format

Each book requires a `metadata.yaml` file:

```yaml
# Required fields
title: "Book Title"
author: "Author Name"
publisher: "Crownwell Press"

# Publication details
copyright_year: 2026
language: "en-US"
slug: "book-slug"  # Used for filename

# Optional but recommended
isbn: "978-X-XXXX-XXXX-X"
subtitle: "Book Subtitle"
description: |
  Book description text.
  Multiple lines supported.

# Classification
subjects:
  - "Category / Subcategory"
  - "Another Category"

# Rights
rights: "Copyright 2026 by Author"
rights_holder: "Crownwell Press"
```

## GitHub Actions Workflow

### Automated Building

1. Go to: **Actions** → **Build EPUB**
2. Click: **Run workflow**
3. Enter: Book directory name (e.g., `cartwright-autobiography`)
4. Click: **Run workflow**

The workflow will:
- Install all dependencies
- Build the EPUB
- Validate with epubcheck
- Upload artifacts (downloadable EPUB)

### Downloading Results

1. Open the completed workflow run
2. Scroll to **Artifacts** section
3. Download: `epub-[book-name].zip`
4. Extract: Contains EPUB, logs, validation report

## Build Process Details

The build script performs these steps:

1. **Load Metadata**: Read `metadata.yaml`
2. **Find Input**: Locate DOCX in `input/` directory
3. **Clean DOCX**: Remove old publisher references (TODO: implement)
4. **Generate Metadata**: Create Pandoc metadata YAML
5. **Run Pandoc**: Convert DOCX → EPUB3 with:
   - Automatic TOC generation (`--toc`)
   - Cover image integration
   - Professional typography (CSS)
   - Semantic HTML5
6. **Validate**: Run epubcheck for quality assurance
7. **Finalize**: Copy EPUB to output, write logs

## Quality Standards

All EPUBs must meet these standards:

- **Format**: EPUB3 specification compliant
- **Validation**: Zero epubcheck errors
- **Metadata**: Complete Dublin Core metadata
- **Structure**: Semantic HTML5 with proper headings
- **Typography**: Professional CSS styling
- **Accessibility**: WCAG 2.1 AA compliant
- **Cover**: 1600x2560px minimum resolution

## Adding a New Book

1. **Create directory**:
```bash
cp -r books/_example books/new-book-name
```

2. **Add content**:
```bash
cp manuscript.docx books/new-book-name/input/original.docx
cp cover.jpg books/new-book-name/cover.jpg
```

3. **Edit metadata**:
```bash
nano books/new-book-name/metadata.yaml
```

4. **Build**:
```bash
python tools/build-epub.py books/new-book-name
```

## Troubleshooting

### Error: "Pandoc not found"
**Solution**: Install Pandoc
```bash
# Ubuntu/Debian
sudo apt-get install pandoc

# macOS
brew install pandoc

# Windows
# Download from: https://pandoc.org/installing.html
```

### Error: "No DOCX file found"
**Solution**: Ensure DOCX is in `input/` directory
```bash
ls books/your-book/input/
# Should show: original.docx or any .docx file
```

### Error: "Missing required metadata"
**Solution**: Verify `metadata.yaml` has required fields:
- `title`
- `author`
- `publisher`

### EPUB validation warnings
**Not critical**: Most warnings about missing optional elements are acceptable.
**Critical**: Errors must be fixed before publication.

## Advanced Usage

### Custom CSS Styling

Edit `templates/epub-styles.css` to modify typography, layout, colors, etc.

### Batch Processing

Build multiple books:
```bash
for book in books/*/; do
  python tools/build-epub.py "$book"
done
```

### Cover Image Requirements

- **Format**: JPG or PNG
- **Minimum Resolution**: 1600 x 2560 pixels
- **Aspect Ratio**: 1:1.6 (portrait)
- **Filename**: `cover.jpg` or `cover.png`
- **Location**: Book directory root

### DOCX Cleaning (Future Enhancement)

The `clean_docx()` function is designed to:
- Remove "Delmarva Publications" text
- Remove old copyright pages
- Remove old title page content

**Current status**: Basic copy (cleaning not yet implemented)
**To implement**: Use `python-docx` library to parse and modify content

## Future Enhancements

- [ ] Implement full DOCX cleaning (remove old publisher refs)
- [ ] Add MOBI/KPF conversion for Kindle
- [ ] Batch processing workflow
- [ ] Cover design automation
- [ ] ISBN assignment system
- [ ] KDP upload integration
- [ ] EPUB → Print PDF conversion

## Support

For issues or questions:
1. Check build-log.md in output directory
2. Review validation-report.txt for EPUB errors
3. Consult Pandoc documentation: https://pandoc.org/MANUAL.html
4. EPUB3 specification: https://www.w3.org/TR/epub-33/

## License

Crownwell Press Publishing System
© 2026 Crownwell Press
