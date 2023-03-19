<!-- Carousel for Home page -->
<script lang="ts">
    import { onMount } from 'svelte';
    let container: HTMLElement;

    onMount(() => {
        const arrowLeft = document.getElementById('arrow-left');
        const arrowRight = document.getElementById('arrow-right');
        
        // swipe left when left arrow pressed
        arrowLeft.addEventListener('click', () => {
        container.scrollLeft -= 720;
        });
        
        // swipe right when right arrow pressed
        arrowRight.addEventListener('click', () => {
        container.scrollLeft += 720;
        });
    });

</script>
  
<div class="pb-10 pt-10 px-8 relative">
    <div class="flex overflow-x-auto no-scroll rounded-lg drop-shadow-lg" bind:this={container}>
        <img src="swimming_pool_c.jpg" class="block w-full" alt="Swimming pool" />
        <img src="fitness_room_c.jpg" class="block w-full" alt="Fitness room" />
        <img src="squash_court_c.jpg" class="block w-full" alt="Squash court" />
        <img src="sports_hall_c.jpg" class="block w-full" alt="Sports hall" />
        <img src="climbing_wall_c.jpg" class="block w-full" alt="Climbing wall" />
        <img src="studio_c.jpg" class="block w-full" alt="Studio" />
    </div>
    <div class="absolute pl-2 text-white text-2xl top-2/4 pt-24 left-28 font-semibold">New classes available</div>
    <div class="absolute pl-2 text-[#D7D7D7] text-base top-3/4 left-28">Book one of our new classes now!</div>
    <div class="absolute flex justify-between items-center w-full transform -translate-y-1/2 top-1/2">
        <img class="cursor-pointer p-3 rounded-full bg-white/50 absolute top-1/2 left-5 transform -translate-y-1/2 rounded-full bg-white/50" src="arrowleft2.svg" alt="arrow-left" id="arrow-left" />
        <img class="cursor-pointer p-3 rounded-full rotate-180 bg-white/50 absolute top-1/2 right-24 transform -translate-y-1/2 rounded-full bg-white/50" src="arrowleft2.svg" alt="arrow-right" id="arrow-right" />
    </div>
</div>

<style>
    .no-scroll::-webkit-scrollbar {
        display: none;
    }
</style>