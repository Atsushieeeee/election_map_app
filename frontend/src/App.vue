<template>
  <v-app>
    <v-app-bar app color="primary">
      <v-toolbar-title>タイトル</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <v-container fluid class="fill-height pa-0">
        <Map />
      </v-container>
    </v-main>
    <v-footer app color="primary" class="white--text d-flex align-center justify-center">
      フッター
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
</style>
