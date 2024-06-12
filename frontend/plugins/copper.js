import * as Copper from "copper3d";
import * as THREE from "three";

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
    inject("three", () => {
      return THREE;
    }),
    inject("Copper", () => {
      return Copper;
    });
};
