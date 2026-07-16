<template>
    <div

    v-if="application.student && application.drive"

    class="container py-4"

>

    <div class="card shadow-sm">

        <div class="card-header">

            <h3>

                Student Application

            </h3>

        </div>

        <div class="card-body">

            <div class="row">

                <!-- Left Side -->

                <div class="col-md-8">

                    <p>

                        <strong>

                            Student Name :

                        </strong>

                        {{ application.student.user.name }}

                    </p>

                    <p>

                        <strong>

                            Department :

                        </strong>

                        {{ application.student.branch }}

                    </p>

                    <p>

                        <strong>

                            Drive :

                        </strong>

                        {{ application.drive.company_name }}

                    </p>

                    <p>

                        <strong>

                            Job Title :

                        </strong>

                        {{ application.drive.job_title }}

                    </p>

                    <div
                        v-if="isCompany"
                        class="mt-4"
                    >

                        <label class="form-label">

                            Application Status

                        </label>

                        <select
                            v-model="status"
                            class="form-select"
                        >

                            <option>

                                Applied

                            </option>

                            <option>

                                Shortlisted

                            </option>

                            <option>

                                Selected

                            </option>

                            <option>

                                Rejected

                            </option>

                        </select>

                    </div>

                    <div
                        v-else
                        class="mt-4"
                    >

                        <strong>

                            Status :

                        </strong>

                        {{ application.status }}

                    </div>

                </div>

                <!-- Right Side -->

                <div class="col-md-4 text-center">

                    <img

                        src="https://cdn-icons-png.flaticon.com/512/3135/3135755.png"

                        class="img-fluid"

                        style="max-width:180px"

                    >

                </div>

            </div>

            <hr>

            <div class="d-flex justify-content-end">

                <button

                    v-if="isCompany"

                    class="btn btn-success me-2"

                    @click="saveStatus"

                >

                    Save

                </button>

                <button

                    class="btn btn-secondary"

                    @click="$router.back()"

                >

                    Back

                </button>

            </div>

        </div>

    </div>

</div>

</template>
<script>

import api from "@/utils/api";

export default{

    name:"ApplicationReview",

    data(){

        return{
application:{

    student:{

        user:{}

    },

    drive:{}

},

            status:"",

            isCompany:false

        }

    },

    async mounted(){

        await this.loadApplication();

    },

    methods:{

        async loadApplication(){

            try{

                const res = await api.get(

                    "/application/" +

                    this.$route.params.id

                );

                this.application = res;

                this.status = res.status;

                const user = JSON.parse(

                    localStorage.getItem("user")

                );

                this.isCompany =

                    user.role === "company";

            }

            catch(err){

                alert(err.message);

            }

        },

        async saveStatus(){

            try{

                await api.patch(

                    "/application/" +

                    this.application.id,

                    {

                        status:this.status

                    }

                );

                alert(

                    "Application updated successfully."

                );

                this.$router.back();

            }

            catch(err){

                alert(err.message);

            }

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

    padding:18px 24px;

}

.card-body{

    padding:30px;

}

p{

    font-size:17px;

    margin-bottom:18px;

}

strong{

    display:inline-block;

    width:150px;

}

.form-select{

    max-width:280px;

}

img{

    border-radius:50%;

    border:2px solid #ddd;

    padding:10px;

    background:white;

}

.btn{

    min-width:110px;

}

@media(max-width:768px){

    .col-md-4{

        margin-top:30px;

    }

    strong{

        width:120px;

    }

}

</style>
