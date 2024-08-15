<template>
  <v-app>
    <div id="app">
      <div class="container">
        <Sidebar v-if="!isDashboardView" class="sidebar" />
        <button class="dashboard-toggle" @click="toggleDashboard">ダッシュボード変更</button>
        <div>
          <div v-if="!isDashboardView">
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
          <div v-else class="dashboard-view">
            <div class="row">
              <Map class="tile map-tile" @data-updated="updateData" />
              <VotesChart class="tile" :data="votesData" :totalVotes="totalVotes || 0" />
            </div>
            <div class="row">
              <PopulationChart class="tile" :data="ageGroupData" :totalPopulation="totalPopulation || 0" />
              <GenderChart class="tile" :data="ageGroupData" :totalMen="totalMen || 0" :totalWomen="totalWomen || 0" />
            </div>
            <div class="row">
              <FertilityRateChart class="tile" :data="fertilityRateData" />
              <IncomeDistributionChart class="tile" :data="incomeDistributionData" />
            </div>
            <!-- <div class="row">
            </div> -->
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
    const isDashboardView = ref(false);
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

    const toggleDashboard = () => {
      isDashboardView.value = !isDashboardView.value;
    };

    return {
      isDashboardView,
      votesData,
      totalVotes,
      ageGroupData,
      totalPopulation,
      totalMen,
      totalWomen,
      fertilityRateData,
      incomeDistributionData,
      updateData,
      toggleDashboard,
    };
  },
};
</script>

<style>
.container {
  display: flex;
  height: 100vh;
  background: #f5f5f5;
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
  position: relative;
}

.dashboard-toggle {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

.map {
  flex: 1;
  position: relative;
  width: 100%;
  height: calc(100% - 300px);
  padding: 16px 16px 0 16px;
}

.chart-container {
  height: 300px;
  background-color: #f5f5f5;
  overflow-x: auto;
  white-space: nowrap;
  display: flex;
}

.charts-wrapper {
  display: flex;
  height: 100%;
}

.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px;
  height: calc(100vh - 32px);
  width: 100vw;
}

.row {
  display: flex;
  gap: 16px;
  flex: 1;
}

.tile {
  background: white;
  padding: 16px;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  flex: 1;
}

.map-tile {
  flex: 1;
}
</style>
