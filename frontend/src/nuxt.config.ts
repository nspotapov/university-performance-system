// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@nuxt/image',
    '@nuxtjs/color-mode',
  ],
  imports: {
    autoImport: true,
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
  colorMode: {
    preference: 'system',
    fallback: 'light',
    classSuffix: '',
  },
})
