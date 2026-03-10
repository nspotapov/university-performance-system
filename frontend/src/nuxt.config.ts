// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@nuxt/image',
  ],
  imports: {
    autoImport: true,
    dirs: [
      './types',
    ],
  },
  css: [
    '~/assets/css/nuxtui.css',
    '~/assets/scss/main.scss',
  ],
  runtimeConfig: {
    public: {
      baseApiUrl: '/api',
    },
  },
  // Отключаем темную тему
  colorMode: {
    preference: 'light',
    fallback: 'light',
  },
})
