import os
import re
import glob
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, Tag

# Configuration Constants
CHAPTERS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chapters"))
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
    """Modular parser for converting EPUB documents to cleaned Markdown chapters."""

    def __init__(self, epub_path: str, output_dir: str):
        self.epub_path = epub_path
        self.output_dir = output_dir
        self.chapter_counter = 0

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

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

    def process_document_content(self, html_content: bytes) -> str:
        """Extract paragraph and heading text from HTML, preserving inline styles and ignoring images."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Completely remove all image tags and embedded SVG elements
        for img in soup.find_all(["img", "image", "svg", "picture"]):
            img.decompose()

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

            content = self.process_document_content(item.get_content())
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
        parser = EPUBParser(epub_path=epub_file, output_dir=CHAPTERS_DIR)
        parser.parse()
    except Exception as e:
        print(f"[X] Error during parsing: {e}")
