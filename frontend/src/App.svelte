<script lang="ts">
    import { getMetadata } from "./api";
    import Screen from "./components/shared/Screen.svelte";
    import Error from "./components/shared/Error.svelte";
    import Spinner from "./components/shared/Spinner.svelte";
    import Main from "./components/Main.svelte";

    let metadataPromise = getMetadata();
</script>

{#await metadataPromise}
    <Screen>
        <Spinner sizeEm={5} />
    </Screen>
{:then metadata}
    <Main {metadata} />
{:catch error}
    <Error {error} />
{/await}
