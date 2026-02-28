import stylistic from '@stylistic/eslint-plugin'
import tsParser from '@typescript-eslint/parser'
import vue from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'
// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt({
  files: ['**/*.{js,ts,jsx,tsx,vue,mjs}'],
  ignores: [
    '**/.nuxt/**',
    '**/.output/**',
    '**/assets/**',
    '**/node_modules/**',
  ],
  languageOptions: {
    parser: vueParser,
    parserOptions: {
      parser: tsParser,
      ecmaVersion: 'latest',
      sourceType: 'module',
      extraFileExtensions: ['.vue'],
    },
  },
  plugins: {
    '@stylistic': stylistic,
    vue,
  },
  rules: {
    ...stylistic.configs.recommended.rules,
    ...vue.configs['strongly-recommended'].rules,

    'vue/max-attributes-per-line': ['error', {
      singleline: {
        max: 1,
      },
      multiline: {
        max: 1,
      },
    }],
  },
})
