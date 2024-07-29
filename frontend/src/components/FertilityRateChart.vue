<template>
  <v-card class="mx-4 my-3">
    <v-card-title class="text-h6">合計特殊出生率</v-card-title>
    <canvas ref="fertilityRateChart"></canvas>
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
              backgroundColor: 'rgba(255, 87, 51, 1)',
              borderColor: 'rgba(255, 87, 51, 1)',
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
  }
});
</script>

<style scoped>
</style>
