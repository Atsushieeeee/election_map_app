<template>
  <v-card class="mx-4 my-3">
    <div class="card-header" @click="toggleChart">
      <v-card-title class="text-h6">得票数</v-card-title>
      <v-card-subtitle class="subtitle">{{ "得票総数：" + formattedTotalVotes + "票" }}</v-card-subtitle>
    </div>
    <v-expand-transition>
      <div v-show="chartVisible">
        <canvas ref="votesChart"></canvas>
      </div>
    </v-expand-transition>
  </v-card>
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
    },
    totalVotes: {
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
    formattedTotalVotes() {
      return new Intl.NumberFormat('ja-JP').format(this.totalVotes);
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
              backgroundColor: 'rgba(82, 104, 204, 1)',
              borderColor: 'rgba(82, 104, 204, 1)',
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
