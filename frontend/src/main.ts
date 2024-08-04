import { createApp } from 'vue';
import vuetify from './plugins/vuetify'; // Vuetifyの設定ファイル
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue';

createApp(App)
  .use(vuetify)
  .mount('#app');
