<script>
    let divProps = {
        class:[$$restProps.class] + " p-4 border-[1px] border-borderColor shadow-md rounded-lg bg-[url('/gym.jpeg')] pb-12"
    }

    /**
     * @type {String}
     */
    export let heading;
    /**
     * @type {String}
     */
    export let subheading;
</script>

<div  {...divProps}>
    <p class="text-xl text-white font-extrabold">{heading}</p>
    <p class="text-sm text-white">{subheading}</p>
</div>