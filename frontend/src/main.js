import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/";
import vuetify from "./plugins/vuetify";

import { CHECK_AUTH } from "./store/actions.type";
import ApiService from "./common/api.service";

Vue.config.productionTip = false;
ApiService.init();

// Ensure we checked auth before each page load.
router.beforeEach((to, from, next) =>
    Promise.all([store.dispatch(CHECK_AUTH)]).then(next)
);

// eslint-disable-next-line
delete L.Icon.Default.prototype._getIconUrl;
// eslint-disable-next-line
L.Icon.Default.mergeOptions({
    iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
    iconUrl: require("leaflet/dist/images/marker-icon.png"),
    shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

new Vue({
    router,
    vuetify,
    store,
    render: (h) => h(App),
}).$mount("#app");