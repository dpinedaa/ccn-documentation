<template>
    <div class="content">
        <!-- tr > row th > header td > table cell  -->
        <table class="customers">
            <thead>
                <tr>
                    <th class="customer-column">Customer Name</th>
                    <th class="document-column">Documents</th>
                    <th class="actions-column">Actions</th>
                </tr>
            </thead>
            <tbody>
                
                <tr v-for="customer in customers" :key="customer.name">
                    
                    <td class="customer-name" v-if=!editCustomerCheck>{{customer.name}}</td>
                    
                    <td v-if=editCustomerCheck style="width: 20%" class="customer-name"><input class="input-document" type="text" v-model="newCustomerName">
                    <button class="list-button" @click="saveCustomer(customer)"><i class="fas fa-save"></i></button>
                    <button class="list-button" @click="cancelEdit()"><i class="fas fa-times"></i></button></td>
                    
                    <td>
                        <ul>
                            <li v-for="document in customer.documents" :key="document.name">
                                <table class="document-table">
                                    <tr>
                                        
                                        <!-- <td v-if=!editDocumentCheck class="document-name">{{document.name}}</td>     -->
                                        <td v-if="!editDocumentCheck" class="document-name">
                                            <a :href="'http://10.7.1.100:' + document.portVue">{{ document.name }}</a>
                                        </td>


                                        <td v-if=!editDocumentCheck ><button class="list-button" @click="editDocument(document)"><i class="fas fa-edit"></i></button></td>
                                        <td v-if=!editDocumentCheck ><button class="list-button" @click="deleteDocument(customer, document)"><i class="fas fa-trash"></i></button></td>
                                        <td v-if=editDocumentCheck class="document-name"><input class="input-document" type="text" v-model="document.name"></td>
                                        <td v-if=editDocumentCheck ><button class="list-button" @click="updateDocumentName(customer, document)"><i class="fas fa-save"></i></button></td>
                                        <td v-if=editDocumentCheck ><button class="list-button" @click="cancelEdit()"><i class="fas fa-times"></i></button></td>

                                    </tr>
                                    
                                </table>
                                
                            </li>





                            <li v-if="addDoc && customer._id == customerId">

                                <div class="upload">
                                    <input class="input-document" type="text" placeholder="Document Name" v-model="documentName">
                                    <label for="file" class="list-button"><i class="fas fa-file-upload"></i></label>
                                    <input id="file" class="upload-file" type="file" @change="uploadFile" ref="file" accept=".docx"/>
                                    <!-- <input class="upload-file" type="file" ref="file" @change="handleFileUpload" accept=".word" style="display: none" /> -->
                                    <!-- <label for="file" class="list-button" @click="uploadFile"><i class="fas fa-file-upload"></i></label> -->
                                    <button class="list-button" @click="saveDocument(customer)"><i class="fas fa-save"></i></button>
                                    <button class="list-button" @click="cancelDocument"><i class="fas fa-times"></i></button>

                                    <!-- Display the selected file name -->
                                    <div v-if="imageFile" class="selected-file-name">
                                    {{ fileName }}
                                    </div>
                                </div>

                            </li>
                        </ul>
                    </td>
                    <td>
                        <button class="list-button" @click="addDocument(customer)">+ <i class="fas fa-file-alt"></i></button>

                        <button class="list-button" @click="editCustomer(customer)"><i class="fas fa-edit"></i></button>
                        <button class="list-button" @click="deleteCustomer(customer)"><i class="fas fa-trash"></i></button>
                    </td>
                    
                </tr>
                <!-- Make the column to all of them  -->
                

            </tbody>
        </table>

    </div>


    

