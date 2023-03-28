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
    <!--  <div class="w-5/6">
        <label for="customerEmail">Customer Email</label>
        <input
          class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-ful w-full"
          type="text"
          id="customerEmail"
          name="customerEmail"
        />
      </div>
      <div>
        <JoinUsButton class="items-end m-5 w-3/4 mt-7 h-10">Search</JoinUsButton
        >
      </div> -->
    <!--     <div class="flex flex-row w-full mb-10">
      <ClientCard class="w-5/6" />
      <div class="flex flex-col">
        <MainButton class="m-8 w-5/6">Bookings</MainButton>
        <MainButton class="m-8 w-5/6">Membership</MainButton>
      </div>
    </div> -->

    <!--     <div class="flex flex-row">
      <div class="flex flex-col w-1/2 px-1">
        <BookingCard class="w-4/5" />
        <BookingCard class="w-4/5" />
        <BookingCard class="w-4/5" />
      </div>
      <div class="flex-1 w-1/2 items-start">
        <ViewBooking class="w-4/5" />
      </div>
    </div> -->
    <!--  <MembershipCard
      active="1"
      heading="No membership"
      subHeading="Pay as you go"
      bulletPoints={[
        "Most flexible option.",
        "Pay whenever you want to book.",
        "Perfect for newcomers who are looking to try out before committing to a membership.",
      ]}
      class="col-span-4"
    />
    <MembershipCard
      active="0"
      heading="Cleargym One"
      subHeading="All-inclusive membership"
      bulletPoints={[
        "Highest cost savings.",
        "Unlimited access to all of our facilities.",
        "One simple monthly payment.",
        "Cancel at any time.",
      ]}
      class="col-span-4"
    /> -->
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>
