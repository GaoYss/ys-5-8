<script setup>
const props = defineProps({
  error: {
    type: String,
    default: ''
  },
  notice: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close-error', 'close-notice'])

function handleCloseError() {
  emit('close-error')
}

function handleCloseNotice() {
  emit('close-notice')
}
</script>

<template>
  <div v-if="error || notice || loading" class="status-row">
    <span v-if="loading" class="status neutral">加载中</span>
    <span v-if="notice" class="status success">
      {{ notice }}
      <button class="close-btn" type="button" @click="handleCloseNotice">&times;</button>
    </span>
    <span v-if="error" class="status danger">
      {{ error }}
      <button class="close-btn" type="button" @click="handleCloseError">&times;</button>
    </span>
  </div>
</template>

<style scoped>
.close-btn {
  margin-left: 8px;
  padding: 0 4px;
  background: transparent;
  border: 0;
  color: inherit;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  line-height: 1;
  opacity: 0.8;
}

.close-btn:hover {
  opacity: 1;
}
</style>
