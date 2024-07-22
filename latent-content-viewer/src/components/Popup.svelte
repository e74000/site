<script>
  import { onMount, afterUpdate, onDestroy } from 'svelte';
  import '../markdown.css'; // Import the markdown CSS file

  export let nodeData = null;
  export let nodeScreenPos = { x: 0, y: 0 };
  export let closePopup = () => {};

  let content = '';
  let loading = false;
  let popupElement;
  let popupRect = { l: 0, r: 0, t: 0, b: 0 };
  let popupPosition = 'right';
  let isMobileView = window.innerWidth <= 768;

  async function fetchContent(path) {
    loading = true;
    const response = await fetch(path);
    content = await response.text();
    loading = false;
  }

  $: if (nodeData) {
    if (nodeData.filetype === 'markdown' || nodeData.filetype === 'html') {
      fetchContent(nodeData.path);
    }
  }

  $: if (nodeScreenPos.x < window.innerWidth / 2) {
    popupPosition = 'right';
  } else {
    popupPosition = 'left';
  }

  function handleLinkClick(event) {
    if (event.target.tagName === 'A') {
      const href = event.target.getAttribute('href');
      if (href.startsWith('/?node=')) {
        event.preventDefault();
        const url = new URL(href, window.location.origin);
        const nodeId = url.searchParams.get('node');
        if (nodeId) {
          selectNodeById(nodeId);
        }
      }
    }
  }

  function stopPropagation(event) {
    event.stopPropagation();
  }

  function selectNodeById(id) {
    const event = new CustomEvent('selectnode', {
      detail: { id }
    });
    window.dispatchEvent(event);
  }

  afterUpdate(() => {
    if (popupElement) {
      const rect = popupElement.getBoundingClientRect();
      popupRect = {
        l: rect.left,
        r: rect.right,
        t: rect.top,
        b: rect.bottom,
      };
      popupElement.addEventListener('click', handleLinkClick);
    }
  });

  onDestroy(() => {
    if (popupElement) {
      popupElement.removeEventListener('click', handleLinkClick);
    }
  });

  function updateViewMode() {
    isMobileView = window.innerWidth <= 768;
  }

  window.addEventListener('resize', updateViewMode);

  onDestroy(() => {
    window.removeEventListener('resize', updateViewMode);
  });
</script>

<style>
  .popup {
    top: 10%;
    width: 40%;
    background: #191919;
  }

  .popup-right {
    right: 5%;
  }

  .popup-left {
    left: 5%;
  }

  .popup-mobile {
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #191919;
  }

  .line {
    position: absolute;
    background: none;
    z-index: 10;
    pointer-events: none;
  }

  .slanted-bg {
    position: absolute;
    z-index: 1;
  }
  
  .slanted-bg::after {
    content: '';
    position: absolute;
    bottom: 0;
    right: 0;
    width: 100%;
    height: 100%;
    background-color: inherit;
    transform: skewX(-30deg);
    transform-origin: bottom right;
    z-index: -1;
  }

  .custom-scrollbar::-webkit-scrollbar {
    width: 8px;
  }

  .custom-scrollbar::-webkit-scrollbar-track {
    background: none;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: #585a58
  }

  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #343835;
  }

  .close-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: #191919;
    color: #f7f6ec;
    border: 1px solid #a57fc4;
    border-radius: 0;
    padding: 0.25rem 0.5rem;
    cursor: pointer;
    z-index: 20;
  }
</style>

