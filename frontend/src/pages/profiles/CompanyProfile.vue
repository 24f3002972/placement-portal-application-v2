<template>

<div class="container py-4">

    <!-- Header -->

    <div
        class="d-flex justify-content-between align-items-center mb-4"
    >

        <div>

            <h2 class="fw-bold">

                {{ company.company_name }}

            </h2>

        </div>

        <div>

            <button
                class="btn btn-link text-danger"
                @click="logout"
            >
                Logout
            </button>

        </div>

    </div>

    <!-- Overview -->

    <div class="card shadow-sm mb-4">

        <div class="card-header">

            <h4 class="mb-0">

                Overview

            </h4>

        </div>

        <div class="card-body">

            <p>

                {{ company.overview }}

            </p>

            <div class="row mt-4">

                <div class="col-md-4">

                    <strong>Website</strong>

                    <br>

                    {{ company.website }}

                </div>

                <div class="col-md-4">

                    <strong>HR Contact</strong>

                    <br>

                    {{ company.hr_contact }}

                </div>

                <div class="col-md-4">

                    <strong>Status</strong>

                    <br>

                    <span
                        class="badge"
                        :class="company.status=='Active'
                            ? 'bg-success'
                            : 'bg-danger'"
                    >

                        {{ company.status }}

                    </span>

                </div>

            </div>

        </div>

    </div>

    <!-- Drives -->

    <div class="card shadow-sm">

        <div class="card-header">

            <h4 class="mb-0">

                Current Drives

            </h4>

        </div>

        <div class="card-body">

            <div

                v-if="company.drives && company.drives.length"

            >

                <div

                    v-for="drive in company.drives"

                    :key="drive.id"

                    class="border rounded p-3 mb-3 d-flex justify-content-between align-items-center"

                >

                    <div>

                        <h5 class="mb-1">

                            {{ drive.job_title }}

                        </h5>

                        <small>

                            Deadline :
                            {{ drive.deadline }}

                        </small>

                    </div>

                    <button

                        class="btn btn-outline-primary"

                        @click="viewDrive(drive.id)"

                    >

                        View Details

                    </button>

                </div>

            </div>

            <div
                v-else
                class="alert alert-info"
            >

                No active drives.

            </div>

        </div>

    </div>

</div>

</template>

<script>

import api from "@/utils/api";

export default {

    name: "CompanyProfile",

    data() {

        return {

            company: {

                company_name: "",

                overview: "",

                website: "",

                hr_contact: "",

                status: "",

                drives: []

            }

        };

    },

    async mounted() {

        await this.loadCompany();

    },

    methods: {

        async loadCompany() {

            try {

                const res = await api.get(

                    "/company/" +

                    this.$route.params.id +

                    "/summary"

                );
                console.log(res)
                this.company = res;

            }

            catch (err) {

                console.log(err);

                alert("Failed to load company profile.");

            }

        },

        viewDrive(id) {

            this.$router.push("/drive/" + id);

        },

        logout() {

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

/* Cards */

.card{

    border:none;

    border-radius:12px;

    overflow:hidden;

}

.card-header{

    background:#f8f9fa;

    font-weight:600;

    border-bottom:1px solid #ddd;

}

.card-body{

    padding:25px;

}

/* Drive cards */

.border{

    transition:.25s;

}

.border:hover{

    background:#f8f9fa;

    transform:translateY(-2px);

}

/* Buttons */

.btn-outline-primary{

    min-width:140px;

}

/* Header */

h2{

    font-weight:700;

}

.btn-link{

    color:#444;

    text-decoration:none;

}

.btn-link:hover{

    color:#0d6efd;

}

/* Badge */

.badge{

    font-size:14px;

    padding:8px 14px;

}

/* Responsive */

@media(max-width:768px){

    .d-flex{

        flex-direction:column;

        align-items:flex-start !important;

    }

    .btn-outline-primary{

        margin-top:15px;

        width:100%;

    }


}

</style>
