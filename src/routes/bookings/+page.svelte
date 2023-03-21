<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../components/navbar.svelte"
  import BookingCard from "../../components/bookingCard.svelte"
  import BookingInfo from "../../components/viewBooking.svelte"
  import QuickBooking from "../../components/quickBooking.svelte"
  import { PUBLIC_BOOKINGS_URL } from '$env/static/public'

  export let data;

  // data fetched from server-side-rendering (SSR)
  // +page.ts
  export let bookings = data.bookings;
  let user = data.user;
  let i = -1;

  // format date
  function formatDate(date : number) {
      var d = new Date(date),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2)
          month = '0' + month;
      if (day.length < 2)
          day = '0' + day;

      return [year, month, day].join('-');
    }

    // when clicking on bookings in the list (left) this is called.
    // based on 'i' the BookingInfo component will display the appropriate
    // booking info
    function setViewFocus(id : number) {
      i = id
    }

</script>

<div class="grid grid-cols-12">
  <NavBar active=1 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
      <div class="grid grid-cols-6">
          <div class="col-span-2">
            <p class="font-bold text-5xl text-[#1A1A1A]">Your bookings...</p>
            <p class="font-light text-2xl ml-2 text-[#515151]">view and manage your bookings</p>

            <div class="overflow-y-auto h-[80vh] mt-16">
              <!--display all bookings-->
              {#each bookings as b, i}
                <BookingCard on:click={() => setViewFocus(i)}
                  class="my-2 transition transform hover:-translate-y-1 motion-reduce:transition-none motion-reduce:hover:transform-none"
                  heading="Booking #{b.id}"
                  subheading={b.bookingType}/>
              {/each}
            </div>

          </div>
          <div class="col-span-4 px-4 ml-20 mt-20">
          <div class="ml-auto">
            <!--display selected bookings' information-->
            {#if i != -1}
              <BookingInfo on:click={()=> i=-1}
                           bookingNumber={bookings[i].id}
                           bookedOn={bookings[i].createDate}
                           bookingDate={formatDate(bookings[i].bookingDate)}
                           bookingTime={bookings[i].bookingTime}
                           bookingLength={bookings[i].bookingLength}
                           facility={bookings[i].facilitiesId}/>
            {:else}
              <!--booking creating component-->
              <QuickBooking/>
            {/if}
          </div>
          </div>
      </div>
   </div>
</div>


<style lang="postcss">
  :global(body) {
      font-family:"Manrope",
  }
</style>