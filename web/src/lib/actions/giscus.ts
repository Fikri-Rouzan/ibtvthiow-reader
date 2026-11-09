import { GISCUS_CONFIG } from '#lib/config/giscus';

export interface GiscusActionOptions {
	term: string;
	theme: string;
}

/**
 * Safely mount and update Giscus discussion script.
 */
export function giscusAction(node: HTMLElement, options: GiscusActionOptions) {
	let currentTerm = options.term;

	function mountScript(term: string, theme: string) {
		node.replaceChildren();

		if (!term) return;

		const script = document.createElement('script');
		script.src = 'https://giscus.app/client.js';
		script.setAttribute('data-repo', GISCUS_CONFIG.repo);
		script.setAttribute('data-repo-id', GISCUS_CONFIG.repoId);
		script.setAttribute('data-category', GISCUS_CONFIG.category);
		script.setAttribute('data-category-id', GISCUS_CONFIG.categoryId);
		script.setAttribute('data-mapping', 'specific');
		script.setAttribute('data-term', term);
		script.setAttribute('data-strict', '0');
		script.setAttribute('data-reactions-enabled', '1');
		script.setAttribute('data-emit-metadata', '1');
		script.setAttribute('data-input-position', 'top');
		script.setAttribute('data-theme', theme);
		script.setAttribute('data-lang', 'en');
		script.setAttribute('data-loading', 'lazy');
		script.setAttribute('crossorigin', 'anonymous');
		script.async = true;

		node.appendChild(script);
	}

	mountScript(options.term, options.theme);

	return {
		update(newOptions: GiscusActionOptions) {
			if (newOptions.term !== currentTerm) {
				currentTerm = newOptions.term;
				mountScript(newOptions.term, newOptions.theme);
			} else {
				const iframe = node.querySelector<HTMLIFrameElement>('iframe.giscus-frame');
				if (iframe?.contentWindow) {
					iframe.contentWindow.postMessage(
						{
							giscus: {
								setConfig: {
									theme: newOptions.theme
								}
							}
						},
						'https://giscus.app'
					);
				}
			}
		},
		destroy() {
			node.replaceChildren();
		}
	};
}
