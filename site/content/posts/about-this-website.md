---
title: "about this website"
description: "about e74000.net"
date: "2024-12-08"
template: "post.tmpl"
meta_description: "about this website"
meta_keywords: "net, e74net, e74000, about, website, static site generator"
data:
  Preview: "https://e74000.net/x-card.png"

sitemap_include: true
sitemap_change_freq: "monthly"
sitemap_priority: "0.8"

rss_include: true
---

# about this website

this website is acting as my personal blog, where i'm going to post more long-form content, as well as interactive programs and stuff.

# how it works

i built this website using [shizuka](https://github.com/e74000/shizuka), a custom static site generator i wrote. this is kind of a pointless amount of effort to go to for such a small site, but i was motivated entirely by how much i hated using hugo.

shizuka is named after the character from the anime 君のことが大大大大大好きな100人の彼女, on account of being small and doing lots of reading, much like the character.

the aim of shizuka is to make an ssg with the shortest possible time delta between installation and having a site running. for this reason it focuses on extreme simplicity over actual features. this simplicity goes hand in hand with being pretty generic, so it is pretty easy to add customise to your usecase.

## try shizuka!

to install shizuka, just run:

```bash
go install github.com/e74000/shizuka@latest
```

you can then scaffold a new project into your current directory with:

```bash
shizuka init
```

and then start a development server with:

```bash
shizuka dev
```
aAnd you are done! you can edit files, templates etc and the preview (should) hot-reload as you save.

when you want to deploy a site, run:

```bash
shizuka build
```

if you want to use shizuka with a hosting service like [Cloudflare Pages](https://pages.cloudflare.com/) (how this site is hosted) then you can select "custom framework" and set the build command to:

```bash
go run github.com/e74000/shizuka@latest build
```

i hope you take some time to try it out! i tried to make it super fast to get started with ([<1min lol](https://x.com/e74net/status/1868395665921102070)) so hopefully you can try it out and let me know what you think!

also if you like shizuka and want to help contribute to it, just make a pull request on github! if you need ideas on what to contribute there's a few different things i want to improve with it:

- RSS integration
- sitemap.xml
- better hot-reloading
- a nicer default theme
- (maybe a collection of pre-configured themes?)
