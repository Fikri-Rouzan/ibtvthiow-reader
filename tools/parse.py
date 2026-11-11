import os
import re
import glob
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, Tag

# Configuration Constants
CHAPTERS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chapters"))
IMAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../images"))
TOOLS_DIR = os.path.abspath(os.path.dirname(__file__))
IGNORED_KEYWORDS = {
    "cover",
    "information",
    "illustrations",
    "title",
    "copyright",
    "toc",
}


class EPUBParser:
    """Modular parser for converting EPUB documents to cleaned Markdown chapters and extracting images."""

    def __init__(self, epub_path: str, output_dir: str, images_dir: str):
        self.epub_path = epub_path
        self.output_dir = output_dir
        self.images_dir = images_dir
        self.chapter_counter = 0

        # Ensure output and images directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

    def is_ignored_item(self, item_name: str) -> bool:
        """Check if the document item should be skipped based on ignored keywords."""
        item_lower = item_name.lower()
        return any(keyword in item_lower for keyword in IGNORED_KEYWORDS)

    def clean_inline_formatting(self, element: Tag) -> str:
        """Convert HTML inline formatting tags (bold, italic) to Markdown syntax."""
        for tag in element.find_all(["b", "strong"]):
            tag.replace_with(f"**{tag.get_text()}**")
        for tag in element.find_all(["i", "em"]):
            tag.replace_with(f"*{tag.get_text()}*")
        return element.get_text().strip()

    def sanitize_line_escapes(self, line: str) -> str:
        """Escape special Markdown triggers at line starts without flattening symbols."""
        # Escape standalone or leading star characters (*, ***, ****)
        if re.match(r"^\*+$", line):
            return "\\" + line

        # Escape leading stars, hashes, or dashes that trigger Markdown blocks
        if re.match(r"^(\*+|-|#+)\s", line):
            return "\\" + line

        return line

    def remove_duplicate_titles(self, lines: list[str]) -> list[str]:
        """Detect and remove redundant chapter title headers at the beginning of content."""
        if len(lines) < 2:
            return lines

        first_line = lines[0].strip()
        second_line = lines[1].strip()

        # Extract base chapter identifier (e.g., "Chapter 0" from "Chapter 0 - Prologue")
        match_first = re.search(r"chapter\s+\d+", first_line, re.IGNORECASE)
        match_second = re.search(r"chapter\s+\d+", second_line, re.IGNORECASE)

        if (
            match_first
            and match_second
            and match_first.group().lower() == match_second.group().lower()
        ):
            # Keep the longer, more descriptive title line and discard the shorter duplicate
            if len(first_line) >= len(second_line):
                return [lines[0]] + lines[2:]
            else:
                return lines[1:]

        return lines

    def find_image_item(self, book: epub.EpubBook, src_filename: str):
        """Find EPUB image item matching the target source filename."""
        src_base = os.path.basename(src_filename).lower()
        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if os.path.basename(item.get_name()).lower() == src_base:
                return item
        return None

    def process_document_content(self, html_content: bytes, book: epub.EpubBook) -> str:
        """Extract paragraph, heading, and image content from HTML, saving images and converting tags to Markdown syntax."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Process and save embedded image files
        image_counter = 1
        for img in soup.find_all(["img", "image"]):
            src = img.get("src") or img.get("href") or img.get("xlink:href")
            if not src:
                img.decompose()
                continue

            src_filename = os.path.basename(src)
            image_item = self.find_image_item(book, src_filename)
            if image_item:
                ext = os.path.splitext(src_filename)[1].lower()
                if not ext or ext not in [
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                    ".gif",
                    ".svg",
                ]:
                    ext = ".jpg"

                image_filename = f"{self.chapter_counter:03d}_{image_counter:02d}{ext}"
                alt_text = (
                    f"Image Chapter {self.chapter_counter:03d}-{image_counter:02d}"
                )
                markdown_image = f"![{alt_text}](/images/{image_filename})"
                image_dest_path = os.path.join(self.images_dir, image_filename)

                with open(image_dest_path, "wb") as f:
                    f.write(image_item.get_content())

                # Replace image element directly inside paragraph or wrap parent container to avoid duplicate paragraphs
                parent_p = img.find_parent("p")
                if parent_p:
                    svg_or_pic = img.find_parent(["svg", "picture"])
                    if svg_or_pic:
                        svg_or_pic.replace_with(markdown_image)
                    else:
                        img.replace_with(markdown_image)
                else:
                    new_p = soup.new_tag("p")
                    new_p.string = markdown_image
                    container = img.find_parent(["svg", "picture"])
                    target_tag = container if container else img
                    target_tag.replace_with(new_p)

                image_counter += 1
            else:
                img.decompose()

        # Remove remaining empty SVG or picture containers
        for tag in soup.find_all(["svg", "picture"]):
            tag.decompose()

        extracted_lines = []

        # Target explicit text blocks (headings and paragraphs)
        for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
            text = self.clean_inline_formatting(element)
            if not text:
                continue

            # Skip standalone `# Chapter X` header lines
            if re.match(r"^#\s*chapter\s*\d+", text, re.IGNORECASE):
                continue

            # Apply Markdown syntax escaping to prevent accidental formatting triggers
            sanitized_text = self.sanitize_line_escapes(text)
            extracted_lines.append(sanitized_text)

        # Clean redundant chapter title occurrences at the document top
        cleaned_lines = self.remove_duplicate_titles(extracted_lines)

        return "\n\n".join(cleaned_lines)

    def parse(self) -> int:
        """Main execution flow for parsing the EPUB file into Markdown files."""
        book = epub.read_epub(self.epub_path)
        documents = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        print(f"[*] Processing EPUB: {os.path.basename(self.epub_path)}")

        for item in documents:
            item_name = item.get_name()
            if self.is_ignored_item(item_name):
                print(f"[!] Ignored non-chapter document: {item_name}")
                continue

            content = self.process_document_content(item.get_content(), book)
            if not content.strip():
                continue

            # Zero-padded filename (e.g., 000.md, 001.md, 002.md)
            filename = f"{self.chapter_counter:03d}.md"
            file_path = os.path.join(self.output_dir, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"[+] Generated: {filename} from {item_name}")
            self.chapter_counter += 1

        print(f"[✓] Parsing complete. Total chapters generated: {self.chapter_counter}")
        return self.chapter_counter


def get_target_epub_file() -> str:
    """Locate the first available .epub file inside the tools directory."""
    epub_files = glob.glob(os.path.join(TOOLS_DIR, "*.epub"))
    if not epub_files:
        raise FileNotFoundError("No .epub file found inside the tools directory.")
    return epub_files[0]


if __name__ == "__main__":
    try:
        epub_file = get_target_epub_file()
        parser = EPUBParser(
            epub_path=epub_file, output_dir=CHAPTERS_DIR, images_dir=IMAGES_DIR
        )
        parser.parse()
    except Exception as e:
        print(f"[X] Error during parsing: {e}")
