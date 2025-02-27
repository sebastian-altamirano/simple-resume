/** @type {import("prettier").Options} */
const prettierConfig = {
	endOfLine: "lf",
	printWidth: 100,
	tabWidth: 4,
	useTabs: true,
};

/** @type {import("prettier-plugin-jsdoc").Options} */
const jsdocPluginConfig = {
	jsdocSeparateTagGroups: true,
};

/** @type {import("prettier").Config} */
export default {
	overrides: [
		{
			files: "*.jinja",
			options: {
				parser: "jinja-template",
			},
		},
	],
	plugins: ["prettier-plugin-jinja-template", "prettier-plugin-jsdoc"],
	...prettierConfig,
	...jsdocPluginConfig,
};
