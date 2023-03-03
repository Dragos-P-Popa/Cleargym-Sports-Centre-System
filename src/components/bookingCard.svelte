<script>
    let divProps = {
        class:[$$restProps.class] + " p-4 border-[1px] border-borderColor shadow-md rounded-lg bg-[url('/gym.jpeg')] pb-12"
    }

</script>

<div  {...divProps}>
    <p class="text-xl text-white font-extrabold"><slot name="heading"/></p>
    <p class="text-sm text-white"><slot name="subheading"/></p>
</div>