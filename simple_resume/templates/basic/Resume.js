import { initializeCssColorVariables } from "/static/color-scheme.js";

initializeCssColorVariables(
	{
		"Open Color": {
			cssVariablesConfigBuilder: ({ neutral, primary }) => ({
				"color-primary": [primary, 9],
				"color-primary-light": [primary, 1],
				"color-background": [neutral, 0],
				"link-color": [primary, 7],
				"reference-border-color": [primary, 3],
				"contact-information-link-color": [primary, 1],
				"example-fixed-color": ["red", 1],
			}),
			defaultColorScheme: {
				neutral: "gray",
				primary: "blue",
			},
		},
		"Radix Colors": {
			cssVariablesConfigBuilder: ({ neutral, primary }) => ({
				"color-primary": [primary, 12],
				"color-primary-light": [primary, 3],
				"color-background": [neutral, 1],
				"link-color": [primary, 11],
				"reference-border-color": [primary, 6],
				"contact-information-link-color": [primary, 5],
			}),
			defaultColorScheme: {
				neutral: "gray",
				primary: "indigo",
			},
		},
		"Reasonable Colors": {
			cssVariablesConfigBuilder: ({ neutral, primary }) => ({
				"color-primary": [primary, 6],
				"color-primary-light": [primary, 2],
				"color-background": [neutral, 1],
				"link-color": [primary, 4],
				"reference-border-color": [primary, 3],
				"contact-information-link-color": [primary, 2],
			}),
			defaultColorScheme: {
				neutral: "gray",
				primary: "indigo",
			},
		},
	},
	"Radix Colors",
);
