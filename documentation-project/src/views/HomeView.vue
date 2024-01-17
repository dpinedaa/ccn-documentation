<template> 
  <ContentTitle></ContentTitle>
  <AddFile></AddFile>
  <div class="layout">

      

      <!-- COPY FROM HERE -->
      
      <div class="content">
        <ul>
          <li v-for="(content, fileName) in fileContents" :key="fileName" style="display: flex; justify-content: space-between;">
            <div style="width: 97%;">
              <!-- Content -->
              <span v-if="!editMode[fileName]">
                <span v-if="isText(fileName)">
                  {{ content }}
                  <br />
                  Style: {{ style }}
                  <br />
                </span>

                <span v-else-if="isCSV(fileName)">
                  <table>          
                    <thead>
                      <tr>
                        <th v-for="(header, index) in fileContents[fileName].headers" :key="index">{{ header }}</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(row, rowIndex) in fileContents[fileName].rows" :key="rowIndex">
                        <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
                      </tr>
                    </tbody>
                  </table>
                  <br />
                </span>


                <span v-else-if="isImage(fileName)">
                    <img :src="getFilePath(fileName)" alt="Image" style="max-width: 100%; max-height: 200px;" />
                    <br />
                  </span>
                </span>

                <!-- Edit File -->
                <span v-else>
                  <span v-if="isText(fileName)">
                    <EditText></EditText>
                  </span>

                  <span v-else-if="isCSV(fileName)">
                    <EditCSV></EditCSV>
                  </span>

                  <span v-else-if="isImage(fileName)">
                    <EditImage></EditImage>
                  </span>
                </span>
              </div>

              <div style="width: 3%;">
                <!-- Buttons -->
                <button class="file-item" @click="toggleEditMode(fileName)">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="file-item" @click="deleteFile(fileName)">
                  <i class="fas fa-trash"></i>
                </button>
                <button class="file-item" @click="moveFileUp(fileName)" :disabled="isFirstFile(fileName)">
                  <i class="fas fa-arrow-up"></i>
                </button>
                <button class="file-item" @click="moveFileDown(fileName)" :disabled="isLastFile(fileName)">
                  <i class="fas fa-arrow-down"></i>
                </button>
              </div>
            </li>
          </ul>


          
          <div v-if="addTextBoolean">
            <input class="title-input" type="text" v-model="newTextFileName">
            <button class="section-title-btn" @click="addTextFile"><i class="fas fa-save"></i></button>
            <button class="section-title-btn" @click="cancelAddText"><i class="fas fa-times"></i></button>

          </div>  

          <div v-if="addCSVBoolean">
            <input class="title-input" type="text" v-model="newCSVFileName">
            <button class="section-title-btn" @click="addCSVFile"><i class="fas fa-save"></i></button>
          </div>  


          <div v-if="addImageBoolean">

            
            <button class="section-title-btn" @click="addImageFile"><i class="fas fa-save"></i></button>
          </div>
      </div>
  </div>
</template>

<script>
// import axios from 'axios';

import ContentTitle from '../components/ContentTitle.vue';
import AddFile from '../components/AddFile.vue';
import EditImage from '../components/EditImage.vue';
import EditCSV from '../components/EditCSV.vue';
import EditText from '../components/EditText.vue';


