<script>

async function add() {
		const response = await fetch('/api/getm', {
			method: 'GET',
			headers: {
				'content-type': 'application/json'
			}
		});

		total = await response.json();
        console.log(total);
	}
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<button on:click={add}>click</button>