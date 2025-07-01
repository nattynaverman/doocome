<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

interface TextCountResult {
  total_words: number
  total_chars: number
  all_total_chars: number
}

const inputText = ref<string>('')
const result = ref<TextCountResult | null>(null)
const isLoading = ref<boolean>(false)
const error = ref<string>('')

const API_URL = 'http://localhost:8000'

const countText = async (): Promise<void> => {
  if (!inputText.value.trim()) {
    error.value = 'กรุณาใส่ข้อความที่ต้องการวิเคราะห์'
    return
  }

  isLoading.value = true
  error.value = ''
  result.value = null

  try {
    const response = await axios.post<TextCountResult>(
      `${API_URL}/count-text`,
      { text: inputText.value },
      { headers: { 'Content-Type': 'application/json' } },
    )
    result.value = response.data
  } catch (err: any) {
    console.error('Error analyzing text:', err)
    error.value =
      err.response?.data?.detail ||
      'เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <header class="bg-white shadow-sm">
      <div class="max-w-5xl mx-auto px-6 py-6">
        <p class="text-2xl font-extrabold text-gray-500">DooCome</p>
      </div>
    </header>

    <section class="flex items-start justify-center py-10 px-4">
      <div class="w-full max-w-3xl bg-white rounded-md shadow-lg p-8">
        <h1 class="text-2xl font-bold text-center text-gray-700 mb-6 drop-shadow-sm">
          DooCome: โปรแกรมวิเคราะห์จำนวนคำและอักษรออนไลน์ฟรี
        </h1>
        <label for="textInput" class="block text-gray-600 mb-2 font-semibold">
          กรุณาใส่ข้อความในช่อง:
        </label>
        <textarea id="textInput" v-model="inputText" placeholder="พิมพ์ข้อความภาษาไทยหรือภาษาอังกฤษที่นี่..." rows="8"
          class="w-full p-4 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-400 focus:outline-none resize-y mb-6"></textarea>

        <div class="text-center">
          <button @click="countText" :disabled="!inputText.trim() || isLoading"
            class="relative inline-flex items-center justify-center px-8 py-3 font-semibold rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed bg-indigo-600 text-white hover:bg-indigo-700 cursor-pointer">
            <span v-if="!isLoading">วิเคราะห์ข้อความ</span>
            <span v-else>กำลังวิเคราะห์…</span>
          </button>
        </div>

        <p v-if="error" class="text-center text-red-600 mt-6">{{ error }}</p>

        <div v-if="result" class="grid grid-flow-col grid-cols-3 gap-4 mt-10">
          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
            <span class="mt-2 text-gray-600">จำนวนคำ
            </span>
            <span class="text-4xl font-bold text-indigo-700">{{
              result.total_words
            }}</span>
            <span class="text-gray-600">คำ</span>
          </div>

          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
            <span class="mt-2 text-gray-600">
              จำนวนตัวอักษร
            </span>
            <span class="text-4xl font-bold text-indigo-700">{{
              result.total_chars
            }}</span>
            <span class="text-gray-600">ตัวอักษร</span>
          </div>

          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
            <span class="mt-2 text-gray-600">จำนวนตัวอักษรทั้งหมด</span>
            <span class="text-4xl font-bold text-indigo-700">{{
              result.all_total_chars
            }}</span>
            <span class="text-gray-600">ตัวอักษร</span>
          </div>
        </div>

      </div>
    </section>

  </div>
</template>
