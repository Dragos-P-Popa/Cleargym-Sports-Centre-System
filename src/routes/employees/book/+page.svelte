<script lang="ts">
  import "@fontsource/manrope";
  import EmployeeBooking from "../../../components/employeeBooking.svelte";
  import NavBar from "../../../components/employeeNavbar.svelte";
  import QuickBooking from "../../../components/quickBooking.svelte";

  export let data;
  let user = data.user;
</script>

<div class="grid grid-cols-12">
  <NavBar active="0" firstName={user.firstName} lastName={user.lastName} />

  <div class="col-span-10 pt-12 px-8">
    <p class="font-bold text-5xl text-[#1A1A1A] w-full pb-10">
      Create a Booking
    </p>
    <EmployeeBooking />
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
