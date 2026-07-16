<template>

<div class="container py-4">

    <div class="card shadow-sm">

        <div class="card-header">

            <h3>

                Update Applications for the Drive

            </h3>

            <h5 class="text-muted">

                {{ driveTitle }}

            </h5>

        </div>

        <div class="card-body">

            <table class="table table-hover">

                <thead>

                    <tr>

                        <th>

                            Student

                        </th>

                        <th width="180">

                            Action

                        </th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="application in applications"

                        :key="application.id"

                    >

                        <td>

                            {{ application.student.user.name }}

                        </td>

                        <td>

                            <button

                                class="btn btn-primary btn-sm"

                                @click="review(application.id)"

                            >

                                Review Application

                            </button>

                        </td>

                    </tr>

                </tbody>

            </table>

        </div>

    </div>

</div>

</template>
<script>

import api from "@/utils/api";

export default{

    name:"DriveApplications",

    data(){

        return{

            applications:[],

            driveTitle:""

        }

    },

    async mounted(){

        await this.loadApplications();

    },

    methods:{

        async loadApplications(){

            const res = await api.get(

                "/drive/" +

                this.$route.params.id +

                "/applications"

            );

            this.applications = res;

            if(res.length){

                this.driveTitle =

                    res[0].drive.job_title;

            }

        },

        review(id){

            this.$router.push(

                "/application/" + id

            );

        }

    }

}

</script>
<style scoped>

.container{

    max-width:900px;

}

.card{

    border:none;

    border-radius:12px;

}

.card-header{

    background:#f8f9fa;

}

.table td,

.table th{

    vertical-align:middle;

}

</style>