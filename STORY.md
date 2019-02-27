# The Story

## Tuesday, February 26
We were sitting in the back row of class, being obnoxious as usual. As Sam noticed, we'd actually ordered ourselves in j-p-a-c order (well, we were reversed, but `'jpac'[::-1]`, right?). After lecture, we started to divide ourselves up into teams to address the various parts of our project. It took way longer to come to this conclusion than it should have, but Parth and Jade decided to work together on the AI team (to design an AI to play the racing game) and Antonio and Colin decided to work together on the Graphics team (to design the interface for game playing). 

For some reason, Jade and Colin really wanted to be on their own 'Moral Support Taskforce' but as a team, we gently decided against that idea (read: moral support, my ass!).

Then, we got to work and started to write some code.

### The Graphics Journey: A Copy-Paste Legend
Colin, seemingly within two seconds, found starter code on Github for *exactly what we wanted to do* (display a screen, read input, draw things)! He copy-pasted that into the repository and then Antonio and Colin spent the rest of the time making commit jokes about Parth's pedantic code practices.

### The AI Journey: AAAAAAAH
Jade and Parth had no clue what to do. After looking at some AI libraries, they gestured Sam over and asked him for help with ideas. Sam suggested to make a very simple AI: no neural nets, genetic algorithms, or anything of the sort.

We wanted our AI to be able to 'see' the distances to each of the walls from the side of the car. It would be able to 'see' in eight directions:

(insert image here)

So, Jade and Parth thought of a simple algorithm: have the car move in the direction which it is farthest away from (think the most 'open' direction) and, to break ties, just move in a 'forward'-ish direction. They started to think about writing this in code but first had to write a `Movement` class that would interface between the graphics and backend. `Movement` would be the instantaneous direction that the car should move in (i.e., left, right, forwards, backwards, forwards-left, forwards-right, nowhere, etc.).

They started to write some code for this, and class ended pretty soon.
