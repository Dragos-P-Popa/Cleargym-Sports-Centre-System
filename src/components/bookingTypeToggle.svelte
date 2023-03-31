<script lang="ts">
    export let selection: number;
</script>

{#if selection == 1}
    <div class="rounded-xl drop-shadow">
        <label
            for="themeSwitcherOne"
            class="themeSwitcherTwo shadow-card relative inline-flex cursor-pointer select-none items-center justify-center rounded-xl bg-[#EEEEEE] p-1.5 space-x-1"
        >
            <input
                type="checkbox"
                name="themeSwitcherOne"
                id="themeSwitcherOne"
                class="sr-only"
            />
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span
                on:click={() => (selection = 1)}
                class="light text-primary bg-[#C0D7E4] flex items-center space-x-[6px] rounded-xl py-2 px-[18px] text-sm font-medium"
            >
                General booking
            </span>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span
                on:click={() => (selection = 2)}
                class="dark text-body-color hover:bg-babyBlue transition flex items-center space-x-[6px] rounded-xl py-2 px-[18px] text-sm font-medium"
            >
                Activity booking
            </span>
        </label>
    </div>
{:else}
    <div class="rounded-xl drop-shadow">
        <label
            for="themeSwitcherOne"
            class="themeSwitcherTwo shadow-card relative inline-flex cursor-pointer select-none items-center justify-center rounded-xl bg-[#EEEEEE] p-1.5 space-x-1"
        >
            <input
                type="checkbox"
                name="themeSwitcherOne"
                id="themeSwitcherOne"
                class="sr-only"
            />
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span
                on:click={() => (selection = 1)}
                class="light text-primary flex hover:bg-babyBlue transition items-center space-x-[6px] rounded-xl py-2 px-[18px] text-sm font-medium"
            >
                General booking
            </span>
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span
                on:click={() => (selection = 2)}
                class="dark text-body-color bg-[#C0D7E4] flex items-center space-x-[6px] rounded-xl py-2 px-[18px] text-sm font-medium"
            >
                Activity booking
            </span>
        </label>
    </div>
{/if}
