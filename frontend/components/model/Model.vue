<template>
  <div class="model">
    {{ modelName }}
    <div
        ref="baseDomObject"
        :class="mdAndUp ? 'baseDom-md' : 'baseDom-sm'"
      />
  </div>
</template>

<script>
import axios from "axios";

export default {

  data() {
    return {
      Copper: null,
      THREE: null,
      baseRenderer: null,
      container: null,
      modelName: "Model load on here!",
      helloworld:"",
      model:null,
    };
  },

  async fetch() {
     await axios.get('http://127.0.0.1:8000/hello/model').then((res)=>{
      console.log(res.data);
      })
    await axios.get('http://127.0.0.1:8000/api/model',{ responseType: "blob" }).then((res)=>{
      // console.log(res.data);
    })
    // this.helloworld = await fetch(
    //     'http://127.0.0.1:8000/hello/model'
    //   ).then(res => res.json())
    //   console.log(this.helloworld);
      
    //   this.model = await fetch(
    //     'http://127.0.0.1:8000/api/model'
    //   ).then(res => res.blob())

    //   console.log(this.model);
    },

  created: async function (){

    // await axios.get('http://127.0.0.1:8000/hello/model').then((res)=>{
    //   console.log(res);
    // })
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
    async start(){
      console.log("load model functions.");
      // get model from backend
      this.model = await fetch(
        'http://127.0.0.1:8000/api/model'
      ).then(res => res.blob())

      const model_url = URL.createObjectURL(this.model) 

      this.loadModel(model_url,"test");
    },

    loadModel(model_url, model_name) {

      const viewURL = 'modelView/noInfarct_view.json';

      this.scene = this.baseRenderer.getSceneByName(model_name);
      if (this.scene === undefined) {
        this.scene = this.baseRenderer.createScene(model_name);
        // this.scene.controls.staticMoving = true;
        // this.scene.controls.rotateSpeed = 3.0;
        // this.scene.controls.panSpeed = 3.0;
        this.baseRenderer.setCurrentScene(this.scene);
        this.scene.loadOBJ(model_url, (content) => {
          // this.scene.setModelPosition(content, { x: 5, y: 2 });
          console.log(content);
        });
        this.scene.loadViewUrl(viewURL);
      }
      this.scene.onWindowResize();
    },
  },

  watch: {},

  beforeDestroy() {
    // Wirte code before destory this component
  }
};
</script>

<style scoped lang="scss">

</style>
