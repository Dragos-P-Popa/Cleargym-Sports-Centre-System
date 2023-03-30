<script lang="ts">
    import MainButton from "./mainButton.svelte"
    import CancelButton from "./cancelButton.svelte";
    import { PUBLIC_AUTH_URL } from '$env/static/public';

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

      if (res.status == 204) {
        alert('Employee demoted successfully!');
      } else {
        alert('Error demoting employee.');
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

      if (res.status == 204) {
        alert('Employee promoted successfully!');
      } else {
        alert('Error promoting employee.');
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
    </div>
</div>