export default {
  data() {
    return {
      fileContents: {},
      contentsArray: [],
      editedContents: {},
      newColumnValues: {},
      editMode: {},
      errorMessage: '',
      addTextBoolean: false,
      addCSVBoolean: false,
      addImageBoolean: false,
      fileName: '',
      style: '',


    };
  },
  components:{
    ContentTitle,
    AddFile,
    EditImage,
    EditText,
    EditCSV,

  },  


  computed: {
    sectionNumber() {
      return this.$store.getters.sectionNumber;
    }
  },
  mounted() {
    //this.getSectionTitle();
    this.getFiles();
  },
  methods: {
    async getFiles() {
      const url = `http://192.168.6.79:PORTFLASK/files/${this.sectionNumber}`;
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        this.contentsArray = data
        .filter(file => !file.name.includes('title'))
        .map(file => ({
          content: file.content,
          name: file.name,
        }));

        this.contentsArray.forEach((file) => {

          // if(file.name.contains('title')){
          //   console.log(file.name);
          // }
          
          if(file.name.endsWith('.txt')){
            const fileContent = file.content;

            const match1 = fileContent.match(/Style:\s*(.+)/);
            this.style = match1 ? match1[1].trim() : '';
            console.log(this.style);

            const match = fileContent.match(/Content:\s*([\s\S]+)/);
            this.fileContents[file.name] = match ? match[1] : '';
            this.editedContents[file.name] = match ? match[1] : '';
            this.editMode[file.name] = false;
            
          }
          else if(file.name.endsWith('.csv')){
            const fileContent = file.content;
            const csvRows = fileContent.split('\n').map(row => row.split(','));
            const csvHeaders = csvRows.shift(); // Assuming the first row contains headers

            this.fileContents[file.name] = {
              headers: csvHeaders,
              rows: csvRows,
            };

            this.editedContents[file.name] = this.fileContents[file.name];
            this.editMode[file.name] = false;

            // Initialize newColumnValues for each CSV file
            this.newColumnValues[file.name] = Array.from(
              { length: this.fileContents[file.name].headers.length },
              () => ''
            );


          }


          else if(file.name.endsWith('.png')||file.name.endsWith('.jpg')||file.name.endsWith('.jpeg')){
            this.fileContents[file.name] = '';
            this.editedContents[file.name] = this.fileContents[file.name];
            this.editMode[file.name] = false;
          }


        });

      } catch (error) {
        console.error('Error fetching data:', error);
        this.errorMessage = 'Error fetching data';
      }
    },
      // Add your other methods here (toggleEditMode, deleteFile, moveFileUp, moveFileDown, etc.)
    
      isImage(fileName) {
        return fileName.toLowerCase().endsWith('.png') || fileName.toLowerCase().endsWith('.jpeg');
      },
      isCSV(fileName) {
        return fileName.toLowerCase().endsWith('.csv');
      },
      isText(fileName) {
        return fileName.toLowerCase().endsWith('.txt');
      },

      isFirstFile(fileName) {
        return Object.keys(this.fileContents).indexOf(fileName) === 0;
      },

      isLastFile(fileName) {
        const fileKeys = Object.keys(this.fileContents);
        return Object.keys(this.fileContents).indexOf(fileName) === fileKeys.length - 1;
      },

      getFilePath(fileName) {
        return `http://192.168.6.79:PORTFLASK/files/${this.sectionNumber}/${fileName}`;
      },

      toggleEditMode(fileName) {

        for (const file in this.editMode) {
          this.editMode[file] = false;
        }

        this.editMode[fileName] = !this.editMode[fileName];
        this.$store.commit('setFilename', fileName);

        if(fileName.endsWith('.csv')){
          this.$store.commit('setFileContentCSV', this.fileContents[fileName]);
          console.log(this.$store.getters.fileContentCSV);
        }
        else if(fileName.endsWith('.txt')){
          this.$store.commit('setFileContentText', this.fileContents[fileName]);
          console.log(this.$store.getters.fileContentText); 
        }
      },
      deleteFile(fileName) {
          const apiUrl = 'http://192.168.6.79:PORTFLASK/delete_file/' + this.sectionNumber + '/' + fileName;

          const scrollPosition = window.scrollY;
          console.log(scrollPosition);

          fetch(apiUrl, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
          })
            .then(response => response.json())
            .then(data => {
              console.log(data.message);
              window.sessionStorage.setItem('scrollPosition', scrollPosition); // Store scroll position in sessionStorage
              window.location.reload();
            })
            .catch(error => {
              console.error('Error:', error);
            });

          // After reloading the page
          window.onload = function() {
            setTimeout(function() {
              const scrollPosition = window.sessionStorage.getItem('scrollPosition');
              if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition));
                window.sessionStorage.removeItem('scrollPosition');
              }
            }, 0);
          };
        },


      moveFileUp(fileName) {
        const url = 'http://192.168.6.79:PORTFLASK/move_up/' + this.sectionNumber + '/' + fileName;
        const scrollPosition = window.scrollY;

        fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
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

                    // After reloading the page
          window.onload = function() {
            setTimeout(function() {
              const scrollPosition = window.sessionStorage.getItem('scrollPosition');
              if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition));
                window.sessionStorage.removeItem('scrollPosition');
              }
            }, 0);
          };
      },

      moveFileDown(fileName) {
        const url = 'http://192.168.6.79:PORTFLASK/move_down/' + this.sectionNumber + '/' + fileName;
        const scrollPosition = window.scrollY;

        fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
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

                    // After reloading the page
          window.onload = function() {
            setTimeout(function() {
              const scrollPosition = window.sessionStorage.getItem('scrollPosition');
              if (scrollPosition) {
                window.scrollTo(0, parseInt(scrollPosition));
                window.sessionStorage.removeItem('scrollPosition');
              }
            }, 0);
          };
      },

    addText() {
      this.addTextBoolean = true;
      this.addCSVBoolean  = false;
      this.addImageBoolean = false;

    },

    addCSV() {
      this.addTextBoolean = false;
      this.addCSVBoolean  = true;
      this.addImageBoolean = false;

    },

    addImage() {
      this.addTextBoolean = false;
      this.addCSVBoolean  = false;
      this.addImageBoolean = true;

    },

      
  }
  
};
</script>

  

