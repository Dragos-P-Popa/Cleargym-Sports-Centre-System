<script>
    let buttonProps = {
        class:
            [$$restProps.class] +
            " py-1 my-2 rounded-lg text-white font-extrabold text-xl bg-mainBlue drop-shadow-md",
    };
</script>

<button {...buttonProps} on:click on:mouseenter on:mouseleave on:mouseover>
    <slot />
</button>
