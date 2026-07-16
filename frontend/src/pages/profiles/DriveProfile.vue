<template>

<div
    class="container py-4"
    v-if="drive.job_title"
>

    <!-- Header -->

    <div class="mb-4">

        <h2 class="fw-bold">

            {{ drive.job_title }}

        </h2>

        <h5 class="text-muted">

            {{ drive.company_name }}

        </h5>

    </div>

    <!-- Drive Details -->

    <div class="card shadow-sm">

        <div class="card-header">

            <h4 class="mb-0">

                Drive Details

            </h4>

        </div>

        <div class="card-body">

            <div class="mb-4">

                <h5>Description</h5>

                <p>

                    {{ drive.job_description }}

                </p>

            </div>

            <div class="row gy-4">

                <div class="col-md-6">

                    <strong>Eligible Branch</strong>

                    <p>{{ drive.eligible_branch }}</p>

                </div>

                <div class="col-md-6">

                    <strong>Eligible Year</strong>

                    <p>{{ drive.eligible_year }}</p>

                </div>

                <div class="col-md-6">

                    <strong>Minimum CGPA</strong>

                    <p>{{ drive.minimum_cgpa }}</p>

                </div>

                <div class="col-md-6">

                    <strong>Deadline</strong>

                    <p>{{ drive.deadline }}</p>

                </div>

                <div class="col-md-6">

                    <strong>Status</strong>

                    <span
                        class="badge"
                        :class="drive.status=='Approved'
                            ? 'bg-success'
                            : 'bg-secondary'"
                    >

                        {{ drive.status }}

                    </span>

                </div>

            </div>

        </div>

    </div>

    <!-- Buttons -->

    <div class="mt-4 d-flex gap-3">

        <button

            v-if="isStudent"

            class="btn btn-success"
            :class="applied ? 'btn-secondary' : 'btn-success'"
            :disabled="applied"
            @click="apply"

        >

            {{ applied ? "Applied" : "Apply" }}

        </button>

        <button

            class="btn btn-outline-secondary"

            @click="goBack"

        >

            Go Back

        </button>

    </div>

</div>

</template>

<script>

import api from "@/utils/api";

export default{

    name:"DriveProfile",

    data(){

        return{

            drive:{

                id:null,

                job_title:"",

                company_name:"",

                job_description:"",

                eligible_branch:"",

                eligible_year:null,

                minimum_cgpa:null,

                deadline:"",

                status:""

            },
            applied: false,
            user: JSON.parse(

                localStorage.getItem("user")

            )

        }

    },

    computed:{

        isStudent(){

            return this.user &&
                   this.user.role==="student";

        }

    },

    async mounted(){

        await this.loadDrive();
        await this.checkApplication();

    },

    methods:{

        async loadDrive(){

            try{

                const res = await api.get(

                    "/drive/" +

                    this.$route.params.id +

                    "/summary"

                );

                this.drive = res;

            }

            catch(err){

                console.log(err);

            }

        },

        async apply(){

            try{

                await api.post(
                    "/application",
                {
                    drive_id: this.drive.id
                }
            );
            this.applied = true;
            alert("Application submitted successfully!");

            this.$router.push("/student");

        }

        catch(err){
 
            alert(err.message);

        }

        },
        async checkApplication(){

            try{

                const applications = await api.get("/application");

                this.applied = applications.some(application =>

                application.drive.id === this.drive.id

                );

            }

            catch(err){

                console.log(err);

            }

        },

        goBack(){

            this.$router.back();

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

    overflow:hidden;

}

.card-header{

    background:#f8f9fa;

    border-bottom:1px solid #ddd;

}

.card-body{

    padding:30px;

}

.badge{

    font-size:14px;

    padding:8px 14px;

}

.btn{

    min-width:140px;

}

@media(max-width:768px){

    .d-flex{

        flex-direction:column;

    }

    .btn{

        width:100%;

    }

}

</style>