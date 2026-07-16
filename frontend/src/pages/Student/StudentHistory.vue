<template>

<div class="container py-4">

    <!-- Header -->

    <div
        class="d-flex justify-content-between align-items-center mb-4"
    >

        <div>

            <h2 class="fw-bold">

                Student Application History

            </h2>

            <h5 class="text-muted">

                {{ studentName }}

            </h5>

            <small>

                {{ studentBranch }}

            </small>

        </div>

        <button
            class="btn btn-outline-secondary"
            @click="$router.back()"
        >

            Back

        </button>

    </div>

    <!-- Loading -->

    <div
        v-if="loading"
        class="text-center py-5"
    >

        <div class="spinner-border text-primary"></div>

    </div>

    <!-- Table -->

    <div
        v-else
        class="card shadow-sm"
    >

        <div class="card-header">

            <h5 class="mb-0">

                Application History

            </h5>

        </div>

        <div class="card-body p-0">

            <table class="table table-hover mb-0">

                <thead>

                    <tr>

                        <th>Sr No.</th>

                        <th>Company</th>

                        <th>Job Title</th>

                        <th>Applied On</th>

                        <th>Status</th>

                        <th></th>

                    </tr>

                </thead>

                <tbody>

                    <tr

                        v-for="(application,index) in applications"

                        :key="application.id"

                    >

                        <td>

                            {{ index+1 }}

                        </td>

                        <td>

                            {{ application.drive.company_name }}

                        </td>

                        <td>

                            {{ application.drive.job_title }}

                        </td>

                        <td>

                            {{ formatDate(application.date) }}

                        </td>

                        <td>

                            <span

                                class="badge"

                                :class="statusClass(application.status)"

                            >

                                {{ application.status }}

                            </span>

                        </td>

                        <td>

                            <button

                                class="btn btn-outline-primary btn-sm"

                                @click="viewDrive(application.drive.id)"

                            >

                                View Details

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

    name:"StudentHistory",

    data(){

        return{

            applications:[],

            loading:false,

            studentName:"",

            studentBranch:""

        }

    },

    async mounted(){

        await this.loadHistory();

    },

    methods:{

        async loadHistory(){

            this.loading = true;

            try{

                const res = await api.get("/application");

                this.applications = res;

                if(res.length){

                    const user = JSON.parse(

                        localStorage.getItem("user")

                    );

                    this.studentName = user.name;

                }

                const student = await api.get("/student");

                this.studentBranch = student.branch;

            }

            catch(err){

                console.log(err);

            }

            finally{

                this.loading = false;

            }

        },

        viewDrive(id){

            this.$router.push("/drive/" + id);

        },

        formatDate(date){

            return new Date(date)

            .toLocaleDateString();

        },

        statusClass(status){

            switch(status){

                case "Applied":

                    return "bg-primary";

                case "Shortlisted":

                    return "bg-warning text-dark";

                case "Selected":

                    return "bg-success";

                case "Rejected":

                    return "bg-danger";

                default:

                    return "bg-secondary";

            }

        }

    }

}

</script>

<style scoped>

.container{

    max-width:1000px;

}

.card{

    border:none;

    border-radius:12px;

    overflow:hidden;

}

.card-header{

    background:#f8f9fa;

    border-bottom:1px solid #ddd;

}

.badge{

    padding:8px 14px;

    font-size:13px;

}

.table td,

.table th{

    vertical-align:middle;

}

</style>