import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Axios from "axios";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;

Vue.prototype.$http = Axios;
const token = localStorage.getItem("token");
if (token) {
    Vue.prototype.$http.defaults.headers.common["Authorization"] = token;
}

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