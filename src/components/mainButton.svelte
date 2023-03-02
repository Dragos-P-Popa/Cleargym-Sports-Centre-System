<script>
    let buttonProps = {
        class:[$$restProps.class] + " py-2 my-2 w-3/5 min-w-xl rounded-lg text-white font-extrabold text-xl bg-mainBlue drop-shadow-md",
    }
</script>
<button {...buttonProps}
        on:click
        on:mouseenter
        on:mouseleave
        on:mouseover>
    <slot/>
</button>