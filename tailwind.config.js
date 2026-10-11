/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nyaya: {
          bg: '#08090B',       // Primary background
          surface: '#111318',  // Secondary background / sidebar
          card: '#191B20',     // Elevated cards
          elevated: '#22252C', // Hover / popovers
          border: '#2B2D33',   // Border line
          subtle: '#1C1E24',   // Subtle separators
        },
        violet: {
          400: '#9E91FF',
          500: '#8B7CFF',      // Primary accent: Electric Violet
          600: '#7564F5',
          700: '#5F4EE0',
          900: '#231F47',
          950: '#15132A',
        },
        amber: {
          400: '#F5B942',      // Important highlights: Warm amber
          500: '#E5A52B',
          900: '#3D2A0E',
        },
        emerald: {
          400: '#36C98F',      // Verified evidence: Restrained emerald
          500: '#28B079',
          900: '#0E3624',
        },
        text: {
          primary: '#F5F5F5',  // Primary text
          secondary: '#A5A7AD',// Secondary text
          dim: '#6E7079',
          // Backward-compatible tokens
          warm: '#F5F5F5',
          slate: '#A5A7AD',
        },
        // Mapped legacy tokens for seamless backward compatibility
        navy: {
          950: '#040507',
          900: '#08090B',
          850: '#111318',
          800: '#191B20',
          750: '#22252C',
          700: '#2B2D33',
          600: '#3D404A',
          500: '#525562',
        },
        gold: {
          300: '#9E91FF',
          400: '#8B7CFF', // Replaced with electric violet
          500: '#7564F5',
          600: '#5F4EE0',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Geist', 'Manrope', 'system-ui', 'sans-serif'],
        serif: ['"Playfair Display"', 'Merriweather', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'monospace']
      },
      boxShadow: {
        'card': '0 4px 24px -2px rgba(0, 0, 0, 0.65)',
        'violet-glow': '0 0 24px -4px rgba(139, 124, 255, 0.25)',
        'amber-glow': '0 0 24px -4px rgba(245, 185, 66, 0.25)',
        'modal': '0 25px 60px -15px rgba(0, 0, 0, 0.85)',
      }
    },
  },
  plugins: [],
}
