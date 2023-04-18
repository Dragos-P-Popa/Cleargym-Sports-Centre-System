<script>
    let buttonProps = {
        class:[$$restProps.class] + "pr-4 pl-4 py-1 my-2 rounded-lg border-4 text-mainBlue font-extrabold text-xl bg-white drop-shadow-md transition transform hover:-translate-y-[1.5px] motion-reduce:transition-none motion-reduce:hover:transform-none",
    }
</script>
<button {...buttonProps}
        on:click
        on:mouseenter
        on:mouseleave
        on:mouseover>
    <slot/>
</button>