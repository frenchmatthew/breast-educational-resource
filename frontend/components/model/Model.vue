<template>
  <div class="model">
    <div ref="baseDomObject" :class="mdAndUp ? 'baseDom-md' : 'baseDom-sm'" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      Copper: null,
      THREE: null,
      baseRenderer: null,
      container: null,
      modelName: "Model load on here!",
      helloworld: "",
      model: null,
    };
  },

  created: async function () {
    this.$nuxt.$on("send-emitter-data", (data) => {
      console.log(data);
    });
  },

  computed: {
    mdAndUp() {
      return this.$vuetify.breakpoint.mdAndUp;
    },
  },

  mounted() {
    this.Copper = this.$Copper();
    this.baseRenderer = this.$baseRenderer();
    this.THREE = this.$three();
    const baseContainer = this.$baseContainer();
    this.container = this.$refs.baseDomObject;
    setTimeout(() => {
      this.mdAndUp
        ? (baseContainer.style.height = "100vh")
        : (baseContainer.style.height = "100vw");
      this.container.appendChild(baseContainer);
      this.start();
    }, 100);

    window.addEventListener("resize", () => {
      setTimeout(() => {
        this.mdAndUp
          ? (baseContainer.style.height = "100vh")
          : (baseContainer.style.height = "100vw");
        this.scene.onWindowResize();
      }, 500);
    });
  },

  methods: {
    async start() {
      this.loadModel("modelView/prone_surface.obj", "breastmodel");
    },

    loadModel(model_url, model_name) {
      const viewURL = "modelView/noInfarct_view.json";

      this.scene = this.baseRenderer.getSceneByName(model_name);
      if (this.scene === undefined) {
        this.scene = this.baseRenderer.createScene(model_name);
        // this.scene.controls.staticMoving = true;
        // this.scene.controls.rotateSpeed = 3.0;
        // this.scene.controls.panSpeed = 3.0;
        this.baseRenderer.setCurrentScene(this.scene);
        this.scene.loadOBJ(model_url, (content) => {
          console.log(content);
          const box = new this.THREE.Box3().setFromObject(content);
          const size = box.getSize(new this.THREE.Vector3()).length();
          const center = box.getCenter(new this.THREE.Vector3());

          content.position.x += content.position.x - center.x;
          content.position.y += content.position.y - center.y;
          content.position.z += content.position.z - center.z;

          content.renderOrder = 3;
          content.traverse((child) => {
            if (child.isMesh) {
              child.material = new this.THREE.MeshBasicMaterial({
                side: this.THREE.DoubleSide,
                transparent: true,
                opacity: 0.4,
                color: "#a3932a",
                wireframe: true,
              });
            }
          });
        });
        this.scene.loadViewUrl(viewURL);
      }
      this.scene.onWindowResize();
    },
  },

  watch: {},

  beforeDestroy() {
    // Wirte code before destory this component
  },
};
</script>

<style scoped lang="scss">
.model {
  background-color: rgb(248 205 214) !important;
}
</style>
