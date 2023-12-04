import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        videoStream: null,
        user: {
            id: '',
            name: '',
        }
    },
    mutations: {
        start (state, video) {
            state.videoStream = video;
        },
        stop (state) {
            if (state.videoStream) {
                state.videoStream.getTracks().forEach(track => track.stop());
                state.videoStream = null;
            }
        },
        updateUser(state, userData) {
            state.user = userData;
        },
        updateUserId(state, id) {
            state.user.id = id;
        },
        updateUserName(state, name) {
            state.user.name = name;
        },
        saveUser(state) {
            sessionStorage.setItem('user', JSON.stringify(state.user));
        },
        loadUserFast(state){
            const userString = sessionStorage.getItem('user');
            if (userString) {
                const userData = JSON.parse(userString);
                state.user = userData;
            }
        }
    },
    actions: {
        async startCamera({ commit, state }) {
            if (!state.videoStream &&
                navigator &&
                navigator.mediaDevices &&
                navigator.mediaDevices.getUserMedia) {
                const devices = await navigator.mediaDevices.enumerateDevices();
                const videoDevices = devices.filter(device => device.kind === 'videoinput');
                const selectedCameraId = videoDevices[2].deviceId;
                const constraints = {
                    video: {
                        deviceId: selectedCameraId
                    }
                };
                const stream = await navigator.mediaDevices.getUserMedia(constraints)
                    .catch((e) => {
                        console.log(e);
                        throw new Error(e);
                    });
                commit('start', stream);
                return stream;

            } else {
                throw new Error('This browser doesn\'t support WebRTC');
            }
        },
        stopCamera ({ commit }) {
            commit('stop');
        },
        setUser({ commit }, userData) {
            commit('updateUser', userData);
        },
        setUserId({ commit }, id) {
            commit('updateUserId', id);
        },
        setUserName({ commit }, name) {
            commit('updateUserName', name);
        },
        loadUser({ commit }) {
            const userString = sessionStorage.getItem('user');
            if (userString) {
                const userData = JSON.parse(userString);
                commit('setUser', userData);
            }
        }
    },
    getters: {
        isCameraStarted: (state) => {
            return !!state.videoStream;
        },
        getUser: (state) => {
            return state.user;
        }
    }
});