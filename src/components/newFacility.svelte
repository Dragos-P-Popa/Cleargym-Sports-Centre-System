<script lang="ts">
    import MainButton from "./mainButton.svelte";
    import { PUBLIC_FACILITIES_URL } from '$env/static/public'


  
    async function addFacility(e: { target: HTMLFormElement; }) {

      // fetch form fields
      const formData = new FormData(e.target);

      const facility : any = {};
  
      // for each form field, update the facility object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        facility[key] = value;
      }

      let facilityName = facility.name;
      let capacity = facility.capacity;
      let openingTime = facility.opening;
      let closingTime = facility.closing;
      let managerId = facility.manager;
  
      const res = await fetch(PUBLIC_FACILITIES_URL + 'facility', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          facilityName,
          capacity,
          openingTime,
          closingTime,
          managerId
        }),
      });
  
      if (res.status == 200) {
        alert('Facility added successfully!');
      } else {
        alert('Error adding facility.');
      }
    }
</script>

<!-- Add facility -->
<div class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
    <p class="text-4xl text-center text-[#1A1A1A]">Add Facility</p>
    <p class="font-light text-md text-[#515151] text-center">Create a new facility.</p>
  
    <hr class="m-6 mx-24 rounded bg-borderColor">
  
    <form on:submit|preventDefault={addFacility}>
      <div class="py-2">
        <label for="time">Name</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="name" name="name" placeholder="Name" value="" />
      </div>
      <div class="py-2">
        <label for="time">Opening Time</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" step="1" id="opening" name="opening" value="" />
      </div>
      <div class="py-2">
        <label for="time">Closing Time</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="time" step="1" id="closing" name="closing" value="" />
      </div>
      <div class="py-2">
        <label for="time">Capacity</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="capacity" name="capacity" value="0" min="0" />
      </div>
      <div class="py-2">
        <label for="time">Manager ID</label> <br>
        <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="name" id="manager" name="manager" value="" />
      </div>
      <div class="grid">
        <MainButton type="submit" class="mt-12 w-4/5 place-self-center">Add</MainButton>          
      </div>
    </form>
</div>