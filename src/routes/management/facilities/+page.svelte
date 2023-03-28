<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import EditFacility from "../../../components/editFacility.svelte";
  import AddFacility from "../../../components/newFacility.svelte";
  import FacilityCard from "../../../components/facilityCardManager.svelte";
  /** @type {import('./$types').PageData} */
  export let data;
  let user = data.user;
  let facilities = data.facilities;

  // // window is undefined when this code is running on the server side.
  // // svelte does some processing on the server side, see svelte docs for more info
  // if (typeof window !== "undefined") {
  //     // if its running on client side, save the user id as a local variable
  //     localStorage.setItem("uid", user._id);
  // }

</script>

<div class="grid grid-cols-12">
  <NavBar active=1 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-8">
      <div class="col-span-5">
        <p class="font-bold text-5xl text-[#1A1A1A]">Manage Facilities</p>
        <p class="font-light text-2xl text-[#515151]">view and manage facilities</p>
        
        <div class="overflow-y-auto h-[80vh]">
          <div>
            <!-- <EditFacility></EditFacility> -->
            {#each facilities as facility}
              <FacilityCard class="my-3" facilityName={facility.facilityName} capacity={facility.capacity} openingTime={facility.openingTime} closingTime={facility.closingTime}/>
            {/each}
          </div> 
        </div>
      </div>
      <div class="col-span-3 px-4 mt-20 ml-5">
        <div class="ml-auto">
          <div><AddFacility></AddFacility></div> 
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