<style>

.content {
    max-width: 70%;
    width: 70%; /* Keeps the content from getting too wide */
    font-family: Arial, Helvetica, sans-serif; /* Makes the font consistent across all platforms */
    justify-content: center; /* Centers the content horizontally */
    text-align: center; 
  }

.content {
  /* background-color: pink; */
  margin-top: 10px;
}
.content{
  margin-left: 15%;
  margin-right: 15%;
}

.section-content {

  margin-left: 2.5%;
  width: 95%;
  /* background-color: #ccc; */
  font-size: medium;
  font-family: 'Courier New', Courier, monospace;
  
  border-radius: 5px;
}




ul {
    list-style: none; /* Remove default list-style (bullet points) */
    padding: 0;
    margin: 0;
  }

  li {
    /* margin: 0; */
    border: 4.5px double black;
    border-color: black;
    border-radius: 5px;
    margin-top: 5px;
    margin-bottom: 10px;
    padding: 5px;
    /*Center text*/
    /* display: flex; */
    justify-content: center;
    align-items: center;
  }

.file-item {
  margin-top: 30px;
  margin-bottom: 20px;
}




/* Add the following styles to adjust table width */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px; /* Optional: Add margin between tables */
  table-layout: fixed;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  text-align: center;
}

.table thead{
  background-color: #f2f2f2;
  text-align: center;
}


.modify-text{
  width: 100%;
  height: 100px;
  border: 1px solid #ddd;
  padding: 1px;
  text-align: left;
  font-size: 20px;
  font-weight: bold;
  color: black;
  margin-top: auto; /* Set margin-top to auto to center vertically */
  margin-bottom: auto; /* Set margin-bottom to auto for additional centering */
  /* width: 50%; */
  align-self: center; /* Center within the flex container */
  font-weight: bold;
  /* padding: 10px; */  
}


.csv-input{
  width:90%;
  height: 100%;
  border: 1px solid #ddd;
  padding: none;
  margin: none;
  border-radius: 1px;
  background-color: transparent;
  /*Center horizontally*/
  font-family: Arial, Helvetica, sans-serif; /* Makes the font consistent across all platforms */
  font-size: 14px;

  
}


.modify-table {
  display: block;
  margin: auto;
  /* background-color: green; */
  border: 1px solid black;
  table-layout: fixed;
  
}

table th {
  /* display: flex; */
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-weight: bold;  
}




.delete-column{
  margin-top: 0px;
  background-color: transparent;
  border: none;
}






</style>
  