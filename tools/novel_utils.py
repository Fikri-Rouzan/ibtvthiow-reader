"""Shared configuration constants and file helpers for EPUB and PDF generators."""

import glob
import json
import os
import frontmatter

# Shared Configuration Constants
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
NOVEL_DIR = os.path.join(BASE_DIR, "novel")
METADATA_PATH = os.path.join(CHAPTERS_DIR, "metadata.json")
COVER_PATH = os.path.join(BASE_DIR, "web", "static", "assets", "cover.jpg")
STYLE_PATH = os.path.join(os.path.dirname(__file__), "style.css")
NOVEL_FILENAME_BASE = "I-Became-The-Villain-The-Hero-Is-Obsessed-With"


def ensure_output_dir(output_path: str) -> None:
    """Create the parent output directory if it does not already exist.

    Args:
        output_path: Target file path for the generated artifact.
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)


def load_novel_metadata(metadata_path: str) -> dict:
    """Load and parse novel metadata from a JSON configuration file.

    Args:
        metadata_path: Path to metadata.json.

    Returns:
        Parsed metadata dictionary.

    Raises:
        FileNotFoundError: If the metadata file does not exist.
        ValueError: If the metadata file contains invalid JSON.
    """
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in metadata file: {exc}") from exc


def load_chapter_markdowns(chapters_dir: str) -> list[tuple[str, str, str]]:
    """Read and parse all padded chapter Markdown files in ascending order.

    Args:
        chapters_dir: Directory containing three-digit padded Markdown files.

    Returns:
        List of tuples containing (slug, raw_title, markdown_body).

    Raises:
        FileNotFoundError: If no chapter Markdown files match the expected pattern.
    """
    pattern = os.path.join(chapters_dir, "[0-9][0-9][0-9].md")
    chapter_files = sorted(glob.glob(pattern))

    if not chapter_files:
        raise FileNotFoundError(f"No chapter files found in {chapters_dir}")

    chapters: list[tuple[str, str, str]] = []
    for file_path in chapter_files:
        slug = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        chapter_title = post.get("title", f"Chapter {slug}")
        chapters.append((slug, chapter_title, post.content))

    return chapters
