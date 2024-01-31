<template>
    <div class="layout">
      <div>
        <textarea class="add-text-textbox" v-model="content" required></textarea>
      </div>
      
      <!-- <input class="modify-text" v-model="content" /> -->
      <button class="add-text-buttons" @click="saveFile"><i class="fas fa-save"></i></button>
      <button class="add-text-buttons" @click="cancelEdit"><i class="fas fa-times"></i></button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        content: '',
      };
    },
    computed: {
      sectionNumber() {
        return this.$store.getters.sectionNumber;
      },
      fileName() {
        return this.$store.getters.filename;
      },

    },
    mounted() {
  // Set the initial content when the component is mounted
        this.content = this.$store.getters.fileContentText;
    },

    methods: {
      saveFile() {
        const updatedContent = this.content;
        const apiUrl =
          'http://192.168.6.79:4002/update_file/' +
          this.sectionNumber +
          '/' +
          this.fileName;
  
        if (this.fileName.endsWith('.txt')) {
          fetch(apiUrl, {
            method: 'PUT',
            headers: {
              'Content-Type': 'text/plain',
            },
            body: updatedContent,
          })
            .then((response) => response.json())
            .then((data) => {
              console.log(data.message);
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        }
      },
  
      cancelEdit() {
        // Reload page
        this.$router.go();
      },
    },

  };
  </script>
  
  <style>
  /* Add any necessary styles */
  </style>
  