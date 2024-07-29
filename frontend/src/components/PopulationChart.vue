<template>
  <v-card class="mx-4 my-3">
    <v-card-title class="text-h6">人口年齢分布</v-card-title>
    <v-card-subtitle>{{ "人口総数:" + totalPopulation }}</v-card-subtitle>
    <canvas ref="populationChart"></canvas>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
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
              backgroundColor: 'rgba(75, 192, 192, 1)',
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
</style>
