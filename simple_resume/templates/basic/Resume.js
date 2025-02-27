import { initializeCssColorVariables } from "/static/color-scheme.js";

initializeCssColorVariables(
	{
		"Open Color": {
			cssVariablesConfigBuilder: ({ neutral, primary }) => ({
				"color-background": [neutral, 0],
				"color-primary": [primary, 9],
				"color-primary-light": [primary, 1],
				"contact-information-link-color": [primary, 1],
				"link-color": [primary, 7],
				"reference-border-color": [primary, 3],
			}),
			defaultColorScheme: {
				neutral: "gray",
				primary: "blue",
			},
		},
		"Radix Colors": {
			cssVariablesConfigBuilder: ({ neutral, primary }) => ({
				"color-background": [neutral, 1],
				"color-primary": [primary, 12],
				"color-primary-light": [primary, 3],
				"contact-information-link-color": [primary, 5],
				"link-color": [primary, 11],
				"reference-border-color": [primary, 6],
			}),
			defaultColorScheme: {
				neutral: "gray",
				primary: "indigo",
			},
		},
		"Reasonable Colors": {
			cssVariablesConfigBuilder: ({ neutral, primary }) => ({
				"color-background": [neutral, 1],
				"color-primary": [primary, 6],
				"color-primary-light": [primary, 2],
				"contact-information-link-color": [primary, 2],
				"link-color": [primary, 4],
				"reference-border-color": [primary, 3],
			}),
			defaultColorScheme: {
				neutral: "gray",
				primary: "indigo",
			},
		},
	},
	"Radix Colors",
);
