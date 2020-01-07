
# Game of Life vs. Multiprocessing

Hi,

Firstly let me say thank you for letting me join this group. I'm not a programmer or CS guy but it's my hobby and nice support for my work as Electrical Engineer.

## Quick intro:

I wanted to learn and understood the use of multiprocessing in python. as a training ground I made simple code that simulates the "game Of Life". In sort words, it create a 2D numpy array which is the game world. And utilize the builded gen() function to calculate the next generation of the cell.

The gen() function is made in a way that can do the calculation for only a piece of the world array at the time.
So I do divide the whole array to some sub arrays and to solve thew hole thing the gen() function is ran for each such piece.

This is once done just in normal serial computations, running in a loop(more less like):
> Not exact code like in file, just to illustrate
```python
for subarray in subarrays:
    solution += solve_for(subarray)
```

Then when I can hit M key i switch the solution to parallel one, like:

```python
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(solve, subarrays)
    for res in result):
        solution += res        
```

## The Question
Whenever I do this experiments the serial calculations are way faster than the parallel ones.

**And I wonder if I'm doing something wrong or there is another reason it behave like that?**

I really want to understand how and way it works this way. 

## The files:
File is available on GH:

https://github.com/tymancjo/Game-Of-Life/blob/master/exampleGOL.py

The piece that is responsible of the serial or parallel starts on line 231. 

### Thank you for any advice!