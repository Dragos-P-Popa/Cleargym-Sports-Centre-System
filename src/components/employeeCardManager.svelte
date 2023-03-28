<script lang="ts">
    // import MainButton from "./mainButton.svelte"
    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }
    export let name:string;
    export let surname:string;
    export let email:string;
    export let employeeId:string;
</script>

<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{name} {surname}</p>
        <div class="flex grid grid-cols-2 text-[#515151]">
            <div>
                <p class="text-sm">Email: {email}</p>
                <p class="text-sm">Employee ID: {employeeId}</p>
            </div>
            <!-- <div class="justify-self-end">
                <MainButton class="py-2 px-8">Edit</MainButton>
            </div> -->
        </div>
    </div>
</div>