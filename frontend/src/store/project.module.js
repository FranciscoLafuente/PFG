import { ProjectService } from "../common/api.service";
import {
    ADD_PROJECT,
    DEL_PROJECT,
    FETCH_START,
    FETCH_END
} from "./mutations.type";
import { FETCH_PROJECTS, PROJECT_CREATE, PROJECT_DELETE } from "./actions.type";

const state = {
    project: {
        id: "",
        name: "",
        type: Boolean
    },
    listProjects: [],
    isLoading: true
};

const actions = {
    async [FETCH_PROJECTS]({ commit }) {
        commit(FETCH_START);
        return ProjectService.get()
            .then(r => {
                commit(FETCH_END, r.data);
            })
            .catch(error => {
                throw new Error(error);
            });
    },
    async [PROJECT_CREATE]({ commit }, params) {
        return ProjectService.create(params)
            .then(r => {
                commit(ADD_PROJECT, r.data);
            })
            .catch(error => {
                if (error.request.status === 400) {
                    throw new Error(error.response.data.msg);
                }
            });
    },
    async [PROJECT_DELETE]({ commit }, params) {
        return ProjectService.remove(params.id).then(() => {
            commit(DEL_PROJECT, params.index);
        });
    }
};

const mutations = {
    [FETCH_START](state) {
        state.isLoading = true;
    },
    [FETCH_END](state, data) {
        state.listProjects = data;
        state.isLoading = false;
    },
    [ADD_PROJECT](state, project) {
        state.listProjects = state.listProjects.concat([project]);
    },
    [DEL_PROJECT](state, index) {
        state.listProjects.splice(index, 1);
    }
};

const getters = {
    projects(state) {
        return state.listProjects;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
};