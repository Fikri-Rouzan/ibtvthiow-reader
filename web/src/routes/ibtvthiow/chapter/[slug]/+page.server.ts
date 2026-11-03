import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { getChapterBySlug, getNovelMetadata } from '#lib/server/reader';

export const load: PageServerLoad = async ({ params }) => {
	if (!/^\d+$/.test(params.slug)) {
		error(404, `Chapter ${params.slug} not found`);
	}

	const [metadata, chapter] = await Promise.all([
		getNovelMetadata(),
		getChapterBySlug(params.slug)
	]);

	if (!chapter) {
		error(404, `Chapter ${params.slug} not found`);
	}

	const currentIndex = chapter.meta.index;
	const totalChapters = metadata.total_chapters;

	const prevIndex = currentIndex - 1;
	const nextIndex = currentIndex + 1;

	const prevSlug = prevIndex >= 0 ? String(prevIndex).padStart(3, '0') : null;
	const nextSlug = nextIndex < totalChapters ? String(nextIndex).padStart(3, '0') : null;

	return {
		metadata,
		chapter,
		prevSlug,
		nextSlug
	};
};
