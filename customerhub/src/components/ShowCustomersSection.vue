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
                                            <a :href="'http://192.168.6.79:' + document.portVue">{{ document.name }}</a>
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
                                    <button class="list-button" @click="saveDocument"><i class="fas fa-save"></i></button>
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


        }
    },

    mounted(){
        this.getCustomers();
    },
    methods:{
        getCustomers(){
            const url = 'http://192.168.6.79:3000/customers';

            axios.get(url).then((response) => {
                console.log(response);
                this.customers = response.data;
                console.log(this.customers);
            }).catch((error) => {
                console.log(error);
            });
        },

        deleteCustomer(customer){
            const url = 'http://192.168.6.79:3000/customers/' + customer._id;

            axios.delete(url).then((response) => {
                console.log(response);
                this.getCustomers();
                
            }).catch((error) => {
                console.log(error);
            });
            window.location.reload();
        },

        addDocument(customer){
            this.addDoc = true;
            this.customerId = customer._id;
            console.log(customer);
            this.customerId = customer._id;
        },

        saveDocument(){
            console.log(this.file);
            if(this.file){
                alert('File uploaded successfully');
            }
            console.log(this.customerId);
            const url = 'http://192.168.6.79:3000/add-document/' + this.customerId;
            
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
                window.location.reload();
            }).catch((error) => {
                console.log(error);
            });
        },

        deleteDocument(customer, document){
            const url = 'http://192.168.6.79:3000/delete-document/' + customer._id + '/' + document._id;
            axios.delete(url).then((response) => {
                console.log(response);
                this.getCustomers();
                window.location.reload();
                
            }).catch((error) => {
                console.log(error);
            });
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

        saveCustomer(customer){
            const url = 'http://192.168.6.79:3000/update-customer/' + customer._id;

            axios.put(url, {
                name: this.newCustomerName,
            }).then((response) => {
                console.log(response);
                this.getCustomers();
                this.editCustomerCheck = false;
                this.newCustomerName = '';
                window.location.reload();
            }).catch((error) => {
                console.log(error);
            });

        },

        editDocument(document){
            this.editDocumentCheck = true;
            console.log(document);
        },

        updateDocumentName(customer, document){
            const url = 'http://192.168.6.79:3000/update-document/' + customer._id + '/' + document._id;

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

        uploadFile(event) {
            this.file = event.target.files[0];
            console.log(this.file);
            // You can now send 'this.file' to your server
            // Make sure to handle the upload on the server side as well
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