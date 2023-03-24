<script lang="ts">
    import { goto } from "$app/navigation";
    import { PUBLIC_AUTH_URL } from '$env/static/public'

     export let active : string = "0";
     export let firstName : string = "";
     export let lastName : string = "";

     async function logout() {
          const res = await fetch(PUBLIC_AUTH_URL + 'logout/', {
			method: 'POST',
               credentials: 'include',
               // essential to set the header
               headers: {
               "Content-Type": "application/json",
               }
          })
          goto('auth/')
     }
</script>

<div class="grid sticky top-0 h-screen border-r-2 border-borderColor col-span-2 mr-2 p-8 pt-16">
    
     <!--Logo and navigation buttons-->
     <div>
          <img class="place-self-center pr-3 mb-16" src = "../logo.svg" alt="logo"/>

          {#if active == "0"}
          <button class="py-2 px-2 my-1 bg-[#EEEEF2] transition-colors duration-200 border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
               <span>Book</span>
          </button> <br>
          <button on:click={() => goto('/employees/amend', { replaceState: false })} class="py-2 px-2 my-1 hover:bg-[#EEEEF2] transition-colors duration-200 hover:border-[#DDDDDD] border-[#FFFFFF] border-[1px] rounded-lg w-full text-left inline-flex items-center">
               <span>Amend</span>
          </button> <br>
          <button on:click={() => goto('/employees/memberships', { replaceState: true })} class="py-2 px-2 my-1 transition-colors duration-200 hover:bg-[#EEEEF2] border-[#FFFFFF] transition-colors duration-200 hover:border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <span>Memberships</span>
          </button>
          {:else if active == "1"}
          <button on:click={() => goto('/employees/book', { replaceState: true })} class="py-2 px-2 my-1 transition-colors duration-200 hover:bg-[#EEEEF2] border-[#FFFFFF] transition-colors duration-200 hover:border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
               <span>Book</span>
          </button> <br>
          <button class="py-2 px-2 my-1 bg-[#EEEEF2] transition-colors duration-200 border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <span>Amend</span>
          </button> <br>
          <button on:click={() => goto('/employees/memberships', { replaceState: true })} class="py-2 px-2 my-1 transition-colors duration-200 hover:bg-[#EEEEF2] border-[#FFFFFF] transition-colors duration-200 hover:border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <span>Memberships</span>
          </button>
          {:else if active == "2"}
          <button on:click={() => goto('/employees/book', { replaceState: false })} class="py-2 px-2 my-1 hover:bg-[#EEEEF2] transition-colors duration-200 hover:border-[#DDDDDD] border-[#FFFFFF] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <span>Book</span>
          </button> <br>
          <button on:click={() => goto('/employees/amend', { replaceState: false })} class="py-2 px-2 my-1 hover:bg-[#EEEEF2] transition-colors duration-200 hover:border-[#DDDDDD] border-[#FFFFFF] border-[1px] rounded-lg w-full text-left inline-flex items-center">
            <span>Amend</span>
          </button> <br>
          <button class="py-2 px-2 my-1 bg-[#EEEEF2] border-[#DDDDDD]  border-[1px] rounded-lg w-full text-left inline-flex items-center">
               <span>Memberships</span>
          </button>
          {/if}
     </div>

     <!--Account related UI-->
     <div class="place-self-center self-end">
          <hr class="rounded bg-[#EDEDEF]">
          <!-- svelte-ignore a11y-mouse-events-have-key-events -->
          <div class="flex mt-6">
               <div class="flex select-none grid p-3 rounded-lg bg-mainBlue">
                    <p class="text-white font-bold text-center text-auto self-center justify-self-center">{firstName[0]+lastName[0]}</p>
               </div>
               <p class="text-[#1A1A1A] pl-2 self-center font-semibold text-auto text-[#1A1A1A] select-none">{firstName + " " + lastName}</p>
          </div>

          <button class="mt-8 py-2 px-2 my-1 transition-colors duration-200 hover:bg-[#EEEEF2] border-[#FFFFFF] transition-colors duration-200 hover:border-[#DDDDDD] border-[1px] rounded-lg w-full text-left inline-flex items-center">
               <img class="pr-3" src = "../setting.svg" alt="settings icon"/>
               <span>Settings</span>
          </button> <br>
          <button on:click={() => logout()} class="py-2 px-2 my-1 hover:bg-[#EEEEF2] transition-colors duration-200 hover:border-[#DDDDDD] border-[#FFFFFF] border-[1px] rounded-lg w-full text-left inline-flex items-center">
               <img class="pr-3" src = "../logout.svg" alt="logout icon"/>
               <span>Logout</span>
          </button>
     </div>
 </div>