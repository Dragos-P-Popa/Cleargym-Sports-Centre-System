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

    // window is undefined when this code is running on the server side. 
    // svelte does some processing on the server side, see svelte docs for more info
    if (typeof window !== 'undefined') {
        // if its running on client side, save the user id as a local variable
        localStorage.setItem("uid", user._id);
    }

</script>


<div class="grid grid-cols-12">
    <NavBar firstName={user.firstName} lastName={user.lastName}/>

    <div class="col-span-10 pt-12 px-8">
        <div class="grid grid-cols-6">
            <div class="col-span-4">
                <p class="font-bold text-5xl text-[#1A1A1A]">{user.firstName},</p>
                 <!--<p>{u._id}</p>-->
                <p class="font-light text-2xl text-[#515151]">welcome back!</p>
            </div>
            <div class="col-span-2 px-4">
                <!--if the user has at least 1 booking, show one here-->
                {#if bookings?.length > 0}
                <p class="text-4xl text-[#1A1A1A] pb-4">Next booking</p>
                <BookingCard class="" heading={bookings[0].bookingType} subheading={bookings[0].bookingTime}></BookingCard>
                {/if}

                <!--booking creating component-->
                <QuickBooking/>

            </div>
        </div>
     </div>
</div>

<style lang="postcss">
    :global(body) {
        font-family:"Manrope",
    }
</style>
