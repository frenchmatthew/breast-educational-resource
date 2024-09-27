export default (context, inject) => {
  inject("currentRender", () => {
    return context.store.getters.getBaseRender;
  }),
  inject("perviousCamera", () => {
    return context.store.getters.getPreviousCamera;
  });
};
