/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                // Shared Theme Tokens? Or specific?
                // Using CSS variables allows dynamic theming if we share index.css
                primary: "var(--color-primary)",
                bg: {
                    main: "var(--color-bg-MAIN)",
                    surface: "var(--color-bg-SURFACE)",
                }
            },
        },
    },
    plugins: [],
}
