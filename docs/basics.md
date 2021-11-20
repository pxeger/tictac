# Basics of Tictac
Tictac is, on the surface, a stack-based language: constants are pushed to the stack, and functions pop their arguments
off the top and push their results. However, what makes Tictac unique is this: if a function tries to pop arguments from
a stack which doesn't have enough, a partial function taking the remaining needed arguments is pushed instead. Later,
when a value is pushed, it sees the partial function on the stack and applies it.

For example, consider the function `H`, which halves a number. We can push `6` and then `H`alve it, like so:
```
6 H  § prints 3
```
Alternatively, if we put `H` first, it has no arguments, so the function `H` itself is pushed to the stack.
```
H
```
This doesn't do much when you run it, but if we now push `6`:

```
H 6
```
the value and the partial function annihilate each other by applying the function and producing `3`.

In this way, we effectively achieve programs which are partially agnostic to the order in which elements are pushed.

Here is an example with a 2-argument function `+`:

```
1 2 +  § ordinary postfix notation as used by most stack-based languages - pushes 1 and 2, then adds them
+ 1 2  § pushes a partial function needing two arguments, and then applies it with one argument each at a time
1 + 2  § pushes 1, then a partial function needing only one argument (the function is curried, so the first argument has
       §    already been decided as 1); then pushes 2 which calls the partial function and produces the result
```

There is just one more thing to note: implicit input. Some stack-based golfing languages start with the inputs on the
stack, but Tictac doesn't do that. Instead, the program is executed normally, and only afterwards are the inputs pushed
to the stack - where they will be consumed by whatever partial functions the program left on the stack.
