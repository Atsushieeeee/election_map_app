<template>
  <div class="chart-container">
    <div>{{ "人口総数:" + totalPopulation }}</div>
    <canvas ref="populationChart"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import { Chart } from 'chart.js';
import 'chart.js/auto';

interface AgeGroup {
  age_group: string;
  total_population: number;
}

export default defineComponent({
  name: 'PopulationChart',
  props: {
    data: {
      type: Array as () => AgeGroup[],
      required: true
    },
    totalPopulation: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const populationChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    const createChart = () => {
      const populationChartCanvas = populationChart.value?.getContext('2d');
      if (populationChartCanvas) {
        if (chartInstance) {
          chartInstance.destroy();
        }
        chartInstance = new Chart(populationChartCanvas, {
          type: 'bar',
          data: {
            labels: props.data
              .filter(group => group.age_group !== '総数')
              .map(group => group.age_group),
            datasets: [{
              label: '年齢分布',
              data: props.data
                .filter(group => group.age_group !== '総数')
                .map(group => group.total_population),
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
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

    return { populationChart };
  }
});
</script>

<style scoped>
.chart-container {
  padding: 16px;
}
</style>
