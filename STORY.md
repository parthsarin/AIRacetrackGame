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

## Thursday, February 28 (Sam's Birthday-ish!?)

Being the dilligent workers we are, we arrived promptly at lab and instantly got to work, making massive strides towards a working game.

I'm just kidding of course. Colin was, like 30 minutes late, and everyone else wasted a good amount of time watching YouTube videos, making Parth a Genius Bar appointment (his phone just... died), and trying desperatly not to kill off another one of Jade's seven remaining brain cells.

Actually, since Parth's phone had died, he couldn't use Two-Factor Authentication to fill out the attendance code for the day, so he promised to write Sam a birthday haiku in exchange. Here's what he came up with (after Googling to remind himself about the syllable counts):
> Has a sweet, cute dog
> Writes excellent Python code
> Happy birthday, Sam.

Yeah, he's not a poet. Although... Sam's response:
> THANK YOU!
> I love it.
> --Sam

### The Graphics Journey: Interactive Map Generation and A Promising Start

Antonio and Colin split the Graphics into two pieces: making a racetrack for the car to drive on (which they called a 'map') and writing dynamics for the car. Antonio worked on the first and Colin worked on the second.

By the end of the day, Colin had implemented a `Car` class which drew a car from its $(x,y)$ coordinates and a rotation variable. You can't control it yet, but it's getting there!

Antonio, working separately, wrote a Python script where, by clicking on the screen, users could design their own maps with their own 'reward gates' and its own start point. The program pickled the files and stored them in the root directory, the idea being that you could later load the file into the main script and display the map to the user. 

By the way, the 'reward gates' are a concept that the AI team requested: for Q-learning algorithms, the idea is to train an AI by giving it punishments or rewards for doing certain actions. The most natural punishment for this type of game is to punish the AI if it runs into a wall. The most natural reward would be to reward the AI for, say, driving around the entire racetrack. The problem, though, is that an AI put in this situation is supposed to be able to randomly stumble upon the rewards. It learns by doing the things that it randomly stumbled upon again and again and slowly getting better at them. If the only reward was for getting *all the way around the track*, the AI could never stumble upon it randomly and would never learn anything.

The pickling worked successfully, and, later that night, Parth managed to import Antonio's map that he'd created on his laptop onto Parth's laptop (which is pretty cool!).

### The AI Journey: We made... a parachute

Things were moving more slowly with the AI team. Jade had roughly seven brain cells remaining after a late night and a stressful week. Parth and Jade got to work on finishing the AI they'd started last time. By 'got to work', I mean Parth peered over Jade's shoulder at her computer and they talked about / wrote code together.

This process was not the most efficient... at one point, they were passing the laptop back and forth every two lines of code because Parth was making fun of the way Jade types (instead of keeping four fingers on the keyboard, her pointer fingers float in the air, pointing at the screen, as though they're really excited about what Jade is typing). It was long, but they got it done. They implemented the *entire* (backup) AI! The AI, which I've described before, works by measuring the distance to the walls in eight directions. It moves in the forward-ish direction towards which it is farthest away from the wall.

This was like... 10 lines of code?

After that, they kinda relaxed, focusing on next steps. They were deciding whether to build a slightly-more-advanced, perhaps-still-hardcoded AI or to take on a much more advanced algorithm like Q-learning. As Jade described the second option, "now that we've built a parachute, we can go skydiving." So, they watched YouTube videos and played [qwop](http://www.foddy.net/Athletics.html) until the day was over.

Jade promised her brain cells would regenerate by Saturday, so the AI team planned to meet again then.

> With <3 by @jpac
