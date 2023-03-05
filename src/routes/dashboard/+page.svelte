<script >
    import "@fontsource/manrope";
    import BookingCard from "../../components/bookingCard.svelte"
    import QuickBooking from "../../components/quickBooking.svelte"
    import NavBar from "../../components/navbar.svelte"
    import { onMount, onDestroy } from 'svelte';
      /** @type {import('./$types').PageData} */
    export let data;

    // data fetched from server-side-rendering (SSR)
    // +page.server.ts
    let user = data.user;
    let bookings = data.bookings;


</script>


<div class="grid grid-cols-12">
    <NavBar/>

    <div class="col-span-10 pt-12 px-8">
        <div class="grid grid-cols-6">
            <div class="col-span-4">
                <p class="font-bold text-5xl text-[#1A1A1A]">{user.firstName},</p>
                 <!--<p>{u._id}</p>-->
                <p class="font-light text-2xl text-[#515151]">welcome back!</p>
            </div>
            <div class="col-span-2 pt-16 px-4">
                <p class="text-4xl text-[#1A1A1A] pb-4">Next booking</p>

                {#each bookings as b}
                    <BookingCard class="" heading={b.bookingDate} subheading={b.bookingLength}></BookingCard>
                {/each}

                <QuickBooking active="0"/>

            </div>
        </div>
     </div>
</div>

<style lang="postcss">
    :global(body) {
        font-family:"Manrope",
    }
</style>
