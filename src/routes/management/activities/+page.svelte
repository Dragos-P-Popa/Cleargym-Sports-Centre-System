<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import EditActivity from "../../../components/editActivity.svelte";
  import AddActivity from "../../../components/newActivity.svelte";
  import ActivityCard from "../../../components/activityCardManager.svelte";
  /** @type {import('./$types').PageData} */
  export let data;
  let user = data.user;
  let activities = data.activities;
</script>

<div class="grid grid-cols-12">
  <NavBar active=0 firstName={user.firstName} lastName={user.lastName}/>
  
  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-8">
      <div class="col-span-5">
        <p class="font-bold text-5xl text-[#1A1A1A]">Manage Activities</p>
        <p class="font-light text-2xl text-[#515151]">view and manage activities</p>
        
        <div class="overflow-y-auto h-[80vh]">
          <!--display all activities-->
          <!-- {#each activities as b, i} -->
            <div>
              <!-- <EditActivity /> -->
              <!--activity booking-->
              {#each activities as activity}
                <ActivityCard class="my-3" activityType={activity.activityType} location="Swimming pool" activityDay={activity.activityDay} activityStartTime={activity.activityStartTime} activityEndTime={activity.activityEndTime} activityPrice="10"/>
              {/each}
              <!-- <ActivityCard class="my-3" heading="Test" location="Swimming pool" startTime="12:00" sessionLength="2" activityPrice="10"/> -->
              <!-- <ActivityCard class="my-3" heading="Test" location="Swimming pool" startTime="12:00" sessionLength="2" activityPrice="10"/>
              <ActivityCard class="my-3" heading="Test" location="Swimming pool" startTime="12:00" sessionLength="2" activityPrice="10"/> -->
            </div> 
          <!-- {/each} -->
        </div>
      </div>
      <div class="col-span-3 px-4 mt-20 ml-5">
        <div class="ml-auto">
          <div><AddActivity></AddActivity></div> 
        </div>
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>