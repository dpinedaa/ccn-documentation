<template>
    <NavBar/>
    <HeaderSection/>
    <CustomerList/>
  </template>
  
  <script>
  import NavBar from '../components/NavBar.vue';
  import HeaderSection from '../components/HeaderSection.vue';
  import CustomerList from '../components/ShowCustomersSection.vue';
  export default {
    components: {
        NavBar,
        HeaderSection,
        CustomerList,
    },
  };
  
  </script>
  
  <style>
  
  </style>