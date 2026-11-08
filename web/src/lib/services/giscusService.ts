import { GISCUS_CONFIG } from '#lib/config/giscus';

/**
 * Fetches combined comment and reply count for a specific chapter discussion term
 * using internal server API proxy.
 */
export async function getCommentCount(term: string): Promise<number> {
	if (!term || !GISCUS_CONFIG.repo) return 0;

	try {
		const url = new URL('/api/giscus-count', window.location.origin);
		url.searchParams.set('repo', GISCUS_CONFIG.repo);
		url.searchParams.set('term', term);

		const response = await fetch(url.toString());
		if (!response.ok) return 0;

		const data = await response.json();
		return data?.totalCommentCount ?? 0;
	} catch {
		return 0;
	}
}
