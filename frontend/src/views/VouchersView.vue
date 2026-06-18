<script setup>
import { onMounted, ref, computed } from 'vue'
import StatusBanner from '../components/StatusBanner.vue'
import { useLoyaltyData } from '../stores/useLoyaltyData'

const { state, refreshAll, issueBirthdayVouchers, redeemVoucher, revertVoucher } = useLoyaltyData()
const issuedCount = ref(null)

const confirmDialog = ref({
  visible: false,
  title: '',
  message: '',
  confirmText: '确定',
  cancelText: '取消',
  onConfirm: null
})

onMounted(refreshAll)

async function submitIssue() {
  const vouchers = await issueBirthdayVouchers()
  issuedCount.value = vouchers.length
}

function showConfirm(options) {
  confirmDialog.value = {
    visible: true,
    title: options.title || '确认',
    message: options.message || '',
    confirmText: options.confirmText || '确定',
    cancelText: options.cancelText || '取消',
    onConfirm: options.onConfirm
  }
}

function closeConfirm() {
  confirmDialog.value.visible = false
}

async function handleConfirm() {
  if (confirmDialog.value.onConfirm) {
    await confirmDialog.value.onConfirm()
  }
  closeConfirm()
}

function handleRedeem(voucher) {
  showConfirm({
    title: '确认核销',
    message: `确定要核销「${voucher.title}」吗？核销后将不可恢复使用。`,
    confirmText: '确认核销',
    cancelText: '取消',
    onConfirm: async () => {
      await redeemVoucher({ voucher_id: voucher.id })
    }
  })
}

function handleRevert(voucher) {
  showConfirm({
    title: '确认撤销',
    message: `确定要撤销「${voucher.title}」的核销吗？撤销后礼券将恢复为未使用状态。`,
    confirmText: '确认撤销',
    cancelText: '取消',
    onConfirm: async () => {
      await revertVoucher({ voucher_id: voucher.id })
    }
  })
}

function getStatusInfo(status) {
  const map = {
    unused: { label: '未使用', class: 'success' },
    used: { label: '已核销', class: 'neutral' },
    expired: { label: '已过期', class: 'danger' }
  }
  return map[status] || { label: status, class: 'neutral' }
}

function getActionButton(voucher) {
  if (voucher.status === 'unused') {
    return { type: 'redeem', label: '核销', class: '' }
  } else if (voucher.status === 'used') {
    return { type: 'revert', label: '撤销', class: 'secondary' }
  }
  return null
}
</script>

<template>
  <section class="view-stack">
    <div class="section-header">
      <div>
        <p class="eyebrow">Birthday</p>
        <h2>生日礼券发放</h2>
      </div>
      <StatusBanner :error="state.error" :notice="state.notice" :loading="state.loading" />
    </div>

    <div class="toolbar-panel">
      <button class="primary-button" type="button" @click="submitIssue">发放今日生日礼券</button>
      <span v-if="issuedCount !== null">本次发放 {{ issuedCount }} 张</span>
    </div>

    <section class="panel">
      <h3>礼券记录</h3>
      <div class="data-table">
        <div class="table-head voucher-cols">
          <span>会员</span>
          <span>礼券</span>
          <span>内容</span>
          <span>有效期</span>
          <span>状态</span>
          <span>操作</span>
        </div>
        <div v-for="voucher in state.vouchers" :key="voucher.id" class="table-row voucher-cols">
          <span>{{ voucher.member_name }}</span>
          <span>{{ voucher.title }}</span>
          <span>{{ voucher.value }}</span>
          <span>{{ voucher.expires_at }}</span>
          <span>
            <span :class="['status', getStatusInfo(voucher.status).class]">
              {{ getStatusInfo(voucher.status).label }}
            </span>
          </span>
          <span>
            <button
              v-if="getActionButton(voucher)"
              :class="['action-btn', getActionButton(voucher).class]"
              type="button"
              @click="getActionButton(voucher).type === 'redeem' ? handleRedeem(voucher) : handleRevert(voucher)"
            >
              {{ getActionButton(voucher).label }}
            </button>
            <span v-else style="color: #74695f; font-size: 13px;">—</span>
          </span>
        </div>
      </div>
    </section>

    <div v-if="confirmDialog.visible" class="confirm-overlay" @click.self="closeConfirm">
      <div class="confirm-dialog">
        <h4>{{ confirmDialog.title }}</h4>
        <p>{{ confirmDialog.message }}</p>
        <div class="confirm-actions">
          <button class="secondary-btn" type="button" @click="closeConfirm">
            {{ confirmDialog.cancelText }}
          </button>
          <button class="primary-button" type="button" @click="handleConfirm">
            {{ confirmDialog.confirmText }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.action-btn {
  min-height: 32px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 700;
  border-radius: 6px;
  border: 0;
  cursor: pointer;
  background: #c45f35;
  color: #fff;
}

.action-btn:hover {
  background: #a94f2c;
}

.action-btn.secondary {
  background: #6c6258;
}

.action-btn.secondary:hover {
  background: #5a5149;
}

.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(25, 49, 45, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-dialog {
  background: #fffdf8;
  border-radius: 10px;
  padding: 28px;
  max-width: 420px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(54, 45, 34, 0.3);
}

.confirm-dialog h4 {
  margin: 0 0 12px;
  font-size: 18px;
  color: #19312d;
}

.confirm-dialog p {
  margin: 0 0 24px;
  color: #4d463f;
  line-height: 1.6;
}

.confirm-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.secondary-btn {
  min-height: 40px;
  padding: 9px 16px;
  font-size: 14px;
  font-weight: 700;
  border-radius: 8px;
  border: 1px solid #d9cbbb;
  background: #fff;
  color: #4d463f;
  cursor: pointer;
}

.secondary-btn:hover {
  background: #fbf6ee;
}
</style>
