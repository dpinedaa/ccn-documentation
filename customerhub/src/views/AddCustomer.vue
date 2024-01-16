<template>
    <NavBar/>
    <HeaderSection/>
    <AddCustomerSection/>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import HeaderSection from '../components/HeaderSection.vue';
import AddCustomerSection from '../components/AddCustomerSection.vue';


export default {
components: {
    NavBar,
    HeaderSection,
    AddCustomerSection,
},
};

</script>

<style>

</style>