<script >
  import "@fontsource/manrope";
  import NavBar from "../../components/navbar.svelte"
  import BookingCard from "../../components/bookingCard.svelte"
  import { UserID, UserEmail } from '../../stores/user'
  export let data;

  // data fetched from server-side-rendering (SSR)
  // +page.server.ts
  let bookings = data.bookings;

  // Hooks (line 8 - 20) not working
  let userEmail;
  let userId;

  UserID.subscribe(UserID => {
    userId = UserID;
  });

  UserEmail.subscribe(UserEmail => {
    userEmail = UserEmail
  })

  console.log(userEmail)
</script>

<div class="grid grid-cols-12">
  <NavBar active=1/>

  <div class="col-span-10 pt-12 px-8">
      <div class="grid grid-cols-6">
          <div class="col-span-2">
            <p class="font-bold text-5xl text-[#1A1A1A]">Your bookings...</p>
            <p class="font-light text-2xl ml-2 text-[#515151]">view and manage your bookings</p>
            
            
            <div class="mt-16">
              {#each bookings as b}
                <BookingCard class="my-2" heading={bookings[0].bookingType} subheading={bookings[0].bookingTime}/>
              {/each}
            </div>
          
          </div>
          <div class="col-span-4 pt-16 px-4">

          </div>
      </div>
   </div>
</div>


<style lang="postcss">
  :global(body) {
      font-family:"Manrope",
  }
</style>