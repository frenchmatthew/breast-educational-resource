<template>
  <div class="w-full h-1/2">
    <span style="color: rgb(244, 55, 149);" class="font-bold">
      {{ modelControl }}
    </span>

    <div ref="rightContainer" class="w-full h-full">
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      modelControl: "MRI",
      Copper: null,
      THREE: null,
      baseRenderer: null,
      baseContainer: null,
      nrrdMaxIndex:-1,
      nrrdSliceZ:null,
      nrrdMeshes: null,
      modelData: null,
      modelName: null,
      mouseActions: null,
      modelUrlsArray:{
        normal: [
          "modelView/density-1/right/mri.nrrd",
          "modelView/density-1/right/mri_view.json",
        ],
        density_2: [
          "modelView/density-2/right/mri.nrrd",
          "modelView/density-2/right/mri_view.json",
        ],
        density_3: [
          "modelView/density-3/right/mri.nrrd",
          "modelView/density-3/right/mri_view.json",
        ],
        density_4: [
          "modelView/density-4/right/mri.nrrd",
          "modelView/density-4/right/mri_view.json",
        ],
      },
    };
  },
  mounted() {
    this.Copper = this.$Copper();
    this.THREE = this.$three();
    this.raycaster = this.$raycaster();
    this.baseRenderer = this.$baseRightRenderer();
    this.baseContainer = this.$baseRightContainer();
    this.modelData = this.$modelData();
    this.container = this.$refs.rightContainer;

    this.container.appendChild(this.baseContainer);
    // Write code after mount this component
    this.modelName = this.$model().name;
    
    this.start();

    window.addEventListener("resize", () => {
      setTimeout(() => {
        if (!!this.scene) this.scene.onWindowResize();
      }, 500);
    });
  },

  methods: {
    async start() {
      this.loadNrrd(this.modelUrlsArray[this.modelName][0], this.modelName+"right_mri");
    },

    loadNrrd(nrrdUrl, modelName) {
      const viewURL = this.modelUrlsArray[this.modelName][1];
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

            this.nrrdMeshes = nrrdMesh;
            this.scene.addObject(nrrdMesh.z);
            console.log(volume.header);
            
            const nrrdOrigin = volume.header.space_origin.map((num) => Number(num));
            const nrrdRas = volume.RASDimensions; 
            

            const x_bias = -(nrrdOrigin[0] * 2 + nrrdRas[0]) / 2;
            const y_bias = -(nrrdOrigin[1] * 2 + nrrdRas[1]) / 2;
            const z_bias = -(nrrdOrigin[2] * 2 + nrrdRas[2]) / 2;

            this.nrrdMaxIndex = nrrdSlices.z.MaxIndex;
            this.nrrdSliceZ = nrrdSlices.z;

            this.nrrdBias = new this.THREE.Vector3(x_bias, y_bias, z_bias);

            if(this.modelUrlsArray[this.modelName].length > 2)
              this.loadModel(this.modelUrlsArray[this.modelName][2]);
            
            const data = {
              nrrdSliceZ: this.nrrdSliceZ, 
              nrrdMesh: this.nrrdMeshes.z, 
              nrrdMaxIndex: this.nrrdMaxIndex
            };
            if(this.modelData[this.modelName] === undefined){
              this.modelData[this.modelName] = {};
            }
            this.modelData[this.modelName]["right"] = data;
            this.addContainerListener();
          },
          { openGui: false }
        );

        this.scene.loadViewUrl(viewURL);
        this.scene.updateBackground("#f8cdd6", "#f8cdd6");
        this.Copper.setHDRFilePath("environment/venice_sunset_1k.hdr");
        this.baseRenderer.updateEnvironment();
      }else{
        this.baseRenderer.setCurrentScene(this.scene);
        this.addContainerListener();
      }
      this.scene.onWindowResize();
    },

    loadModel(model_url) {
      this.scene.loadOBJ(model_url, (content) => {
        const box = new this.THREE.Box3().setFromObject(content);
        const size = box.getSize(new this.THREE.Vector3()).length();
        const center = box.getCenter(new this.THREE.Vector3());

        // content.position.x += content.position.x - center.x;
        // content.position.y += content.position.y - center.y;
        // content.position.z += content.position.z - center.z;
        content.position.set(this.nrrdBias.x, this.nrrdBias.y, this.nrrdBias.z);
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

    addContainerListener() {
      console.log(this.modelData[this.modelName]);
      
      const data = this.modelData[this.modelName]["right"];
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
  },
  beforeDestroy() {
    // Wirte code before destory this component
    this.removeContainerListener();
  },
};
</script>

<style scoped lang="scss">
.model-control {
  padding-top: 80px;
  span {
    font-size: 1rem;
    font-weight: bold;
    color: rgb(244, 55, 149);
  }
  .mri {
    padding: 0;
    width: 500px;
    height: 500px;
  }
}
</style>
