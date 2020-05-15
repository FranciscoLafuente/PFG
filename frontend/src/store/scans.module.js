import { ScanService } from "../common/api.service";
import {
    ADD_SCAN,
    DEL_SCAN,
    FETCH_START,
    FETCH_END,
    FETCH_END_GEO,
    SAVE_TIMELINE,
    FULL_SCAN,
    ONE_SCAN,
    SEARCH_SAVE,
} from "./mutations.type";
import {
    FETCH_SCANS,
    FETCH_INFO,
    FETCH_ONE_INFO,
    SCAN_CREATE,
    SCAN_RELUNCH,
    SCAN_DELETE,
    SCAN_EDIT,
    FETCH_TIMELINE,
    SAVE_FULL_SCAN,
    SEARCH_SCAN,
} from "./actions.type";

const state = {
    listScans: [],
    geoInfo: [],
    scansTLine: [],
    fullScan: {},
    oneScan: [],
    search: [],
    isLoading: true,
};

const actions = {
    async [FETCH_SCANS]({ commit }, id) {
        commit(FETCH_START);
        return ScanService.get(id)
            .then((r) => {
                commit(FETCH_END, r.data);
            })
            .catch((error) => {
                throw new Error(error);
            });
    },
    async [FETCH_INFO](context, id) {
        const response = await ScanService.getInfo(id);
        context.commit(FULL_SCAN, response.data);
    },
    async [FETCH_ONE_INFO](context, params) {
        const response = await ScanService.getOneInfo(params.id_scan, params.domain, params.num);
        context.commit(ONE_SCAN, response.data);
    },
    async [FETCH_TIMELINE]({ commit }, params) {
        commit(FETCH_START);
        return ScanService.getTimeLine(params.id_scan, params.domain)
            .then((r) => {
                commit(SAVE_TIMELINE, r.data);
            })
            .catch((error) => {
                throw new Error(error);
            });
    },
    async [SCAN_CREATE]({ commit }, params) {
        return ScanService.create(params.id, params.scan)
            .then((r) => {
                commit(ADD_SCAN, r.data);
            })
            .catch((error) => {
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
    async [SEARCH_SCAN]({ commit }, params) {
        console.log("PARAMS MODULE", params);

        return ScanService.search(params).then((r) => {
            commit(SEARCH_SAVE, r.data);
        });
    },
    [SCAN_EDIT](context, params) {
        return ScanService.renameBot(params.id, params.name);
    },
    [SCAN_RELUNCH](context, id) {
        return ScanService.update(id);
    },
    [SAVE_FULL_SCAN](context, scan) {
        context.commit(FULL_SCAN, scan);
    },
};

const mutations = {
    [FETCH_START](state) {
        state.geoInfo = [];
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
    [ADD_SCAN](state, scan) {
        state.listScans = state.listScans.concat([scan]);
    },
    [DEL_SCAN](state, index) {
        state.listScans.splice(index, 1);
    },
    [SAVE_TIMELINE](state, data) {
        state.scansTLine = data;
        state.isLoading = false;
    },
    [FULL_SCAN](state, scan) {
        state.fullScan = scan;
    },
    [ONE_SCAN](state, scan) {
        state.oneScan = scan;
    },
    [SEARCH_SAVE](scate, scan) {
        state.search = scan;
    },
};

const getters = {
    scans(state) {
        return state.listScans;
    },
    geoInfo(state) {
        return state.geoInfo;
    },
    timeline(state) {
        return state.scansTLine;
    },
    fullScan(state) {
        return state.fullScan;
    },
    oneScan(state) {
        return state.oneScan;
    },
    getSearch(state) {
        return state.search;
    },
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters,
};