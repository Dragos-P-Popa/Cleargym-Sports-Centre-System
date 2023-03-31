<!-- Carousel for Home page -->
<script lang="ts">
    import { onMount } from "svelte";

    onMount(() => {
        const arrowLeft = document.getElementById("arrow-left")!;
        const arrowRight = document.getElementById("arrow-right")!;
        const img = document.getElementById("showcase")!;

        let images = [
            "swimming_pool_c.webp",
            "fitness_room_c.webp",
            "squash_court_c.webp",
            "sports_hall_c.webp",
            "climbing_wall_c.webp",
            "studio_c.webp",
        ];
        let i = 0;

        // swipe left when left arrow pressed
        arrowLeft.addEventListener("click", () => {
            if (i > 0) {
                i = i - 1;
                img.src = images[i];
            }
        });

        // swipe right when right arrow pressed
        arrowRight.addEventListener("click", () => {
            if (i < images.length - 1) {
                i = i + 1;
                img.src = images[i];
            }
        });
    });
</script>

<div class="pb-10 pt-10 px-8 relative">
    <div
        class="flex overflow-x-auto no-scroll rounded-lg drop-shadow-lg h-[300px]"
    >
        <img
            id="showcase"
            src="swimming_pool_c.webp"
            class="block w-full"
            alt="showcase"
        />
    </div>
    <div
        class="absolute pl-2 text-white text-2xl top-[40%] pt-24 left-28 font-semibold"
    >
        New classes available
    </div>
    <div class="absolute pl-2 text-[#D7D7D7] text-base top-3/4 left-28">
        Book one of our new classes now!
    </div>
    <div
        class="absolute flex justify-between items-center w-full transform -translate-y-1/2 top-1/2"
    >
        <img
            class="cursor-pointer p-3 rounded-full bg-white/50 absolute top-1/2 left-5 transform -translate-y-1/2 rounded-full bg-white/50"
            src="arrowleft2.svg"
            alt="arrow-left"
            id="arrow-left"
        />
        <img
            class="cursor-pointer p-3 rounded-full rotate-180 bg-white/50 absolute top-1/2 right-24 transform -translate-y-1/2 rounded-full bg-white/50"
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
