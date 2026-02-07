<template>

  <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-1 border-bottom">
    <h1 class="h4 d-flex">
      <i class="bi bi-house me-3"></i>
      Dashboard
    </h1>

    <div class="btn-toolbar mb-2 mb-md-0">
      <button class="btn btn-sm btn-outline-secondary">
        <i class="bi bi-calendar"></i>
        This week
      </button>
    </div>
  </div>

  <!-- KPI Cards -->
  <div class="row g-3 mb-4 mt-1">
    <KPICard v-for="(kpi, index) in kpis" :key="index" :label="kpi.label" :value="kpi.value" :icon="kpi.icon"
      :variant="kpi.variant" />
  </div>

  <!-- Recent Requests Table -->
  <div class="card shadow-sm">
    <div class="card-header d-flex align-items-center justify-content-between">
      <span class="fw-semibold">Requests By Area</span>
      <button class="btn btn-sm btn-outline-primary">
        View all
      </button>
    </div>

    <RequestAreaBarChart />
  </div>

</template>

<script>
import KPICard from '@/components/KPICard.vue'
import axios from 'axios'
import { API } from '@/utils/constants'
import RequestAreaBarChart from '@/components/RequestAreaBarChart.vue';

export default {
  name: 'HomeView',
  components: { KPICard, RequestAreaBarChart },

  data() {
    return {
      requestKpiData: null
    }
  },

  computed: {
    kpis() {
      if (!this.requestKpiData) return []

      return [
        {
          label: 'Total Requests',
          value: this.requestKpiData.total_count,
          icon: 'bi bi-hash',
          variant: 'primary'
        },
        {
          label: 'Not Started',
          value: this.requestKpiData.not_started_count,
          icon: 'bi-hourglass',
          variant: 'danger'
        },
        {
          label: 'In Progress',
          value: this.requestKpiData.in_progress_count,
          icon: 'bi-arrow-repeat',
          variant: 'warning'
        },
        {
          label: 'Completed',
          value: this.requestKpiData.completed_count,
          icon: 'bi-check-circle',
          variant: 'success'
        }
      ]
    }
  },

  async mounted() {
    await this.getRequestKpiData()
  },

  methods: {
    async getRequestKpiData() {
      const response = await axios.get(API.DASHBOARD.request_kpi_data)
      this.requestKpiData = response.data
    }
  }
}
</script>


<style scoped>
.home {
  padding-bottom: 2rem;
}
</style>
