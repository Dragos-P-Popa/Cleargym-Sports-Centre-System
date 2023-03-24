<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/employeeNavbar.svelte";

  export let data;
  let user = data.user;
</script>

<div class="grid grid-cols-12">
  <NavBar active=0 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
    
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>