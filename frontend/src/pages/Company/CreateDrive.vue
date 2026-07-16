<template>
  <div class="container py-4">

    <h2 class="mb-4">Create Placement Drive</h2>

    <form @submit.prevent="createDrive">

      <div class="mb-3">
        <label class="form-label">Job Title</label>
        <input
          v-model="drive.job_title"
          class="form-control"
          required
        >
      </div>

      <div class="mb-3">
        <label class="form-label">Job Description</label>
        <textarea
          v-model="drive.job_description"
          rows="4"
          class="form-control"
        ></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Eligible Branch</label>
        <select
          v-model="drive.eligible_branch"
          class="form-select"
        >
          <option>CSE</option>
          <option>ECE</option>
          <option>EEE</option>
          <option>ME</option>
          <option>CE</option>
        </select>
      </div>

      <div class="row">

        <div class="col-md-4">

          <label class="form-label">
            Minimum CGPA
          </label>

          <input
            type="number"
            step="0.01"
            v-model="drive.minimum_cgpa"
            class="form-control"
          >

        </div>

        <div class="col-md-4">

          <label class="form-label">
            Eligible Year
          </label>

          <select
            v-model="drive.eligible_year"
            class="form-select"
          >
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
          </select>

        </div>

        <div class="col-md-4">

          <label class="form-label">
            Deadline
          </label>

          <input
            type="datetime-local"
            v-model="drive.deadline"
            class="form-control"
          >

        </div>

      </div>

      <button
        class="btn btn-primary mt-4"
      >
        Create Drive
      </button>

    </form>

  </div>
</template>

<script>
import api from "@/utils/api";

export default {

    name:"CreateDrive",

    data(){

        return{

            drive:{

                job_title:"",
                job_description:"",
                eligible_branch:"",
                minimum_cgpa:null,
                eligible_year:null,
                deadline:""

            }

        }

    },

    methods: {

    async createDrive() {

        const payload = {
            ...this.drive,
            deadline: this.drive.deadline.replace("T", " ") + ":00"
        };

        try {

            await api.post("/drive", payload);

            alert("Drive created.");

            this.$router.push("/company");

        }
        catch (err) {

            alert(err.message);

        }

      }

    }

}
</script>