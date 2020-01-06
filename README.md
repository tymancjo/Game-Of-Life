# Game-Of-Life
## File GOL.py
Just a **Game Of life** engine with numpy and pygame

requires:
numpy
pygame

usage: 

- mouse click on bottom (below) pause the sim and in pause mode you can draw shapes (left mouse set right reset)
click below resume
click above reset to empty world

Update:

Simple key binding added:
- S - toggle run/pause simulation
- space - when in pause - advance single generation
- R - reset to empty world and pause 

## File mGOL.py 
This module is doing the same thing but can use multiprocessing for the generation calc.
Use as the one above plus:
- M - switch between use of multiprocessor or single serial calc.

In multiprocessing mode the background is red.

## File pGOL.py
Works the same way like mGOL.py just uses different multiprocessing system.

