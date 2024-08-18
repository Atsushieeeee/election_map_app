<template>
  <div class="container">
    <div :class="['leftsidebar', { 'leftsidebar-closed': !isOpen }]">
      <div class="leftsidebar-wrap">
        <!-- <div class="leftsidebar-title">
          <span class="mdi mdi-chart-line-variant"></span>
          <div class="text-subtitle-1">選挙得票数可視化サイト</div>
        </div> -->

        <v-expansion-panels v-model="panel" multiple accordion>
          <v-expansion-panel>
            <v-expansion-panel-title>
              <span class="mdi mdi-vote"></span>
              <label class="text-subtitle-2" for="">選挙選択</label>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-select
                hide-details
                density="compact"
                label="選挙"
                :items="['東京都知事選']"
                variant="outlined"
              ></v-select>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-title>
              <span class="mdi mdi-map-marker-outline"></span>
              <label class="text-subtitle-2" for="">エリアを選択</label>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-select
                hide-details
                density="compact"
                label="市区町村"
                :items="['千代田区', '港区']"
                variant="outlined"
              ></v-select>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <v-expansion-panel>
            <v-expansion-panel-title>
              <span class="mdi mdi-map-legend"></span>
              <label class="text-subtitle-2" for="">ヒートマップ</label>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-radio-group>
                <v-radio label="得票数" value="one" color="primary"></v-radio>
                <v-radio label="人口" value="two" color="primary"></v-radio>
                <v-radio label="収入" value="three" color="primary"></v-radio>
              </v-radio-group>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </div>

    <v-btn class="toggle-button" @click="toggleSidebar">
      <span class="mdi" :class="isOpen ? 'mdi-chevron-left' : 'mdi-chevron-right'"></span>
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'LeftSidebar',
  data() {
    return {
      panel: [0, 1, 2],
      isOpen: true,
    };
  },
  methods: {
    toggleSidebar() {
      this.isOpen = !this.isOpen;
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  position: relative;
  height: 100%;
}

.leftsidebar {
  /* padding: 16px 0 16px 16px; */
  transition: transform 0.3s ease-in-out;
  transform: translateX(0);
  /* background: #fff; */
  /* border-radius: 4px; */
  overflow: hidden;
  width: 300px;
}

.leftsidebar-closed {
  transform: translateX(-100%);
}

.leftsidebar-wrap {
  height: 100%;
  width: 100%;
}

.leftsidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
}

.text-subtitle-1 {
  padding: 16px 0;
}

.v-expansion-panel {
  border-radius: 0;
  margin: 0;
  border-bottom: 1px solid #ddd;
}

.v-expansion-panel__shadow {
  box-shadow: none !important;
}

.v-expansion-panel-title span {
  font-size: 24px;
  margin-right: 16px;
}

.v-expansion-panel--active:not(:first-child), .v-expansion-panel--active + .v-expansion-panel {
  margin-top: 0 !important;
}


.toggle-button {
  font-size: 20px;
  position: absolute;
  left: 300px;
  background-color: #fff;
  box-shadow: none !important;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); */
  z-index: 100;
  padding: 8px;
  width: 32px;
  height: 80px !important;
  min-width: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 0 2px 0 !important;
}

.leftsidebar-closed + .toggle-button {
  left: 0;
}
</style>
