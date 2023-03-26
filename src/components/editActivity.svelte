<script lang="ts">
    import MainButton from "./mainButton.svelte";
  
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
  </script>
<!-- Edit activity -->
<div class="p-4 py-8 mt-4 shadow-md rounded-lg border-[1px] border-borderColor mt-20 ml-auto">
    <!-- <p class="px-2 font-light text-md text-[#515151] text-left">Name</p> -->
    <p class="px-2 text-4xl text-left text-[#1A1A1A]">Swimming class</p>
  
    <hr class="m-6 place-self-start rounded bg-borderColor">
    
    <form on:submit={editActivity}>
      <div class="py-2">
        <label for="time">Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" value="Name" />
      </div>
      <div class="py-2">
        <label for="day">Facility</label> <br>
        <select class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" name="length" id="length">
            <option value="">Swimming pool</option>
            <option value="">Fitness Room</option>
            <option value="">Squash Court 1</option>
            <option value="">Squash Court 2</option>
            <option value="">Sports Hall</option>
            <option value="">Climbing Wall</option>
            <option value="">Studio</option>
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
      <div class="grid pr-5">
        <MainButton type="submit" class="mt-5 w-1/5 place-self-end">Save</MainButton>          
      </div>
    </form>
</div>
