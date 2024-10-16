<template>
  <div :class="mdAndUp ? 'aboutPanel-l' : 'aboutPanel-s'">
    
    <div
      v-if="section == 'team'"
      class="container-default research-page flexbox --vertical"
      :class="$vuetify.breakpoint.mdAndUp ? 'full-height' : ''"
    >
      <div class="pt-1 heading">
        <h3 class="heading__main">Our Breast Biomechanics Research Team</h3>
      </div>
      <div class="detail">
        <!-- <img src="~assets/images/headshots.png" /> -->
      </div>
      <div class="detail">
        <img src="~assets/images/team.jpg" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: "default",
  name: "AboutPage",

  data() {
    return {
      section: "team",
    };
  },
  computed: {
    mdAndUp() {
      return this.$vuetify.breakpoint.mdAndUp;
    },
  },
  created() {
    this.$nuxt.$on("about-navigation", (componentName) => {
      this.section = "team";
    });
    // this.$store.commit("setChartLoaded", "");
  },

  beforeDestroy() {
    this.$nuxt.$off("about-navigation");
  },
};
</script>

<style lang="scss" scoped src="@/assets/sass/pages/about.scss"></style>
