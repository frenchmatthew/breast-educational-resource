import * as Copper from "copper3d";
import * as THREE from "three";

const modelData = {};

const container = document.createElement("div");
container.style.width = "100vw";
container.style.height = "100vh";
container.style.margin = 0;
container.style.padding = 0;
const guiOpen = false;
const baseRenderer = new Copper.copperRenderer(container, {
  guiOpen,
  camera: true,
  performance: true,
  alpha: false,
  logarithmicDepthBuffer: true,
  light: false,
  controls: "copper3d",
});
if (guiOpen) baseRenderer.gui.closed = true;
baseRenderer.animate();

const leftContainer = document.createElement("div");
leftContainer.style.width = "100%";
leftContainer.style.height = "100%";


const baseLeftRenderer = new Copper.copperRenderer(leftContainer, {
  guiOpen: false,
  alpha: false,
  cameraGui: true,
  performance: true,
  logarithmicDepthBuffer: true,
  light: false,
  controls: "copper3d",
});
baseLeftRenderer.animate();

const rightContainer = document.createElement("div");
rightContainer.style.width = "100%";
rightContainer.style.height = "100%";

const baseRightRenderer = new Copper.copperRenderer(rightContainer, {
  guiOpen: false,
  alpha: false,
  cameraGui: true,
  performance: true,
  logarithmicDepthBuffer: true,
  light: false,
  controls: "copper3d",
});
baseRightRenderer.animate();

const raycaster = (scene, container, nrrdSliceZ, nrrdMesh, nrrdMaxIndex) => {
  let startY = null;
  let endY = null;
  let findMesh = false;
  const mouseDown = (event) => {
    if (event.button === 0) {
      startY = event.clientY;
    }
  }

  const mouseUp = (event) => {
    if (event.button === 0 && startY !== null) { 
      endY = event.clientY; 
      const distance = Math.ceil((endY - startY)/100);
      let index = Math.ceil(nrrdSliceZ.index / nrrdSliceZ.volume.spacing[2]);
      index += distance;
      if (index > nrrdMaxIndex) index = nrrdMaxIndex;
      if (index < 0) index = 0;
      nrrdSliceZ.index = index * nrrdSliceZ.volume.spacing[2];
      nrrdSliceZ.repaint.call(nrrdSliceZ);
      startY = null;
    }
  }
  const mouseMove = (event) => {
    const a = scene.pickSpecifiedModel(nrrdMesh, {x: event.offsetX, y: event.offsetY});
    if(!!a.intersectedObject){
      if(!findMesh){
        scene.controls.noRotate = true;
        container.style.cursor = "pointer";
        container.addEventListener("mousedown", mouseDown);
        container.addEventListener("mouseup", mouseUp);
      }
      findMesh = true;
    }else{
      findMesh = false;
      scene.controls.noRotate = false;
      container.style.cursor = "auto";
      container.removeEventListener("mousedown", mouseDown);
      container.removeEventListener("mouseup", mouseUp);
    }
  }
  return {mouseMove, mouseDown, mouseUp};
}

export default (context, inject) => {
  inject("baseRenderer", () => {
    return baseRenderer;
  }),
  inject("baseContainer", () => {
    return container;
  }),
  inject("baseLeftRenderer", () => {
    return baseLeftRenderer;
  }),
  inject("baseLeftContainer", () => {
    return leftContainer;
  }),
  inject("baseRightRenderer", () => {
    return baseRightRenderer;
  }),
  inject("baseRightContainer", () => {
    return rightContainer;
  }),
  inject("modelData", () => {
    return modelData;
  }),
  inject("three", () => {
    return THREE;
  }),
  inject("Copper", () => {
    return Copper;
  });
  inject("raycaster", () => {
    return raycaster;
  });
};
