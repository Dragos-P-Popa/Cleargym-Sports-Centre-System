<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import EditActivity from "../../../components/editActivity.svelte";
  import AddActivity from "../../../components/newActivity.svelte";

  export let data;
  let user = data.user;
</script>

<div class="grid grid-cols-12">
  <NavBar active=0 firstName={user.firstName} lastName={user.lastName}/>
  
  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-8">
      <div class="col-span-5">
        <p class="font-bold text-5xl text-[#1A1A1A]">Manage Activities</p>
        <p class="font-light text-2xl text-[#515151]">view and manage activities</p>

        <!-- Need to move button to the right without just using padding -->
        <div class="w-full pl-96">
          <img class="cursor-pointer pt-4 pl-64" src="../plus.svg" alt="add" id="add" />
        </div>
        
        
        <div class="overflow-y-auto h-[80vh]">
          <div><EditActivity></EditActivity></div> 
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