/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
      extend: {
          "colors": {
              "surface-bright": "#2c3a4c",
              "on-surface": "#d4e4fa",
              "on-secondary-fixed-variant": "#6900b3",
              "on-tertiary": "#283044",
              "surface-dim": "#051424",
              "on-background": "#d4e4fa",
              "on-primary": "#640039",
              "surface-container-low": "#0d1c2d",
              "surface-container": "#122131",
              "inverse-on-surface": "#233143",
              "on-secondary": "#490080",
              "inverse-primary": "#b4136d",
              "on-tertiary-fixed-variant": "#3f465c",
              "background": "#051424",
              "surface": "#051424",
              "secondary-fixed": "#f0dbff",
              "outline": "#a68992",
              "error": "#ffb4ab",
              "on-error": "#690005",
              "tertiary": "#bec6e0",
              "surface-container-high": "#1c2b3c",
              "surface-tint": "#ffb0cd",
              "on-error-container": "#ffdad6",
              "primary-container": "#f751a1",
              "on-primary-container": "#570032",
              "secondary": "#ddb7ff",
              "on-tertiary-fixed": "#131b2e",
              "on-secondary-container": "#d6a9ff",
              "tertiary-container": "#8990a8",
              "tertiary-fixed-dim": "#bec6e0",
              "on-primary-fixed": "#3e0022",
              "on-primary-fixed-variant": "#8c0053",
              "tertiary-fixed": "#dae2fd",
              "surface-variant": "#273647",
              "on-surface-variant": "#debec8",
              "primary": "#ffb0cd",
              "on-tertiary-container": "#22293d",
              "on-secondary-fixed": "#2c0051",
              "surface-container-highest": "#273647",
              "primary-fixed": "#ffd9e4",
              "error-container": "#93000a",
              "inverse-surface": "#d4e4fa",
              "surface-container-lowest": "#010f1f",
              "secondary-fixed-dim": "#ddb7ff",
              "secondary-container": "#6f00be",
              "outline-variant": "#574048",
              "primary-fixed-dim": "#ffb0cd"
          },
          "borderRadius": {
              "DEFAULT": "0.25rem",
              "lg": "0.5rem",
              "xl": "0.75rem",
              "full": "9999px"
          },
          "spacing": {
              "gutter": "24px",
              "unit": "8px",
              "margin-desktop": "48px",
              "container-max": "1280px",
              "margin-mobile": "16px"
          },
          "fontFamily": {
              "body-md": ["Inter"],
              "display-lg-mobile": ["Inter"],
              "display-lg": ["Inter"],
              "headline-md": ["Inter"],
              "label-sm": ["Inter"],
              "body-lg": ["Inter"],
              "subtitle-md": ["Inter"]
          },
          "fontSize": {
              "body-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
              "display-lg-mobile": ["36px", { "lineHeight": "44px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
              "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
              "headline-md": ["24px", { "lineHeight": "32px", "letterSpacing": "-0.01em", "fontWeight": "600" }],
              "label-sm": ["14px", { "lineHeight": "20px", "letterSpacing": "0.05em", "fontWeight": "500" }],
              "body-lg": ["18px", { "lineHeight": "28px", "fontWeight": "400" }],
              "subtitle-md": ["16px", { "lineHeight": "24px", "fontWeight": "400" }]
          }
      }
  },
  plugins: [],
}
