<template>
  <div>
    <NavBar></NavBar>
    <Header></Header>
    <!-- <ContentTitle></ContentTitle> -->
    <p> </p>
  
    <router-view></router-view>


  </div>
  <!-- <ShowFiles></ShowFiles> -->
  <!-- Add the AddFile component -->
  
</template>

<script>
//Navigation bar on the top 
import NavBar from './components/NavBar.vue';
import Header from './components/HeaderSection.vue';
// import AddFile from './components/AddFile.vue';
// import ContentTitle from './components/ContentTitle.vue';
// import ShowFiles from './components/ShowFiles.vue';


export default {
  components: {
    NavBar,
    Header,
    // AddFile,
    // ContentTitle,
    // ShowFiles
  },
  // Your other component logic goes here
};
</script>


<style>


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
