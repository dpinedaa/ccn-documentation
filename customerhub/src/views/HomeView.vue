<template>
  <NavBar/>
  <HeaderSection/>
  <HomeContent/>
  
</template>

<script>
import NavBar from '../components/NavBar.vue';
import HeaderSection from '../components/HeaderSection.vue';
import HomeContent from '../components/HomeContent.vue';

export default {
  components: {
    NavBar,
    HeaderSection,
    HomeContent,
  },
};

</script>

<style>

</style>