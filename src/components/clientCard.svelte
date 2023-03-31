<script>
    let divProps = {
        class:
            [$$restProps.class] +
            "  border-[1px] border-borderColor shadow-md rounded-lg bg-[url('/climbing_wall_c.jpg')] bg-cover select-none",
    };

    // export 2 variables, when a bookingCard is created on any page,
    // it will accept these variables like so;
    // <BookingCard heading="foo" subheading="bar"/>

    /**
     * @type {String}
     */
    export let heading;
    /**
     * @type {String}
     */
    export let subheading;
</script>

<div on:click {...divProps}>
    <div class="backdrop-blur-sm w-full h-full p-4 pb-12 rounded-lg">
        <p class="text-xl text-white font-extrabold">{heading}</p>
        <p class="text-sm text-white">{subheading}</p>
    </div>
</div>
