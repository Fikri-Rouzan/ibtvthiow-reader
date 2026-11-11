import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { marked, type TokensList } from 'marked';
import type { NovelMetadata } from '#lib/types/novel';

// Base directory path pointing to the root /chapters folder
const CHAPTERS_DIR = path.resolve(process.cwd(), '../chapters');

/**
 * Fetch unified novel metadata (title, author, total chapters, synopsis, chapter list).
 * Throws an error if metadata.json is missing.
 */
export async function getNovelMetadata(): Promise<NovelMetadata> {
	const jsonPath = path.join(CHAPTERS_DIR, 'metadata.json');
	if (!fs.existsSync(jsonPath)) {
		throw new Error(`Metadata file not found at ${jsonPath}`);
	}
	const fileContent = fs.readFileSync(jsonPath, 'utf-8');
	return JSON.parse(fileContent);
}

/**
 * Retrieve specific chapter content by its padded slug (e.g., "000", "001")
 * and parse Markdown into structured AST tokens using marked.lexer.
 */
export async function getChapterBySlug(slug: string) {
	const filePath = path.join(CHAPTERS_DIR, `${slug}.md`);
	if (!fs.existsSync(filePath)) return null;

	const fileContent = fs.readFileSync(filePath, 'utf-8');
	const { data, content } = matter(fileContent);

	// Parse Markdown content into structured AST tokens
	const tokens: TokensList = marked.lexer(content);

	return {
		meta: {
			...(data as { title: string; index: number }),
			slug
		},
		tokens
	};
}
