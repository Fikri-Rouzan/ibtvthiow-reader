import { DEFAULT_READER_SETTINGS, type ReaderSettings } from '#lib/types/reader';

const LAST_READ_KEY = 'ibtvthiow_last_read_chapter';
const SETTINGS_KEY = 'ibtvthiow_reader_settings';

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

/**
 * Retrieve saved reader configuration settings (theme, font family, sizes) from localStorage.
 * Returns default configuration fallback on SSR or error.
 */
export function getReaderSettings(): ReaderSettings {
	if (typeof window === 'undefined') return DEFAULT_READER_SETTINGS;
	try {
		const saved = localStorage.getItem(SETTINGS_KEY);
		return saved ? { ...DEFAULT_READER_SETTINGS, ...JSON.parse(saved) } : DEFAULT_READER_SETTINGS;
	} catch {
		return DEFAULT_READER_SETTINGS;
	}
}

/**
 * Save updated reader preference settings into client-side localStorage.
 */
export function setReaderSettings(settings: ReaderSettings): void {
	if (typeof window === 'undefined') return;
	localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}
