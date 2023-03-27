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
      facility: "",
      time: "",
      length: "",
      price: "",
      dscount: "",
    };
  
    async function editActivity(e: { target: HTMLFormElement; }) {
      e.preventDefault();
  
      // fetch form fields
      const formData = new FormData(e.target);
  
      // for each form field, update the activity object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        activity[key] = value;
      }
  
      const res = await fetch(PUBLIC_ACTIVITIES_URL + 'activity/' + activity.id, {
        method: 'PUT',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(activity),
      });
  
      if (res.status == 200) {
        alert('Activity updated successfully!');
      } else {
        alert('Error updating activity.');
      }
  
      e.target.reset();
    }

    async function facilityLoading() {
      // fetch all facilities
      const res = await fetch(PUBLIC_FACILITIES_URL + 'facilities', {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
        }
      })

      // this data is used to populate the facility selection UI element (line 97-112)
      facilities = await res.json()
      return facilities
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
  <!-- Edit activity -->
  <div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor mt-20 ml-auto">
    <p class="px-2 text-4xl text-left text-[#1A1A1A]">{activityName}</p>

    <hr class="m-6 place-self-start rounded bg-borderColor">
    
    <form on:submit={editActivity}>
      <div class="py-2">
        <label for="time">Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" value="Name" />
      </div>
      <div class="py-2">
        <label for="day">Facility</label> <br>
        <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
          {#await facilityLoading()}
          <option value="loading">Loading...</option>
          {:then facilities}
            {#each facilities as facility, i}
              <option value={facility.facilitiesId}>{facility.facilityName}</option>
            {/each}
          {/await}
        </select>
      </div>
      <div class="flex space-x-6 text-[#1A1A1A]">
        <div class="py-2 flex-1">
            <label for="time">Time</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value="" />
        </div>
        <div class="py-2 flex-1">
            <label for="length">Length</label> <br>
            <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
            <option value="01:00">1 hour</option>
            <option value="02:00">2 hours</option>
            <option value="03:00">3 hours</option>
            </select>
        </div>
      </div>
      <div class="flex space-x-6 text-[#1A1A1A]">
        <div class="py-2 flex-1">
            <label for="time">Price £</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="price" name="price" value="0" min="0" />
        </div>
        <div class="py-2 flex-1">
            <label for="time">Discount %</label> <br>
            <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="discount" name="discount" value="0" min="0" />
        </div>
      </div>
      <div class="flex space-x-6 pr-3">
        <CancelButton on:click={() => editMode = false} class="mt-5 mx-2 flex-1">Cancel</CancelButton>
        <MainButton type="submit" class="mt-5 mx-2 flex-1">Save</MainButton>          
      </div>
    </form>
  </div>
{/if}

