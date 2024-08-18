<template>
  <v-card class="mx-4 my-3">
    <div class="card-header" @click="toggleChart">
      <v-card-title class="text-h6">合計特殊出生率</v-card-title>
    </div>
    <v-expand-transition>
      <div v-show="chartVisible">
        <canvas ref="fertilityRateChart"></canvas>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { Chart } from 'chart.js';
import 'chart.js/auto';

interface FertilityRate {
  year: string;
  rate: number;
}

export default defineComponent({
  name: 'FertilityRateChart',
  props: {
    data: {
      type: Array as () => FertilityRate[],
      required: true
    }
  },
  data() {
    return {
      chartVisible: true
    };
  },
  setup(props) {
    const fertilityRateChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    const createChart = (data: FertilityRate[]) => {
      const fertilityRateChartCanvas = fertilityRateChart.value?.getContext('2d');
      if (fertilityRateChartCanvas) {
        if (chartInstance) {
          chartInstance.destroy();
        }
        chartInstance = new Chart(fertilityRateChartCanvas, {
          type: 'line',
          data: {
            labels: data.map(rate => rate.year),
            datasets: [{
              label: '合計特殊出生率',
              data: data.map(rate => rate.rate),
              backgroundColor: 'rgba(247, 88, 29, 0.9)',
              borderColor: 'rgba(247, 88, 29, 0.9)',
              borderWidth: 1,
              fill: false
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

    watch(() => props.data, (newData) => {
      if (Array.isArray(newData)) {
        createChart(newData);
      } else {
        console.error('props.data is not an array:', newData);
      }
    }, { immediate: true });

    return { fertilityRateChart };
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
