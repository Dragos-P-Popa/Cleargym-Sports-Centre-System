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


<button class="py-2 m-2 px-24 rounded-lg text-white font-extrabold text-xl bg-mainBlue drop-shadow-lg"><slot/></button>