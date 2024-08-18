<template>
  <v-card class="mx-4 my-3">
    <div class="card-header" @click="toggleChart">
      <v-card-title class="text-h6">人口年齢分布</v-card-title>
      <v-card-subtitle class="subtitle">{{ "人口総数：" + formattedPopulation + "人" }}</v-card-subtitle>
    </div>
    <v-expand-transition>
      <div v-show="chartVisible">
        <canvas ref="populationChart"></canvas>
      </div>
    </v-expand-transition>
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
  data() {
    return {
      chartVisible: true
    };
  },
  computed: {
    formattedPopulation() {
      return new Intl.NumberFormat('ja-JP').format(this.totalPopulation);
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
              backgroundColor: 'rgba(92, 202, 208, 1)',
              borderColor: 'rgba(92, 202, 208, 1)',
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

.subtitle {
  margin-left: auto;
}
</style>
