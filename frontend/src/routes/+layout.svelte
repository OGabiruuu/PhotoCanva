<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}

<style>
    :root {
        --clr-background: #292929;
        --clr-outer-box: #121212;
        --clr-outer-box-dtl: #202020;
        --clr-inner-box: #1E1E1E;
        --clr-txt: #FFFFFF;
        --clr-txt-dsbl: #a9a9a9;

        --clr-dtl: #F93827;
        --clr-dtl-shadowy: #C72D1F;
        --clr-dtl-weak: #FF5F52;

        --clr-dtl-invt: #06C7D8;
        --clr-dtl-invt-shadowy: #035B63;
    }

    :global(html, body) {
        height: 100vh;
        width: 100vw;
        margin: 0;
        overflow: hidden;
        background-color: var(--clr-background);

        font-family: sans-serif;
        color: var(--clr-txt);
    }
</style>
