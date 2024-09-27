export const state = () => ({
  currentContent: {},
  previousCamera: {},
});

export const getters = {
  getCurrentContent: (state) => state.currentContent,
  getPreviousCamera: (state) => state.previousCamera,
  getModelData: (state) => state.modelData,
};

export const mutations = {
  setCurrentContent(state, newContent) {
    state.currentContent = newContent;
  },
  setPreviousCamera(state, preCamera) {
    state.previousCamera = preCamera;
  },
};
