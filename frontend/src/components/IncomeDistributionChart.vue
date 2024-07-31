<template>
  <v-card class="mx-4 my-3">
    <div class="card-header" @click="toggleChart">
      <v-card-title class="text-h6">1世帯あたり年収高</v-card-title>
    </div>
    <v-expand-transition>
      <div v-show="chartVisible">
        <canvas ref="incomeDistributionChart"></canvas>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { Chart } from 'chart.js';
import 'chart.js/auto';

interface IncomeDistribution {
  income_class: string;
  household_count: number;
}

export default defineComponent({
  name: 'IncomeDistributionChart',
  props: {
    data: {
      type: Array as () => IncomeDistribution[],
      required: true
    }
  },
  data() {
    return {
      chartVisible: true
    };
  },
  setup(props) {
    const incomeDistributionChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    const createChart = () => {
      const incomeDistributionChartCanvas = incomeDistributionChart.value?.getContext('2d');
      if (incomeDistributionChartCanvas) {
        if (chartInstance) {
          chartInstance.destroy();
        }
        chartInstance = new Chart(incomeDistributionChartCanvas, {
          type: 'bar',
          data: {
            labels: props.data.map(item => item.income_class),
            datasets: [{
              label: '世帯数',
              data: props.data.map(item => item.household_count),
              backgroundColor: 'rgba(54, 162, 235, 1)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    };

    watch(() => props.data, createChart, { immediate: true });

    return { incomeDistributionChart };
  },
  methods: {
    toggleChart() {
      this.chartVisible = !this.chartVisible;
    }
  }
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
</style>
