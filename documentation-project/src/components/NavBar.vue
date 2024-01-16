<template>
    <div class="navbar">
    <h3>Section: </h3>
    <select class="dropdown-section" v-model="selectedSection" @change="selectSection">
              <!-- <option value="">{{ sectionNumber }}</option> -->
      <option v-for="(section, index) in sections" :value="section" :key="index">{{ section }}</option>
    </select>
      <button class="nav-btn" @click="updateSphinx"><i class="fas fa-sync-alt"></i></button>
      <button class="nav-btn" @click="goToDocumentation"><i class="fas fa-book"></i></button>
    </div>
</template>

<script>
export default{
    data(){
        return{
            selectedSection: '',
            sections: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
    }

    },
    computed: {
        sectionNumber() {
        return this.$store.getters.sectionNumber;
        }
    },
    methods:{
        goToDocumentation() {
            this.$router.push('/documentation');
        },
        
        async updateSphinx() {
            const url = 'http://192.168.4.31:9876/update'
            const response = await fetch(url, {
                method: 'POST',
            });
            console.log(response.status);
            if(response.status == 200){
                alert("Sphinx documentation updated successfully!");
            }
        },

        selectSection() {
            console.log(this.selectedSection);
            this.$store.commit('setSectionNumber', this.selectedSection);
            //Refresh current page 
            this.$router.go();
        },
    }
}

</script>

<style>
@import '../assets/navbar.css';

</style>