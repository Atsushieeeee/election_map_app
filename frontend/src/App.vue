<template>
  <v-app>
    <div id="app">
      <div class="container">
        <Sidebar class="sidebar" />
        <div class="main-content">
          <Map class="map" @data-updated="updateData" />
          <div class="chart-container">
            <div class="charts-wrapper">
              <VotesChart :data="votesData" :totalVotes="totalVotes || 0" />
              <PopulationChart :data="ageGroupData" :totalPopulation="totalPopulation || 0" />
              <GenderChart :data="ageGroupData" :totalMen="totalMen || 0" :totalWomen="totalWomen || 0" />
              <FertilityRateChart :data="fertilityRateData" />
              <IncomeDistributionChart :data="incomeDistributionData" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </v-app>
</template>

<script>
import { ref } from 'vue';
import Sidebar from './components/Sidebar.vue';
import Map from './components/Map.vue';
import VotesChart from './components/VotesChart.vue';
import PopulationChart from './components/PopulationChart.vue';
import GenderChart from './components/GenderChart.vue';
import FertilityRateChart from './components/FertilityRateChart.vue';
import IncomeDistributionChart from './components/IncomeDistributionChart.vue';

export default {
  name: 'App',
  components: {
    Sidebar,
    Map,
    VotesChart,
    PopulationChart,
    GenderChart,
    FertilityRateChart,
    IncomeDistributionChart,
  },
  setup() {
    const votesData = ref([]);
    const totalVotes = ref(null);
    const ageGroupData = ref([]);
    const totalPopulation = ref(null);
    const totalMen = ref(null);
    const totalWomen = ref(null);
    const fertilityRateData = ref([]);
    const incomeDistributionData = ref([]);

    const updateData = (data) => {
      votesData.value = data.votesData || [];
      totalVotes.value = data.totalVotes || null;
      ageGroupData.value = data.ageGroupData || [];
      totalPopulation.value = data.totalPopulation || null;
      totalMen.value = data.totalMen || null;
      totalWomen.value = data.totalWomen || null;
      fertilityRateData.value = data.fertilityRateData || [];
      incomeDistributionData.value = data.incomeDistributionData || [];
    };

    return {
      votesData,
      totalVotes,
      ageGroupData,
      totalPopulation,
      totalMen,
      totalWomen,
      fertilityRateData,
      incomeDistributionData,
      updateData,
    };
  },
};
</script>

<style>
.container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 240px;
  height: 100%;
  position: fixed;
}

.main-content {
  margin-left: 240px;
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: calc(100vw - 240px);
}

.map {
  flex: 1;
  position: relative;
  width: 100%;
  height: calc(100% - 300px);
}

.chart-container {
  height: 300px;
  background-color: #fff;
  overflow-x: auto;
  white-space: nowrap;
  display: flex;
}

.charts-wrapper {
  display: flex;
  gap: 16px;
  height: 100%;
}
</style>