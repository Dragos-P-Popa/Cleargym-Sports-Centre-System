<script>

    let buttonProps = {
        class:[$$restProps.class]
    }
</script>
<button {...buttonProps}
        on:click
        on:mouseenter
        on:mouseleave
        on:mouseover>
    <slot/>
</button>