<template>
    <div class="document-details">
            <table class="doc-table">
                <tbody>
                    <tr> 
                        <td class="label"><label class="doc-label">Title</label></td>
                        <td class="input">
                            <input class="doc-input" placeholder="Title" v-model="docTitle" @keydown.enter="handleEnter('docTitle', $event)">
                            
                        </td>
                    </tr>
                    <tr>
                        <td class="label"><label class="doc-label">Number</label></td>
                        <td class="input">
                            <input class="doc-input" placeholder="Number" v-model="docNumber" @keydown.enter="handleEnter('docNumber', $event)">
                            
                        </td>
                    </tr>
                    <tr>
                        <td class="label"><label class="doc-label">Status</label></td>
                        <td class="input">
                            <input class="doc-input" placeholder="Status" v-model="docStatus" @keydown.enter="handleEnter('docStatus', $event)">
                            
                        </td>
                    </tr>
                    <tr>
                        <td class="label"><label class="doc-label">Issue Date</label></td>
                        <td class="input">
                            <input class="doc-input" type="date" id="datepicker" v-model="docIssueDate" placeholder="Select a Date" @keydown.enter="handleEnter('docIssueDate', $event)">
                            
                        </td>
                    </tr>
                    <tr>
                        <td class="label"><label class="doc-label">Security</label></td>
                        <td class="input">
                            <input class="doc-input" placeholder="Security" v-model="docSecurity" @keydown.enter="handleEnter('docSecurity', $event)">
                            
                        </td>
                    </tr>
                    <tr>
                        <td class="label"><label class="doc-label">Authors</label></td>
                        <td class="input">
                            <input class="doc-input" placeholder="Authors" v-model="docAuthors" @keydown.enter="handleEnter('docAuthors', $event)">
                            
                        </td>

                    </tr>


                    <tr>
                        <td class="label"><label class="doc-label">Client</label></td>
                        <td class="input">
                            <input class="doc-input" placeholder="Client" v-model="docClient" @keydown.enter="handleEnter('docClient', $event)">
                            
                        </td>
                    </tr>

                </tbody>
            </table>


            <button class="Button" role="button" @click="saveAll"><i class="fas fa-save"></i> Update</button>





            
    </div>

</template>

<script>
import axios from 'axios';
// import VueAxios from 'vue-axios';


export default{
    data(){
        return{
            docTitle: '',
            docNumber: '',
            docStatus: '',
            docIssueDate: '',
            docSecurity: '',
            docAuthors: '',
            docClient: '',
            url: ''
            
        }
    },
    mounted(){
        this.getDocumentDetails();
    },
    methods:{
        async getDocumentDetails(){
            const url = 'http://10.7.1.100:65000/document_details'
            axios.get(url)
            .then(response => {
                console.log(response.data);
                console.log(response.data[0]);
                for(let i = 0; i < response.data.length; i++){
                    console.log(response.data[i].content);
                    console.log(response.data[i].name);
                    if(response.data[i].name.includes('authors')){
                        this.docAuthors = response.data[i].content;
                    }
                    else if(response.data[i].name.includes('client')){
                        this.docClient = response.data[i].content;
                    }
                    else if(response.data[i].name.includes('date')){
                        this.docIssueDate = response.data[i].content;
                    }
                    else if(response.data[i].name.includes('number')){
                        this.docNumber = response.data[i].content;
                    }
                    else if(response.data[i].name.includes('security')){
                        this.docSecurity = response.data[i].content;
                    }
                    else if(response.data[i].name.includes('title')){
                        this.docTitle = response.data[i].content;
                    }
                    else{
                        this.docStatus = response.data[i].content;
                    }
                }
           
            })
        },
        async saveAll() {
            const main_url = 'http://10.7.1.100:65000/document_details/';
            const details = [
                { endpoint: 'documenttitle', content: this.docTitle },
                { endpoint: 'documentclient', content: this.docClient },
                { endpoint: 'documentauthors', content: this.docAuthors },
                { endpoint: 'documentnumber', content: this.docNumber },
                { endpoint: 'documentsecuritystatus', content: this.docSecurity },
                { endpoint: 'documentstatus', content: this.docStatus },
                { endpoint: 'documentissuedate', content: this.docIssueDate }
            ];

            const requests = details.map(detail => {
                const url = `${main_url}${detail.endpoint}`;
                return axios.post(url, { content: detail.content });
            });

            try {
                await Promise.all(requests);
                alert("Document details updated successfully!");
                window.location.reload();
            } catch (error) {
                console.error(error);
                // Handle errors here
            }
        }

        
    }

}


        

</script>

<style>
@import '../assets/documentdetails.css'
</style>