// @ts-check
import withNuxt from './.nuxt/eslint.config.mjs'
import stylistic from '@stylistic/eslint-plugin'
import vue from 'eslint-plugin-vue'
import vueParser from 'vue-eslint-parser'
import tsParser from '@typescript-eslint/parser'

export default withNuxt({
  files: ['**/*.{js,ts,vue,mjs}'],
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
  },
})
