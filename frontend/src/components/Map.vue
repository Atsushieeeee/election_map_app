<template>
  <div>
    <div id="map" class="map-container"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import axios from 'axios';
import { defineEmits } from 'vue';

export default defineComponent({
  name: 'Map',
  setup(_, { emit }) {
    const votesData = ref<any[]>([]);
    const totalVotes = ref<number | null>(null);
    const ageGroupData = ref<any[]>([]);
    const totalPopulation = ref<number | null>(null);
    const totalMen = ref<number | null>(null);
    const totalWomen = ref<number | null>(null);
    const fertilityRateData = ref<any[]>([]);
    const incomeDistributionData = ref<any[]>([]);

    const fetchData = async (cityName: string) => {
      try {
        const votesResponse = await axios.get('http://127.0.0.1:8000/api/votes/', {
          params: {
            city: cityName,
            election_date: '2024-07-07',
            region: '東京都'
          }
        });
        const sortedVotes = votesResponse.data.sort((a: any, b: any) => b.votes - a.votes).slice(0, 10);
        votesData.value = sortedVotes;
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

        // データ更新イベントを発火
        emit('data-updated', {
          votesData: votesData.value,
          totalVotes: totalVotes.value,
          ageGroupData: ageGroupData.value,
          totalPopulation: totalPopulation.value,
          totalMen: totalMen.value,
          totalWomen: totalWomen.value,
          fertilityRateData: fertilityRateData.value,
          incomeDistributionData: incomeDistributionData.value,
        });
      } catch (error) {
        console.error('データの読み込みに失敗しました', error);
      }
    };

    onMounted(async () => {
      const mapOptions: google.maps.MapOptions = {
        center: { lat: 35.682839, lng: 139.759455 },
        zoom: 10,
      };

      const map = new google.maps.Map(document.getElementById('map') as HTMLElement, mapOptions);

      try {
        const response = await axios.get('/tokyo.geojson');
        const geoJsonData = response.data;

        map.data.addGeoJson(geoJsonData);

        // デフォルトスタイルを設定
        const defaultStyle = {
          fillColor: '#D3D3D3',
          fillOpacity: 0.5,
          strokeColor: '#4052a2',
          strokeOpacity: 0.8,
          strokeWeight: 2,
        };

        const selectedStyle = {
          fillColor: '#4052a2',
          fillOpacity: 0.7,
          strokeColor: '#4052a2',
          strokeOpacity: 1.0,
          strokeWeight: 2,
        };

        map.data.setStyle(() => defaultStyle);

        // クリックされたポリゴンのスタイルを変更
        let selectedFeature: google.maps.Data.Feature | null = null;

        map.data.addListener('click', async (event: google.maps.Data.MouseEvent) => {
          if (selectedFeature) {
            // 前回選択されたポリゴンのスタイルをデフォルトに戻す
            map.data.overrideStyle(selectedFeature, defaultStyle);
          }

          selectedFeature = event.feature;
          map.data.overrideStyle(selectedFeature, selectedStyle);

          const name = selectedFeature.getProperty('N03_004') as string;
          await fetchData(name);
        });
      } catch (error) {
        console.error('ポリゴンデータの読み込みに失敗しました', error);
      }
    });

    return {};
  },
});
</script>

<style scoped>
#map {
  width: 100%;
  height: 100%;
}
</style>
