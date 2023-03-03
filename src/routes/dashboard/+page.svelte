<script>
    import "@fontsource/manrope";
    import BookingCard from "../../components/bookingCard.svelte"
    import QuickBooking from "../../components/quickBooking.svelte"
    import NavBar from "../../components/navbar.svelte"
    import { onMount } from 'svelte';

    let user = [];
    let bookings = [];

    //http://127.0.0.1:3002/bookings/user/640136331fa3b5d6b18fb0ee

    onMount(async () => {
        let token = localStorage.getItem('accessToken');
		const res = await fetch('http://localhost:3001/user/', {
			method: 'GET',
            // essential to set the header
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        let userData = await res.json();
        user = [...userData];

        const res2 = await fetch('http://127.0.0.1:3002/bookings/user/'+userData[0]._id, {
			method: 'GET'
        })

        let bookingsData = await res2.json();
        bookings = [...bookingsData];
    });

</script>


<div class="grid grid-cols-12">
    <NavBar/>

    <div class="col-span-10 pt-12 px-8">
        <div class="grid grid-cols-6">
            <div class="col-span-4">
                {#each user as u}
                    <p class="font-bold text-5xl text-[#1A1A1A]">{u.firstName},</p>
                    <!--<p>{u._id}</p>-->
                    <p class="font-light text-2xl text-[#515151]">welcome back!</p>
                {/each}

                
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
