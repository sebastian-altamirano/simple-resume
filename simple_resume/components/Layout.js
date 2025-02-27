/**
 * @typedef {object} Dataset
 *
 * @property {string} fileName The file name to use when printing to PDF.
 */

const title = document.title;

window.addEventListener("beforeprint", () => {
	const fileName = /** @type {Dataset} */ (document.body.dataset).fileName;
	document.title = fileName;
});

window.addEventListener("afterprint", () => (document.title = title));
