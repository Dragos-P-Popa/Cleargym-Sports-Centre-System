<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import { PUBLIC_FACILITIES_URL } from '$env/static/public'

    let facilities;

    async function addActivity(e: { target: HTMLFormElement; }) {  
      // fetch form fields
      const formData = new FormData(e.target);

      const activity : any = {};
  
      // for each form field, update the activity object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        activity[key] = value;
      }

      let facilityId = activity.facility;
      let activityType = activity.name;
      let activityStartTime = activity.startTime;
      let activityEndTime = activity.endTime;
      let activityDay = activity.day;
      
      console.log(activity);
      
      const res = await fetch(PUBLIC_FACILITIES_URL + 'activity', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          facilityId,
          activityType,
          activityDay,
          activityStartTime,
          activityEndTime
        }),
      });
  

      if (res.status == 200) {
        alert('Activity added successfully!');
      } else {
        alert('Error adding activity.');
      }
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
  
  <!-- Add activity -->
  <div class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Add Activity</p>
    <p class="font-light text-md text-[#515151] text-center">Create a new activity.</p>
  
    <hr class="m-6 mx-24 rounded bg-borderColor">
  
    <form on:submit|preventDefault={addActivity}>
      <div class="py-2">
        <label for="name">Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" placeholder="Name" value="" />
      </div>
      <div class="py-2">
        <label for="time">Start Time</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="startTime" name="startTime" value="" />
      </div>
      <div class="py-2">
        <label for="time">End Time</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="endTime" name="endTime" value="" />
      </div>
      <div class="py-2">
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
      <div class="py-2">
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
      <div class="py-2">
        <label for="price">Price</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="price" name="price" placeholder="10" value="" min="0" />
      </div>
      <div class="grid">
        <MainButton type="submit" class="mt-12 w-4/5 place-self-center">Add</MainButton>          
      </div>
    </form>
</div>