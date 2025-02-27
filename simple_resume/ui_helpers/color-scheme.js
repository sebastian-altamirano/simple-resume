/** @import {CssVariableMapper, ColorScheme, ColorSchemeConfig, ColorSchemesConfig, ColorSystem, SimpleResumeMetadata} from "simple-resume" */

/**
 * Returns a function to map a color and scale to a CSS variable.
 *
 * @example
 * 	getCssVariableMapper("Open Color")("red", 5); // "var(--oc-red-5)"
 *
 * @example
 * 	getCssVariableMapper("Radix Colors")("red", 5); // "var(--red-5)"
 *
 * @template {ColorSystem} ColorSystemType
 *
 * @param {ColorSystemType} colorSystem The color system to use for the mapping.
 *
 * @returns {CssVariableMapper<ColorSystemType>} The mapping function.
 */
function getCssVariableMapper(colorSystem) {
	/** @type {{ [ColorSystemKey in ColorSystem]: CssVariableMapper<ColorSystemKey> }} */
	const mappers = {
		"Open Color": (color, scale) => `oc-${color}-${scale}`,
		"Radix Colors": (color, scale) => `${color}-${scale}`,
		"Reasonable Colors": (color, scale) => `color-${color}-${scale}`,
	};

	return (color, scale) => `var(--${mappers[colorSystem](color, scale)})`;
}

/**
 * Determines the CSS color variables that need to be initialized.
 *
 * @example
 * 	// { "color-primary": "oc-red-9", "color-primary-light": "oc-red-1" }
 * 	getCssVariablesToInitialize(colorSchemesConfig, "Open Color");
 *
 * @template {string} ColorCategoryType
 * @template {ColorSystem} DefaultColorSystemType
 *
 * @param {ColorSchemesConfig<ColorCategoryType, DefaultColorSystemType>} colorSchemesConfig The
 *   configuration for each supported color system. If a configuration is not provided for a color
 *   system, it is said to be unsupported.
 * @param {DefaultColorSystemType} defaultColorSystem The color system to use in case
 *   `/meta/simpleResume/template/colorSystem` is not set.
 *
 * @returns {{ [variableName: string]: string }} The CSS variables to initialize.
 */
function getCssVariablesToInitialize(colorSchemesConfig, defaultColorSystem) {
	/** @type {SimpleResumeMetadata<ColorSystem, ColorCategoryType>} */
	const simpleResumeMetadata = JSON.parse(
		/** @type {string} */ (
			/** @type {HTMLScriptElement} */ (document.querySelector("#simple-resume-metadata"))
				.textContent
		),
	);

	/** @type {ColorSystem} */
	let colorSystem = defaultColorSystem;
	/** @type {ColorScheme<typeof colorSystem, ColorCategoryType>} */
	let colorScheme = colorSchemesConfig[defaultColorSystem].defaultColorScheme;
	if (
		typeof simpleResumeMetadata.template === "object" &&
		simpleResumeMetadata.template?.colorSystem &&
		simpleResumeMetadata.template.colorSystem in colorSchemesConfig
	) {
		// The color system defined in the metadata is supported.
		colorSystem = simpleResumeMetadata.template.colorSystem;
		colorScheme = { ...colorScheme, ...simpleResumeMetadata.template.colorScheme };
	}

	const cssVariablesConfig = /** @type {ColorSchemeConfig<ColorSystem, ColorCategoryType>} */ (
		colorSchemesConfig[colorSystem]
	).cssVariablesConfigBuilder(colorScheme);

	/** @type {{ [variableName: string]: string }} */
	const cssVariables = {};
	const cssVariableMapper = getCssVariableMapper(colorSystem);
	Object.entries(cssVariablesConfig).forEach(
		([variableName, [color, scale]]) =>
			(cssVariables[variableName] = cssVariableMapper(color, scale)),
	);

	return cssVariables;
}

/**
 * Initializes the CSS color variables for the template.
 *
 * @template {string} ColorCategoryType
 * @template {ColorSystem} DefaultColorSystemType
 *
 * @param {ColorSchemesConfig<ColorCategoryType, DefaultColorSystemType>} colorSchemesConfig The
 *   configuration for each supported color system. If a configuration is not provided for a color
 *   system, it is said to be unsupported.
 * @param {DefaultColorSystemType} defaultColorSystem The color system to use in case
 *   `/meta/simpleResume/template/colorSystem` is not set.
 *
 * @returns {void}
 */
function initializeCssColorVariables(colorSchemesConfig, defaultColorSystem) {
	const cssVariables = getCssVariablesToInitialize(colorSchemesConfig, defaultColorSystem);
	Object.entries(cssVariables).forEach(([name, value]) =>
		document.documentElement.style.setProperty(`--${name}`, value),
	);
}

export { initializeCssColorVariables };
