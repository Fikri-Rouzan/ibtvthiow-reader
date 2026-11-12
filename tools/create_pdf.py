"""Modular PDF generator using WeasyPrint and shared EPUB stylesheet."""

import html
import os
import re
import unicodedata
import markdown
from pathlib import Path
from weasyprint import CSS, Document, HTML
from novel_utils import (
    BASE_DIR,
    CHAPTERS_DIR,
    COVER_PATH,
    IMAGES_DIR,
    METADATA_PATH,
    NOVEL_DIR,
    NOVEL_FILENAME_BASE,
    STYLE_PATH,
    ensure_output_dir,
    load_chapter_markdowns,
    load_novel_metadata,
)

OUTPUT_PDF = os.path.join(NOVEL_DIR, f"{NOVEL_FILENAME_BASE}.pdf")

# Regex matching invalid XML/HTML control characters while preserving tabs, newlines, and Unicode/emojis
INVALID_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class PDFGenerationError(Exception):
    """Custom exception raised when PDF compilation or asset validation fails."""


class PDFGenerator:
    """Compiles Markdown chapters, metadata, and images into a single styled PDF file."""

    def __init__(
        self,
        chapters_dir: str,
        images_dir: str,
        metadata_path: str,
        cover_path: str,
        style_path: str,
        output_path: str,
    ) -> None:
        self.chapters_dir = chapters_dir
        self.images_dir = images_dir
        self.metadata_path = metadata_path
        self.cover_path = cover_path
        self.style_path = style_path
        self.output_path = output_path

    def sanitize_unicode_text(self, text: str) -> str:
        """Normalize Unicode (NFC) and strip invalid control characters for CJK and emoji safety.

        Args:
            text: Raw string containing Latin, Korean, Japanese, or emoji characters.

        Returns:
            Normalized UTF-8 string safe for HTML parsing and Pango/WeasyPrint shaping.
        """
        if not text:
            return ""
        # Strip lone UTF-16 surrogates if present
        cleaned = text.encode("utf-8", errors="ignore").decode("utf-8")
        cleaned = INVALID_CONTROL_CHARS_RE.sub("", cleaned)
        return unicodedata.normalize("NFC", cleaned)

    def build_cover_section(self) -> str:
        """Build HTML markup for the cover section if cover.jpg exists.

        Returns:
            HTML string for the cover container, or empty string if cover is missing.
        """
        if not os.path.exists(self.cover_path):
            print(f"[!] Cover image not found at {self.cover_path}, skipping cover.")
            return ""

        cover_uri = Path(self.cover_path).resolve().as_uri()
        print(f"[+] Added Cover image from {self.cover_path}")
        return f"""
        <section class="cover-container">
            <img src="{cover_uri}" alt="Cover" class="cover-img" />
        </section>
        """

    def build_information_section(self, meta: dict) -> str:
        """Build HTML markup for the novel information and synopsis page.

        Args:
            meta: Novel metadata dictionary.

        Returns:
            HTML string for the information section.
        """
        title = html.escape(
            self.sanitize_unicode_text(meta.get("title", "Information"))
        )
        author = html.escape(self.sanitize_unicode_text(meta.get("author", "Unknown")))
        total_chapters = meta.get("total_chapters", 0)
        synopsis_list = meta.get("synopsis", [])

        synopsis_html = "".join(
            f"<p>{html.escape(self.sanitize_unicode_text(paragraph))}</p>"
            for paragraph in synopsis_list
        )

        print("[+] Built Information section")
        return f"""
        <section class="info-container">
            <h1>{title}</h1>
            <hr />
            <p><strong>Author:</strong> {author}</p>
            <p><strong>Total Chapters:</strong> {total_chapters}</p>
            <p><strong>Synopsis:</strong></p>
            {synopsis_html}
        </section>
        """

    def resolve_chapter_images(self, html_content: str) -> str:
        """Resolve local /images/ paths in HTML to absolute file:// URIs for WeasyPrint.

        Args:
            html_content: Rendered chapter HTML string.

        Returns:
            HTML string with local file:// URIs for valid chapter images.
        """
        images_root = Path(self.images_dir).resolve()

        def _replace_src(match: re.Match) -> str:
            raw_filename = match.group(1)
            # Prevent path traversal by taking basename only
            safe_filename = os.path.basename(raw_filename)
            candidate_path = (images_root / safe_filename).resolve()

            if candidate_path.parent != images_root or not candidate_path.is_file():
                print(f"  [!] Missing image asset: {safe_filename}")
                return match.group(0)

            return f'src="{candidate_path.as_uri()}"'

        return re.sub(r'src=["\']/?images/([^"\']+)["\']', _replace_src, html_content)

    def build_chapters_sections(self) -> str:
        """Read all padded Markdown chapters and compile them into HTML sections.

        Returns:
            Concatenated HTML string of all chapter sections.

        Raises:
            PDFGenerationError: If no chapter Markdown files are found.
        """
        try:
            chapters = load_chapter_markdowns(self.chapters_dir)
        except FileNotFoundError as exc:
            raise PDFGenerationError(str(exc)) from exc

        sections: list[str] = []

        for _, chapter_title, body_md in chapters:
            raw_title = self.sanitize_unicode_text(chapter_title)
            safe_title = html.escape(raw_title)

            sanitized_body = self.sanitize_unicode_text(body_md)
            html_body = markdown.markdown(sanitized_body)
            html_body_with_images = self.resolve_chapter_images(html_body)

            sections.append(f"""
                <section class="chapter-container">
                    <h1>{safe_title}</h1>
                    <hr />
                    {html_body_with_images}
                </section>
                """)

        print(f"[+] Processed {len(sections)} chapter sections.")
        return "\n".join(sections)

    def _wrap_html_document(self, body_html: str, doc_title: str, author: str) -> str:
        """Wrap an HTML fragment inside a complete HTML5 document with metadata.

        Args:
            body_html: Inner body HTML markup for a specific document section.
            doc_title: Escaped document title.
            author: Escaped document author.

        Returns:
            Complete HTML5 string with UTF-8 charset and author metadata.
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="author" content="{author}" />
    <title>{doc_title}</title>
</head>
<body>
    {body_html}
</body>
</html>
"""

    def _render_section_document(
        self,
        body_html: str,
        doc_title: str,
        author: str,
        base_uri: str,
        stylesheet: CSS,
    ) -> Document:
        """Render a standalone HTML section into a WeasyPrint Document with isolated counters.

        Args:
            body_html: Inner HTML markup for the section.
            doc_title: Escaped document title.
            author: Escaped document author.
            base_uri: Base file:// URI for resolving assets.
            stylesheet: Loaded WeasyPrint CSS object.

        Returns:
            Rendered WeasyPrint Document instance.
        """
        full_html = self._wrap_html_document(body_html, doc_title, author)
        return HTML(string=full_html, base_url=base_uri).render(
            stylesheets=[stylesheet]
        )

    def generate(self) -> None:
        """Execute the full PDF generation pipeline with independent section page numbering."""
        if not os.path.exists(self.style_path):
            raise PDFGenerationError(f"Stylesheet not found: {self.style_path}")

        try:
            meta = load_novel_metadata(self.metadata_path)
        except (FileNotFoundError, ValueError) as exc:
            raise PDFGenerationError(str(exc)) from exc

        doc_title = html.escape(self.sanitize_unicode_text(meta.get("title", "Novel")))
        author = html.escape(self.sanitize_unicode_text(meta.get("author", "Unknown")))

        cover_html = self.build_cover_section()
        info_html = self.build_information_section(meta)
        chapters_html = self.build_chapters_sections()

        base_uri = Path(BASE_DIR).resolve().as_uri() + "/"
        stylesheet = CSS(filename=self.style_path)

        rendered_docs: list[Document] = []

        if cover_html:
            print("[*] Rendering Cover page...")
            cover_doc = self._render_section_document(
                cover_html, doc_title, author, base_uri, stylesheet
            )
            rendered_docs.append(cover_doc)

        print("[*] Rendering Information page...")
        info_doc = self._render_section_document(
            info_html, doc_title, author, base_uri, stylesheet
        )
        rendered_docs.append(info_doc)

        print("[*] Rendering Chapters (this may take a moment for 465 chapters)...")
        chapters_doc = self._render_section_document(
            chapters_html, doc_title, author, base_uri, stylesheet
        )
        rendered_docs.append(chapters_doc)

        all_pages = [page for doc in rendered_docs for page in doc.pages]
        merged_doc = rendered_docs[0].copy(all_pages)

        ensure_output_dir(self.output_path)
        merged_doc.write_pdf(target=self.output_path)

        print(
            f"[✓] Successfully generated PDF ({len(all_pages)} total pages, "
            f"{len(chapters_doc.pages)} chapter pages) at: {self.output_path}"
        )


if __name__ == "__main__":
    try:
        generator = PDFGenerator(
            chapters_dir=CHAPTERS_DIR,
            images_dir=IMAGES_DIR,
            metadata_path=METADATA_PATH,
            cover_path=COVER_PATH,
            style_path=STYLE_PATH,
            output_path=OUTPUT_PDF,
        )
        generator.generate()
    except Exception as exc:
        print(f"[X] Error during PDF generation: {exc}")
        raise SystemExit(1) from exc
