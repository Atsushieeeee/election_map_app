<template>
  <div class="main-container">
    <div class="map-container">
      <Map @polygon-click="handlePolygonClick" />
    </div>
    <div class="sidebar-container">
      <Sidebar :cityName="cityName" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import Map from './Map.vue';
import Sidebar from './Sidebar.vue';

export default defineComponent({
  name: 'Main',
  components: {
    Map,
    Sidebar,
  },
  setup() {
    const cityName = ref<string>('');

    const handlePolygonClick = (name: string) => {
      cityName.value = name;
    };

    return { cityName, handlePolygonClick };
  },
});
</script>

<style scoped>
.main-container {
  display: flex;
  height: 100%;
  width: 100%;
  background-color: #f5f5f5;
}

.map-container {
  flex: 1;
}

.sidebar-container {
  flex: 1;
  max-width: 400px;
}
</style>
