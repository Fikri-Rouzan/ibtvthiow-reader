import { getNovelMetadata } from '#lib/server/reader';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const metadata = await getNovelMetadata();
	return { metadata };
};
