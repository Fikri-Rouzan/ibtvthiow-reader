import fs from 'node:fs';
import path from 'node:path';
import type { RequestHandler } from './$types';

// Path pointing to the root /images folder
const IMAGES_DIR = path.resolve(process.cwd(), '../images');

const MIME_TYPES: Record<string, string> = {
	'.jpg': 'image/jpeg',
	'.jpeg': 'image/jpeg',
	'.png': 'image/png',
	'.webp': 'image/webp',
	'.gif': 'image/gif',
	'.svg': 'image/svg+xml'
};

/**
 * Serve extracted chapter image assets from the root /images directory.
 */
export const GET: RequestHandler = async ({ params }) => {
	const filename = params.file;
	const safeFilename = path.basename(filename);
	const filePath = path.join(IMAGES_DIR, safeFilename);

	if (!fs.existsSync(filePath)) {
		return new Response('Image not found', { status: 404 });
	}

	const ext = path.extname(safeFilename).toLowerCase();
	const contentType = MIME_TYPES[ext] || 'application/octet-stream';
	const fileBuffer = fs.readFileSync(filePath);

	return new Response(fileBuffer, {
		headers: {
			'Content-Type': contentType,
			'Cache-Control': 'public, max-age=31536000, immutable'
		}
	});
};
