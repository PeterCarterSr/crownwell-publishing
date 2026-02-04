# CROWNWELL PRESS PUBLISHING SYSTEM
## Architecture Redesign - February 2026

### OBJECTIVE
Transform DOCX manuscripts from previous publisher (Delmarva Publications) into 
professional EPUB3 files meeting Big Five publishing standards (Simon & Schuster quality).

### REQUIREMENTS
1. Remove all "Delmarva Publications" references
2. Insert "Crownwell Press" branding
3. Generate professional title page
4. Generate professional copyright page
5. Preserve manuscript content (no prose editing)
6. Produce validated EPUB3
7. Automated pipeline via GitHub Actions

### ARCHITECTURE

Input:
- original.docx (manuscript from old publisher)
- metadata.yaml (book metadata)
- cover.jpg (cover image, 1600x2560px minimum)

Process:
1. DOCX cleaning (remove old publisher refs)
2. Front matter generation (title page, copyright)
3. Pandoc DOCX → EPUB3 conversion
4. Cover integration
5. EPUB validation (epubcheck)

Output:
- book.epub (production-ready EPUB3)
- validation-report.txt
- build-log.md

### TECHNOLOGY STACK
- Python 3.11+
- Pandoc 3.x
- epubcheck 5.x
- python-docx (DOCX manipulation)
- lxml (XML processing)

### QUALITY STANDARDS
- EPUB3 specification compliant
- Zero epubcheck errors
- Dublin Core metadata complete
- Semantic HTML5
- Professional typography
- Accessible (WCAG 2.1 AA)
