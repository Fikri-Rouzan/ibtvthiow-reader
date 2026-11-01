import os
import glob
import json
import re
import frontmatter

# Configuration Constants
CHAPTERS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chapters"))

# Novel General Information
NOVEL_METADATA = {
    "title": "I Became The Villain The Hero Is Obsessed With",
    "author": "Seo Eun-ha / Westway / 서은하",
    "status": "Completed",
    "synopsis": [
        "I became the villain in the story of a hero.",
        "So I was about to quit after fighting the main character.",
        "But she's obsessed with me. Why…?",
    ],
}


class FrontmatterProcessor:
    """Modular processor to inject frontmatter in-place and generate metadata.json."""

    def __init__(self, chapters_dir: str):
        self.chapters_dir = chapters_dir
        self.chapters_meta_list = []

        os.makedirs(self.chapters_dir, exist_ok=True)

    def extract_title_and_body(
        self, raw_content: str, default_title: str
    ) -> tuple[str, str]:
        """
        Extract the title from the first non-empty line if it acts as a chapter heading,
        and return the extracted title along with the remaining cleaned body text.
        """
        lines = [
            line.strip() for line in raw_content.strip().split("\n") if line.strip()
        ]
        if not lines:
            return default_title, raw_content

        first_line = lines[0]
        cleaned_first_line = re.sub(r"^#+\s*", "", first_line).strip()

        # Detect chapter title headers (e.g., "Chapter 0 - Prologue" or short header lines)
        if (
            re.match(r"^chapter\s+\d+", cleaned_first_line, re.IGNORECASE)
            or len(cleaned_first_line) < 80
        ):
            title = cleaned_first_line
            body = "\n\n".join(lines[1:])
            return title, body

        return default_title, raw_content

    def process_file_in_place(self, file_path: str) -> dict:
        """Inject frontmatter into target markdown file and write back in-place."""
        filename = os.path.basename(file_path)
        slug = os.path.splitext(filename)[0]

        try:
            index = int(slug)
        except ValueError:
            index = 0

        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()

        default_title = f"Chapter {index}"
        title, body_content = self.extract_title_and_body(raw_content, default_title)

        # Build frontmatter post structure
        post = frontmatter.Post(
            body_content, title=title, index=index, discussion=str(index)
        )

        # Write formatted frontmatter back to the original file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))

        return {"index": index, "title": title, "slug": slug}

    def generate_metadata_json(self, total_chapters: int) -> None:
        """Generate unified chapters/metadata.json."""
        metadata = {
            "title": NOVEL_METADATA["title"],
            "author": NOVEL_METADATA["author"],
            "status": NOVEL_METADATA["status"],
            "total_chapters": total_chapters,
            "synopsis": NOVEL_METADATA["synopsis"],
            "chapters": self.chapters_meta_list,
        }

        json_path = os.path.join(self.chapters_dir, "metadata.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"[✓] Created metadata.json with total_chapters: {total_chapters}")

    def execute(self) -> int:
        """Run frontmatter injection across all padded chapter markdown files."""
        pattern = os.path.join(self.chapters_dir, "[0-9][0-9][0-9].md")
        chapter_files = sorted(glob.glob(pattern))

        print(f"[*] Processing Frontmatter for {len(chapter_files)} markdown files...")

        for file_path in chapter_files:
            entry = self.process_file_in_place(file_path)
            self.chapters_meta_list.append(entry)
            print(
                f"[+] Added Frontmatter to {os.path.basename(file_path)} -> Title: '{entry['title']}' | Discussion: '{entry['index']}'"
            )

        total_count = len(self.chapters_meta_list)
        self.generate_metadata_json(total_count)
        return total_count


if __name__ == "__main__":
    try:
        processor = FrontmatterProcessor(CHAPTERS_DIR)
        processor.execute()
    except Exception as e:
        print(f"[X] Error during frontmatter processing: {e}")
