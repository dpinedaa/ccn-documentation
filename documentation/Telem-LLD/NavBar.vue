<!-- NavBar.vue -->
<template>
    <div class="layout">
      <div class="navbar">
        <h3>Section: </h3>
        <select class="dropdown-section" v-model="selectedSection" @change="selectSection">
          <option v-for="(section, index) in sections" :value="section" :key="index">{{ section }}</option>
        </select>
        <button class="nav-btn" @click="updateSphinx">Update</button>
        <button class="nav-btn" @click="goToDocumentation">Documentation</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sections: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
        selectedSection: ' ',
      };
    },
    computed: {
      sectionNumber() {
        return this.$store.getters.sectionNumber;
      }
    },
    methods: {
      selectSection() {
        console.log(this.selectedSection);
        this.$store.commit('setSectionNumber', this.selectedSection);
        // Refresh current page
        this.$router.go();
        console.log(this.sectionNumber);
      },
      updateSphinx() {
        // Implement your logic for updating Sphinx
      },
      goToDocumentation() {
        // Implement your logic for navigating to documentation
      }
    }
  };
  </script>
  
  <style>
  /* Add your styles here if needed */
  </style>
  