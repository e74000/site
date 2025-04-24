# About This Website 

I built [this website](https://e74000.net) using [shizuka](https://github.com/e74000/shizuka), a custom static site generator I wrote. Despite seeming like a pointless amount of effort to go to for making a small personal blog like this, I did this because I found stuff like Hugo and Jekyll annoying to use.

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

## Hosting

This website is being hosted on Cloudflare pages, and is automatically updated by this repository.

To do this I selected "Custom Framework" and set set the build command to:

```bash
go run github.com/e74000/shizuka@latest build
```
