import { ScanService } from "../common/api.service";
import {
    ADD_SCAN,
    DEL_SCAN,
    FETCH_START,
    FETCH_END,
    FETCH_END_GEO,
    FETCH_END_INFO,
    ONE_SCAN
} from "./mutations.type";
import {
    FETCH_SCANS,
    FETCH_INFO,
    SCAN_CREATE,
    SCAN_RELUNCH,
    SCAN_DELETE,
    INFO_SAVE,
    ONE_SCAN_INFO
} from "./actions.type";

const state = {
    scan: {
        name: "",
        bots: 0,
        executiontime: 0,
        hosts: ""
    },
    listScans: [],
    geoInfo: [],
    allInfo: [],
    oneScan: [],
    isLoading: true
};

const actions = {
    async [FETCH_SCANS]({ commit }, id) {
        commit(FETCH_START);
        return ScanService.get(id)
            .then(r => {
                commit(FETCH_END, r.data);
            })
            .catch(error => {
                throw new Error(error);
            });
    },
    async [FETCH_INFO](context, id) {
        const response = await ScanService.getInfo(id);
        context.dispatch(INFO_SAVE, response.data);
    },
    async [SCAN_CREATE]({ commit }, params) {
        return ScanService.create(params.id, params.scan)
            .then(r => {
                commit(ADD_SCAN, r.data);
            })
            .catch(error => {
                if (error.request.status === 400) {
                    throw new Error(error.response.data.msg);
                }
            });
    },
    async [SCAN_DELETE]({ commit }, params) {
        return ScanService.delete(params.id_project, params.id_scan).then(() => {
            commit(DEL_SCAN, params.index);
        });
    },
    [SCAN_RELUNCH](context, id) {
        return ScanService.update(id);
    },
    [INFO_SAVE](context, data) {
        context.commit(FETCH_START);
        data.forEach(element => {
            context.commit(FETCH_END_INFO, element);
            element.forEach(e => {
                if (e.type === "geo") {
                    context.commit(FETCH_END_GEO, e.data);
                }
            });
        });
    },
    [ONE_SCAN_INFO](context, index) {
        context.commit(ONE_SCAN, index);
    }
};

const mutations = {
    [FETCH_START](state) {
        state.geoInfo = [];
        state.allInfo = [];
        state.isLoading = true;
    },
    [FETCH_END](state, data) {
        state.listScans = data;
        state.isLoading = false;
    },
    [FETCH_END_GEO](state, data) {
        state.geoInfo = state.geoInfo.concat([data]);
        state.isLoading = false;
    },
    [FETCH_END_INFO](state, data) {
        state.allInfo = state.allInfo.concat([data]);
        state.isLoading = false;
    },
    [ADD_SCAN](state, scan) {
        state.listScans = state.listScans.concat([scan]);
    },
    [DEL_SCAN](state, index) {
        state.listScans.splice(index, 1);
    },
    [ONE_SCAN](state, index) {
        state.oneScan = state.allInfo[index];
    }
};

const getters = {
    scans(state) {
        return state.listScans;
    },
    geoInfo(state) {
        return state.geoInfo;
    },
    oneScan(state) {
        return state.oneScan;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};