<template>
  <v-card class="mx-4 my-3">
    <div class="card-header" @click="toggleChart">
      <v-card-title class="text-h6">男女比年齢分布</v-card-title>
      <div class="subtitles">
        <v-card-subtitle>{{ "男性総数：" + formattedMen + "人"}}</v-card-subtitle>
        <v-card-subtitle>{{ "女性総数：" + formattedWomen + "人" }}</v-card-subtitle>
      </div>
    </div>
    <v-expand-transition>
      <div v-show="chartVisible">
        <canvas ref="genderChart"></canvas>
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
  total_men: number;
  total_women: number;
}

export default defineComponent({
  name: 'GenderChart',
  props: {
    data: {
      type: Array as () => AgeGroup[],
      required: true
    },
    totalMen: {
      type: Number,
      required: true
    },
    totalWomen: {
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
    formattedMen() {
      return new Intl.NumberFormat('ja-JP').format(this.totalMen);
    },
    formattedWomen() {
      return new Intl.NumberFormat('ja-JP').format(this.totalWomen);
    }
  },
  setup(props) {
    const genderChart = ref<HTMLCanvasElement | null>(null);
    let chartInstance: Chart | null = null;

    const createChart = () => {
      const genderChartCanvas = genderChart.value?.getContext('2d');
      if (genderChartCanvas) {
        if (chartInstance) {
          chartInstance.destroy();
        }
        chartInstance = new Chart(genderChartCanvas, {
          type: 'bar',
          data: {
            labels: props.data
              .filter(group => group.age_group !== '総数')
              .map(group => group.age_group),
            datasets: [{
              label: '男性人口',
              data: props.data
                .filter(group => group.age_group !== '総数')
                .map(group => -group.total_men), // 男性データを負の値にする
              backgroundColor: 'rgba(54, 162, 235, 1)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }, {
              label: '女性人口',
              data: props.data
                .filter(group => group.age_group !== '総数')
                .map(group => group.total_women),
              backgroundColor: 'rgba(255, 99, 132, 1)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            indexAxis: 'y',
            plugins: {
              legend: {
                position: 'top'
              },
              tooltip: {
                callbacks: {
                  title: function(tooltipItems) {
                    return tooltipItems[0].label;
                  },
                  label: function(tooltipItem) {
                    const datasetLabel = tooltipItem.dataset.label || '';
                    const value = tooltipItem.raw as number;
                    return `${datasetLabel}: ${Math.abs(value)}`; // ツールチップでは絶対値を表示
                  }
                }
              }
            },
            scales: {
              x: {
                stacked: true,
                beginAtZero: true,
                ticks: {
                  callback: function(value) {
                    return Math.abs(value as number); // 軸上の値を絶対値にする
                  }
                }
              },
              y: {
                stacked: true,
                beginAtZero: true
              }
            }
          }
        });
      }
    };

    watch(() => props.data, createChart, { immediate: true });

    return { genderChart };
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
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.subtitles {
  display: flex;
  flex-direction: column;
  margin-left: 16px;
}

canvas {
  width: 400px;
}

</style>
