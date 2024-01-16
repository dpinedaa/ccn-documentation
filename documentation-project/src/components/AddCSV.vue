<template>
    <div class="add-csv-title">
      <h3>Add Table</h3>
    </div>

    <div class="generate-table">
      <button class="generate-table-section-buttons" @click="uploadCSV"><i class="fas fa-file-upload"></i></button>
      <button class="generate-table-section-buttons" @click="generateTable"><i class="fas fa-table"></i></button>
    </div>
  
    <div class="add-csv-caption">
      <input class="add-csv-caption-input" type="text" v-model="tableCaption" placeholder="Table Caption">
    </div>
  

  
    <div class="upload" v-if="upload">
        <input class="upload-file" type="file" id="file" ref="file" @change="handleFileUpload" accept=".csv" multiple>
        <label for="file" class="generate-table-section-buttons"><i class="fas fa-file-upload"></i></label>
        <button class="generate-table-section-buttons" @click="uploadFile"><i class="fas fa-save"></i></button>
        <button class="generate-table-section-buttons" @click="cancelModify"><i class="fas fa-times"></i></button>

        <!-- Display the selected file name -->
        <div v-if="file" class="selected-file-name">
            {{ fileName }}
        </div>
    </div>

  
    <div v-if="create">
      <div class="create-table-section" :style="{ height: containerHeight }">
        <table class="create-table">
          <thead>
            <tr>
              <th class="column-buttons" v-for="(header, columnIndex) in csvHeaders" :key="columnIndex">
                <button class="modify-table" @click="removeColumn(columnIndex)">
                  <i class="fas fa-minus"></i>
                </button>
              </th>
            </tr>
            <tr>
              <th v-for="(header, columnIndex) in csvHeaders" :key="columnIndex">
                <input class="csv-input" v-model="csvHeaders[columnIndex]" />
              </th>
              <th>
                <button class="modify-table" @click="addColumn">
                  <i class="fas fa-plus"></i>
                </button>
              </th>
            </tr>
          </thead>
  
          <tbody>
            <tr v-for="(row, rowIndex) in csvData" :key="rowIndex">
              <td v-for="(cell, columnIndex) in row" :key="columnIndex">
                <input class="csv-input" v-model="csvData[rowIndex][columnIndex]" />
              </td>
              <td>
                <!-- Show the "Add Row" button only for the last row -->
                <button class="modify-table" @click="addRow" v-if="rowIndex === csvData.length - 1">
                  <i class="fas fa-plus"></i>
                </button>
                <!-- Show the "Remove Row" button only for existing rows (not the last one) -->
                <button class="modify-table" @click="removeRow(rowIndex)" v-else>
                  <i class="fas fa-minus"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
  
        <div class="add-csv-buttons-section">
          <button class="add-text-buttons" type="submit" @click="saveCSV"><i class="fas fa-save"></i></button>
          <button class="add-text-buttons" type="submit" @click="cancelModify"><i class="fas fa-times"></i></button>
        </div>
      </div>
    </div>
  </template>


<script>
import axios from 'axios';

export default {
  components: {
    // AddText,
  },
  data() {
    return {
      csvHeaders: ['', ''],
      csvData: [['', '']],
      tableCaption: '',
      style: '',
      upload: true,
      create: false,
      fileName: '',
      file: null
    };
  },
  computed: {
    sectionNumber() {
      return this.$store.getters.sectionNumber;
    },

  },
  methods: {
    addRow() {
      this.csvData.push(Array(this.csvData[0].length).fill(''));
    },
    addColumn() {
      this.csvData.forEach((row) => row.push(''));
      this.csvHeaders.push('');
    },
    removeRow(rowIndex) {
      if (this.csvData.length > 1) {
        this.csvData.splice(rowIndex, 1);
      }
    },
    removeColumn(columnIndex) {
      if (this.csvData[0].length > 1) {
        this.csvData.forEach((row) => row.splice(columnIndex, 1));
        this.csvHeaders.splice(columnIndex, 1);
      }
    },
    saveCSV() {
      this.saveCaption();
      console.log('Saving CSV');
      console.log(this.csvHeaders);
      console.log(this.csvData);

      const url = `http://192.168.4.31:9876/save_csv/${this.sectionNumber}`;

      axios
        .post(url, {
          headers: this.csvHeaders,
          data: this.csvData,
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
      window.location.reload();
    },
    saveCaption() {
      if (!this.tableCaption == '') {
        this.style = 'Caption';

        const url = 'http://192.168.4.31:9876/save_text/' + this.sectionNumber;

        axios
          .post(url, { text: this.tableCaption, style: this.style })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },
    cancelModify() {
      //Reload page
      window.location.reload();
    },
    uploadCSV() {
      this.upload = true;
      this.create = false;
    },
    generateTable() {
      this.upload = false;
      this.create = true;
    },
    uploadFile(){
        // Create FormData object
      let formData = new FormData();

        // Append the file to FormData
        formData.append('file', this.file);

        // Make a POST request to the server
        const url = `http://192.168.4.31:9876/add_csv/${this.sectionNumber}`;

        axios
        .post(url, formData)
        .then((response) => {
            console.log(response.data);
            // Optionally, you can handle the server's response here
        })
        .catch((error) => {
            console.error(error);
            // Handle the error if needed
        });

        //Reload page
        window.location.reload();

    },
    handleFileUpload() {
        this.file = this.$refs.file.files[0];
        this.fileName = this.file.name;
    },


  },
};
</script>


<style>
@import '../assets/addCSV.css';




</style>