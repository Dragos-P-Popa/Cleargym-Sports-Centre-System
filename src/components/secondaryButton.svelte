<script>
    let buttonProps = {
        class:[$$restProps.class] + " py-1 my-2 rounded-lg border-4 text-mainBlue font-extrabold text-xl bg-white drop-shadow-md",
    }
</script>
<button {...buttonProps}
        on:click
        on:mouseenter
        on:mouseleave
        on:mouseover>
    <slot/>
</button>