{#if nodeData}
  {#if !loading}
    {#if nodeData.filetype === 'markdown' || nodeData.filetype === 'html'}
      <div class="popup {popupPosition === 'right' ? 'popup-right' : 'popup-left'} {isMobileView ? 'popup-mobile' : ''} absolute shadow-xl z-10 border-color5 border-t border-b overflow-hidden h-4/5" bind:this={popupElement} on:click={stopPropagation}>
        <button class="close-button" on:click={closePopup}>Close</button>
        <h1 class="absolute top-0 left-0 slanted-bg text-sm bg-color5 w-fit px-2 font-mono">{nodeData.decorativePath}</h1>
        <div class="custom-scrollbar overflow-y-auto h-full p-0">
          <div class="popup-content">{@html content}</div>
        </div>
      </div>
    {:else if nodeData.filetype === 'image'}
      <div class="popup {popupPosition === 'right' ? 'popup-right' : 'popup-left'} {isMobileView ? 'popup-mobile' : ''} absolute shadow-xl z-10 border-color5 border-t border-b overflow-hidden" bind:this={popupElement} on:click={stopPropagation}>
        <button class="close-button" on:click={closePopup}>Close</button>
        <h1 class="absolute top-0 left-0 slanted-bg text-sm bg-color5 w-fit px-2 font-mono">{nodeData.decorativePath}</h1>
          <div class="custom-scrollbar overflow-y-auto h-full bg-background text-foreground font-mono">
              <img src="{nodeData.path}" class="w-full h-auto">
              <div class="metadata border-t border-color5">
                  {#each Object.entries(nodeData.metadata) as [key, value]}
                      <div class="flex py-1">
                          <span class="text-color8 mx-2">{key}:</span>
                          <span class="ml-auto text-color8 w-1/2 mx-2">{value}</span>
                      </div>
                  {/each}
              </div>
          </div>
      </div>
    {:else}
      <div class="popup {popupPosition === 'right' ? 'popup-right' : 'popup-left'} {isMobileView ? 'popup-mobile' : ''} absolute shadow-xl z-10 border-color5 border-t border-b overflow-hidden" bind:this={popupElement} on:click={stopPropagation}>
        <button class="close-button" on:click={closePopup}>Close</button>
        <h1 class="absolute top-0 left-0 slanted-bg text-sm bg-color5 w-fit px-2 font-mono">{nodeData.decorativePath}</h1>
        <div class="custom-scrollbar overflow-y-auto h-full">
          <pre class="whitespace-pre-wrap break-words p-2">{@html content}</pre>
          <pre class="whitespace-pre-wrap break-words p-2">{JSON.stringify(nodeData.metadata)}</pre>
        </div>
      </div>
    {/if}
  {:else}
    <div class="popup {popupPosition === 'right' ? 'popup-right' : 'popup-left'} {isMobileView ? 'popup-mobile' : ''} absolute shadow-xl z-10 border-color5 border-t border-b overflow-hidden h-4/5 flex justify-center items-center" bind:this={popupElement} on:click={stopPropagation}>
      <button class="close-button" on:click={closePopup}>Close</button>
      <h1 class="absolute top-0 left-0 slanted-bg text-sm bg-color5 w-fit px-2 font-mono">{nodeData.decorativePath}</h1>
      <div class="text-foreground">Loading...</div>
    </div>
  {/if}

  {#if !isMobileView}
    {#if popupPosition === 'right'}
      {#if nodeScreenPos.y > popupRect.t}
        <div
          class="absolute bg-none z-10 pointer-events-none"
          style="top: {popupRect.t}px; left: {nodeScreenPos.x}px; height: {nodeScreenPos.y - popupRect.t}px; width: {popupRect.l - nodeScreenPos.x}px; border-top: 1px solid #a57fc4; border-left: 1px solid #a57fc4;"
        ></div>
      {:else}
        <div
          class="absolute bg-none z-10 pointer-events-none"
          style="top: {nodeScreenPos.y + 1}px; left: {nodeScreenPos.x}px; height: {popupRect.t - nodeScreenPos.y}px; width: {popupRect.l - nodeScreenPos.x}px; border-bottom: 1px solid #a57fc4; border-left: 1px solid #a57fc4;"
        ></div>
      {/if}
    {:else}
      {#if nodeScreenPos.y > popupRect.t}
        <div
          class="absolute bg-none z-10 pointer-events-none"
          style="top: {popupRect.t}px; left: {popupRect.r}px; height: {nodeScreenPos.y - popupRect.t}px; width: {nodeScreenPos.x - popupRect.r}px; border-top: 1px solid #a57fc4; border-right: 1px solid #a57fc4;"
        ></div>
      {:else}
        <div
          class="absolute bg-none z-10 pointer-events-none"
          style="top: {nodeScreenPos.y + 1}px; left: {popupRect.r}px; height: {popupRect.t - nodeScreenPos.y}px; width: {nodeScreenPos.x - popupRect.r}px; border-bottom: 1px solid #a57fc4; border-right: 1px solid #a57fc4;"
        ></div>
      {/if}
    {/if}
  {/if}  
{/if}
