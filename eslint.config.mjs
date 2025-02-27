import { includeIgnoreFile } from "@eslint/compat";
import js from "@eslint/js";
import json from "@eslint/json";
import markdown from "@eslint/markdown";
import jsdoc from "eslint-plugin-jsdoc";
import perfectionist from "eslint-plugin-perfectionist";
import globals from "globals";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const gitignorePath = path.resolve(__dirname, ".gitignore");

/** @type {import("eslint").Linter.Config[]} */
export default [
	includeIgnoreFile(gitignorePath),

	{
		...js.configs.recommended,
		files: ["**/*.{js,mjs}"],
		languageOptions: { globals: globals.browser },
	},
	{
		...jsdoc.configs["flat/recommended-typescript-flavor-error"],
		files: ["**/*.{js,mjs}"],
	},
	{
		files: ["**/*.{js,mjs}"],
		plugins: { jsdoc },
		rules: {
			// Conflicts with `prettier-plugin-jsdoc`:
			"jsdoc/tag-lines": ["off"],
		},
	},
	{
		...perfectionist.configs["recommended-natural"],
		files: ["**/*.{js,mjs}"],
		languageOptions: { globals: globals.browser },
	},

	{
		...json.configs.recommended,
		files: ["**/*.json"],
		ignores: ["package-lock.json"],
		language: "json/json",
	},
	{
		...json.configs.recommended,
		files: ["**/*.jsonc", ".vscode/*.json", "tsconfig.json"],
		language: "json/jsonc",
	},

	...markdown.configs.recommended.map((config) => ({
		...config,
		language: "markdown/gfm",
	})),
];
