<script setup lang="ts">
import type { HeaderLink } from '#ui-pro/types'

defineProps<{
  links: HeaderLink[]
}>()

// const route = useRoute()
const { $ui } = useNuxtApp()

const route = useRoute()
</script>

<template>
  <UHeader
    :links="links"
    :class="{
      'border-primary-200/75 dark:border-primary-900/50': route.path === '/',
      'border-gray-200 dark:border-gray-800': route.path !== '/',
    }"
    :ui="{
      left: 'min-w-0',
    }"
  >
    <template #left>
      <NuxtLink to="/" class="flex items-end gap-2 font-bold text-xl text-gray-900 dark:text-white min-w-0" aria-label="Nuxt UI">
        <!-- <LogoPro v-if="$route.path.startsWith('/pro')" class="w-auto h-6 shrink-0" /> -->
        <!-- <Logo v-else class="w-auto h-6 shrink-0" /> -->
        <p>综述写作助手</p>
      </NuxtLink>
    </template>

    <template #right>
      <ColorPicker />

      <UColorModeButton />

      <UButton
        to="https://github.com/34-3021/Overview-Writer"
        target="_blank"
        icon="i-simple-icons-github"
        aria-label="GitHub"
        v-bind="($ui.button.secondary as any)"
      />
    </template>

    <template #panel>
      <UAsideLinks :links="links" />

      <UDivider type="dashed" class="my-4" />
    </template>
  </UHeader>
</template>
