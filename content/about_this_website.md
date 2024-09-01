![[mirror_banner.png]]

# about this website

i built this website out of two main parts:
1. the frontend, built using svelte/three.js/tailwind,
2. the static site generator, written in python,

## frontend

the frontend is an interactive node viewer, representing the semantic positions of each piece of media, and the connections between them.

yellow nodes represent text posts, while blue nodes represent images.

i think it's still a little buggy on mobile, but it is mostly working at the moment.

## generator

the static site generator is used to embed the posts into a semantic embedding space using CLIP, before using UMAP to reduce the dimensionality of the embeddings so they can be viewed in 3d.

it also extracts metadata from the media, such as links and tags, and converts the markdown documents into HTML.

there's not really much point to doing this, but i thought it was neat so i did it anyway.

## roadmap

- i want to start doing some more photography/art again, and post that stuff here too.
