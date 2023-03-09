<script >
  import "@fontsource/manrope";
  import NavBar from "../../components/navbar.svelte"
  import BookingCard from "../../components/bookingCard.svelte"
</script>

<div class="grid grid-cols-12">
  <NavBar active=1/>

  <div class="col-span-10 pt-12 px-8">
      <div class="grid grid-cols-6">
          <div class="col-span-2">
            <p class="font-bold text-5xl text-[#1A1A1A]">Your bookings...</p>
            <p class="font-light text-2xl ml-2 text-[#515151]">view and manage your bookings</p>
            
            
            <div class="mt-16">
              <BookingCard class="my-2"/>
              <BookingCard class="my-2"/>
              <BookingCard class="my-2"/>
              <BookingCard class="my-2"/>
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