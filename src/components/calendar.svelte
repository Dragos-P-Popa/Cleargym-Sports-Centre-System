<script lang="ts">
    var weekdays = new Array(7);
    weekdays[0] = "Sunday";
    weekdays[1] = "Monday";
    weekdays[2] = "Tuesday";
    weekdays[3] = "Wednesday";
    weekdays[4] = "Thursday";
    weekdays[5] = "Friday";
    weekdays[6] = "Saturday";

    export let selectedDate:Date;
</script>

<div class="grid grid-cols-7 grid-rows-3 gap-2 place-content-evenly">
    <div class="col-span-7 row-span-1 flex place-content-evenly">
        {#each Array(7) as _, i} 
            <p class="font-bold">{weekdays[(new Date().getDay() + i) % weekdays.length]}</p>
        {/each}
    </div>
    <div class="col-span-7 row-span-1 flex place-content-evenly select-none">
        {#each Array(7) as _, i} 
            {@const dateNum = new Date().setDate(new Date().getDate() + i)}
            {#if new Date(dateNum).getDate() == new Date(selectedDate).getDate()}
                <p on:click={() => selectedDate = new Date(dateNum)} class="rounded-full bg-[#d2ecfc] p-4 drop-shadow-sm transition justify-self-center">{new Date(dateNum).getDate()}</p>
            {:else}
                <p on:click={() => selectedDate = new Date(dateNum)} class="rounded-full hover:bg-babyBlue p-4 hover:drop-shadow-sm transition justify-self-center">{new Date(dateNum).getDate()}</p>
            {/if}
        {/each}
    </div>
    <div class="col-span-7 row-span-1 flex place-content-evenly select-none">
        {#each Array(7) as _, i} 
            {@const dateNum = new Date().setDate(new Date().getDate() + i + 7)}
            {#if new Date(dateNum).getDate() == new Date(selectedDate).getDate()}
                <p on:click={() => selectedDate = new Date(dateNum)} class="rounded-full bg-[#d2ecfc] p-4 drop-shadow-sm transition justify-self-center">{new Date(dateNum).getDate()}</p>
            {:else}
                <p on:click={() => selectedDate = new Date(dateNum)} class="rounded-full hover:bg-babyBlue p-4 hover:drop-shadow-sm transition justify-self-center">{new Date(dateNum).getDate()}</p>
            {/if}
        {/each}
    </div>
</div>