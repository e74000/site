---
title: "about this website"
date: "2024-12-08"
template: "post.tmpl"
meta_description: "about this website"
meta_keywords: "net, e74net, e74000, about, website, static site generator"
---

# About This Website 

I built this website using [shizuka](https://github.com/e74000/shizuka), a custom static site generator I wrote. Despite seeming like a pointless amount of effort to go to for making a small personal blog like this, I did this because I found stuff like Hugo and Jekyll annoying to use.

Shizuka is named after the character from 君のことが大大大大大好きな100人の彼女, on account of being small and doing lots of reading, much like the character.

The aim of writing Shizuka was to make something with the shortest possible installation -> having a site time. For this reason it focuses on extreme simplicity over features. However, a core focus was to ensure that it remains our of the user's way when designing themes or making templates.

The focus on simplicity also means that I should be able to add new features pretty easily, for example embedding interactive programs in posts, nice link previews, etc.

## Try Shizuka!

To install shizuka, just run:

```bash
go install github.com/e74000/shizuka@latest
```

You can then scaffold a new project into your current directory with:

```bash
shizuka init
```

And then start a development server with:

```bash
shizuka dev
```

And you are done! You can edit files, templates etc and the preview (should) hot-reload to preview your site.

When you want to deploy a site, just run:

```bash
shizuka build
```