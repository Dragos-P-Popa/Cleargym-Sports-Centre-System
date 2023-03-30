<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import CancelButton from "./cancelButton.svelte";
    import { PUBLIC_FACILITIES_URL } from '$env/static/public';

    let divProps = {
        class:[$$restProps.class] + "  border-[1px] border-borderColor shadow-md rounded-lg bg-cover select-none"
    }
    export let activityType:string;
    export let activityFacility:string;
    export let activityStartTime:string;
    export let activityEndTime:string;
    export let activityDay:string;
    // set activity price, change later
    export let price:string;
    export let activityId; 

    console.log(activityType)
        
    let editMode : boolean = false;
    let facilities : any = {};
  
    async function editActivity(e: { target: HTMLFormElement; }) {
      // fetch form fields
      const formData = new FormData(e.target);
  
      const activity : any = {};

      // for each form field, update the activity object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        activity[key] = value;
      }

      const res = await fetch(PUBLIC_FACILITIES_URL + '/activity/'+activityId, {
        method: 'PATCH',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          activityType : activity.name,
          activityFacility : activity.facility,
          activityDay : activity.day,
          activityStartTime : activity.startTime,
          activityEndTime : activity.endTime,
          price : activity.price
        }),
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

<div on:click {...divProps}>
    <!-- List of activities -->
    {#if editMode == false}
    <div class="backdrop-blur-sm w-full h-full p-4 rounded-lg">
        <p class="text-3xl pb-2 font-extrabold">{activityType}</p>
        <div class="flex grid grid-cols-2 text-[#515151]">
            <div>
                <!-- <p class="text-sm">Facility: {location}</p> -->
                <p class="text-sm">Day: {activityDay}</p>
                <p class="text-sm">Time: {activityStartTime} - {activityEndTime}</p>
                <p class="text-sm">Price per hour: £{price}</p>
            </div>
            <div class="justify-self-end">
                <MainButton on:click={()=>editMode=true} class="py-2 px-8">Edit</MainButton>
            </div>
        </div>
    </div>
    {:else if editMode == true}
    <!-- Edit selected activity -->
    <div class="p-4 py-8 shadow-md rounded-lg border-[1px] border-borderColor ml-auto">
        <p class="px-2 text-4xl text-left text-[#1A1A1A]">{activityType}</p>

        <hr class="m-6 place-self-start rounded bg-borderColor">
        
        <form on:submit={editActivity}>
            <div class="py-2">
                <label for="name">Name</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" value="{activityType}" />
            </div>
            <div class="flex space-x-6 text-[#1A1A1A]">
                <div class="py-2 flex-1">
                    <label for="facility">Facility</label> <br>
                    <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="facility" id="facility">
                    {#await facilityLoading()}
                    <option value="loading">Loading...</option>
                    {:then facilities}
                        {#each facilities as facility, i}
                        <option value={facility.id}>{facility.facilityName}</option>
                        {/each}
                    {/await}
                    </select>
                </div>
                <div class="py-2 flex-1">
                    <label for="day">Activity Day</label> <br>
                    <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="day" id="day">
                        <option value="Monday">Monday</option>
                        <option value="Tuesday">Tuesday</option>
                        <option value="Wednesday">Wednesday</option>
                        <option value="Thursday">Thursday</option>
                        <option value="Friday">Friday</option>
                        <option value="Saturday">Saturday</option>
                        <option value="Sunday">Sunday</option>
                    </select>
                </div>
            </div>
            <div class="flex space-x-6 text-[#1A1A1A]">
                <div class="py-2 flex-1">
                    <label for="startTime">Start Time</label> <br>
                    <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="startTime" name="startTime" value="{activityStartTime}"/>
                </div>
                <div class="py-2 flex-1">
                    <label for="endTime">End Time</label> <br>
                    <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="endTime" name="endTime" value="{activityEndTime}" />
                </div>
            </div>
            <div class="py-2">
                <label for="price">Price per hour</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="price" name="price" value="{price}" min="0" />
            </div>
            <div class="flex space-x-6 pr-3">
                <CancelButton on:click={() => editMode = false} class="mt-5 mx-2 flex-1">Close</CancelButton>
                <MainButton type="submit"  class="mt-5 mx-2 flex-1">Save</MainButton>          
            </div>
        </form>
    </div>
    {/if}
</div>