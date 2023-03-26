<script lang="ts">
    import MainButton from "./mainButton.svelte";
  
    let activity = {
      name: "",
      time: "",
      length: "",
      day: "",
      facility: "",
    };
  
    async function addActivity(e: { target: HTMLFormElement; }) {
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
        alert('Activity added successfully!');
      } else {
        alert('Error adding activity.');
      }
  
      e.target.reset();
    }
  </script>
  
  <!-- Add activity -->
  <div class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Add Activity</p>
    <p class="font-light text-md text-[#515151] text-center">Create a new activity.</p>
  
    <hr class="m-6 mx-24 rounded bg-borderColor">
  
    <form on:submit={addActivity}>
      <div class="py-2">
        <label for="time">Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" value="Name" />
      </div>
      <div class="py-2">
        <label for="time">Time</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" id="time" name="time" value="" />
      </div>
      <div class="py-2">
        <label for="length">Length</label> <br>
        <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
          <option value="01:00">1 hour</option>
          <option value="02:00">2 hours</option>
          <option value="03:00">3 hours</option>
        </select>
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
        <label for="day">Facility</label> <br>
        <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="facility" id="facility">
            <option value="">Swimming pool</option>
            <option value="">Fitness Room</option>
            <option value="">Squash Court 1</option>
            <option value="">Squash Court 2</option>
            <option value="">Sports Hall</option>
            <option value="">Climbing Wall</option>
            <option value="">Studio</option>
        </select>
      </div>
      <div class="grid">
        <MainButton type="submit" class="mt-12 w-4/5 place-self-center">Add</MainButton>          
      </div>
    </form>
</div>