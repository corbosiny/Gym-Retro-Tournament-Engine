# Source Code

This directory contains all of the source code pertaining to the project.

## Basic Descriptions

### Lobby.py
Lobby handles all of the interfacing with the retro environment, generating the training data, and providing the game state to the models playing. A lobby is an abstraction of the training environment, a lobby can be loaded up with a variety of roms to play and will manage all of the back end interfacing.

### Agent.py
This class acts as a skeletal abstract interface for all other Agents to inherit from and also provides some backend helper functions to get other Agents started. All children classes must implement two abstract methods in order to keep with the desired interface for an Agent. More can be read in the "How to make an Agent" section further on in this readme.

### DeepQAgent.py
A DeepQ Reinforcement learning model implemented using a dense reward function.

### HumanAgent.py
A child of the agent class that allows for a human to enter live inputs during a match. This allows the human to either act as a training partner or enter into the tournaments themselves to compete.

### GameMaster.py
The game master runs tournaments between models listed in a tournament roster config file. The game master can run a variety of tournament styles on any of the supported retro roms and will track the individual performances of models to provide overall rankings.

### watchAgent.py
A helper script that when run loads in a desired network and lets the user visualize how well the network is running on some test save states.

### LossHistory.py
A class used to store the training error logs after each training episode as consistent with the typical keras log format.

---
## How to make an agent

To make your own agent it is recommended to make a class that inherits from Agent.py. Agent.py contains several useful helper functions that allow you to:

-Find and loop through every save state  
-Handle opening and cleaning up of the gym environment  
-Recording data during the fights
-And even training the agent after the fights

Some of these methods aren't filled in but the overall framework in place makes it easy to drop in your own versions of the getMove, train, and initialize network functions such that there is little work outside of network design that has to be done to get your agent up and running. The goal is to create a streamlined platform to rapidly prototype, train, and deploy new agents instead of starting for scratch every time. As well enforcing the interface for the agent class allows for high level software to be developed that can import various user created agents without fear of breaking due to interface issues.

### Agent class

There are only two functions that need to be implemented in order to create a new child agent:

-getMove  
-trainNetwork

Each section below gives a description of the interface required for each function and it's purpose. Further documentation can be seen inside the code of Agent.py. 

In addition to these functions a config file needs to be fed into the Agent to load and build a network. This can be overwritten by implementing your own initModel function in a child class.

#### getMove

Get move simply returns a multivariate array of the action space of the game. A one in a given index represents the button corresponding to that index being pressed, a zero means the button is not pressed. This way multiple buttons can be pushed in one move and special moves can be preformed. This function must take in the observation and info about the current state. The observation is the contents of each pixel of the game screen and info is a dictionary containing key word mapped variables as specified in data.json. The indices correspond to Up, Down, Left, Right, A, B, X, Y, L, R.

#### trainNetwork

Takes in the prepared training data and the current model and runs a desired amount of training epochs on it. The trained model is then returned once training is finished. The local_models directory is where you may store your models to avoid any merge conflicts. The way you store your checkpoints and training logs is up to you.

---
## Example Implemented Agents

### DeepQAgent

DeepQAgent is an implementation of the DeepQ reinforcement algorithm for playing StreetFighter using policy gradients, a dense reward function, and greedy exploration controlled by an epsilon value that decreases as the model is trained. Each action the Agent takes during a steo is rewarded after a change in time in order to see what effect the move had on the fight outcome. When the model is first initialized it plays completely randomly in order to kick start rapid greedy exploration. As the model trains epsilon slowly decreases until the model begins to take over now that it has watched random play for a while and hopefully begins to guide the random exploration to a subset of the state space that it thinks would be advantageouss to play in.

#### Get Move

 The current state is converted into a feature vector via the prepareNetworkInputs function. The output of the network is a list of the predicted rewards for playing each of the possible moves in the current state. The move with the max predicted reward is the move the Agent make. However whenever a move is requested by the Agent a random number is generated, if this number is below the epsilon value(the chance to explore new moves), a random move is picked instead. This forces exploration of new strategies by the Agent during training and challenges its preconceived notions of certain game sequences. However this exploration is not informed by any model the Agent has and so is simply random greedy exploration.

#### trainNetwork

For training the method of policy gradients is used. A dense reward function has been designed so that the Agent can be given frequent rewards for using good moves. Policy gradients essentially uses the reward for each state, action, new state sequence as the gradient for training our network. The gradient vector then has the index of the move chosen set to the reward and all other indices are left zero. So the network is either trained to pick solely that move more or less in that state depending on the reward, but other moves are not penalized. 
