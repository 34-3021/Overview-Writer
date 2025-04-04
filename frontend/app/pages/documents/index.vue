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

// 初始化加载论文
onMounted(async () => {
  await refreshDocuments()
})

// 刷新论文列表
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

// 创建论文
const handleCreate = async () => {
  errors.value = []
  
  try {
    // 校验输入
    if (!form.title) throw new Error('论文标题不能为空')
    
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
    useToast().add({ title: '论文创建成功', color: 'primary' })
  } catch (error: any) {
    errors.value = [error.message]
    useToast().add({ 
      title: '创建失败',
      description: error.message,
      color: 'error'
    })
  }
}

// 删除论文
const handleDelete = async (docId: number) => {
  deleteLoading.value = docId
  try {
    await callApi(documentAPIs.delete, {}, { doc_id: docId.toString() })
    await refreshDocuments()
    useToast().add({ title: '论文删除成功', color: 'primary' })
  } finally {
    deleteLoading.value = null
  }
}
</script>

<template>
  <UCard class="max-w-4xl mx-auto">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">论文管理</h2>
        <UModal v-model:open="popover">
          <UButton 
            icon="i-heroicons-plus"
            label="新建论文"
            color="primary"
            @click="popover = true"
            class="ml-10 mr-3"
          />
          <UButton
            icon="i-heroicons-arrow-path-20-solid"
            color="neutral"
            label="刷新文件列表"
            variant="ghost"
            @onclick="refreshDocuments"
          />

          <template #content>
            <UCard class="mx-0 my-0">
              <template #header>
                <h3 class="font-semibold text-lg">新建论文</h3>
              </template>
              <UForm
                :state="form"
                class="space-y-4"
              >
                <UFormField label="论文标题" name="title" required>
                  <UInput
                    v-model="form.title"
                    placeholder="请输入论文标题"
                    autofocus
                    class="w-full"
                  />
                </UFormField>

                <UFormField  
                  label="配置项（JSON格式）"
                  help="可在此处输入论文的配置参数"
                  name="configJson"
                >
                  <UTextarea
                    v-model="form.configJson"
                    placeholder='{"autoSave": true, "template": "default"}'
                    :rows="5"
                    resize
                    class="font-mono text-sm w-full"
                  />
                </UFormField>
              
              </UForm>

              <UAlert
                v-if="errors.length"
                title="校验错误"
                :description="errors.join(', ')"
                icon="i-heroicons-exclamation-triangle"
                color="error"
                variant="subtle"
                class="mt-2"
              />

              <template #footer>
                <UButton
                  label="创建"
                  color="primary"
                  :loading="loading"
                  @click="handleCreate"
                  class="mr-3"
                />
                <UButton
                  label="取消"
                  color="neutral"
                  @click="popover = false"
                  variant="ghost"
                />
              </template>
            </UCard>
          </template>
        </UModal>
      </div>
    </template>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <UProgress animation="elastic" />
    </div>

    <!-- 论文列表 -->
    <div v-if="documents.length" class="space-y-4">
      <div 
        v-for="doc in documents"
        :key="doc.id"
        class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
        @click="navigateTo(`/documents/${doc.id}`)"
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
    <div v-else class="flex flex-col items-center justify-center space-y-2 border border-gray-200 rounded-lg p-6 shadow-sm text-center">
      <UIcon name="i-material-symbols-warning-rounded" class="text-gray-400 text-xl"/>
      <div class="text-gray-600 font-medium text-lg">暂无论文</div>
      <div class="text-gray-400 text-sm">点击上方按钮创建第一个论文</div>
    </div>
  </UCard>
</template>
