<template>

<div class="container py-4">

    <!-- Header -->

    <div
        class="d-flex justify-content-between align-items-center mb-4"
    >

        <h2 class="fw-bold">

            Welcome

        </h2>

        <button
            class="btn btn-link text-decoration-none text-danger"
            @click="logout"
        >

            Logout

        </button>

    </div>

    <!-- Loading -->

    <div
        v-if="loading"
        class="text-center py-5"
    >

        <div class="spinner-border text-primary"></div>

    </div>

    <!-- Error -->

    <div
        v-if="error"
        class="alert alert-danger"
    >

        {{ error }}

    </div>

    <!-- Dashboard -->

    <div v-if="!loading">

        <!-- Upcoming Drives -->

        <div class="card shadow-sm mb-4">

            <div
                class="card-header d-flex justify-content-between align-items-center"
            >

                <h5 class="mb-0">

                    Upcoming Drives

                </h5>

                <button
                    class="btn btn-success"
                    @click="$router.push('/company/create_drive')"
                >

                    Create Drive

                </button>

            </div>

            <div class="card-body p-0">

                <table class="table table-hover mb-0">

                    <thead>

                        <tr>

                            <th width="90">

                                Sr No.

                            </th>

                            <th>

                                Drive Name

                            </th>

                            <th width="180">

                                Actions

                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr

                            v-for="(drive,index) in upcomingDrives"

                            :key="drive.id"

                        >

                            <td>

                                {{ index + 1 }}

                            </td>

                            <td>

                                {{ drive.job_title }}

                            </td>

                            <td>

                                <button
                                    class="btn btn-outline-primary btn-sm"
                                    @click="reviewApplications(drive.id)"
                                >

                                    View Details

                                </button>

                            </td>

                        </tr>

                        <tr
                            v-if="upcomingDrives.length==0"
                        >

                            <td
                                colspan="3"
                                class="text-center text-muted py-4"
                            >

                                No upcoming drives.

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>
                <!-- Closed Drives -->

        <div class="card shadow-sm">

            <div class="card-header">

                <h5 class="mb-0">

                    Closed Drives

                </h5>

            </div>

            <div class="card-body p-0">

                <table class="table table-hover mb-0">

                    <thead>

                        <tr>

                            <th width="90">

                                Sr No.

                            </th>

                            <th>

                                Drive Name

                            </th>

                            <th width="180">

                                Actions

                            </th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr

                            v-for="(drive,index) in closedDrives"

                            :key="drive.id"

                        >

                            <td>

                                {{ index + 1 }}

                            </td>

                            <td>

                                {{ drive.job_title }}

                            </td>

                            <td>

                                <button

                                    class="btn btn-outline-secondary btn-sm"

                                    @click="updateDrive(drive.id)"

                                >

                                    Update

                                </button>

                            </td>

                        </tr>

                        <tr
                            v-if="closedDrives.length==0"
                        >

                            <td
                                colspan="3"
                                class="text-center text-muted py-4"
                            >

                                No closed drives.

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

    </div>

</div>

</template>
<script>

import api from "@/utils/api";

export default {

    name: "CompanyDashboard",

    data() {

        return {

            drives: [],

            company_name: "",

            loading: false,

            error: ""

        };

    },

    computed: {

        upcomingDrives() {

            return this.drives.filter(

                drive => drive.status !== "Closed"

            );

        },

        closedDrives() {

            return this.drives.filter(

                drive => drive.status === "Closed"

            );

        }

    },

    async mounted() {

        await this.fetchDrives();

        const user = JSON.parse(

            localStorage.getItem("user")

        );

    },

    methods: {

        async fetchDrives() {

            this.loading = true;

            this.error = "";

            try {

                const res = await api.get("/drive");

                this.drives = res;

            }

            catch(err){

                this.error = err.message;

            }

            finally{

                this.loading = false;

            }

        },

        reviewApplications(id){

    this.$router.push(

        "/company/drive/" +

        id +

        "/applications"

    );

},

        updateDrive(id){

            this.$router.push(

                "/company/drive/" + id + "/edit"

            );

        },

        logout(){

            localStorage.clear();

            this.$router.push("/login");

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

    padding:18px 20px;

}

.table td,

.table th{

    vertical-align:middle;

}

.btn-outline-primary,

.btn-outline-secondary{

    min-width:120px;

}

.btn-link{

    text-decoration:none;

}

.btn-link:hover{

    text-decoration:none;

}

</style>