# QUICK START GUIDE

One-page reference for common operations.

---

## Build a Single Book

```bash
python tools/build-epub.py books/book-name
```

**Output**: `books/book-name/output/book-name.epub`

---

## Build via GitHub Actions

1. Go to: Actions → Build EPUB → Run workflow
2. Enter book name: `book-name`
3. Download artifact when complete

---

## Add a New Book

```bash
# 1. Copy template
cp -r books/_example books/new-book

# 2. Add DOCX
cp manuscript.docx books/new-book/input/original.docx

# 3. Edit metadata
nano books/new-book/metadata.yaml

# 4. Build
python tools/build-epub.py books/new-book
```

---

## Check EPUB Quality

```bash
# Validate with epubcheck
epubcheck books/book-name/output/book-name.epub

# View build log
cat books/book-name/output/build-log.md

# View validation report
cat books/book-name/output/validation-report.txt
```

---

## Common Issues

### "Pandoc not found"
```bash
sudo apt install pandoc  # Linux
brew install pandoc      # macOS
```

### "No DOCX file found"
Check: `ls books/book-name/input/`
Should have: `original.docx` or any `.docx` file

### "Missing required metadata"
Edit `books/book-name/metadata.yaml`
Must have: `title`, `author`, `publisher`

---

## File Locations

| Item | Location |
|------|----------|
| Source DOCX | `books/book-name/input/original.docx` |
| Metadata | `books/book-name/metadata.yaml` |
| Cover | `books/book-name/cover.jpg` |
| Output EPUB | `books/book-name/output/book-name.epub` |
| Build log | `books/book-name/output/build-log.md` |
| Validation | `books/book-name/output/validation-report.txt` |

---

## Metadata Template

```yaml
title: "Book Title"
author: "Author Name"
publisher: "Crownwell Press"
copyright_year: 2026
language: "en-US"
slug: "book-slug"
isbn: ""
description: "Book description"
subjects:
  - "Category"
```

---

## Need Help?

1. Check: `books/book-name/output/build-log.md`
2. Read: `README.md`
3. Review: `MIGRATION_NOTES.md`
