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

    let audience = user.emai

    // function which sents a refresh request to the Auth API
    async function refreshToken() {
        const res = await fetch('http://localhost:3001/refresh/', {
			method: 'POST',
            credentials: 'include',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
				"audience": ""+user.email
			})
        });
    }

    // svelte interval which will run every 5 minutes
    const interval = setInterval(async () => {
        refreshToken();
    }, 300000);

    onMount(async () => {
        // initial token refresh when page is loaded
        refreshToken();
    });

  onDestroy(() => clearInterval(interval));
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
