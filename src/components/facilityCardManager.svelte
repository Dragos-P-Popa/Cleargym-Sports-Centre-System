<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import CancelButton from "./cancelButton.svelte";
    import { PUBLIC_FACILITIES_URL } from '$env/static/public';

    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }
    export let facilityName:string;
    export let capacity:string;
    export let openingTime:string;
    export let closingTime:string;
    export let managerId:string;

    let editMode : boolean = false;
  
    async function editFacility(e: { target: HTMLFormElement; }) {
      // fetch form fields
      const formData = new FormData(e.target);
      
      const facility : any = {};

      // for each form field, update the facility object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        facility[key] = value;
      }
  
      const res = await fetch(PUBLIC_FACILITIES_URL + 'facility', {
        method: 'PATCH',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          facilityName : facility.name,
          capacity : facility.length,
          openingTime : facility.time,
          closingTime : facility.time,
          managerId : facility.text,
        }),
      });
  
      if (res.status == 200) {
        alert('Facility updated successfully!');
      } else {
        alert('Error updating facility.');
      }
  
      e.target.reset();
    }
</script>

<div on:click {...divProps}>
    {#if editMode == false}
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{facilityName}</p>
        <div class="flex grid grid-cols-2 text-[#515151]">
            <div>
                <p class="text-sm">{capacity} people capacity</p>
                <p class="text-sm">{openingTime} - {closingTime}</p>
                <p class="text-sm">Manager: {managerId}</p>
            </div>
            <div class="justify-self-end">
                <MainButton on:click={()=>editMode=true} class="py-2 px-8">Edit</MainButton>
            </div>
        </div>
    </div>
    {:else if editMode == true}
    <!-- Edit facility -->
    <div class="p-4 py-8 shadow-md rounded-lg border-[1px] border-borderColor ml-auto">
        <p class="px-2 text-4xl text-left text-[#1A1A1A]">{facilityName}</p>
    
        <hr class="m-6 place-self-start rounded bg-borderColor">
        
        <form on:submit|preventDefault={editFacility}>
        <div class="py-2">
            <label for="time">Name</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" value="{facilityName}" />
        </div>
        <div class="flex space-x-6 text-[#1A1A1A]">
            <div class="py-2 flex-1">
                <label for="time">Opening Time</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="opening" name="opening" value="{openingTime}" />
            </div>
            <div class="py-2 flex-1">
                <label for="time">Closing Time</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="closing" name="closing" value="{closingTime}" />
            </div>
        </div>
        <div class="flex space-x-6 text-[#1A1A1A]">
            <div class="py-2 flex-1">
                <label for="time">Capacity</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="capacity" name="capacity" value="{capacity}" min="0" />
            </div>
            <div class="py-2 flex-1">
                <label for="time">Manager ID</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="manager" name="manager" value="{managerId}" />
            </div>
        </div>
        
        <div class="flex space-x-6 pr-3">
            <CancelButton on:click={() => editMode = false} class="mt-5 mx-2 flex-1">Cancel</CancelButton>
            <MainButton on:click={() => editMode = false} type="submit" class="mt-5 flex-1">Save</MainButton>          
        </div>
        </form>
    </div>
    {/if}
</div>