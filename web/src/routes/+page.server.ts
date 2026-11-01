import type { PageServerLoad } from './$types';
import { getNovelMetadata } from '#lib/server/reader';

export const load: PageServerLoad = async () => {
	const metadata = await getNovelMetadata();
	return { metadata };
};
