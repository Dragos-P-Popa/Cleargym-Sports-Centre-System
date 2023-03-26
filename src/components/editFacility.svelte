<script lang="ts">
    import MainButton from "./mainButton.svelte";
  
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
      
      <div class="grid pr-5">
        <MainButton type="submit" class="mt-5 w-1/5 place-self-end">Save</MainButton>          
      </div>
    </form>
</div>
