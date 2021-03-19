Musical Bird
===============

A Flappy Bird Clone made using [python-pygame][pygame]
Originally from https://github.com/sourabhv/FlapPyBird and adapted to Raspberry Pi and take input from pressure pads which result in different chords being played

How-to (as tested on Raspberry Pi)
---------------------------

1. Install Python 3.x (recommended) 2.x from [here](https://www.python.org/download/releases/)

1. Install [pipenv]

1. Install PyGame 1.9.x from [here](http://www.pygame.org/download.shtml)

1. Clone the repository:

   ```bash
   $ git clone https://github.com/ktoutanova/flappy_first_lego.git
   ```

   or download as zip and extract.

1. In the root directory run

   ```bash
   $ pipenv install
   $ pipenv run python flappy.py
   ```

More instructions on how to set up the hardware to the pressure pads will be coming soon.

ScreenShot
----------

![Flappy Bird](screenshot1.png)

[pygame]: http://www.pygame.org
[pipenv]: https://pipenv.readthedocs.io/en/latest/
