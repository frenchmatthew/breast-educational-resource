<template>
  <div :class="model_panel" ref="leftContainer" :style="panelStyle">
    <div :class="model_title">
      <lazy-panel />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      Copper: null,
      THREE: null,
      baseRenderer: null,
      panelStyle: null,
      model_panel: null,
      model_title: null,
    };
  },

  created: async function () {},

  computed: {
    mdAndUp() {
      return this.$vuetify.breakpoint.mdAndUp;
    },
  },

  mounted() {
    this.Copper = this.$Copper();
    this.THREE = this.$three();
    this.$nuxt.$on("panel-height", this.setupPanelHeight);

    window.addEventListener("resize", () => {
      setTimeout(() => {
        if(!!this.scene) this.scene.onWindowResize();
      }, 500);
    });
  },

  methods: {
    setupPanelHeight(h) {
      // set up container height
      this.panelStyle = {
        height: h - 2 + "px",
      };
      this.model_panel = "model_name";
      this.model_title = "model_title";
      if (h > 0) {
        setTimeout(() => {
          this.baseRenderer = new this.Copper.copperRenderer(
            this.$refs.leftContainer,
            {
              guiOpen: false,
              alpha: false,
              cameraGui: true,
              performance: true,
              logarithmicDepthBuffer: true,
              light: false,
              controls: "copper3d",
            }
          );
          this.baseRenderer.animate();
          this.start();
        }, 500);
      }
    },
    start() {
      // console.log(this.baseRenderer);
      this.loadModel("modelView/breast-l.glb", "breastmodel");
      // this.loadModel("modelView/prone_surface.obj", "breastmodel");
    },

    loadModel(model_url, model_name) {
      const viewURL = "modelView/left_breast_view.json";
      this.scene = this.baseRenderer.getSceneByName(model_name);

      if (this.scene === undefined) {
        this.scene = this.baseRenderer.createScene(model_name);
        this.scene.addLights();
        // this.scene.controls.staticMoving = true;
        // this.scene.controls.rotateSpeed = 3.0;
        // this.scene.controls.panSpeed = 3.0;
        this.scene.controls.panSpeed = 0.2;
        this.baseRenderer.setCurrentScene(this.scene);

        this.scene.loadGltf(model_url, (content) => {
          content.traverse((child) => {
            if (child.isMesh && child.name == "VH_F_fat_L") {
              child.material = new this.THREE.MeshPhysicalMaterial({
                // side: this.THREE.DoubleSide,
                transparent: true,
                opacity: 0.4,
                color: "#a3932a",
                // wireframe: true,
              });
            }
          });
        });
        this.scene.loadViewUrl(viewURL);
        this.scene.updateBackground("#fab9c5", "#fab9c5");
        this.Copper.setHDRFilePath("environment/venice_sunset_1k.hdr");
        this.baseRenderer.updateEnvironment();
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
.model_panel {
  position: relative;
}
.model_title {
  position: absolute;
  top: 0;
  left: 0;
}
</style>
