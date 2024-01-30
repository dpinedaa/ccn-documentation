<template>
    <div class="content">
        <div class="add-customer-section">
            <h1>Add Customer</h1>
            <input class="main-input" type="text" placeholder="Customer Name" v-model="customerName">
            <div class="main-buttons-section">
                <button class="main-buttons" @click="addCustomer"><i class="fas fa-check"></i></button>
                <!-- <button class="main-buttons" @click="cancel"><i class="fas fa-times"></i></button> -->
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            customerName: '',
        }
    },
    methods:{
        addCustomer(){
            const url = 'http://10.7.1.100:1502/add-customer';
            // Upload customer name to database it's a post method so we need to pass the data

            axios.post(url, {name: this.customerName}).then((response) => {
                console.log(response);
                this.$router.push('/list');
            }).catch((error) => {
                console.log(error);
            });

        }

    }
}

</script>

<style>
@import '../assets/addcustomersection.css';

</style>