<script lang="ts">
  import "@fontsource/manrope";
  import NavBar from "../../../components/managementNavbar.svelte";
  import AddEmployee from "../../../components/newEmployee.svelte";
  import EmployeeCard from "../../../components/employeeCardManager.svelte";

  export let data;
  let user = data.user;
  let employees = data.employees;
</script>

<div class="grid grid-cols-12">
  <NavBar active=2 firstName={user.firstName} lastName={user.lastName}/>

  <div class="col-span-10 pt-12 px-8">
    <div class="grid grid-cols-8">
      <div class="col-span-5">
        <p class="font-bold text-5xl text-[#1A1A1A]">Manage Employees</p>
        <p class="font-light text-2xl text-[#515151]">view and add employees</p>
        
        <div class="overflow-y-auto h-[80vh]">
          <!-- List all employees -->
          <div>
            {#each employees as employee}
              {#if 32 == employee.privilegeLevel}
                <EmployeeCard class="my-3" firstName={employee.firstName} lastName={employee.lastName} email={employee.email} employeeId={employee._id} password={employee.password} privilegeLevel={employee.privilegeLevel} />
              {/if}
            {/each}
          </div> 
        </div>
      </div>
      <div class="col-span-3 px-4 mt-20 ml-5">
        <!-- Add new employee -->
        <div class="ml-auto">
          <div><AddEmployee></AddEmployee></div> 
        </div>
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  :global(body) {
    font-family: "manrope";
  }
</style>