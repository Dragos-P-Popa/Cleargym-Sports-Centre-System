<script>
    export let active;
    export let heading;
    export let subHeading;
    export let bulletPoints;

    let divProps = {
        class: [$$restProps.class] + " w-full py-2 h-full px-2 max-h-40 mt-8 transition hover:shadow-md rounded-lg "
    }

    if (active == 0) {
        divProps.class = divProps.class + "border-borderColor border"
    } else if (active == 1){
        divProps.class = divProps.class + "border-[#4B84A4] border-2"
    }

</script>

<div on:click {...divProps}>
    <div class="grid grid-cols-10 divide-x divide-borderColor h-full flex">
        <div class="col-span-3 m-1">
            <p class="text-xl font-bold ">{heading}</p>
            <p class="text">{subHeading}</p>
        </div>
        <div class="grid col-span-7 m-1 self-center">
            {#if active==1}
                <p class="justify-self-end text-[#4B84A4] font-bold">Current Plan</p>
            {/if}
            <ul role="list" class="list-disc ml-6">
                {#each bulletPoints as point}
                <li>{point}</li>
                {/each}
            </ul>
        </div>
    </div>
</div>
