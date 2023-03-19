<script>
    import JoinUsButton from "./joinUsButton.svelte";
    import { goto } from "$app/navigation";
</script>

<div class="flex flex-row w-full px-8 py-40">
    <div class="flex w-1/2 flex-col pl-40 py-10">
        <h3 class="py-1 text-[34px] font-bold">Welcome to cleargym!</h3>
        <p>The most complete and beginner friendly gym in the UK.</p>
        <p>Join us to make use of all our fantastic facilities!</p>
        <JoinUsButton
            on:click={() => goto("/dashboard")}
            class="w-1/4 text-base">Join Us</JoinUsButton
        >
    </div>

    <div class="w-1/2 relative">
        <img
            src="climbing_wall.jpg"
            alt="climbing wall"
            class="absolute w-1/3 rounded-lg z-20 left-[35%] top-[40%] transition-all hover:z-30 hover:scale-110"
        />
        <img
            src="swimming_pool.jpg"
            alt="swimming pool"
            class="absolute w-1/5 rounded-lg z-10 left-[20%] top-[50%] transition-all hover:z-30 hover:scale-110"
        />
        <img
            src="sports_hall.jpg"
            alt="sports hall"
            class="absolute w-1/2 rounded-lg transition-all hover:z-30 hover:scale-110"
        />
    </div>
</div>
