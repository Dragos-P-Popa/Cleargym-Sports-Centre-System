<script>
    let buttonProps = {
        class:[$$restProps.class] + " py-2 my-2 min-w-xl rounded-lg text-white font-extrabold text-xl bg-mainBlue drop-shadow-md transition transform hover:-translate-y-[1.5px] motion-reduce:transition-none motion-reduce:hover:transform-none",
    }
</script>
<button {...buttonProps}
        on:click
        on:mouseenter
        on:mouseleave
        on:mouseover>
    <slot/>
</button>