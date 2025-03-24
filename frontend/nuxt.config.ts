import tailwindcss from "@tailwindcss/vite";
// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  extends: ['@nuxt/ui-pro'],
  devtools: { enabled: true },

  modules: [
    '@nuxt/content',
    '@nuxt/fonts',
    '@nuxt/image',
    '@nuxt/ui',
    '@pinia/nuxt',
    '@pinia-plugin-persistedstate/nuxt',
    '@nuxtjs/tailwindcss',
    'motion-v/nuxt',
  ],

  pinia: {
    storesDirs: ['./store/**'],
  },

  piniaPersistedstate: {
    storage: 'cookies',
  },

  runtimeConfig: {
    public: {
      httpBase: process.env.HTTP_BASE || 'http://localhost:3000',
    }
  },

  nitro: {
    devProxy: {
      "/API": {
        target: process.env.NUXT_PUBLIC_HTTP_BASE,
        changeOrigin: true,
        prependPath: true,
      },
    }
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      title: '综述写作助手',
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
    },
  },
  
  compatibilityDate: '2025-02-03',

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  
  css: ['~/assets/css/main.css'],
})