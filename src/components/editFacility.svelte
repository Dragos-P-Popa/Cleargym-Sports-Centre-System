<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import CancelButton from "./cancelButton.svelte";
    import { PUBLIC_FACILITIES_URL } from '$env/static/public'
  
    let editMode : boolean = false;
    let facilities : any = {};
    export let activityName : string;
    export let activityFacility : string;
    export let activityStartTime : string;

    let activity = {
      name: "",
      opening: "",
      closing: "",
      capacity: "",
      manager: "",
    };
  
    async function editFacility(e: { target: HTMLFormElement; }) {
      e.preventDefault();
  
      // fetch form fields
      const formData = new FormData(e.target);
  
      // for each form field, update the facility object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        facility[key] = value;
      }
  
      const res = await fetch(PUBLIC_FACILITIES_URL + 'facility/' + facility.id, {
        method: 'PUT',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(facility),
      });
  
      if (res.status == 200) {
        alert('Facility updated successfully!');
      } else {
        alert('Error updating facility.');
      }
  
      e.target.reset();
    }
</script>

{#if editMode == false}
  <div class="p-4 pb-4 pt-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor mt-20 ml-auto">
    <p class="px-2 text-4xl text-left text-[#1A1A1A]">{activityName}</p>
    <div class="flex grid grid-cols-2">
      <div>
        <p class="px-2 pt-2 text-lg text-left text-[#1A1A1A]">{activityFacility}</p>
        <p class="px-2 text-lg text-left text-[#1A1A1A]">Starts at {activityStartTime}.</p>
      </div>
      <div class="justify-self-end self-end">
        <MainButton on:click={() => editMode = true} class="py-2 px-8 justify-self-end">Edit</MainButton>
      </div>
    </div>
  </div>
{:else}
  <!-- Edit facility -->
  <div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor mt-20 ml-auto">
      <!-- <p class="px-2 font-light text-md text-[#515151] text-left">Name</p> -->
      <p class="px-2 text-4xl text-left text-[#1A1A1A]">Swimming pool</p>
    
      <hr class="m-6 place-self-start rounded bg-borderColor">
      
      <form on:submit={editFacility}>
        <div class="py-2">
          <label for="time">Name</label> <br>
          <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" value="Name" />
        </div>
        <div class="flex space-x-6 text-[#1A1A1A]">
          <div class="py-2 flex-1">
              <label for="time">Opening Time</label> <br>
              <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="opening" name="opening" value="" />
          </div>
          <div class="py-2 flex-1">
              <label for="time">Closing Time</label> <br>
              <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="closing" name="closing" value="" />
          </div>
        </div>
        <div class="flex space-x-6 text-[#1A1A1A]">
          <div class="py-2 flex-1">
              <label for="time">Capacity</label> <br>
              <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="capacity" name="capacity" value="0" min="0" />
          </div>
          <div class="py-2 flex-1">
              <label for="time">Manager ID</label> <br>
              <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="manager" name="manager" value="" />
          </div>
        </div>
        
        <div class="flex space-x-6 pr-3">
          <CancelButton on:click={() => editMode = false} class="mt-5 mx-2 flex-1">Cancel</CancelButton>
          <MainButton type="submit" class="mt-5 flex-1">Save</MainButton>          
        </div>
      </form>
  </div>
{/if}