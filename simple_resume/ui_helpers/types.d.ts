export type ColorSystem = "Open Color" | "Radix Colors" | "Reasonable Colors";

// #region ColorSystemColor
export type OpenColorColor =
	| "blue"
	| "cyan"
	| "grape"
	| "gray"
	| "green"
	| "indigo"
	| "lime"
	| "orange"
	| "pink"
	| "red"
	| "teal"
	| "violet"
	| "yellow";

export type RadixColorsColor =
	| "amber"
	| "blue"
	| "bronze"
	| "brown"
	| "crimson"
	| "cyan"
	| "gold"
	| "grass"
	| "gray"
	| "green"
	| "indigo"
	| "iris"
	| "jade"
	| "lime"
	| "mauve"
	| "mint"
	| "olive"
	| "orange"
	| "pink"
	| "plum"
	| "purple"
	| "red"
	| "ruby"
	| "sage"
	| "sand"
	| "sky"
	| "slate"
	| "teal"
	| "tomato"
	| "violet"
	| "yellow";

export type ReasonableColorsColor =
	| "amber"
	| "aquamarine"
	| "azure"
	| "blue"
	| "cerulean"
	| "chartreuse"
	| "cinnamon"
	| "cyan"
	| "emerald"
	| "gray"
	| "green"
	| "indigo"
	| "lime"
	| "magenta"
	| "orange"
	| "pink"
	| "powder"
	| "purple"
	| "raspberry"
	| "red"
	| "rose"
	| "sky"
	| "teal"
	| "violet"
	| "yellow";

type _ColorSystemColor = {
	"Open Color": OpenColorColor;
	"Radix Colors": RadixColorsColor;
	"Reasonable Colors": ReasonableColorsColor;
};
export type ColorSystemColor = {
	[ColorSystemKey in ColorSystem]: _ColorSystemColor[ColorSystemKey];
};
// #endregion

// #region ColorSystemScale
export type OpenColorScale = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;

export type RadixColorsScale = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

export type ReasonableColorsScale = 1 | 2 | 3 | 4 | 5 | 6;

type _ColorSystemScale = {
	"Open Color": OpenColorScale;
	"Radix Colors": RadixColorsScale;
	"Reasonable Colors": ReasonableColorsScale;
};
export type ColorSystemScale = {
	[ColorSystemKey in ColorSystem]: _ColorSystemScale[ColorSystemKey];
};
// #endregion

export type CssVariablesConfigBuilder<
	ColorSystemType extends ColorSystem,
	ColorCategoryType extends string,
> = (colorScheme: ColorScheme<ColorSystemType, ColorCategoryType>) => {
	[variableName: string]: [ColorSystemColor[ColorSystemType], ColorSystemScale[ColorSystemType]];
};

export type CssVariableMapper<ColorSystemType extends ColorSystem> = (
	color: ColorSystemColor[ColorSystemType],
	scale: ColorSystemScale[ColorSystemType],
) => string;

export type ColorScheme<
	ColorSystemType extends ColorSystem,
	ColorCategoryType extends string,
> = Record<ColorCategoryType, ColorSystemColor[ColorSystemType]>;

export type ColorSchemeConfig<
	ColorSystemType extends ColorSystem,
	ColorCategoryType extends string,
> = {
	cssVariablesConfigBuilder: CssVariablesConfigBuilder<ColorSystemType, ColorCategoryType>;
	defaultColorScheme: ColorScheme<ColorSystemType, ColorCategoryType>;
};

export type ColorSchemesConfig<
	ColorCategoryType extends string,
	DefaultColorSystem extends ColorSystem,
> = {
	[ColorSystemKey in DefaultColorSystem]: ColorSchemeConfig<ColorSystemKey, ColorCategoryType>;
} & {
	[ColorSystemKey in ColorSystem]?: ColorSchemeConfig<ColorSystemKey, ColorCategoryType>;
};

// #region Simple Resume metadata
export type SimpleResumeMetadata<
	ColorSystemType extends ColorSystem,
	ColorCategoryType extends string,
> = {
	language: string | null;
	template: SimpleResumeTemplateMetadata<ColorSystemType, ColorCategoryType> | string | null;
};

export type SimpleResumeTemplateMetadata<
	ColorSystemType extends ColorSystem,
	ColorCategoryType extends string,
> = {
	name: string;
	referencesOnRequest?: boolean;
} & (
	| {
			colorScheme: null;
			colorSystem: null;
	  }
	| {
			colorScheme: ColorScheme<ColorSystemType, ColorCategoryType> | null;
			colorSystem: ColorSystem;
	  }
);
// #endregion
