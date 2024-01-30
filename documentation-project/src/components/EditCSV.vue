<template>
    <div>
      <table>
        <thead>
          <tr class="delete-column">
            <th class="delete-column" v-for="(header, index) in headers" :key="index">
              <br />
              <button class="modify-table" @click="removeColumn(index)"><i class="fas fa-minus"></i></button>
            </th>
            
          </tr>
          <tr>
            <th v-for="(header, index) in headers" :key="index">
              <input class="csv-input" v-model="headers[index]" />
              <br />
            </th>
            <th>
              <!-- Make width to 5% -->
              <button class="modify-table" @click="addColumn()"><i class="fas fa-plus"></i></button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
            <td v-for="(cell, cellIndex) in row" :key="cellIndex">
              <input class="csv-input" v-model="rows[rowIndex][cellIndex]" />
            </td>
            <td>
              <button class="modify-table" @click="removeRow(rowIndex)"><i class="fas fa-minus"></i></button>
            </td>
          </tr>
          <tr>
            <td v-for="(header, index) in headers" :key="index">
              <input class="csv-input" v-model="newColumnValues[index]" />
            </td>
            <td>
              <button class="modify-table" @click="addRow()"><i class="fas fa-plus"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <button class="add-text-buttons" @click="saveFile"><i class="fas fa-save"></i></button>
      <button class="add-text-buttons" @click="cancelEdit"><i class="fas fa-times"></i></button>
    </div>
  </template>
  
  <script>
  export default {
    
    data() {
        return {
            content: null,
            headers: [],
            rows: [],
            newColumnValues: [], // Initialize as an empty array
            editedContents: {}, // Add this line to initialize editedContents
        };
    },

    mounted() {
        // Set the initial content when the component is mounted
        this.content = this.$store.getters.fileContentCSV;
        this.headers = this.content.headers;
        this.rows = this.content.rows;

        // Initialize newColumnValues based on headers length
        this.newColumnValues = Array(this.headers.length).fill('');

        // Set editedContents for the current file
        this.editedContents[this.fileName] = {
            headers: this.headers,
            rows: this.rows
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
    methods: {
      addColumn() {
        const newColumnName = " ";
        this.headers.push(newColumnName);
        // Update newColumnValues for this CSV file
        this.newColumnValues.push('');
        // Update existing rows with the new column
        this.rows.forEach((row) => {
          row.push('');
        });
      },
      removeColumn(columnIndex) {
        this.headers.splice(columnIndex, 1);
        this.newColumnValues.splice(columnIndex, 1);
        this.rows.forEach((row) => row.splice(columnIndex, 1));
      },
      addRow() {
        const newRow = this.newColumnValues.slice();
        this.rows.push(newRow);
        // Reset newColumnValues
        this.newColumnValues = Array.from({ length: this.headers.length }, () => '');
      },
      removeRow(rowIndex) {
        this.rows.splice(rowIndex, 1);
      },
      saveFile() {
        const fileName = this.$store.getters.filename;
        const scrollPosition = window.scrollY;
        const updatedContent = this.editedContents[fileName];
        const apiUrl = 'http://10.7.1.100:65000/update_file/' + this.sectionNumber + '/' + fileName;  
        console.log(updatedContent);
        if (fileName.endsWith('.csv')) {
            const updatedCSVContent = this.convertToCSV(updatedContent);
            fetch(apiUrl, {
            method: 'PUT',
            headers: {
                'Content-Type': 'text/csv',
            },
            body: updatedCSVContent,
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

            window.onload = function() {
            setTimeout(function() {
              const scrollPosition = window.sessionStorage.getItem('scrollPosition');
              if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition));
                window.sessionStorage.removeItem('scrollPosition');
              }
            }, 0);
          };

      } 
      },
      cancelEdit() {
        // Reload page
        window.location.reload();
      },

    convertToCSV(data) {
        const headers = data.headers.join(',');
        const rows = data.rows.map(row => row.join(',')).join('\n');
        return `${headers}\n${rows}`;
    },
    },
  };
  </script>
  
  <style>
  /* Add any necessary styles */
  </style>