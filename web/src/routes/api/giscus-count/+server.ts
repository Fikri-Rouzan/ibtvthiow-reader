import type { RequestHandler } from '@sveltejs/kit';

/**
 * GET request handler to fetch and proxy total comment & reply counts from Giscus API.
 */
export const GET: RequestHandler = async ({ url, fetch }) => {
	const repo = url.searchParams.get('repo');
	const term = url.searchParams.get('term');

	// Return zero count on missing required query parameters
	if (!repo || !term) {
		return Response.json({ totalCommentCount: 0 }, { status: 400 });
	}

	try {
		const giscusUrl = new URL('https://giscus.app/api/discussions');
		giscusUrl.searchParams.set('repo', repo);
		giscusUrl.searchParams.set('term', term);

		// Execute HTTP fetch request to Giscus REST API endpoint
		const response = await fetch(giscusUrl.toString());

		if (!response.ok) {
			return Response.json({ totalCommentCount: 0 });
		}

		const data = await response.json();

		// Aggregate both top-level comments and nested reply comments
		const mainCommentCount = data?.discussion?.totalCommentCount ?? 0;
		const replyCommentCount = data?.discussion?.totalReplyCount ?? 0;
		const totalCommentCount = mainCommentCount + replyCommentCount;

		return Response.json({ totalCommentCount });
	} catch {
		return Response.json({ totalCommentCount: 0 });
	}
};
