<template> 
  <div class="layout">

    


      <div class="content">
        <div class="section-title">
          <h1>Section {{sectionNumber}} Title</h1>
          <div v-if="sectionTitle && !editTitleBoolean && !saveTitleBoolean">
            <p>{{ sectionTitle }}</p>
            <button class="section-title-btn" @click="editTitle"><i class="fas fa-edit"></i></button>
          </div>

          <div v-else-if="editTitleBoolean">
            <input class="title-input" type="text" v-model="sectionTitle">
            
            <button class="section-title-btn" @click="saveTitle"><i class="fas fa-save"></i></button>
          </div>
          
        </div>

        <div class="section-content">
          <ul v-if="Object.keys(fileContents).length">
            <li v-for="(content, fileName) in fileContents" :key="fileName">
              <br />
              
              <br />
              <span v-if="!editMode[fileName]">

                <span v-if="isText(fileName)">
                  {{ content }}
                  <br />
                  <button class="file-item" @click="toggleEditMode(fileName)">
                    <i class="fas fa-edit"></i>
                  </button>

                  <button class="file-item" @click="deleteFile(fileName)">  <i class="fas fa-trash"></i></button>
                  <button class="file-item" @click="moveFileUp(fileName)" :disabled="isFirstFile(fileName)"><i class="fas fa-arrow-up"></i></button>
                  <button class="file-item" @click="moveFileDown(fileName)" :disabled="isLastFile(fileName)"><i class="fas fa-arrow-down"></i></button>
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
                  <button class="file-item" @click="toggleEditMode(fileName)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="file-item" @click="deleteFile(fileName)">  <i class="fas fa-trash"></i></button>
                  <button class="file-item" @click="moveFileUp(fileName)" :disabled="isFirstFile(fileName)"><i class="fas fa-arrow-up"></i></button>
                  <button class="file-item" @click="moveFileDown(fileName)" :disabled="isLastFile(fileName)"><i class="fas fa-arrow-down"></i></button>
                </span>

                <span v-else-if="isImage(fileName)">
                  <img :src="getFilePath(fileName)" alt="Image" style="max-width: 100%; max-height: 200px;" />
                  <br />
                  <button class="file-item" @click="toggleEditMode(fileName)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="file-item" @click="deleteFile(fileName)">  <i class="fas fa-trash"></i></button>
                  <button class="file-item" @click="moveFileUp(fileName)" :disabled="isFirstFile(fileName)"><i class="fas fa-arrow-up"></i></button>
                  <button class="file-item" @click="moveFileDown(fileName)" :disabled="isLastFile(fileName)"><i class="fas fa-arrow-down"></i></button>
                </span>

              </span>
              <span v-else>
                  <span v-if="isText(fileName)">
                    <input class="modify-text" v-model="editedContents[fileName]" />

                    <button @click="saveFile(fileName)"><i class="fas fa-save"></i></button>
                    <button @click="cancelEdit(fileName)">  <i class="fas fa-times"></i></button>
                  </span>

                  <span v-else-if="isCSV(fileName)">
                    <table>
                      <thead>
                        <tr class="delete-column">
                          <th class="delete-column" v-for="(header, index) in fileContents[fileName].headers" :key="index">
                            <br />
                            <button class="modify-table" @click="removeColumn(fileName, index)"><i class="fas fa-minus"></i></button>
                          </th>
                        </tr>
                        <tr>
                          <th v-for="(header, index) in fileContents[fileName].headers" :key="index">
                            <input class="csv-input" v-model="fileContents[fileName].headers[index]" />
                            <br />
                            
                          </th>

                          
                          <th>
                            <button class="modify-table" @click="addColumn(fileName)"><i class="fas fa-plus"></i></button>
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(row, rowIndex) in fileContents[fileName].rows" :key="rowIndex">
                          <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                            <input class="csv-input" v-model="editedContents[fileName].rows[rowIndex][cellIndex]" />
                          </td>
                          <td>
                            <button class="modify-table" @click="removeRow(fileName, rowIndex)"><i class="fas fa-minus"></i></button>
                          </td>
                        </tr>
                        <tr>
                          <td v-for="(header, index) in fileContents[fileName].headers" :key="index">
                            <input  class="csv-input" v-model="newColumnValues[fileName][index]" />
                          </td>
                          <td>
                            <button class="modify-table" @click="addRow(fileName)"><i class="fas fa-plus"></i></button>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <button @click="saveFile(fileName)"><i class="fas fa-save"></i></button>
                    <button @click="cancelEdit(fileName)">  <i class="fas fa-times"></i></button>
                  </span>

                  <span v-else-if="isImage(fileName)">
                    <input type="file" id="myFile" name="filename" accept="image/jpeg, image/png">
                    <button @click="saveFile(fileName)"><i class="fas fa-save"></i></button>
                    <button @click="cancelEdit(fileName)">  <i class="fas fa-times"></i></button>
                  </span>

              </span>
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


          <button class="add-files" @click="addText"><i class="fas fa-font"></i></button>
          <button class="add-files" @click="addCSV"><i class="fas fa-table"></i></button>
          <button class="add-files" @click="addImage"><i class="fas fa-image"></i></button>
          



        </div>
    


      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      
      
      sectionTitle: '-',
      //sectionTitle: 'Diana is the best que te parece esto? sera que ya no esta asi? que itneresante todo esto vamos a ver que tal',
      editTitleBoolean: false,
      saveTitleBoolean: false,
      fileContents: {},
      contentsArray: [],
      editedContents: {},
      newColumnValues: {},
      editMode: {},
      errorMessage: '',
      addTextBoolean: false,
      addCSVBoolean: false,
      addImageBoolean: false,


    };
  },



  mounted() {
    this.getSectionTitle();
    this.getFiles();
  },
  methods: {
    async getFiles() {
      const url = `http://192.168.6.79:9876/files/${this.sectionNumber}`;
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
    










  
    goToDocumentation() {
      this.$router.push('/documentation');
    },
    updateSphinx() {
      this.$router.push('/section1');
    },
    
    editTitle() {
      this.editTitleBoolean = true;  
      console.log(this.sectionNumber);
    },
    saveTitle() {
      this.editTitleBoolean = false;

      const url = 'http://192.168.6.79:9876/update_title/' + this.sectionNumber;
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
        
        const url = 'http://192.168.6.79:9876/get_title/'+this.sectionNumber;

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
        return `http://192.168.6.79:9876/files/${this.sectionNumber}/${fileName}`;
      },



      toggleEditMode(fileName) {
        this.editMode[fileName] = !this.editMode[fileName];
      },


      saveFile(fileName) {
        const updatedContent = this.editedContents[fileName];
        const apiUrl = 'http://192.168.6.79:9876/update_file/' + this.sectionNumber + '/' + fileName;  
        console.log(updatedContent);


        if (fileName.endsWith('.txt')) {
        fetch(apiUrl, {
          method: 'PUT',
          headers: {
            'Content-Type': 'text/plain',
          },
          body: updatedContent,
        })
          .then(response => response.json())
          .then(data => {
            console.log(data.message);
          })
          .catch(error => {
            console.error('Error:', error);
          });
      } else if (fileName.endsWith('.csv')) {
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
          })
          .catch(error => {
            console.error('Error:', error);
          });



      } 
      else if (fileName.endsWith('.png') || fileName.endsWith('.jpeg')) {
        const file = document.getElementById("myFile").files[0];
        console.log(file);
        const formData = new FormData();
        formData.append("file", file);
        
        console.log(file);
        const reader = new FileReader();
        reader.onload = () => {
          const base64String = reader.result.split(',')[1]; // Extract base64 string
          formData.append("base64Data", base64String);

          fetch(apiUrl, {
            method: 'PUT',
            body: formData,
          })
            .then(response => response.json())
            .then(data => {
              console.log(data.message);
            })
            .catch(error => {
              console.error('Error:', error);
            });
        };
        reader.readAsDataURL(file);

      }
        

      },



      cancelEdit(fileName) {
        this.editedContents[fileName] = this.fileContents[fileName];
        this.editMode[fileName] = false;
        //Reload the page
        this.$router.go();
      },









      deleteFile(fileName) {
        const apiUrl = 'http://192.168.6.79:9876/delete_file/' + this.sectionNumber + '/' + fileName;


        fetch(apiUrl, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then(response => response.json())
          .then(data => {
            console.log(data.message);
            window.location.reload();
          })
          .catch(error => {
            console.error('Error:', error);
          });
      },












      // Inside methods object
    addColumn(fileName) {
      const newColumnName = "New Column";
      this.fileContents[fileName].headers.push(newColumnName);
      
      // Update newColumnValues for this CSV file
      this.newColumnValues[fileName].push('');

      // Update existing rows with the new column
      this.editedContents[fileName].rows.forEach((row) => {
        row.push('');
      });
    },

    removeColumn(fileName, columnIndex) {
      this.fileContents[fileName].headers.splice(columnIndex, 1);
      this.newColumnValues[fileName].splice(columnIndex, 1);
      this.editedContents[fileName].rows.forEach((row) => row.splice(columnIndex, 1));
    },
    addRow(fileName) {
      const newRow = this.newColumnValues[fileName].slice();
      this.editedContents[fileName].rows.push(newRow);
      // Reset newColumnValues
      this.newColumnValues[fileName] = Array.from(
        { length: this.fileContents[fileName].headers.length },
        () => ''
      );
    },
    removeRow(fileName, rowIndex) {
      this.editedContents[fileName].rows.splice(rowIndex, 1);
    },
    convertToCSV(data) {
      const headers = data.headers.join(',');
      const rows = data.rows.map(row => row.join(',')).join('\n');
      return `${headers}\n${rows}`;
    },

    moveFileUp(fileName) {
      const currentIndex = Object.keys(this.fileContents).indexOf(fileName);
      const newIndex = currentIndex - 1;

      this.swapFiles(currentIndex, newIndex);
    },

    moveFileDown(fileName) {
      const currentIndex = Object.keys(this.fileContents).indexOf(fileName);
      const newIndex = currentIndex + 1;

      this.swapFiles(currentIndex, newIndex);
    },

    swapFiles(index1, index2) {
      const fileKeys = Object.keys(this.fileContents);

      if (index1 >= 0 && index1 < fileKeys.length && index2 >= 0 && index2 < fileKeys.length) {
        [fileKeys[index1], fileKeys[index2]] = [fileKeys[index2], fileKeys[index1]];
        const newFileContents = {};
        fileKeys.forEach((key) => {
          newFileContents[key] = this.fileContents[key];
        });
        this.fileContents = newFileContents;

        const newOrder = fileKeys.join(',');
        this.saveFileOrder(newOrder);
      }
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


.content{
  max-width: 70%;
  width: 70%; /* Keeps the content from getting too wide */
  font-family: Arial, Helvetica, sans-serif; /* Makes the font consistent across all platforms */
  justify-content: center; /* Centers the content horizontally */
  text-align: center; 
}



.content {
  background-color: pink;
  margin-top: 10px;
}



.section-content {
  margin-left: 2.5%;
  width: 95%;
  background-color: #ccc;
  
  border-radius: 5px;
}




.section-title {
  margin-top: 40px;
  margin-left: 2.5%;
  width: 95%;
  /* background-color: aqua; */
  height: 170px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.section-title p {
  /* background-color: aqua; */
  margin: 0; /* Remove default margin to align with input */
  padding-top: 10px; /* Adjust as needed */
  overflow: hidden; /* Hide any overflow content */
  white-space: normal; /* Wrap the content to the next line */
  height: auto; /* Adjust the height to automatically accommodate the wrapped content */
  /* width: 90%;  */
  font-size: 30px; /* Decrease the font size to fit the content */
  color: black;
  font-weight: bold;
  word-wrap: break-word; /* Break words at any character */
  hyphens: auto; /* Add hyphens when words are broken */
   /* Keeps the content from getting too wide */
  overflow-wrap: break-word;

}





.title-input {
  border: none;
  border-bottom: solid 1.5px #9e9e9e;
  /* border-radius: 1rem; */
  background: none;
  padding-top: 10px; /* Adjust as needed */
  /* font-size: 1rem; */
  font-size: 25px;
  color: black;
  margin-top: auto; /* Set margin-top to auto to center vertically */
  margin-bottom: auto; /* Set margin-bottom to auto for additional centering */
  width: 50%;
  align-self: center; /* Center within the flex container */
  font-weight: bold;
  /* padding: 10px; */  
}


.section-title-btn {
  width: 60px;
  background-color: #e6e6e6;
  border: 1px solid black;
  font-size: 18px;
  text-align: center;
  font-weight: bold;
  border-radius: 5px;
  margin: 10px; /* Adjust as needed */
}

ul {
    list-style: none; /* Remove default list-style (bullet points) */
    padding: 0;
    margin: 0;
  }

  li {
    /* margin: 0; */
    border: 1px solid black;
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
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
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
  