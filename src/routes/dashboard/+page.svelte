<script>
    import "@fontsource/manrope";
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
        <p>MAIN</p> 
     </div>
</div>

<style lang="postcss">
    :global(body) {
        font-family:"Manrope",
    }
</style>
