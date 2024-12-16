/**
 * @typedef {Object} Dataset
 * @property {string} fileName
 */

const title = document.title;

window.addEventListener("beforeprint", () => {
	const fileName = /** @type {Dataset} */ (document.body.dataset).fileName;
	document.title = fileName;
});

window.addEventListener("afterprint", () => (document.title = title));
