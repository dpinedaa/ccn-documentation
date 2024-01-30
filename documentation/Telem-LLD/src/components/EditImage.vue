<template>

    <div v-if="imageFile" class="selected-file-name">
      {{ fileName }}
    </div>

  <div class="upload">
    <!-- Display the selected file name -->

    <input class="upload-file" type="file" id="file" ref="file" @change="handleImageChange" accept=".jpeg,.png,.jpg" multiple>
    <label for="file" class="generate-table-section-buttons"><i class="fas fa-file-upload"></i></label>
    <button class="generate-table-section-buttons" @click="saveImage"><i class="fas fa-save"></i></button>
    <button class="generate-table-section-buttons" @click="cancelModify"><i class="fas fa-times"></i></button>
  </div>

</template>

<script>
export default {
  data() {
    return {
      editedContents: {},
      editMode: {},
      imageFile: null,
      fileName: '',
    };
  },
  computed: {
    sectionNumber() {
      return this.$store.getters.sectionNumber;
    },
    filename() {
      return this.$store.getters.filename;
    },
  },
  methods: {
    saveImage() {
      const scrollPosition = window.scrollY;
      const fileName = this.filename;
      const apiUrl = 'http://192.168.6.79:4002/update_file/' + this.sectionNumber + '/' + fileName;

      if (fileName.endsWith('.png') || fileName.endsWith('.jpeg')) {
        const file = this.$refs.file.files[0];
        const formData = new FormData();
        formData.append("file", file);

        const reader = new FileReader();
        reader.onload = () => {
          const base64String = reader.result.split(',')[1];
          formData.append("base64Data", base64String);

          fetch(apiUrl, {
            method: 'PUT',
            body: formData,
          })
          .then(response => response.json())
          .then(data => {
            console.log(data.message);
            window.scrollTo(0, scrollPosition);
            window.location.reload();
          })
          .catch(error => {
            console.error('Error:', error);
          });
        };
        reader.readAsDataURL(file);
      }
    },

    cancelModify() {
      // Handle cancel action here
      // For example, you may want to reset the file input and clear any selections
      this.$refs.file.value = null;
      this.imageFile = null;
      this.fileName = '';
    },

    handleImageChange() {
      // Handle file change if needed
      // For example, update imageFile and fileName based on the selected file
      const fileInput = this.$refs.file;
      if (fileInput.files.length > 0) {
        this.imageFile = fileInput.files[0];
        this.fileName = this.imageFile.name;
      } else {
        this.imageFile = null;
        this.fileName = '';
      }
    },
  },
};
</script>

<style>

.upload{
  margin: 30px;
}

</style>
