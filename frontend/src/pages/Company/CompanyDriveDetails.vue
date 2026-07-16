<template>
  <div class="container py-4">

    <button
      class="btn btn-secondary mb-4"
      @click="$router.back()"
    >
      ← Back
    </button>

    <!-- Drive Details -->

    <div
      v-if="drive"
      class="card mb-4"
    >

      <div class="card-header">
        <h3>{{ drive.job_title }}</h3>
      </div>

      <div class="card-body">

        <p>
          <strong>Description:</strong><br>
          {{ drive.job_description }}
        </p>

        <div class="row">

          <div class="col-md-4">
            <strong>Branch</strong><br>
            {{ drive.eligible_branch }}
          </div>

          <div class="col-md-4">
            <strong>Minimum CGPA</strong><br>
            {{ drive.minimum_cgpa }}
          </div>

          <div class="col-md-4">
            <strong>Eligible Year</strong><br>
            {{ drive.eligible_year }}
          </div>

        </div>

        <hr>

        <strong>Deadline</strong>

        {{ formatDate(drive.deadline) }}

      </div>

    </div>

    <!-- Applications -->

    <h3 class="mb-3">

      Applications

    </h3>

    <div class="table-responsive">

      <table class="table table-hover">

        <thead class="table-dark">

          <tr>

            <th>Student</th>

            <th>Branch</th>

            <th>CGPA</th>

            <th>Applied On</th>

            <th>Status</th>

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

              {{ application.student.branch }}

            </td>

            <td>

              {{ application.student.cgpa }}

            </td>

            <td>

              {{ formatDate(application.date) }}

            </td>

            <td>

              <select
                class="form-select form-select-sm"
                :value="application.status"
                @change="
                  updateStatus(
                    application.id,
                    $event.target.value
                  )
                "
              >

                <option>Applied</option>

                <option>Shortlisted</option>

                <option>Selected</option>

                <option>Rejected</option>

              </select>

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>
</template>

<script>
import api from "@/utils/api";

export default {

    name:"CompanyDriveDetails",

    data(){

        return{

            drive:null,

            applications:[],

            loading:false,

            error:""

        }

    },

    created(){

        this.fetchDrive();

        this.fetchApplications();

    },

    methods:{

        async fetchDrive(){

            const id=this.$route.params.id;

            const res=await api.get(`/drive/${id}`);

            this.drive=res;

        },

        async fetchApplications(){

            const id=this.$route.params.id;

            const res=await api.get("/application");

            this.applications=res.filter(
                application=>application.drive.id==id
            );

        },

        async updateStatus(id,status){

            try{

                await api.patch(
                    `/application/${id}`,
                    {
                        status
                    }
                );

                await this.fetchApplications();

            }

            catch(err){

                alert(err.message);

            }

        },

        formatDate(date){

            return new Date(date).toLocaleDateString();

        }

    }

}
</script>