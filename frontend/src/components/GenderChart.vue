<template>
  <div class="chart-container">
    <div>{{ "男性総数:" + totalMen }}</div>
    <div>{{ "女性総数:" + totalWomen }}</div>
    <canvas ref="genderChart"></canvas>
  </div>
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
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }, {
              label: '女性人口',
              data: props.data
                .filter(group => group.age_group !== '総数')
                .map(group => group.total_women),
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
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
                    const value = tooltipItem.raw;
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
  }
});
</script>

<style scoped>
.chart-container {
  padding: 16px;
}
</style>
