// src/main.ts
import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; // Vuetify プラグインのインポート
import 'vuetify/styles';

createApp(App).use(vuetify).mount('#app');
