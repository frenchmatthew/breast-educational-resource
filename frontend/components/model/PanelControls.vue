<template>
  <div class="model-control">
    <span>
      {{ modelControl }}
    </span>

    <div class="mammo">
      <img src="~assets/images/breast_2.jpeg" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      modelControl: "Mammogram",
    };
  },

  beforeDestroy() {
    // Wirte code before destory this component
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
  .mammo {
    display: flex;
    flex-direction: column;
    padding: 20px 0;
    img {
      width: 15vw;
      height: auto;
    }
  }
}
</style>
