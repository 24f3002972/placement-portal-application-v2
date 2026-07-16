<template>

<div class="container py-4">

    <div class="card shadow-sm">

        <div class="card-header">

            <h3>Edit Profile</h3>

        </div>

        <div class="card-body">

            <form @submit.prevent="saveProfile">

                <!-- Name -->

                <div class="mb-3">

                    <label>Name</label>

                    <input
                        v-model="user.name"
                        class="form-control"
                    >

                </div>

                <!-- Email -->

                <div class="mb-3">

                    <label>Email</label>

                    <input
                        v-model="user.email"
                        class="form-control"
                    >

                </div>

                <!-- Branch -->

                <div class="mb-3">

                    <label>Branch</label>

                    <input
                        v-model="student.branch"
                        class="form-control"
                    >

                </div>

                <!-- CGPA -->

                <div class="mb-3">

                    <label>CGPA</label>

                    <input
                        type="number"
                        step="0.01"
                        v-model="student.cgpa"
                        class="form-control"
                    >

                </div>

                <!-- Year -->

                <div class="mb-3">

                    <label>Year</label>

                    <input
                        type="number"
                        v-model="student.year"
                        class="form-control"
                    >

                </div>

                <hr>

                <h5>

                    Change Password (Optional)

                </h5>

                <div class="mb-3">

                    <label>New Password</label>

                    <input
                        type="password"
                        v-model="password"
                        class="form-control"
                    >

                </div>

                <div class="mb-4">

                    <label>Confirm Password</label>

                    <input
                        type="password"
                        v-model="confirmPassword"
                        class="form-control"
                    >

                </div>

                <button
                    class="btn btn-primary me-2"
                >

                    Save Changes

                </button>

                <button
                    type="button"
                    class="btn btn-secondary"
                    @click="$router.back()"
                >

                    Cancel

                </button>

            </form>

        </div>

    </div>

</div>

</template>
<script>

import api from "@/utils/api";

export default{

    name:"EditProfile",

    data(){

        return{

            user:{},

            student:{},

            password:"",

            confirmPassword:""

        }

    },

    async mounted(){

        await this.loadProfile();

    },

    methods:{

        async loadProfile(){

            const currentUser = JSON.parse(

                localStorage.getItem("user")

            );

            this.user = await api.get(

                "/user/" + currentUser.id

            );

            this.student = await api.get(

                "/student/" + currentUser.id

            );

        },

        async saveProfile(){
            console.log("saveprofile called")
            if(this.password !== this.confirmPassword){

                alert("Passwords do not match.");

                return;

            }

            await api.put(

                "/user/" + this.user.id,

                {

                    name: this.user.name,

                    email: this.user.email,

                    password: this.password

                }

            );

            await api.put(

                "/student/" + this.student.id,

                {

                    branch: this.student.branch,

                    cgpa: this.student.cgpa,

                    year: this.student.year

                }

            );

    // Update localStorage
        const currentUser = JSON.parse(

            localStorage.getItem("user")

        );

        currentUser.name = this.user.name;

        currentUser.email = this.user.email;

        localStorage.setItem(

            "user",

            JSON.stringify(currentUser)

        );

        alert("Profile updated successfully.");

        this.$router.push("/student");

    }

    }

}

</script>
<style scoped>

.container{

    max-width:700px;

}

.card{

    border:none;

    border-radius:12px;

}

.card-header{

    background:#f8f9fa;

}

</style>
