import os
import re
import subprocess
from datetime import datetime

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def yaml_get_path(yaml_text: str, dotted: str) -> str:
    """
    Minimal extractor for our controlled YAML structure.
    Assumes 2-space indentation, simple scalars, no lists.
    """
    parts = dotted.split(".")
    block = yaml_text
    for p in parts[:-1]:
        m = re.search(rf"^{re.escape(p)}:\s*$", block, re.MULTILINE)
        if not m:
            return ""
        header_line = block[:m.start()].splitlines()[-1]
        indent = len(header_line) - len(header_line.lstrip(" "))
        rest = block[m.end():]
        lines = rest.splitlines()
        kept = []
        for ln in lines:
            if not ln.strip():
                kept.append(ln)
                continue
            ln_indent = len(ln) - len(ln.lstrip(" "))
            if ln_indent <= indent:
                break
            kept.append(ln)
        block = "\n".join(kept)

    last = parts[-1]
    m2 = re.search(rf"^{re.escape(last)}:\s*\"?([^\"]*)\"?\s*$", block, re.MULTILINE)
    return m2.group(1).strip() if m2 else ""

def pandoc_docx_to_html(docx_path: str) -> str:
    r = subprocess.run(
        ["pandoc", docx_path, "-t", "html5", "--standalone"],
        check=True,
        capture_output=True,
        text=True,
    )
    return r.stdout

def extract_body(html: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1) if m else html

def markdown_block_to_html(md: str) -> str:
    md = md.strip()
    if not md:
        return ""
    md = md.replace("\r\n", "\n")
    md = re.sub(r"^# (.*)$", r"<h1>\1</h1>", md, flags=re.MULTILINE)
    md = re.sub(r"^## (.*)$", r"<h2>\1</h2>", md, flags=re.MULTILINE)
    paragraphs = [p.strip() for p in md.split("\n\n") if p.strip()]
    out = []
    for p in paragraphs:
        if p.startswith("<h1>") or p.startswith("<h2>"):
            out.append(p)
        else:
            out.append("<p>" + p.replace("\n", "<br/>\n") + "</p>")
    return "\n".join(out)

def fill_placeholders(tpl: str, mapping: dict) -> str:
    out = tpl
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v or "")
    return out

def main():
    project_yaml = os.environ.get("PROJECT_YAML", "").strip()
    if not project_yaml:
        raise SystemExit("PROJECT_YAML env var is required (path to runs/<run>/project.yaml).")

    y = read_text(project_yaml)

    run_id = yaml_get_path(y, "run.id") or "run"
    title = yaml_get_path(y, "book.title") or "Untitled"
    subtitle = yaml_get_path(y, "book.subtitle")
    author = yaml_get_path(y, "book.author")
    imprint = yaml_get_path(y, "book.imprint") or "Crownwell Press"

    input_path = yaml_get_path(y, "input.path")
    output_root = yaml_get_path(y, "output.path")
    asin = yaml_get_path(y, "metadata.asin") or "PENDING"

    if not input_path or not output_root:
        raise SystemExit("input.path and output.path must be set in project.yaml.")

    if not os.path.exists(input_path):
        raise SystemExit(f"Input DOCX not found at: {input_path}")

    converted_html = pandoc_docx_to_html(input_path)
    body_html = extract_body(converted_html)

    title_tpl = read_text("templates/front-matter/title-page.md")
    copyright_tpl = read_text("templates/copyright/copyright-page.md")
    imprint_tpl = read_text("templates/back-matter/imprint-page.md")
    cta_tpl = read_text("templates/back-matter/call-to-action.md")
    author_bio_tpl = read_text("templates/back-matter/author-bio.md")

    placeholders = {
        "BOOK_TITLE": title,
        "BOOK_SUBTITLE": subtitle or "",
        "BOOK_AUTHOR": author or "",
        "IMPRINT_NAME": imprint,
        "COPYRIGHT_YEAR": str(datetime.now().year),
        "EDITION_STATEMENT": "Ebook edition",
        "ASIN": asin,
        "AUTHOR_BIO": "Author bio forthcoming.",
        "RUN_ID": run_id,
    }

    fm_title = markdown_block_to_html(fill_placeholders(title_tpl, placeholders))
    fm_copyright = markdown_block_to_html(fill_placeholders(copyright_tpl, placeholders))
    bm_author = markdown_block_to_html(fill_placeholders(author_bio_tpl, placeholders))
    bm_imprint = markdown_block_to_html(fill_placeholders(imprint_tpl, placeholders))
    bm_cta = markdown_block_to_html(fill_placeholders(cta_tpl, placeholders))

    assembled = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="publisher" content="{imprint}">
</head>
<body>
<section id="front-matter">
{fm_title}
{fm_copyright}
</section>

<hr/>

<section id="content">
{body_html}
</section>

<hr/>

<section id="back-matter">
{bm_author}
{bm_imprint}
{bm_cta}
</section>
</body>
</html>
"""

    os.makedirs(output_root, exist_ok=True)
    write_text(os.path.join(output_root, "book.html"), assembled)

    report = f"""# Build Report (Phase 1A)

Run: {run_id}

Input: {input_path}

Output:
- {output_root}/book.html
- {output_root}/reports/build-report.md

Notes:
- DOCX converted to HTML via pandoc.
- Crownwell front/back matter templates injected.
- No content rewriting performed.
- TOC generation not implemented yet (Phase 1A.2).
"""
    write_text(os.path.join(output_root, "reports", "build-report.md"), report)

if __name__ == "__main__":
    main()
