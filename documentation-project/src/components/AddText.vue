<template>
    <div class="add-text">
        <div class="add-text-title">
            <h3>Add Text</h3>
        </div>
        
        <div class="add-text-buttons-section">
            <button :class="{ 'add-text-buttons': true, 'active': h2style }" @click="selectH2style">
                <i class="fas fa-heading">2</i>
            </button>
            <button :class="{ 'add-text-buttons': true, 'active': h3style }" @click="selectH3style">
                <i class="fas fa-heading">3</i>
            </button>
            <button :class="{ 'add-text-buttons': true, 'active': pstyle }" @click="selectPstyle">
                <i class="fas fa-paragraph"></i>
            </button>
            <button :class="{ 'add-text-buttons': true, 'active': bstyle }" @click="selectBstyle">
                <i class="fas fa-bold"></i>
            </button>
            <button :class="{ 'add-text-buttons': true, 'active': codestyle }" @click="selectCodeBlock">
                <i class="fas fa-code"></i>
            </button>
        </div>

        <div class="add-text-input">
            <!-- <label for="text">Text:</label> -->
            <textarea class="add-text-textbox" v-model="text" required></textarea>
            <br>
            <button class="add-text-buttons" type="submit" @click="saveText"><i class="fas fa-save"></i></button>
            <button class="add-text-buttons" type="submit" @click="cancelModify"><i class="fas fa-times"></i></button>
        </div>
            
    </div>  
        
        
    

</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            text: "",
            h2style: false,
            h3style: false,
            pstyle: false,
            bstyle: false,
            codeBlock: false,
            finalStyle: "",
        }
    },
    computed: {
      sectionNumber() {
        return this.$store.getters.sectionNumber;
      },
    },
    methods:{

        selectH2style() {
            this.h2style = true;
            this.h3style = false;
            this.pstyle = false;
            this.bstyle = false;
            this.codestyle = false;
        },
        selectH3style() {
            this.h2style = false;
            this.h3style = true;
            this.pstyle = false;
            this.bstyle = false;
            this.codestyle = false;
        },
        selectPstyle() {
            this.h2style = false;
            this.h3style = false;
            this.pstyle = true;
            this.bstyle = false;
            this.codestyle = false;
        },
        selectBstyle() {
            this.h2style = false;
            this.h3style = false;
            this.pstyle = false;
            this.bstyle = true;
            this.codestyle = false;
        },
        selectCodeBlock() {
            this.h2style = false;
            this.h3style = false;
            this.pstyle = false;
            this.bstyle = false;
            this.codestyle = true;
        },


        saveText() {
            if (this.h2style) {
                this.finalStyle = "Heading 2";
                console.log(this.finalStyle);
            }
            else if (this.h3style) {
                this.finalStyle = "Heading 3";
                console.log(this.finalStyle);
            }
            else if (this.pstyle) {
                this.finalStyle = "Normal";
                console.log(this.finalStyle);
            }
            else if (this.bstyle) {
                this.finalStyle = "Bold";
                console.log(this.finalStyle);
            }
            else if (this.codestyle) {
                this.finalStyle = "Code Standalone";
                console.log(this.finalStyle);
            }
            else {
                this.finalStyle = "Normal";
                console.log(this.finalStyle);
            } 
            
            if(this.text == ""){
                alert("Please enter text");
                return;
            }
            else{
                const url = 'http://192.168.4.31:9876/save_text/' + this.sectionNumber;
                
                axios.post(url, { text: this.text, style: this.finalStyle })
                    .then(response => {
                        console.log(response.data);
                    })
                    .catch(error => {
                        console.error(error);
                    });
                // Reload
                window.location.reload();
            }            
        },

        cancelModify() {
            //Reload page 
            window.location.reload();
        },


    }
}



</script>

<style>
@import '../assets/addtext.css'




</style>
