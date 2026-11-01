export interface ChapterItem {
	index: number;
	title: string;
	slug: string;
}

export interface NovelMetadata {
	title: string;
	author: string;
	status: string;
	total_chapters: number;
	synopsis: string[];
	chapters: ChapterItem[];
}

export type PaginationItem = number | '...';
export type SortDirection = 'asc' | 'desc';
