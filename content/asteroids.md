![[berlin_banner.png]]

# relativistic asteroids

this project is combines an (approximate) relatavistic physics engine with the arcade game asteroids.

features inclue:

- relativistic physics engine: this game is built on a modified verlet integration physics + collision solver, it includes things like time dilation and length contraction. as your ship approaches the speed of light, the game world behaves differently.

- dynamic speed of light: the speed of light (c) in the engine isn't a fixed value. it can (and is) be dynamically altered during gameplay.

- collisions: collisions between asteroids, bullets, and your ship are handled using a lorentz-corrected collision detection algorithm. the engine attempts to account for relativistic momentum and energy conservation.

you can try out a demo of this [here](https://r2.e74000.net/wasm/run.html?path=asteroids.wasm).
