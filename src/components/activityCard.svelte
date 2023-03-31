<script lang="ts">
    import MainButton from "./mainButton.svelte"

    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }

    export let heading:string;
    export let location:string;
    export let startTime:string;
    export let sessionLength:string;
</script>

<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{heading}</p>
        <div class="flex grid grid-cols-2">
            <div>
                <p class="text-sm">{location}</p>
                <p class="text-sm">Starts at {startTime} for {sessionLength} hour(s)</p>
            </div>
            <div class="justify-self-end">
                <MainButton class="py-1 px-2">Checkout</MainButton>
            </div>
        </div>
    </div>
</div>