<script setup lang="ts">
import { ref } from 'vue'
import { downloadApi } from '~/../api/download'
import { documentAPIs } from '~/../api/document'
import type { DropdownMenuItem } from '@nuxt/ui'

const props = defineProps<{
  docId: number,
  filename: string
}>()

const toast = useToast()
const loading = ref(false)
const selectedFormat = ref(0)

const formats = ref<DropdownMenuItem[]>([
  { label: 'PDF', icon: 'i-material-symbols-picture-as-pdf-outline', onSelect: () => { selectedFormat.value = 0 } },
  { label: 'Markdown', icon: 'i-material-symbols-format-align-left', onSelect: () => { selectedFormat.value = 1 } },
  { label: 'LaTeX (ZIP)', icon: 'i-material-symbols-code', onSelect: () => { selectedFormat.value = 2 } },
])

const formatLabels = ref([
  'pdf',
  'markdown',
  'latex'
])

const handleExport = async () => {
  loading.value = true
  try {
    await downloadApi(
      documentAPIs.export, 
      { format: formatLabels.value[selectedFormat.value] }, 
      { doc_id: props.docId.toString() },
      props.filename
    )
    
    toast.add({
      title: '导出成功',
      color: 'primary'
    })
  } catch (error) {
    toast.add({
      title: '导出失败',
      description: error instanceof Error ? error.message : '未知错误',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-end">
    <UDropdownMenu :items="formats" class="mx">
      <UButton
        color="neutral"
        variant="outline"
        trailing-icon="i-heroicons-chevron-down-20-solid"
      >
        导出格式
      </UButton>
    </UDropdownMenu>
    <UButton
      color="primary"
      :loading="loading"
      @click="handleExport"
      class="ml-3"
    >
      <UIcon name="i-heroicons-arrow-down-tray-20-solid" class="w-5 h-5" />
      导出为 {{ formats[selectedFormat].label }}
    </UButton>
  </div>
</template>