</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            customers:[], 
            addDoc: false,
            documentName: '',
            costumerId: '',
            editCustomerCheck: false,
            newCustomerName: '',  
            editDocumentCheck: false,  
            file: null,
            imageFile: null,
            fileName: '',
            customername: '',


        }
    },

    mounted(){
        this.getCustomers();
    },
    methods:{
        getCustomers(){
            const url = 'http://10.7.1.100:1502/customers';

            axios.get(url).then((response) => {
                console.log(response);
                this.customers = response.data;
                console.log(this.customers);
            }).catch((error) => {
                console.log(error);
            });
        },

        async deleteCustomer(customer) {
            await this.deteleCustomerProjects(customer);

            const url = 'http://10.7.1.100:1502/customers/' + customer._id;

            axios.delete(url)
                .then((response) => {
                    console.log(response);
                    this.getCustomers();
                })
                .catch((error) => {
                    console.log(error);
                });

            window.location.reload();
        },

        async deteleCustomerProjects(customer) {
            const url = 'http://10.7.1.100:1501/delete-customer-projects/' + customer.name + '/' + customer._id;

            try {
                const response = await axios.post(url);
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        },


        addDocument(customer){
            this.addDoc = true;
            this.customerId = customer._id;
            console.log(customer);
            this.customerId = customer._id;
        },

        async saveDocument(customer){
            console.log(customer.name);
            console.log(this.file);
            if(this.file){
                this.customername = customer.name;
                this.saveFile(this.documentName);
            }
            console.log(this.customerId);
            const url = 'http://10.7.1.100:1502/add-document/' + this.customerId;
            
            fetch(url, {
                method: 'POST',
                body: JSON.stringify({
                    name: this.documentName,
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((response) => {
                console.log(response);
                this.getCustomers();
                this.addDoc = false;
                this.documentName = '';
            }).catch((error) => {
                console.log(error);
            });

            this.createDocumentComponents(this.documentName,customer.name);

            


        },

        async createDocumentComponents(documentname, customername) {
            const full_name = customername + '-' + documentname;
            const url = 'http://10.7.1.100:1501/createdocumentation/' + full_name;

            await axios.post(url)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });

            console.log('Before setTimeout');

            // setTimeout(() => {
            //     console.log('Inside setTimeout');
            //     window.alert(documentname + ' has been created');
            // }, 30000);

            console.log('After setTimeout');

            this.convertDocument(documentname, customername);   

            // window.location.reload();
        },

        async convertDocument(documentname, customername) {
            const full_name = customername + '-' + documentname;
            const url = 'http://10.7.1.100:1501/convert/' + full_name;

            await axios.post(url)
                .then((response) => {
                    console.log(response);
                })
                .catch((error) => {
                    console.log(error);
                });

            console.log('Before setTimeout');

            setTimeout(() => {
                console.log('Inside setTimeout');
                window.alert(documentname + ' is ready');
            }, 1000);

            //Reset the file
            this.file = null;
  
        },


        async deleteDocument(customer, document) {
            await this.deleteDocumentComponent(document.name, customer.name);

            const url = 'http://10.7.1.100:1502/delete-document/' + customer._id + '/' + document._id;
            
            try {
                const response = await axios.delete(url);
                console.log(response);
                this.getCustomers();
                
            } catch (error) {
                console.log(error);
            }


            //tell user that the document has been deleted
            window.alert(document.name + ' has been deleted');
            window.location.reload();

        
        },

        async deleteDocumentComponent(documentname, customername) {
            const full_name = customername + '-' + documentname;
            const url = 'http://10.7.1.100:1501/deletedocumentation/' + full_name;

            try {
                const response = await axios.post(url);
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        },


        editCustomer(customer){
            this.editCustomerCheck = true;
            this.newCustomerName = customer.name;
            this.customerId = customer._id;
            console.log(customer);
        },

        cancelEdit(){
            this.editCustomerCheck = false;
            this.newCustomerName = '';
            window.location.reload();
        },

        async saveCustomer(customer){
            await this.updateCustomerProjects(customer);

            const url = 'http://10.7.1.100:1502/update-customer/' + customer._id;

            axios.put(url, {
                name: this.newCustomerName,
            }).then((response) => {
                console.log(response);
                this.getCustomers();
                this.editCustomerCheck = false;
                window.location.reload();
            }).catch((error) => {
                console.log(error);
            });

        },

        async updateCustomerProjects(customer){
            const url = 'http://10.7.1.100:1501/modify-customer-name/' + customer.name;

            await axios.post(url, {
                name: this.newCustomerName,
            }).then((response) => {
                console.log(response);
            }).catch((error) => {
                console.log(error);
            });

        },

        editDocument(document){
            this.editDocumentCheck = true;
            console.log(document);
        },

        async updateDocumentName(customer, document){
            await this.updateDocumentNameFiles(customer, document);

            const url = 'http://10.7.1.100:1502/update-document/' + customer._id + '/' + document._id;

            axios.put(url, {
                name: document.name,
            }).then((response) => {
                console.log(response);
                this.getCustomers();
                this.editDocumentCheck = false;
                window.location.reload();
            }).catch((error) => {
                console.log(error);
            });
        },

        async updateDocumentNameFiles(customer, document){
            const url = 'http://10.7.1.100:1501/modify-document-name/' + document._id;
            console.log(url);
            try {
                const response = await axios.post(url, {
                    name: document.name,
                });
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        },

        uploadFile(event) {
            this.file = event.target.files[0];
            console.log(this.file);
        },

        saveFile(document_name){
            const full_name = this.customername + '-' + document_name;
            const url = 'http://10.7.1.100:1501/add-word-doc/' + full_name;
            
            const formData = new FormData();
            formData.append('word_doc', this.file);
            fetch(url, {
            method: 'POST',
            body: formData
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));
        },




        
    }
}


</script>

<style>
@import '../assets/customerlist.css';
.upload-file {
    display: none;
}

.upload-label {
    padding: 10px;
    background-color: #4CAF50; /* Green */
    color: white;
    cursor: pointer;
}

.upload-label:hover {
    background-color: #45a049; /* Darker green */
}

</style>