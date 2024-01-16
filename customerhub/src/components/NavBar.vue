<template>
    <div class="navbar">
        <button class="nav-btn" @click="goHome"><i class="fas fa-home"></i></button>
        <button class="nav-btn" @click="goToAddCustomer"><i class="fas fa-user-plus"></i></button>
        <button class="nav-btn" @click="goToCustomers"><i class="fas fa-users"></i></button>
    </div>




</template>

<script>
export default{
    data(){
        return{
            
    }

    },
    computed: {
        
    },
    methods:{
        goHome(){
            this.$router.push({name: 'home'});
        },
        goToAddCustomer(){
            this.$router.push({name: 'add'});
        },
        goToCustomers(){
            this.$router.push({name: 'list'});
        }
    }
}

</script>

<style>
@import '../assets/navbar.css';

</style>