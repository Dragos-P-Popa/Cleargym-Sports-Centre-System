<script>
    import "@fontsource/manrope";
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
    <div class="min-h-screen border-r-2 border-borderColor col-span-2 mr-2 p-8 pt-16">
       <img class="place-self-center pr-3 mb-16" src = "logo.svg" alt="logo"/>

       <button class="py-2 px-2 my-1 bg-[#EEEEF2] transition-colors duration-200 border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <img class="pr-3" src = "home.svg" alt="home icon"/>
            <span>Home</span>
       </button> <br>
       <button class="py-2 px-2 my-1 hover:bg-[#EEEEF2] transition-colors duration-200 hover:border-[#DDDDDD] border-[#FFFFFF] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <img class="pr-3" src = "calendar.svg" alt="calendar icon"/>
            <span>Bookings</span>
       </button>


    </div>
    <div>
        {#each user as u}
            <p>Welcome {u.firstName}!</p>
            <p>{u._id}</p>
        {/each}

        {#each bookings as b}
`           <p>Booking length {b.bookingLength}!</p>
        {/each}
     </div>
</div>

<style lang="postcss">
    :global(body) {
        font-family:"Manrope",
    }
</style>
