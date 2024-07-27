<template>
  <div class="chart-container">
    <canvas ref="votesChart"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { Chart } from 'chart.js';
import 'chart.js/auto';

interface Vote {
  candidate_name: string;
  votes: number;
}

export default defineComponent({
  name: 'VotesChart',
  props: {
    data: {
      type: Array as () => Vote[],
      required: true
    }
  },
  setup(props) {
    const votesChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    const createChart = () => {
      const votesChartCanvas = votesChart.value?.getContext('2d');
      if (votesChartCanvas) {
        if (chartInstance) {
          chartInstance.destroy();
        }
        chartInstance = new Chart(votesChartCanvas, {
          type: 'bar',
          data: {
            labels: props.data.map(vote => vote.candidate_name),
            datasets: [{
              label: '得票数',
              data: props.data.map(vote => vote.votes),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
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

    return { votesChart };
  }
});
</script>

<style scoped>
.chart-container {
  padding: 16px;
}
</style>
