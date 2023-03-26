<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import EditFacility from "../../../components/editFacility.svelte";
  import AddFacility from "../../../components/newFacility.svelte";

  export let data;
  let user = data.user;
</script>

<div class="grid grid-cols-12">
  <NavBar active=1 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-8">
      <div class="col-span-5">
        <p class="font-bold text-5xl text-[#1A1A1A]">Manage Facilities</p>
        <p class="font-light text-2xl text-[#515151]">view and manage facilities</p>

        <!-- Need to move button to the right without just using padding -->
        <div class="w-full pl-96">
          <img class="cursor-pointer pt-4 pl-64" src="../plus.svg" alt="add" id="add" />
        </div>
        
        <div class="overflow-y-auto h-[80vh]">
          <div><EditFacility></EditFacility></div> 
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