<script>
    /**
     * @type {string}
     */
     export let active="0";
</script>

<div class="min-h-screen border-r-2 border-borderColor col-span-2 mr-2 p-8 pt-16">
    <img class="place-self-center pr-3 mb-16" src = "logo.svg" alt="logo"/>

    {#if active == "0"}
    <button class="py-2 px-2 my-1 bg-[#EEEEF2] transition-colors duration-200 border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
         <img class="pr-3" src = "home.svg" alt="home icon"/>
         <span>Home</span>
    </button> <br>
    <button on:click={() => active="1"} class="py-2 px-2 my-1 hover:bg-[#EEEEF2] transition-colors duration-200 hover:border-[#DDDDDD] border-[#FFFFFF] border-[1px] rounded-lg w-full text-left inline-flex items-center">
         <img class="pr-3" src = "calendar.svg" alt="calendar icon"/>
         <span>Bookings</span>
    </button>
    {:else if active == "1"}
    <button on:click={() => active="0"} class="py-2 px-2 my-1 transition-colors duration-200 hover:bg-[#EEEEF2] border-[#FFFFFF] transition-colors duration-200 hover:border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
        <img class="pr-3" src = "home.svg" alt="home icon"/>
        <span>Home</span>
   </button> <br>
   <button class="py-2 px-2 my-1 bg-[#EEEEF2] border-[#DDDDDD]  border-[1px] rounded-lg w-full text-left inline-flex items-center">
        <img class="pr-3" src = "calendar.svg" alt="calendar icon"/>
        <span>Bookings</span>
   </button>
    {/if}
 </div>