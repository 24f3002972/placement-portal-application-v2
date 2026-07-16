<template>

<div class="mb-3">

    <input
        v-model="search"
        @input="searchData"
        class="form-control"
        placeholder="Search company, student or drive..."
    >

</div>

</template>

<script>

import api from "@/utils/api";

export default{

    data(){

        return{

            search:""

        }

    },

    methods:{

        async searchData(){

            if(this.search.trim()=="")
                return;

            const res = await api.get(

                "/search?q=" + this.search

            );

            console.log(res.data);

        }

    }

}

</script>