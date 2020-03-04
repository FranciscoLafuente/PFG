<template>
    <v-container>
        <Search class="bar-search"></Search>
        <div>
            <div>
                <v-btn class="folder-button" color="primary" dark fab @click="sendToken">
                    <v-icon>folder_open</v-icon>
                </v-btn>
                <v-dialog v-model="showModal" max-width="290">
                    <v-card>
                        <v-card-title class="headline">Unregistered User</v-card-title>
                        <v-card-text>You need to be registered for to access your owns projects.</v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="showModal = false">Close</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </div>
        </div>
    </v-container>
</template>

<script>
import axios from "axios";
import Search from "../components/search-component";

export default {
    components: {
        Search,
    },
    data () {
        return {
            showModal: false,
        }
    },
    methods: {
    sendToken(evt) {
        evt.preventDefault();
        let user = localStorage.getItem('token');
        let token = {
          'headers': {
            'Authorization': 'Bearer ' + user
        }};
         
        axios.get("http://localhost:5000/myproject", token)
        .then(r => {
            if (r.status == 200) {
                this.$router.push("/myproject");
                return;
            }
        }).catch(e => {
            console.log(e.response);
            this.showModal = true;
        });
    }
  }
}
</script>

<style scoped>
.container {
    height: 100%;
    width: 60%;
    justify-content: center;
    display: flex;
    align-items: center;
}
.folder-button {
    bottom: 15%;
    right: 10%;
    position: absolute;
}

.v-btn--icon.v-size--default .v-icon, .v-btn--fab.v-size--default .v-icon {
    font-size: 40px;
}
</style>