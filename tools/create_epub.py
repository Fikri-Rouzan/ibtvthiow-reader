"""Modular generator for compiling markdown chapters and assets into an EPUB file."""

import html
import mimetypes
import os
import re
import markdown
from ebooklib import epub
from novel_utils import (
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

OUTPUT_EPUB = os.path.join(NOVEL_DIR, f"{NOVEL_FILENAME_BASE}.epub")


class EPUBGenerator:
    """Modular generator for compiling markdown chapters and assets into an EPUB file."""

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
        self.book = epub.EpubBook()
        self.added_images: set[str] = set()
        self.css_item: epub.EpubItem | None = None

    def setup_book_metadata(self, meta: dict) -> None:
        """Set basic EPUB book metadata attributes."""
        self.book.set_identifier("I Became The Villain The Hero Is Obsessed With Novel")
        self.book.set_title(
            meta.get("title", "I Became The Villain The Hero Is Obsessed With")
        )
        self.book.set_language("en")
        self.book.add_author(meta.get("author", "Seo Eun-ha / Westway / 서은하"))

    def setup_stylesheet(self) -> epub.EpubItem:
        """Load external CSS stylesheet and register item with the EPUB book."""
        if os.path.exists(self.style_path):
            with open(self.style_path, "r", encoding="utf-8") as f:
                css_content = f.read()
        else:
            css_content = "p { text-indent: 0; margin-bottom: 1em; }"

        self.css_item = epub.EpubItem(
            uid="style_css",
            file_name="style.css",
            media_type="text/css",
            content=css_content.encode("utf-8"),
        )
        self.book.add_item(self.css_item)
        print(f"[+] Added CSS stylesheet from {self.style_path}")
        return self.css_item

    def add_cover(self) -> epub.EpubHtml | None:
        """Add cover image asset and dedicated cover HTML page to the EPUB book."""
        if not os.path.exists(self.cover_path):
            print(f"[!] Cover image not found at {self.cover_path}, skipping cover.")
            return None

        with open(self.cover_path, "rb") as f:
            cover_bytes = f.read()
        self.book.set_cover("cover.jpg", cover_bytes, create_page=False)

        cover_page = epub.EpubHtml(title="Cover", file_name="cover.xhtml", lang="en")
        cover_page.content = """
        <div class="cover-container">
            <img src="cover.jpg" alt="Cover" class="cover-img" />
        </div>
        """
        if self.css_item:
            cover_page.add_item(self.css_item)

        self.book.add_item(cover_page)
        print(f"[+] Added Cover page and image from {self.cover_path}")
        return cover_page

    def create_information_page(self, meta: dict) -> epub.EpubHtml:
        """Create information page containing title, author, total chapters, and synopsis."""
        title = html.escape(meta.get("title", "Information"))
        author = html.escape(meta.get("author", ""))
        total_chapters = meta.get("total_chapters", 0)
        synopsis_list = meta.get("synopsis", [])

        synopsis_html = "".join(
            f"<p>{html.escape(paragraph)}</p>" for paragraph in synopsis_list
        )

        content = f"""
        <div class="info-container">
            <h1>{title}</h1>
            <hr />
            <p><strong>Author:</strong> {author}</p>
            <p><strong>Total Chapters:</strong> {total_chapters}</p>
            <p><strong>Synopsis:</strong></p>
            {synopsis_html}
        </div>
        """

        info_item = epub.EpubHtml(
            title="Information", file_name="information.xhtml", lang="en"
        )
        info_item.content = content
        if self.css_item:
            info_item.add_item(self.css_item)

        self.book.add_item(info_item)
        print("[+] Created Information page")
        return info_item

    def process_chapter_images(self, html_content: str) -> str:
        """Scan HTML for image references, embed corresponding image files, and update image paths."""
        img_matches = re.findall(r'src=["\']/?images/([^"\']+)["\']', html_content)

        for raw_filename in img_matches:
            # Prevent path traversal by normalizing to basename
            img_filename = os.path.basename(raw_filename)
            if img_filename not in self.added_images:
                img_path = os.path.join(self.images_dir, img_filename)
                if os.path.isfile(img_path):
                    mime_type, _ = mimetypes.guess_type(img_path)
                    if not mime_type:
                        mime_type = "image/jpeg"

                    with open(img_path, "rb") as f:
                        img_data = f.read()

                    epub_img = epub.EpubItem(
                        uid=f"img_{img_filename}",
                        file_name=f"images/{img_filename}",
                        media_type=mime_type,
                        content=img_data,
                    )
                    self.book.add_item(epub_img)
                    self.added_images.add(img_filename)
                    print(f"  [+] Embedded image asset: {img_filename}")
                else:
                    print(f"  [!] Image asset not found: {img_path}")

        # Normalize image src paths to relative EPUB format
        return re.sub(r'src=["\']/?images/', 'src="images/', html_content)

    def process_chapters(self) -> list[epub.EpubHtml]:
        """Read all chapter markdown files, parse frontmatter, convert to HTML, and create EPUB pages."""
        chapters = load_chapter_markdowns(self.chapters_dir)
        chapter_items: list[epub.EpubHtml] = []

        for slug, chapter_title, body_md in chapters:
            safe_title = html.escape(chapter_title)

            # Convert Markdown body content to HTML
            html_body = markdown.markdown(body_md)

            # Update embedded images and add image assets
            html_body_with_images = self.process_chapter_images(html_body)

            full_html = f"""
            <div class="chapter-container">
                <h1>{safe_title}</h1>
                <hr />
                {html_body_with_images}
            </div>
            """

            chapter_item = epub.EpubHtml(
                title=chapter_title,
                file_name=f"chapter_{slug}.xhtml",
                lang="en",
            )
            chapter_item.content = full_html
            if self.css_item:
                chapter_item.add_item(self.css_item)

            self.book.add_item(chapter_item)
            chapter_items.append(chapter_item)

        print(f"[+] Processed {len(chapter_items)} chapter pages.")
        return chapter_items

    def generate(self) -> None:
        """Execute full EPUB creation workflow."""
        meta = load_novel_metadata(self.metadata_path)
        self.setup_book_metadata(meta)
        self.setup_stylesheet()

        cover_item = self.add_cover()
        info_item = self.create_information_page(meta)
        chapter_items = self.process_chapters()

        # Build ordered sections for both table of contents and reading spine
        ordered_sections = [
            *([cover_item] if cover_item else []),
            info_item,
            *chapter_items,
        ]
        self.book.toc = ordered_sections
        self.book.spine = ordered_sections

        # Add mandatory EPUB navigation items
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # Ensure output directory exists and write EPUB file
        ensure_output_dir(self.output_path)
        epub.write_epub(self.output_path, self.book, {})
        print(f"[✓] Successfully generated EPUB at: {self.output_path}")


if __name__ == "__main__":
    try:
        generator = EPUBGenerator(
            chapters_dir=CHAPTERS_DIR,
            images_dir=IMAGES_DIR,
            metadata_path=METADATA_PATH,
            cover_path=COVER_PATH,
            style_path=STYLE_PATH,
            output_path=OUTPUT_EPUB,
        )
        generator.generate()
    except Exception as exc:
        print(f"[X] Error during EPUB generation: {exc}")
        raise SystemExit(1) from exc
