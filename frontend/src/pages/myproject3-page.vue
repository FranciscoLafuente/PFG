<template>
    <v-container>
        <v-data-table
            :headers="headers"
            :items="projects"
            :items-per-page="5"
            class="elevation-1"
        ></v-data-table>
        <div class="folder-button">
                <router-link to="/myproject/scans">
                    <v-btn color="blue darken-1" dark fab>
                        <v-icon>add</v-icon>
                    </v-btn>
                </router-link>
            </div>
    </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data () {
    return {
      headers: [
        {
          text: 'Project Name',
          align: 'left',
          sortable: false,
          value: 'name',
        },
        { text: 'Scans', value: 'scans' },
        { text: 'Type', value: 'type' },
        //{ text: 'Bots', value: 'fat' },
        //{ text: 'Date', value: 'carbs' },
        //{ text: 'Description', value: 'protein' },
      ],
      projects: [],
    }
  },
      created() {
      this.getProjects();
  },
  methods: {
      getProjects() {
        let user = localStorage.getItem('token');
        let token = {
          'headers': {
            'Authorization': 'Bearer ' + user
          }};

          axios.get("http://localhost:5000/myproject", token)
            .then(r => {               
              r.data.forEach(res => {
                this.projects.push(res);
              });
          })
          .catch(e => {
            console.log(e.response);
          });
      },
      addProject() {
        
      }
  }
}
</script>

<style scoped>
.container {
    height: 90%;
    width: 80%;
    justify-content: center;
    display: flex;
    align-items: center;
}

.v-application .elevation-1 {
  width: inherit;
}

.folder-button {
    bottom: 15%;
    right: 10%;
    position: absolute;
}

.v-btn--icon.v-size--default .v-icon, .v-btn--fab.v-size--default .v-icon {
    font-size: 40px;
}

a {
  text-decoration: none;
}
</style>