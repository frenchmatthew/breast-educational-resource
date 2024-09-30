<template>
  <div class="model">
      <v-tabs class="fixed flex justify-center tab-main" @change="tabsOnChange">
        <v-tab class="tab-main">3D Mammogram</v-tab>
        <v-tab class="tab-main">2D Mammogram</v-tab>
      </v-tabs>
    
    <div ref="baseDomObject" :class="mdAndUp ? 'baseDom-md' : 'baseDom-sm'" />
    <div
        ref="threeDControls"
        class="baseModelControl"
        :class="mdAndUp ? 'baseModelControl-md' : 'baseModelControl-sm'"
      >
        <div class="baseModelCB" :class="mdAndUp ? 'baseModelCB-md' : ''">
          <button
            class="absolute top-0 left-0 w-1/4 h-full hover:bg-zinc-700/30 rounded-lg"
            @click="onResetAllModelsView"
          />
          <img
            src="~/assets/images/gestures-icons.png"
            class="h-full w-full md:object-contain"
          />
        </div>
      </div>
  </div>
</template>

<script>
import loadingSvg from "~/assets/images/loading/loading.svg";
export default {
  data() {
    return {
      Copper: null,
      THREE: null,
      baseRenderer: null,
      baseContainer: null,
      container: null,
      modelData: null,
      nrrdMaxIndex:-1,
      nrrdSliceZ:null,
      nrrdMeshes: null,
      loadFirstTime: true,
      currentView: "3D Mammogram",
      mouseActions: null,
      modelToScenes:{},
      modelUrlsArray:{
        normal: [
          "modelView/density-1/middle/m3d.nrrd",
          "modelView/density-1/middle/m_view.json",
          "modelView/density-1/middle/m2d.nrrd"
        ],
        density_2: [
          "modelView/density-2/middle/m3d.nrrd",
          "modelView/density-2/middle/m_view.json",
          "modelView/density-2/middle/m2d.nrrd"
        ],
        density_3: [
          "modelView/density-3/middle/m3d.nrrd",
          "modelView/density-3/middle/m_view.json",
          "modelView/density-3/middle/m2d.nrrd"
        ],
        density_4: [
          "modelView/density-4/middle/m3d.nrrd",
          "modelView/density-4/middle/m_view.json",
          "modelView/density-4/middle/m2d.nrrd"
        ]
      },
    };
  },

  created: async function () {
    // this.$nuxt.$on("send-emitter-data", (data) => {
    //   console.log(data);
    // });
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
    this.raycaster = this.$raycaster();
    this.modelToScenes = this.$modelToScenes();
    this.baseContainer = this.$baseContainer();
    this.modelData = this.$modelData();
    this.container = this.$refs.baseDomObject;
    this.modelName = this.$model().name;

    if(["cyst", "fibroadenoma", "calcifications", "fat_necrosis", "dcis", "lobular", "ductal"].includes(this.modelName)){
      this.modelName = "normal";
    }

    this.$nuxt.$emit("onNavChange", this.modelName);
    this.container.appendChild(this.baseContainer);
    this.start();

    window.addEventListener("resize", () => {
      setTimeout(() => {
        this.mdAndUp
          ? (this.baseContainer.style.height = "100vh")
          : (this.baseContainer.style.height = "100vw");

        this.scene.onWindowResize();
      }, 500);
    });
  },

  methods: {
    async start() {
      this.loadNrrd(this.modelUrlsArray[this.modelName][0], this.modelName+"middle_3d");
    },

    tabsOnChange(a) {
      if (this.loadFirstTime) return;
      const modelUrl = this.modelUrlsArray[this.modelName][0];
      if (a === 0) {
        this.currentView = "3D Mammogram";
        this.loadNrrd(modelUrl, this.modelName+"middle_3d");
      } else {
        this.currentView = "2D Mammogram";
        this.loadNrrd(this.modelUrlsArray[this.modelName][2], this.modelName+"middle_2d");
      }
    },

    loadNrrd(nrrdUrl, modelName) {
      const viewURL = this.modelUrlsArray[this.modelName][1];
      const loadBar1 = this.Copper.loading(loadingSvg);
      const loadBar2 = this.Copper.loading(loadingSvg);
      
      const loadingContainer = loadBar1.loadingContainer;
      loadingContainer.style.position = "fixed";
      loadingContainer.style.top = 0;
      loadingContainer.style.left = 0;
      loadingContainer.style.right = 0;
      loadingContainer.style.bottom = 0;
      loadingContainer.style.display = "flex";
      this.baseContainer.appendChild(loadingContainer);
      loadBar1.progress.innerHTML = "Loading image...";

      this.scene = this.baseRenderer.getSceneByName(modelName);
      if (this.scene === undefined) {
        this.scene = this.baseRenderer.createScene(modelName);
        this.scene.controls.staticMoving = true;
        // this.scene.controls.rotateSpeed = 3.0;
        this.scene.controls.panSpeed = 0.5;
        
        this.baseRenderer.setCurrentScene(this.scene);

        this.scene.loadNrrd(
          nrrdUrl,
          loadBar2,
          true,
          (volume, nrrdMesh, nrrdSlices, gui) => {
            this.nrrdMeshes = nrrdMesh;
            this.nrrdMeshes.x.name = "x";
            this.nrrdMeshes.y.name = "y";
            this.nrrdMeshes.z.name = "z";
            this.scene.addObject(nrrdMesh.z);
            this.nrrdMaxIndex = nrrdSlices.z.MaxIndex;
            this.nrrdSliceZ = nrrdSlices.z;

            if(this.currentView === "2D Mammogram"){
              this.scene.controls.noRotate = true;
              this.scene.controls.noPan = true;
              this.removeContainerListener();
            }else{
              const data = {
                nrrdSliceZ: this.nrrdSliceZ, 
                nrrdMesh: this.nrrdMeshes.z, 
                nrrdMaxIndex: this.nrrdMaxIndex
              };
              if(this.modelData[this.modelName] === undefined){
                this.modelData[this.modelName] = {};
              }
              this.modelData[this.modelName]["middle"] = data;
              this.addContainerListener();
            }
            loadingContainer.style.display = "none";
          },
          { openGui: false }
        );

        this.scene.loadViewUrl(viewURL);
        this.scene.updateBackground("#f8cdd6", "#f8cdd6");
        this.Copper.setHDRFilePath("environment/venice_sunset_1k.hdr");
        this.baseRenderer.updateEnvironment();
        this.modelToScenes[modelName] = this.scene;
      }else{
        loadingContainer.style.display = "none";
        this.baseRenderer.setCurrentScene(this.scene);
        if(this.currentView === "2D Mammogram"){
          this.scene.controls.noRotate = true;
          this.scene.controls.noPan = true;
          this.removeContainerListener();
        }else{
          this.addContainerListener();
        }
      }
      this.loadFirstTime = false;
      this.scene.onWindowResize();
    },
    addContainerListener() {
      const data = this.modelData[this.modelName]["middle"];
      if(this.mouseActions === null){
          this.mouseActions = this.raycaster(this.scene, this.container, data.nrrdSliceZ, data.nrrdMesh, data.nrrdMaxIndex);
        }
      this.container.addEventListener("mousemove", this.mouseActions.mouseMove);
    },
    removeContainerListener() {
      if(this.mouseActions !== null){
        this.container.removeEventListener("mousemove", this.mouseActions.mouseMove);
        this.container.removeEventListener("mousedown", this.mouseActions.mouseDown);
        this.container.removeEventListener("mouseup", this.mouseActions.mouseUp);
      }
    },
    onResetAllModelsView() {

      for (var k in this.modelToScenes) {
        if (this.modelToScenes.hasOwnProperty(k)) {
          this.modelToScenes[k].resetView();
        }
      }
    },
  },

  watch: {},

  beforeDestroy() {
    // Wirte code before destory this component
    this.removeContainerListener();
  },
};
</script>

<style scoped lang="scss">
.baseModelControl {
  width: 100vw;
  height: 120px;
  // background: red;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-content: center;
  .baseModelCB {
    width: 240px;
    height: 70px;
    position: relative;
  }
  .baseModelCB-md {
    width: 280px;
    height: 100px;
  }
}

.baseModelControl-md {
  position: fixed;
  bottom: 10px;
  padding-left: 100px;
}
.baseModelControl-sm {
  order: -1;
  height: 60px;
}
.tab-main{
  background-color: #EF9BAA !important;
  color: #000 !important;
}
</style>
