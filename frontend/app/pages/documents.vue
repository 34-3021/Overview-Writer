<!-- app/pages/documents.vue -->
<script setup lang="ts">
import { callApi } from '~/../api/api'
import { documentAPIs } from '~/../api/document'
import { z } from 'zod'

const popover = ref(false)
const form = reactive({
  title: '',
  configJson: '{}'
})
const errors = ref<string[]>([])
const configSchema = z.record(z.any()).optional()

const documents = ref<any[]>([])
const loading = ref(false)
const deleteLoading = ref<number | null>(null)

// 初始化加载文档
onMounted(async () => {
  await refreshDocuments()
})

// 刷新文档列表
const refreshDocuments = async () => {
  loading.value = true
  try {
    const { type, data } = await callApi(documentAPIs.list, {})
    if (type !== "success") {
      useToast().add({ title: '加载失败', color: 'warning' })
      return
    }
    documents.value = data
  } finally {
    loading.value = false
  }
}

// 创建文档
const handleCreate = async () => {
  errors.value = []
  
  try {
    // 校验输入
    if (!form.title) throw new Error('文档标题不能为空')
    
    let config = {}
    try {
      config = JSON.parse(form.configJson)
      configSchema.parse(config)
    } catch (e) {
      throw new Error('配置项必须是合法的JSON格式')
    }

    // 调用API
    await callApi(documentAPIs.create, {
      title: form.title,
      content: { sections: [] }, // 初始空内容
      config
    })
    
    // 重置表单
    form.title = ''
    form.configJson = '{}'
    popover.value = false
    
    await refreshDocuments()
    useToast().add({ title: '文档创建成功', color: 'primary' })
  } catch (error: any) {
    errors.value = [error.message]
    useToast().add({ 
      title: '创建失败',
      description: error.message,
      color: 'error'
    })
  }
}

// 删除文档
const handleDelete = async (docId: number) => {
  deleteLoading.value = docId
  try {
    await callApi(documentAPIs.delete, {}, { doc_id: docId.toString() })
    await refreshDocuments()
    useToast().add({ title: '文档删除成功', color: 'primary' })
  } finally {
    deleteLoading.value = null
  }
}
</script>

<template>
  <UCard class="max-w-4xl mx-auto">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">文档管理</h2>
        <UModal v-model="popover">
          <UButton 
            icon="i-heroicons-plus"
            label="新建文档"
            color="primary"
            @click="popover = true"
          />

          <template #content>
            <div class="p-4 w-96 space-y-4">
              <h3 class="font-semibold text-lg">新建文档</h3>
              
              <UFormGroup label="文档标题" required>
                <UInput 
                  v-model="form.title"
                  placeholder="请输入文档标题"
                  autofocus
                />
              </UFormGroup>

              <UFormGroup 
                label="配置项（JSON格式）"
                help="可在此处输入文档的配置参数"
              >
                <UTextarea
                  v-model="form.configJson"
                  placeholder='{"autoSave": true, "template": "default"}'
                  :rows="5"
                  resize
                  class="font-mono text-sm"
                />
              </UFormGroup>

              <UAlert
                v-if="errors.length"
                title="校验错误"
                :description="errors.join(', ')"
                icon="i-heroicons-exclamation-triangle"
                color="error"
                variant="subtle"
              />

              <div class="flex gap-2 justify-end">
                <UButton
                  label="取消"
                  color="neutral"
                  @click="popover = false"
                />
                <UButton
                  label="创建"
                  color="primary"
                  :loading="loading"
                  @click="handleCreate"
                />
              </div>
            </div>
          </template>
        </UModal>
      </div>
    </template>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <UProgress animation="elastic" />
    </div>

    <!-- 文档列表 -->
    <div v-if="documents.length" class="space-y-4">
      <div 
        v-for="doc in documents"
        :key="doc.id"
        class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
      >
        <div>
          <h3 class="font-medium">{{ doc.title }}</h3>
          <p class="text-sm text-gray-500 mt-1">
            创建于 {{ new Date(doc.created_at).toLocaleDateString() }}
          </p>
        </div>
        
        <UButton
          color="warning"
          variant="ghost"
          :loading="deleteLoading === doc.id"
          @click="handleDelete(doc.id)"
          icon="i-heroicons-trash"
        />
      </div>
    </div>

    <!-- 空状态 -->
    <UEmptyState
      v-else
      icon="i-heroicons-document"
      title="暂无文档"
      description="点击上方按钮创建第一个文档"
    />
  </UCard>
</template>
