<script lang="ts">
  import "@fontsource/manrope";
  import BookingTypeToggle from "../../../components/bookingTypeToggle.svelte";
  import EmployeeBooking from "../../../components/employeeBooking.svelte";
  import NavBar from "../../../components/employeeNavbar.svelte";

  export let data;
  let user = data.user;
  let selection = 1;
</script>

<div class="grid grid-cols-12">
  <NavBar active="0" firstName={user.firstName} lastName={user.lastName} />

  <div class="col-span-10 pt-12 px-8">
    <p class="font-bold text-5xl text-[#1A1A1A] w-full pb-10">
      Create a Booking
    </p>
    <div class="flex flex-col">
      <BookingTypeToggle bind:selection />
      {#if selection == 1}
        <EmployeeBooking />
      {:else}
        <p>selection 2</p>
      {/if}
    </div>
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
