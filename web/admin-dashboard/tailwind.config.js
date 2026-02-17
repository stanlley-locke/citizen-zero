/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                mono: {
                    900: '#000000',
                    800: '#111111',
                    700: '#333333',
                    600: '#4B5563',
                    500: '#6B7280',
                    200: '#E5E7EB',
                    100: '#F3F4F6',
                    50: '#FFFFFF',
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                ocr: ['"Share Tech Mono"', 'monospace'], // The "Visa" font
            },
        },
    },
    plugins: [],
}
