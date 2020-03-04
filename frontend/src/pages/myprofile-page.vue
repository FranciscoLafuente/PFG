<template>
    <v-container>
        <v-card class="mx-auto" max-width="400">
            <v-img class="white--text align-end" height="200px" src="https://cdn.vuetifyjs.com/images/cards/docks.jpg">
                <v-card-title>{{ title }}</v-card-title>
            </v-img>

            <v-card-subtitle class="pb-0 display-2" > {{ user.name | uppercase }} </v-card-subtitle>

            <v-card-text class="text--primary">
                <div class="mb-2">Email: {{ user.email }}</div>

                <v-expansion-panels focusable>
                <v-expansion-panel v-for="p in user.projects" :key="p.name">
                    <v-expansion-panel-header>{{ p.name | uppercase }}</v-expansion-panel-header>
                    <v-expansion-panel-content>
                        {{ p.scans }}
                    </v-expansion-panel-content>
                </v-expansion-panel>
                </v-expansion-panels>
            </v-card-text>

            <v-card-actions>
                <v-btn color="orange" text>Edit</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script>
import axios from 'axios'

export default {
    data: () => ({
        title: 'My Profile',
        user: {
            name: String,
            email: String,
            projects: []
        },
        nameProjects: []
    }),

    filters: {
        uppercase: function(v) {
            if (!v) return ''
            v = v.toString()
            return v.charAt(0).toUpperCase() + v.slice(1)
        }
    },

    created() {
        this.initialize()
    },

    methods: {
        initialize() {
        let token = this.getToken()

        axios
            .get("http://localhost:5000/myprofile", token)
            .then(r => {                
                this.user = r.data                
                r.data.projects.forEach(e => {
                    this.nameProjects.push(e.name)
                })
            })
            .catch(e => {
            console.log(e.response)
            });
        },

        getToken() {
            let user = localStorage.getItem("token");
            let token = {
            headers: {
                Authorization: "Bearer " + user
            }
            };
            return token;
        },

        getProjects() {
            let p = []
            this.user.projects.forEach( e => {
                p.push(e.name)
            })
            return p
        }
    }
}
</script>