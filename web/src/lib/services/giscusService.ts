import { GISCUS_CONFIG } from '#lib/config/giscus';

/**
 * Fetch total discussion comment count for a specific chapter term from Giscus REST API.
 * Returns 0 if the discussion does not exist or network request fails.
 */
export async function getCommentCount(term: string): Promise<number> {
	if (!term || !GISCUS_CONFIG.repo) return 0;

	try {
		const url = new URL('https://giscus.app/api/discussions');
		url.searchParams.set('repo', GISCUS_CONFIG.repo);
		url.searchParams.set('term', term);

		const response = await fetch(url.toString());
		if (!response.ok) return 0;

		const data = await response.json();
		return data?.discussion?.totalCommentCount ?? 0;
	} catch {
		return 0;
	}
}
