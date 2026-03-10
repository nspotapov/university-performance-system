export default defineAppConfig({
  // https://ui.nuxt.com/getting-started/theme#design-system
  ui: {
    colors: {
      primary: 'emerald',
      neutral: 'slate',
    },
    // Принудительно отключаем темную тему
    darkMode: 'class',
    strategy: 'class',
    button: {
      defaultVariants: {
        color: 'primary',
      },
    },
    input: {
      defaultVariants: {
        color: 'primary',
      },
    },
    card: {
      base: 'bg-white dark:bg-white',
    },
  },
})
