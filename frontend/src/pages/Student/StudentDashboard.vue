<template>

<div class="container py-4">

    <!-- Header -->

    <div
        class="d-flex justify-content-between align-items-center mb-4"
    >

        <h2 class="fw-bold">

            Welcome {{ studentName }}

        </h2>

        <div>

            <button
                class="btn btn-link text-decoration-none"
                @click="$router.push('student/edit')"
            >
                Edit Profile
            </button>

            |

            <button
                class="btn btn-link text-decoration-none"
                @click="$router.push('student/history')"
            >
                History
            </button>

            |

            <button
                class="btn btn-link text-decoration-none text-danger"
                @click="logout"
            >
                Logout
            </button>

        </div>

    </div>

    <!-- Export Button -->

    <div class="mb-4">

        <button
            class="btn btn-primary"
            @click="exportApplications"
        >

            Export My Applications

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

        <!-- Organizations -->

        <div class="card shadow-sm mb-4">

            <div class="card-header bg-primary text-white">

                <h5 class="mb-0">

                    Organizations

                </h5>

            </div>

            <div class="card-body">

                <div
                    v-if="companies.length==0"
                    class="text-muted"
                >

                    No registered companies.

                </div>

                <div

                    v-for="company in companies"

                    :key="company.id"

                    class="d-flex justify-content-between align-items-center border rounded p-3 mb-3"

                >

                    <div>

                        <strong>

                            {{ company.company_name }}

                        </strong>

                        <br>

                        <small class="text-muted">

                            {{ company.website }}

                        </small>

                    </div>

                    <button

                        class="btn btn-outline-primary"

                        @click="viewCompany(company.id)"

                    >

                        View Details

                    </button>

                </div>

            </div>

        </div>

        <!-- Applied Drives -->

        <div class="card shadow-sm">

            <div class="card-header bg-primary text-white">

                <h5 class="mb-0">

                    Applied Drives

                </h5>

            </div>

            <div class="card-body">

                <div
                    v-if="applications.length==0"
                    class="alert alert-info"
                >

                    You haven't applied for any drives yet.

                </div>

                <table
                    v-else
                    class="table table-bordered align-middle"
                >

                    <thead>

                        <tr>

                            <th width="80">

                                Sr No.

                            </th>

                            <th>

                                Drive Name

                            </th>

                            <th>

                                Company

                            </th>

                            <th>

                                Applied Date

                            </th>

                            <th width="160">

                                Action

                            </th>

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

                                {{ application.drive.job_title }}

                            </td>

                            <td>

                                {{ application.drive.company_name }}

                            </td>

                            <td>

                                {{ formatDate(application.date) }}

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

</div>

</template>

<script>
import api from "@/utils/api";

export default {

    name: "StudentDashboard",

    data() {

        return {

            companies: [],

            applications: [],

            loading: false,

            error: "",

            studentName: ""

        };

    },

    created() {

        this.loadDashboard();

    },

    methods: {

        async loadDashboard() {

            this.loading = true;

            this.error = "";

            try {

                await Promise.all([

                    this.fetchCompanies(),

                    this.fetchApplications()

                ]);

                this.loadStudentName();

            }

            catch (err) {

                this.error = err.message || "Failed to load dashboard.";

            }

            finally {

                this.loading = false;

            }

        },

        async fetchCompanies() {

            try {

                const res = await api.get("/company");

                this.companies = res;

            }

            catch (err) {

                console.log(err);

            }

        },

        async fetchApplications() {

            try {

                const res = await api.get("/application");

                this.applications = res;

            }

            catch (err) {

                console.log(err);

            }

        },

        loadStudentName() {

            const user = JSON.parse(

                localStorage.getItem("user")

            );

            if (user) {

                this.studentName = user.name;

            }

        },

        async exportApplications() {

            try {

                const res = await api.post(

                    "/application/export"
                );

                alert(res.message);

            }

            catch (err) {

                alert(

                    err.message ||

                    "Export failed."

                );

            }

        },

        viewCompany(id) {

            this.$router.push(

                "/company/" + id

            );

        },

        viewDrive(id) {

            this.$router.push(

                "/drive/" + id

            );

        },

        formatDate(date) {

            return new Date(date)

                .toLocaleDateString();

        },

        logout() {

            localStorage.clear();

            this.$router.push("/login");

        }

    }

};
</script>

<style scoped>

/* Page */

.container{

    max-width:1100px;

}

/* Cards */

.card{

    border:none;

    border-radius:12px;

    overflow:hidden;

}

.card-header{

    font-weight:600;

    font-size:18px;

    padding:15px 20px;

}

.card-body{

    padding:20px;

}

/* Company List */

.border{

    transition:.25s;

}

.border:hover{

    background:#f8f9fa;

    transform:translateY(-2px);

}

/* Buttons */

.btn{

    border-radius:8px;

}

.btn-outline-primary{

    min-width:130px;

}

/* Table */

.table{

    margin-bottom:0;

}

.table th{

    background:#f8f9fa;

    font-weight:600;

    text-align:center;

}

.table td{

    vertical-align:middle;

}

/* Header */

h2{

    font-weight:700;

}

/* Top links */

.btn-link{

    color:#444;

    font-weight:500;

}

.btn-link:hover{

    color:#0d6efd;

    text-decoration:none;

}

/* Loading */

.spinner-border{

    width:3rem;

    height:3rem;

}

/* Mobile */

@media(max-width:768px){

    .d-flex{

        flex-direction:column;

        align-items:flex-start !important;

    }

    .btn-outline-primary{

        margin-top:10px;

        width:100%;

    }

}

</style>