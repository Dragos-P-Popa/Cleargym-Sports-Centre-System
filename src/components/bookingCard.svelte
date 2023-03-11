<script>
    let divProps = {
        class:[$$restProps.class] + " p-4 border-[1px] border-borderColor shadow-md rounded-lg bg-[url('/gym.jpeg')] pb-12 select-none"
    }

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
    <p class="text-xl text-white font-extrabold">{heading}</p>
    <p class="text-sm text-white">{subheading}</p>
</div>