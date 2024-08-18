<template>
  <v-app>
    <v-app-bar app color="primary" :elevation="0">
      <v-app-bar-title>
        <span class="mdi mdi-chart-line-variant"></span>選挙得票数可視化アプリ
      </v-app-bar-title>
    </v-app-bar>
    <v-main>
      <v-container fluid class="fill-height pa-0">
        <Map />
      </v-container>
    </v-main>
    <v-footer app color="primary" class="white--text d-flex align-center justify-center">
      <div class="copylight">Copyright©ATSUSHI. All Rights Reserved.
      </div>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Map from './components/Map.vue';

export default defineComponent({
  name: 'App',
  components: {
    Map,
  },
});
</script>

<style scoped>
.fill-height {
  height: 100%;
}
.copylight {
  font-size: 10px;
  text-align: center;
}
</style>
