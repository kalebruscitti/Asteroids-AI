Pythentic Asteroids -- v0.1.0

In 1998 I wrote my first Java program, 'Authentic Asteroids' which was a clone of the classic
Atari Asteroids arcade game of 1978. This is a Python / Pygame port of my Java game. 

Keys: Z,X rotate, N,B thrust & fire, H hyperspace OR
Cursor keys rotate and thrust, Space fire 
Enter start 
P pause 
O frame advance whilst paused 
F toggle full screen moode 

Features: 
Intersecting line geometry used for collision detection. 
Authentic asteroids shapes 
Damped ship handling 
Small and large saucers 
Full screen 
Fading explosion debris 
Engine thrust jet 
Extra life at 10,000 
Hyperspace 

My original Java clone of this game used simple bounding collision detection. I wanted to 
improve on that in this Python version. If a bounding box collision occurs between the 
ship and a rock extra checks are made using the code in the geometry.py to determine if 
any of the line segments intersect. 

All the code is Open Source GPL 

This is my first game with Pygame. The code is pretty rough around the edges and is 
probably not that Pythonic. Any feedback welcome. Turn down the lights, turn up the 
volume and travel back to 1978!
