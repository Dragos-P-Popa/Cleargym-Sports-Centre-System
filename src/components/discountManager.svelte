<script lang="ts">
    import MainButton from "./mainButton.svelte"
    import { PUBLIC_PAYMENTS_URL } from '$env/static/public';

    // This variable controls whether the confirmation message should be displayed.
    // It is set to 'false' by default.
    let display_confirm = false

    export let discount;

    async function changeDiscount(e: { target: HTMLFormElement; }){
        // fetch form fields
      const formData = new FormData(e.target);

      const data : any = {};

      // for each form field, update the discount object with the inputted value
      for (let field of formData) {
        const [key, value] = field;
        data[key] = value;
      }

      let discount = data.discount;

      console.log(data);

      const res = await fetch(PUBLIC_PAYMENTS_URL + 'discount/'+discount, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
            discount
        }),
      });

        // If the code returned from the Payments API was 200
        if (res.status == 200)
        {
            // Set the 'display_confirm' value to 'true'
            display_confirm = true;
        }
        else {
            alert('Error updating discount.');
        }
    }
</script>


<div>
    <div class="p-4 pt-8 mb-4 mt-4 shadow-md rounded-lg border-[1px] border-borderColor">
        <form on:submit|preventDefault={changeDiscount}>
            <div>
                <label for="discount">Change discount %:</label> <br>
                <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="number" id="discount" name="discount" placeholder="{discount.discount}" value="" min="0"/>
            </div>
            <!-- If the request was successful, display a confirmation message -->
            {#if display_confirm==true}
                <p class="mt-8 mb-4 ml-auto mr-auto w-4/5 place-self-center text-center"
                    style="font-size: 20px; color: green;">
                    The discount was changed successfully!
                </p>
                <!-- The page gets refreshed after each successful submission -->
                <script>setTimeout(() => {location.reload();}, 1500);</script>
            {/if}
            <div class="grid">
                <MainButton type="submit" class="mt-10 w-4/5 place-self-center">Save</MainButton>
            </div>
        </form>
    </div>
</div>
