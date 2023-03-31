<script lang="ts">
    import MainButton from "./mainButton.svelte"
    import CancelButton from "./cancelButton.svelte";
    import { PUBLIC_AUTH_URL } from '$env/static/public';

    // These variables control whether the confirmation message should be displayed.
    // It is set to 'false' by default.
    let confirm_demotion = false
    let confirm_promotion = false

    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }
    export let firstName:string;
    export let lastName:string;
    export let email:string;
    export let employeeId:string;
    export let password:string;
    export let privilegeLevel:string;

    async function demoteEmployee(){
        const res = await fetch(PUBLIC_AUTH_URL + 'users/'+employeeId, {
        method: 'PATCH',
        credentials: 'include',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          privilegeLevel: 0
        }),
      });

    // If the code returned from the Auth API was 204
      if (res.status == 204)
      {
        // Set the 'display_confirm' value to 'true'
        confirm_demotion = true;
      }
    }

    async function promoteEmployee(){
        const res = await fetch(PUBLIC_AUTH_URL + 'users/'+employeeId, {
        method: 'PATCH',
        credentials: 'include',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          privilegeLevel: 1028
        }),
      });

        // If the code returned from the Auth API was 204
        if (res.status == 204)
        {
            // Set the 'confirm_promotion' value to 'true'
            confirm_promotion = true;
        }
    }
    
</script>

<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{firstName} {lastName}</p>
        <div class="flex grid grid-cols-2 text-[#515151]">
            <div>
                <p class="text-sm">Email: {email}</p>
                <p class="text-sm">Employee ID: {employeeId}</p>
            </div>
            <div class="justify-self-end">
                <CancelButton on:click={demoteEmployee} type="submit" class="py-2 px-8">Demote</CancelButton>
                <MainButton on:click={promoteEmployee} type="submit" class="py-2 px-8">Promote</MainButton>
            </div>
        </div>
        <!-- If the request was successful, display a confirmation message -->
        {#if confirm_demotion==true}
            <p class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
                style="font-size: 20px; color: green;">
                The employee was demoted successfully!
            </p>
            <!-- The list of employees gets refreshed after each successful submission -->
            <script>setTimeout(() => {location.reload();}, 1500);</script>
        {:else if confirm_promotion==true}
            <p class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
                style="font-size: 20px; color: green;">
                The employee was promoted successfully!
            </p>
            <!-- The list of employees gets refreshed after each successful submission -->
            <script>setTimeout(() => {location.reload();}, 1500);</script>
        {/if}
    </div>
</div>