<template>
    
        
    <div class="section-title">
      <div class="h1-container">
        <h1>Section {{sectionNumber}} Title:</h1>
      </div>
      
      <div class="actual-section-title">
        <div v-if="sectionTitle && !editTitleBoolean && !saveTitleBoolean">
          <p>{{ sectionTitle }}</p>
        </div>

        <div v-else-if="editTitleBoolean">
          <input class="title-input" type="text" v-model="sectionTitle">
        </div>
      </div>


      <div class="section-title-buttons">
        <div v-if="sectionTitle && !editTitleBoolean && !saveTitleBoolean">
          <button class="section-title-btn" @click="editTitle"><i class="fas fa-edit"></i></button>
        </div>

        <div v-else-if="editTitleBoolean">
          <button class="section-title-btn" @click="saveTitle"><i class="fas fa-save"></i></button>
          <button class="section-title-btn" @click="cancelModify"><i class="fas fa-times"></i></button>
        </div>
      </div>
    </div>

</template>

<script>
import axios from 'axios';


export default{
    data(){
        return{
            sectionTitle: ' ',
            editTitleBoolean: false,
            saveTitleBoolean: false,
        }

    },
    computed: {
        sectionNumber() {
        return this.$store.getters.sectionNumber;
        }
    },
    mounted() {
        this.getSectionTitle();
        // this.getFiles();
    },
    methods:{
    editTitle() {
        this.editTitleBoolean = true;  
        console.log(this.sectionNumber);
    },
    saveTitle() {
      this.editTitleBoolean = false;

      const url = 'http://192.168.6.79:4307/update_title/' + this.sectionNumber;
      const newContent = this.sectionTitle;

      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Set the appropriate content type
        },
        body: JSON.stringify({ content: newContent }), // Convert data to JSON format
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.text();
        })
        .then(data => {
          console.log('Success:', data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },

    

    async getSectionTitle() {
      try{
        
        const url = 'http://192.168.6.79:4307/get_title/'+this.sectionNumber;

      axios.get(url)
          .then(response => {
          this.sectionTitle = response.data;

          })
          .catch(error => {
          this.sectionTitle= '-';
          console.error('Error getting files', error);
          });
      }
      catch (error) {
        console.error('Error fetching sectionTitle:', error);
      }
      
    },
    cancelModify() {
      //Reload page 
      // window.location.reload();
        this.editTitleBoolean = false;
    },

    },

};

</script>

<style>
@import '../assets/contentTitle.css';

</style>