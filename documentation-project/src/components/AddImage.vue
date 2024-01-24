<template>

    <div class="add-csv-title">
      <h3>Add Image</h3>
    </div>

    <div class="add-csv-caption">
      <input class="add-csv-caption-input" type="text" v-model="imageCaption" placeholder="Image Caption">
    </div>

    <div class="upload">
        <input class="upload-file" type="file" id="file" ref="file" @change="handleImageChange" accept=".jpeg,.png,.jpg" multiple>
        <label for="file" class="generate-table-section-buttons"><i class="fas fa-file-upload"></i></label>
        <button class="generate-table-section-buttons" @click="saveImage"><i class="fas fa-save"></i></button>
        <button class="generate-table-section-buttons" @click="cancelModify"><i class="fas fa-times"></i></button>

        <!-- Display the selected file name -->
        <div v-if="imageFile" class="selected-file-name">
            {{ fileName }}
        </div>
    </div>
    

    
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            imageFile: null,
            imageCaption: '',
            style: '',
            fileName: '',
            file: null,
        }
    },
    computed: {
      sectionNumber() {
        return this.$store.getters.sectionNumber;
      },
    },
    methods: {
        handleImageChange(event) {
            this.imageFile = event.target.files[0];
            this.fileName = this.imageFile.name;
        },
        saveImage() {
            this.saveCaption();
            
            const formData = new FormData();
            formData.append('image', this.imageFile);
            const url = `http://192.168.6.79:65000/save_image/${this.sectionNumber}`;

            axios.post(url, formData)
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });

            // Reload
            window.location.reload();
        },

        saveCaption(){
            if(this.imageCaption == '')
                console.log("No caption");
            else{
                this.style = "Caption";

            const url = 'http://192.168.6.79:65000/save_text/' + this.sectionNumber;

            axios.post(url, { text: this.imageCaption, style: this.style })
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
            }
        }
    },
};



</script>

<style>

.add-image-container {
    margin: 30px;
}



</style>