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
      this.loadNrrd("modelView/breast_14.nrrd", "breastnrrd");
      this.loadModel("modelView/prone_surface.obj");
    },

    loadNrrd(nrrdUrl, modelName) {
      const viewURL = "modelView/noInfarct_view.json";
      const loadBar1 = this.Copper.loading("loading/loading.svg");

      this.scene = this.baseRenderer.getSceneByName(modelName);
      if (this.scene === undefined) {
        this.scene = this.baseRenderer.createScene(modelName);
        // this.scene.controls.staticMoving = true;
        // this.scene.controls.rotateSpeed = 3.0;
        this.scene.controls.panSpeed = 0.5;
        this.baseRenderer.setCurrentScene(this.scene);

        this.scene.loadNrrd(
          nrrdUrl,
          loadBar1,
          true,
          (volume, nrrdMesh, nrrdSlices, gui) => {
            this.scene.addObject(nrrdMesh.z);
          },
          { openGui: false }
        );

        this.scene.loadViewUrl(viewURL);
        this.scene.updateBackground("#f8cdd6", "#f8cdd6");
        this.Copper.setHDRFilePath("environment/venice_sunset_1k.hdr");
        this.baseRenderer.updateEnvironment();
      }
      this.scene.onWindowResize();
    },

    loadModel(model_url) {
      this.scene.loadOBJ(model_url, (content) => {
        const box = new this.THREE.Box3().setFromObject(content);
        const size = box.getSize(new this.THREE.Vector3()).length();
        const center = box.getCenter(new this.THREE.Vector3());

        content.position.x += content.position.x - center.x;
        content.position.y += content.position.y - center.y;
        content.position.z += content.position.z - center.z;

        content.renderOrder = 3;
        content.traverse((child) => {
          if (child.isMesh) {
            child.material = new this.THREE.MeshPhysicalMaterial({
              side: this.THREE.DoubleSide,
              transparent: true,
              opacity: 0.4,
              color: "#a3932a",
              wireframe: false,
            });
          }
        });
      });
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
  // background-color: rgb(248 205 214) !important;
}
</style>
