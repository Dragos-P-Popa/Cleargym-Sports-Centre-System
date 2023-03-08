<script>
    let buttonProps = {
        class:[$$restProps.class] + " py-2 my-2 min-w-xl rounded-lg text-white font-extrabold text-xl bg-[#A21019] drop-shadow-md",
    }
</script>
<button {...buttonProps}
        on:click
        on:mouseenter
        on:mouseleave
        on:mouseover>
    <slot/>
</button>