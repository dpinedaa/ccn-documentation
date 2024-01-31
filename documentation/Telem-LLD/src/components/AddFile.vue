<template>
  <div class="add-file-buttons">
    <button class="add-files" @click="addText"><i class="fas fa-font"></i>+</button>
    <button class="add-files" @click="addCSV"><i class="fas fa-table"></i>+</button>
    <button class="add-files" @click="addImage"><i class="fas fa-image"></i>+</button>
  </div>

  <div class="add-file-container" :style="{ height: containerHeight }">
    <!-- Add text form -->
    <form v-if="addtext" @submit.prevent="saveText">
      <AddText></AddText>
    </form>
    <!-- Add CSV form -->
    <form v-if="addcsv" @submit.prevent="saveCSV">
      <AddCSV></AddCSV>
    </form>
    <!-- Add Image form -->
    <form v-if="addimage" @submit.prevent="saveImage">
      <AddImage></AddImage>
    </form>
  </div>
</template>

<script>
import AddText from './AddText.vue';
import AddCSV from './AddCSV.vue';
import AddImage from './AddImage.vue';

export default {
  components: {
    AddText,
    AddCSV,
    AddImage,
  },
  data() {
    return {
      text: "",
      addtext: false,
      addcsv: false,
      addimage: false,
    };
  },
  computed: {
    sectionNumber() {
      return this.$store.getters.sectionNumber;
    },
    containerHeight() {
      if(this.addtext){
        return '300px';
      }
      else if(this.addimage){
        return '200px';
      }
      else if(this.addcsv){
        return '1000px';
      }
      else{
        return '0';
      }
    },
  },
  methods: {
    addText() {
      this.addtext = true;
      this.addimage = false;
      this.addcsv = false;
    },
    addCSV() {
      this.addtext = false;
      this.addimage = false;
      this.addcsv = true;
    },
    addImage() {
      this.addtext = false;
      this.addimage = true;
      this.addcsv = false;
    },
  },
};
</script>

<style>
@import '../assets/addfile.css';
</style>
