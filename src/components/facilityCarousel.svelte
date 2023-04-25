<!-- Carousel for Main page -->
<script lang="ts">
    import { onMount } from "svelte";
    let container: HTMLElement;

    onMount(() => {
        const arrowLeft = document.getElementById("arrow-left");
        const arrowRight = document.getElementById("arrow-right");

        // swipe left when left arrow pressed
        arrowLeft.addEventListener("click", () => {
            container.scrollLeft -= 415;
        });

        // swipe right when right arrow pressed
        arrowRight.addEventListener("click", () => {
            container.scrollLeft += 415;
        });
    });
</script>

<div class="py-10 px-48 text-[#1A1A1A] text-[48px]">
    <p><b>Facility showcase</b></p>
</div>

<div class="pb-20 px-10 pl-40 w-11/12 relative">
    <div
        class="flex overflow-x-auto no-scroll drop-shadow-lg"
        bind:this={container}
    >
        <img
            src="swimming_pool_c.webp"
            class="block w-2/6"
            alt="Swimming pool"
        />
        <img src="fitness_room_c.webp" class="block w-2/6" alt="Fitness room"/>
        <img src="squash_court_c.webp" class="block w-2/6" alt="Squash court"/>
        <img src="sports_hall_c.webp" class="block w-2/6" alt="Sports hall"/>
        <img
            src="climbing_wall_c.webp"
            class="block w-2/6"
            alt="Climbing wall"
        />
        <img src="studio_c.webp" class="block w-2/6" alt="Studio"/>
    </div>
    <div
        class="absolute flex justify-between items-center w-full transform -translate-y-1/2 top-1/3"
    >
        <img
            class="cursor-pointer p-3 absolute top-1/2 rounded-full bg-white/50 left-2"
            src="arrowleft2.svg"
            alt="arrow-left"
            id="arrow-left"
        />
        <img
            class="cursor-pointer p-3 rotate-180 absolute top-1/2 rounded-full bg-white/50 right-52"
            src="arrowleft2.svg"
            alt="arrow-right"
            id="arrow-right"
        />
    </div>
</div>

<style>
    .no-scroll::-webkit-scrollbar {
        display: none;
    }
</style>
