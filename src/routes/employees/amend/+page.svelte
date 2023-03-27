<script lang="ts">
  import "@fontsource/manrope";
  import BookingCard from "../../../components/bookingCard.svelte";
  import ClientCard from "../../../components/clientCard.svelte";
  import NavBar from "../../../components/employeeNavbar.svelte";
  import JoinUsButton from "../../../components/joinUsButton.svelte";
  import MainButton from "../../../components/mainButton.svelte";
  import ViewBooking from "../../../components/viewBooking.svelte";

  export let data;
  let user = data.user;
</script>

<div class="grid grid-cols-12">
  <NavBar active="1" firstName={user.firstName} lastName={user.lastName} />

  <div class="col-span-10 pt-12 px-8">
    <p class="font-bold text-5xl text-[#1A1A1A] w-full pb-10">Amendments</p>
    <div class="flex flex-row pb-10">
      <div class="w-5/6">
        <label for="customerEmail">Customer Email</label>
        <input
          class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-ful w-full"
          type="text"
          id="email"
        />
      </div>
      <div>
        <JoinUsButton class="items-end m-5 w-3/4 mt-7 h-10">Search</JoinUsButton
        >
      </div>
    </div>
    <div class="flex flex-row w-full mb-10">
      <ClientCard class="w-5/6" />
      <div class="flex flex-col">
        <MainButton class="m-8 w-5/6">Bookings</MainButton>
        <MainButton class="m-8 w-5/6">Membership</MainButton>
      </div>
    </div>
    <div class="flex flex-row">
      <div class="flex flex-col w-1/2 px-1">
        <BookingCard class="w-4/5" />
        <BookingCard class="w-4/5" />
        <BookingCard class="w-4/5" />
      </div>
      <div class="flex-1 w-1/2 items-start">
        <ViewBooking class="w-4/5" />
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
