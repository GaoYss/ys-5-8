<script setup>
import { onMounted, ref } from 'vue'
import StatusBanner from '../components/StatusBanner.vue'
import { useLoyaltyData } from '../stores/useLoyaltyData'

const { state, refreshAll, issueBirthdayVouchers, redeemVoucher, expireVouchers } = useLoyaltyData()
const issuedCount = ref(null)
const expiredCount = ref(null)

onMounted(refreshAll)

async function submitIssue() {
  const vouchers = await issueBirthdayVouchers()
  issuedCount.value = vouchers.length
}

async function submitExpire() {
  const result = await expireVouchers()
  expiredCount.value = result.expired_count
}

async function submitRedeem(voucherId) {
  await redeemVoucher({ voucher_id: voucherId })
}

function getStatusInfo(status) {
  const map = {
    unused: { label: '未使用', class: 'success' },
    used: { label: '已核销', class: 'neutral' },
    expired: { label: '已过期', class: 'danger' }
  }
  return map[status] || { label: status, class: 'neutral' }
}

function isRedeemable(voucher) {
  return voucher.status === 'unused'
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
      <button class="primary-button" type="button" @click="submitExpire" style="background: #6c6258;">标记过期礼券</button>
      <span v-if="issuedCount !== null">本次发放 {{ issuedCount }} 张</span>
      <span v-if="expiredCount !== null">本次标记 {{ expiredCount }} 张过期</span>
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
              v-if="isRedeemable(voucher)"
              class="primary-button"
              type="button"
              style="min-height: 32px; padding: 6px 12px; font-size: 13px;"
              @click="submitRedeem(voucher.id)"
            >
              核销
            </button>
            <span v-else style="color: #74695f; font-size: 13px;">—</span>
          </span>
        </div>
      </div>
    </section>
  </section>
</template>
