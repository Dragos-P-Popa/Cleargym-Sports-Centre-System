<script lang="ts">
  import "@fontsource/manrope";
  import BookingCard from "../../../components/bookingCard.svelte";
  import ClientCard from "../../../components/clientCard.svelte";
  import NavBar from "../../../components/employeeNavbar.svelte";
  import JoinUsButton from "../../../components/joinUsButton.svelte";
  import MainButton from "../../../components/mainButton.svelte";
  import MembershipCard from "../../../components/membershipCard.svelte";
  import SearchEmail from "../../../components/searchEmail.svelte";
  import ViewBooking from "../../../components/viewBooking.svelte";

  export let data;
  let user = data.user;
</script>

<div class="grid grid-cols-12">
  <NavBar active="1" firstName={user.firstName} lastName={user.lastName} />

  <div class="col-span-10 pt-12 px-8">
    <p class="font-bold text-5xl text-[#1A1A1A] w-full pb-10">Amendments</p>
    <SearchEmail />
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
