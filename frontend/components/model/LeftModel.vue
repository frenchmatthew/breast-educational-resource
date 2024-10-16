<template>
  
  <div :class="model_panel" ref="leftContainer" :style="panelStyle" class="h-full relative">
    <div class="hidden md:flex absolute w-full top-24 flex justify-center items-center text-gray-950 text-xs">
      <div class="w-4/5 text-left" v-html="leftPanelText[navPanelName]"></div>
    </div>
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
      baseContainer: null,
      panelStyle: null,
      model_panel: null,
      model_title: null,
      modelToScenes: {},
      navPanelName: null,
      leftPanelText: {},
      showText: false,
      leftBreastView: "modelView/left_breast_view.json",
      modelUrlsArray:{
        normal: [
          "modelView/density-1/left/density25.glb",
        ],
        density_1: [
          "modelView/density-1/left/density25.glb",
        ],
        density_2:[
          "modelView/density-2/left/density50.glb",
        ],
        density_3:[
          "modelView/density-3/left/density75.glb",
        ],
        density_4:[
          "modelView/density-4/left/density100.glb",
        ],
        cyst: [
          "modelView/benign-cyst/left/density100.glb",
        ],
        fibroadenoma:[
          "modelView/benign-fib/left/density100.glb",
        ],
        calcifications:[
          "modelView/density-1/left/density100.glb",
        ],
        dcis:[
          "modelView/cancer-dcis/left/density100.glb",
        ],
        lobular:[
          "modelView/cancer-lobular/left/density100.glb",
        ],
        ductal:[
          "modelView/cancer-ductal/left/density100.glb",
        ]
      },
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
    this.baseRenderer = this.$baseLeftRenderer();
    this.baseContainer = this.$baseLeftContainer();
    this.container = this.$refs.leftContainer;
    this.modelToScenes = this.$modelToScenes();
    this.leftPanelText = this.$leftPanelText();

    this.container.appendChild(this.baseContainer);

    this.$nuxt.$on("panel-height", this.setupPanelHeight);
    this.model_panel = "model_name";
    this.model_title = "model_title";
    this.$nuxt.$on("onNavChange", this.onNavChange);
    
    !!this.navPanelName ? this.navPanelName : (this.navPanelName = this.$model().name);

    this.start();

    window.addEventListener("resize", () => {
      setTimeout(() => {
        if (!!this.scene) {
          this.scene.onWindowResize();
        }
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
          this.start();
        }, 500);
      }
    },
    onNavChange(modelName) {
      this.navPanelName = modelName;
      console.log(modelName);
      
      this.loadModel(this.modelUrlsArray[this.navPanelName][0], this.navPanelName+"left");
    },
    start() {

      if (this.navPanelName === null) {
        this.loadModel(this.modelUrlsArray.normal[0], this.navPanelName+"left");
      }else{
        this.loadModel(this.modelUrlsArray[this.navPanelName][0], this.navPanelName+"left");
      }
    },

    loadModel(model_url, model_name) {

      let viewURL = this.leftBreastView;
      this.scene = this.baseRenderer.getSceneByName(model_name);

      if (this.scene === undefined) {
        this.scene = this.baseRenderer.createScene(model_name);
        this.scene.addLights();
        this.scene.controls.rotateSpeed = 3.0;
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

          this.scene.onWindowResize();
        });
        this.scene.loadViewUrl(viewURL);
         
        this.scene.updateBackground("#fda4af", "#fda4af");
        this.Copper.setHDRFilePath("environment/venice_sunset_1k.hdr");
        this.baseRenderer.updateEnvironment();
       
        this.modelToScenes[model_name] = this.scene;
      }else{
        this.baseRenderer.setCurrentScene(this.scene);
      }
      this.scene.onWindowResize();
    },
  },

  watch: {},

  beforeDestroy() {
    // Wirte code before destory this component
    this.container.removeChild(this.baseContainer);
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
