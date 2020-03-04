<template>
    <div>
        <button type="summit" @click="onSubmit">Pulse aqui</button>
    </div>
</template>

<script>
import axios from "axios";

export default {
    methods: {
        onSubmit(evt) {
            evt.preventDefault();
            let user = localStorage.getItem('token');
            let token = { 
                'headers': { 
                    'Authorization': 'Bearer ' + user 
                }};

            axios.get("http://localhost:5000/bots", token).then(r => {
                console.log(r);
            });
        }
    }
};
</script>