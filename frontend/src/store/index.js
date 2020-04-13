import Vue from "vue";
import Vuex from "vuex";

import project from "./project.module";
import auth from "./auth.module";
import bots from "./bots.module";
import scans from "./scans.module";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        project,
        auth,
        bots,
        scans
    }
});