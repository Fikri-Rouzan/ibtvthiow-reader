const LAST_READ_KEY = 'ibtvthiow_last_read_chapter';

/**
 * Retrieve the slug of the last read chapter from client-side localStorage.
 */
export function getLastReadChapter(): string | null {
	if (typeof window === 'undefined') return null;
	return localStorage.getItem(LAST_READ_KEY);
}

/**
 * Persist the slug of the currently read chapter to client-side localStorage.
 */
export function setLastReadChapter(slug: string): void {
	if (typeof window === 'undefined') return;
	localStorage.setItem(LAST_READ_KEY, slug);
}
