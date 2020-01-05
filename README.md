# Game-Of-Life
Just a Game Of life engine with numpy and pygame

requires:
numpy
pygame

usage:
mouseclickon bottom (bleow) pause the sim and in pause mode you can draw shapes (left mouse set right reset)
click below resume
click above reset to empty world

Update:
Simple key binding added:
S - toggle run/pause simulation
space - when in pause - advance single generation
R - reset to empty world and pause 

## Module mGOL.py 
This module is doing the same thing but can use multiprocessing for the generation calc.
Use as the one above plus:
key M - switch between use of multiprocessor or single serial calc.
in multiprocessing mode the background is red.


