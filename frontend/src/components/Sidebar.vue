<template>
  <div ref="sidebar" :class="['sidebar', { visible: show, hidden: !show }]">
    <div class="sidebar-header">{{ cityName }}</div>
    <button @click="closeSidebar" class="close-btn">×</button>
    <VotesChart :data="chartData" :totalVotes="totalVotes || 0" />
    <PopulationChart :data="ageGroupData" :totalPopulation="totalPopulation || 0" />
    <GenderChart :data="ageGroupData" :totalMen="totalMen || 0" :totalWomen="totalWomen || 0" />
    <FertilityRateChart :data="fertilityRateData" />
    <IncomeDistributionChart :data="incomeDistributionData" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, nextTick, watch } from 'vue';
import axios from 'axios';
import VotesChart from './VotesChart.vue';
import PopulationChart from './PopulationChart.vue';
import GenderChart from './GenderChart.vue';
import FertilityRateChart from './FertilityRateChart.vue';
import IncomeDistributionChart from './IncomeDistributionChart.vue';

interface Vote {
  candidate_name: string;
  votes: number;
  total_votes: number;
}

interface AgeGroup {
  age_group: string;
  total_population: number;
  total_men: number;
  total_women: number;
}

interface FertilityRate {
  year: string;
  rate: number;
}

interface IncomeDistribution {
  income_class: string;
  household_count: number;
}

export default defineComponent({
  name: 'Sidebar',
  components: { VotesChart, PopulationChart, GenderChart, FertilityRateChart, IncomeDistributionChart },
  props: {
    cityName: {
      type: String,
      required: true,
    },
    show: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    const sidebar = ref<HTMLDivElement | null>(null);
    const chartData = ref<Vote[]>([]);
    const totalVotes = ref<number | null>(null);
    const ageGroupData = ref<AgeGroup[]>([]);
    const totalPopulation = ref<number | null>(null);
    const totalMen = ref<number | null>(null);
    const totalWomen = ref<number | null>(null);
    const fertilityRateData = ref<FertilityRate[]>([]);
    const incomeDistributionData = ref<IncomeDistribution[]>([]);

    const closeSidebar = () => {
      emit('update:show', false);
    };

    const fetchData = async (cityName: string) => {
      try {
        const votesResponse = await axios.get<{ votes: Vote[], total_votes: number }>('http://127.0.0.1:8000/api/votes/', {
          params: {
            city: cityName,
            election_date: '2024-07-07',
            region: '東京都'
          }
        });
        chartData.value = votesResponse.data.sort((a, b) => b.votes - a.votes).slice(0, 10);
        totalVotes.value = votesResponse.data[0].total_votes;

        const populationResponse = await axios.get('http://127.0.0.1:8000/api/population_distribution/', {
          params: {
            region: cityName
          }
        });

        const populationData = populationResponse.data;
        ageGroupData.value = populationData.age_groups;
        totalPopulation.value = populationData.total_population;

        const genderResponse = await axios.get('http://127.0.0.1:8000/api/population_gender_distribution/', {
          params: {
            region: cityName
          }
        });

        const genderData = genderResponse.data;
        totalMen.value = genderData.total_men;
        totalWomen.value = genderData.total_women;
        ageGroupData.value = genderData.age_groups;

        const fertilityResponse = await axios.get('http://127.0.0.1:8000/api/fertility_rate/', {
          params: {
            region: cityName
          }
        });

        fertilityRateData.value = fertilityResponse.data;

        const incomeDistributionResponse = await axios.get('http://127.0.0.1:8000/api/income_distribution/', {
          params: {
            region: cityName
          }
        });

        incomeDistributionData.value = incomeDistributionResponse.data;
      } catch (error) {
        console.error('データの読み込みに失敗しました', error);
      }
    };

    watch(() => props.show, async (newValue: boolean) => {
      if (newValue) {
        await fetchData(props.cityName);
        nextTick();
      }
    });

    watch(() => props.cityName, async (newValue: string) => {
      if (props.show) {
        await fetchData(newValue);
        nextTick();
      }
    });

    return { sidebar, closeSidebar, chartData, totalVotes, ageGroupData, totalPopulation, totalMen, totalWomen, fertilityRateData, incomeDistributionData };
  }
});
</script>

<style scoped>
.sidebar {
  position: fixed;
  right: 0;
  width: 600px;
  height: calc(100% - 95px);
  background: #fff;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
  overflow-y: auto;
  background: #f5f5f5;
}

.sidebar.visible {
  transform: translateX(0);
}

.sidebar.hidden {
  transform: translateX(100%);
}

.sidebar-header {
  font-size: 24px;
  padding: 16px 16px 0 16px;
  background: #f5f5f5;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.chart-container {
  padding: 16px;
}
</style>
