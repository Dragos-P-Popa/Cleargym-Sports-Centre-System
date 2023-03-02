<script lang="ts">
  import   MainButton from "../../components/mainButton.svelte"
  import  SecondaryButton from "../../components/secondaryButton.svelte"

  function onSubmit(e: { target: HTMLFormElement; }) {
    const formData = new FormData(e.target);

    const data = {};
    for (let field of formData) {
      const [key, value] = field;
      data[key] = value;
    }
    console.log(data);
  }
</script>

<div class="rounded-xl bg-white shadow-lg border-[1px] border-borderColor m-8 mx-[20%] max-w-[60%] px-16 pt-12 pb-4">
  <p class="text-center">LOGO</p>
  <p class="text-center text-5xl font-bold pt-4">Welcome to cleargym!</p>
  <p class="text-center text-xl font-light pb-20">Lorem ipsum lorem ipsum lerem ipsum</p>

  <form on:submit|preventDefault={onSubmit}>
    <div>
      <label for="email">Email</label> <br>
      <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="text" id="email" name="email" placeholder="example@email.com" value="" />
    </div>
    <div class="mt-4 pb-8">
      <label for="password">Password</label> <br>
      <input class="border-borderColor border-[1px] rounded-md px-2 py-2 mt-1 shadow-sm min-w-full" type="password" id="password" placeholder="password" name="password" value="" />
    </div>

    <div class="grid">
      <MainButton type="submit" class="mt-12 max-w-lg place-self-center">Login</MainButton>
    </div>
  </form>

  <div class="grid">
    <div class="inline-flex items-center justify-center w-full">
      <hr class="w-64 h-px my-4 bg-gray-200 border-0">
      <span class="absolute px-3 font-medium text-gray-900 -translate-x-1/2 bg-white left-1/2">or</span>
    </div>
    <SecondaryButton class="place-self-center max-w-lg ">Register</SecondaryButton>
  </div>

</div>

<style lang="postcss">
  :global(hmtl) {
      background-color: theme(colors.mainBlue);
    }
</style>