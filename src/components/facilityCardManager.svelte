<script lang="ts">
    import MainButton from "./mainButton.svelte"
    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }
    export let heading:string;
    export let capacity:string;
    export let startTime:string;
    export let endTime:string;
</script>

<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{heading}</p>
        <div class="flex grid grid-cols-2 text-[#515151]">
            <div>
                <p class="text-sm">{capacity} people capacity</p>
                <p class="text-sm">{startTime} - {endTime}</p>
            </div>
            <div class="justify-self-end">
                <MainButton class="py-2 px-8">Edit</MainButton>
            </div>
        </div>
    </div>
</div>