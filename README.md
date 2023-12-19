The purpose of this project is to design and implement a logical agent that navigates through the 
Wumpus World, a partially-observable environment. 
The Wumpus World presents the following key features:
− The environment is an underground cave with a network of interconnected two-dimensional 
rooms.
− A room may contain a deadly pit, signaled by a perceivable breeze, or a fatal Wumpus
monster, detectable via a discernible stench. 
o The agent will die immediately when entering a room containing one of those harmful 
factors. No withdrawal is possible,
o The percepts are available in the four-neighborhood of the room containing one of 
those harmful factors.
− The agent has an arrow to shoot in the direction he is facing.
− There is one chest of gold, located somewhere in the cave.
− Movement options: forward, backward, left, or right by 90 degrees.
