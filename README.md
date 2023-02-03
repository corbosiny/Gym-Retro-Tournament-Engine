The Trello board for dev tasks can be found here: https://trello.com/b/bLHQK3YK/tournament-engine-dev

# About this Project

## Introduction

The Gym Retro Tournament Engine is a project aimed at building a flexible platform for quickly organizing and hosting AI tournaments for any games supported by the gym retro engine along with any custom made environments.

## Key Project Points
This project has two key points that we are trying to deliver. First is a flexible training platform where users can quickly create a model, have it start playing in a large library of different game environments, and hook it up to a variety of supplied or custom training methods. The majority of the work of running the environments, gathering performance metrics, and generating training data to review is handled by the back end and supplied to your model making it easy to focus on just designing your model. Secondly we provide a seconday service, the Game Master, of creating a program that can load a batch of user supplied models and run them through competitive adversarial tournaments. The Game Master tracks individual model performance and tournament rankings for a comprehensive overview of how the models perform against one another.

### Training Platform
This goal aims to design and implement a clear and concise interface between a backend training environment that handles running the emulator and any custom AI Agent the users want to develop. The training environment will ask the Agents for moves when they are able to act, gather training data for use after the game, handle shifting through training states, and log the results of the training over several episodes. A user's custom Agent need only inherit from the Agent interface and implement the abstract functions required of it's children for it to be compatable with the training platform. The user can implement any functionality on top of those functions as they see fit as long as the interface between the Agent and the training environment is held to. The hope is to allow a broad range of models and algorithms to be developed that can all make use of the same training platform without having to replicate work done on setting up the backend.

### Community Tournaments
This goal aims to design a system wherein user submitted models can compete against one another in a simulated tournament of varying styles(round robin, bracket, etc) on a variety of interchangeable games. The tournaments are scalable to any size, are rendered to be human watchable with trackable ranking charts, and can even feature human players involed in the games to compete against the models themselves. Replays of the games can be saved and shared with the models competing for training purposes. 

## Repo Organization
This section will explain the organization of the repo, if you are trying to install the dependancies then skip to the next section.  

The top level of the repo contains four main directories:

### src
This directory contains all of the source related to the engine, machine learning algorithms, and helper scripts

### local_models
This directory contains a set of unique directories containing model checkpoints for each separate model that is trained locally. These models are not saved online to avoid merge conflicts.

### examples
This directory contains a set of basic examples that demonstrate basic functionality of several libraries used in the source code. New features usually start off as example scripts that serve as launching off points for development. The readme in the directory as a short description of what each example is demonstrating.

### docs
This folder contains boiler plate documents such as the software license and the code of conduct for contributions.

---
# Getting Started

This section will take you through how to get this repo up and running with the example agents, make your own test agents, and also how to create your own save states to test your agents on. 

---
## Installing Dependancies

This code only works with Python 3.6 or later. Before trying to install dependencies it is recommend to open the terminal and run:  
`sudo apt-get update`  
`sudo apt-get upgrade`  
`sudo -H pip3 install --upgrade pip`  

To download the necessary dependencies after cloning the repo call:
`pip3 install -r requirements.txt`

This should be called in the top level directory of the repo. This will install the following libraries you will need to create game environments that serve as a wrapper abstracting the interface between your agent and the underlying emulator:

-gym  
-gym-retro   
-tensorflow   
-keras   

These libraries can sometimes have serious issues installing themselves or their dependencies on a windows machine. It is recommended to work on Linux. The server we will be training on runs Linux and all libraries plus code have been confirmed to work on Ubuntu's latest stable distribution.

---
## The first test run

To double check that the dependancies were properly set up the example agent can be run. cd into the src directory. Then either run the following command on your terminal or from your preferred IDE of choice by supplying the -r flag:

`python3 Agent.py -r`

A small emulator window should pop up and show the agent randomly playing a game of pole cart. The -r flag makes the game the agent is playing human renderable for you to observe. When training agents on a server via an ssh shell or some other remote desktop method it is important to leave this flag off as an error will be thrown when trying to render to a non-existent monitor. 

---
## Preparing custom game files

After the dependencies have been installed you are free to play any game already supported by the library. However there is also the possibility of adding your own custom supported games to the library itself. This section will walk you through installing your own custom game via an example installation of **StreetFighterIISpecialChampionEdition-Genesis**. The game files for a custom game need to be copied into the actual game data files inside the installation of the retro library on your local machine. This location can be found by running the following lines in the command line:  

`python3`  
`import retro`  
`print(retro.__file__)`    

That should return the path to where the retro __init__.py script is stored. One level up from that should be the data folder. Inside there should be the stable folder. This is where all of the different game files are stored. Inside any specific game you can see a number of files: 

-rom.md    
-rom.sha    
-scenario.json  
-data.json  
-metadata.json  
-reward_script.lua   
-.state files that contain a saved emulator state

Creating a named directory with these files inside will allow the library to find and run this game. Further on in this section we will explain what these game files are and how to generate these game files.

## Json Files

There are three json files that the gym environment reads in order to setup the high level "rules" of the emulation. These files are metadata.json, data.json, and scenario.json. 

### Metadata.json

The metadata.json file holds high level global information about the game environment. For now this simply tells the environment the default save state that the game ROM should launch in if none has been selected. 

### Data.json

The data.json file is an abstraction of the games ram into callable variables with specified data types that the environment, user, and environment.json files can interact with. A complete list of named variables and their corresponding addresses in memory can be found listed in the file itself. If a publicly available RAM dump for a game can not be found finding new variables on your own is an involved process and requires monitoring RAM and downloading the bizhawk emulator. Bizhawk is an emulator used for developing tool assisted speedruns and has a wide selection of tools for RAM snooping. This video is a good reference for learning how to snoop RAM:

https://www.youtube.com/watch?v=zsPLCIAJE5o&t=900s

### Scenario.json

Scenario.json specifies several conditions over which that define the goal of the simulation or specify what criteria the agent will be judged on for rewards. The main specifications are the reward function and the done flag. The reward function for the StreetFighterAgents is seperated into it's own lua script to make designing a more complex reward function easier. The script can be imported and pointed to for use by gym-retro's environment for it's reward function by including the code snippet in scenario.json as follows:

```

"reward": {
        "script": "lua:calculate_reward"
    },
"scripts": [
        "reward_script.lua"
    ],

```

#### Reward Function

The reward function specifies what variables make up the reward function and what weights are assigned, whether that be positive or negative, to each variable. After each action is taken by an agent a reward calculated by this function is returned to the agent. This is then recorded and stored for later training after all fights in an epoch are finished. For now the default reward function utilizes the agent's score, agent's health, the enemy health, the number of rounds the agent has won, and the number of rounds the enemy has won. 

#### Done

Done is a flag that signifies whether the current environment has completed. Currently Done is set if the enemy or the agent get two round wins, which in game is what determines if a match is over. So once the match is over the agent moves onto the next save state.

---
## Generating New Save States

Save states are generated by a user actually saving their games state while playing in an emulator. In order to make new save states to contribute to the variety of matches your agent will play in you have to actually play the Street Fighter ROM up until the point you want the agent to start at. 

### Installing the Emulator

Retroarch is the emulator that is needed to generate the correct save states under the hood. It can be installed at:  
https://www.retroarch.com/?page=platforms


### Preparing the Cores

Retroarch needs a core of the architecture it is trying to simulate. The Street Fighter ROM we are working with is for the Sega Genisis. Retro actually has a built in core that can be copy and pasted into Retroarchs core folder and this is their recommended installation method. However finding the retroarch installation folder can be difficult and so can finding the cores in the Retro library. Instead open up Retroarch and go into Load Core. Inside Load Core scroll down and select download core. Scroll way down until you see genesis_plus_gx_libretro.so.zip and install it. Now go back to the main menu and select Load Content. Navigate to the Street Fighter folder at the top level of the repo and load the rom.md file. From here the game should load up correctly.

### Saving states

F2 is the shortcut key that saves the current state of the game. The state is saved to the currently selected game state slot. This starts at slot zero and can be incremented with the F6 key and decremented with the F7 key. When a fight is about to start that you want to create a state for hit F2. Then I would recommend incrementing the save slot by pressing F6 so that if you try to save another state you don't accidentally overwrite the last state you saved. There are 8 slots in total. By pressing F5 and going to view->settings-Directory you can control where the save states are stored. The states will be saved with the extension of 'state' plus the number of the save slot it was saved in. To prep these for usage cleave off the number at the end of each extension and rename each file to the name of the fighter that the agent will be going up against plus some other context information if necessary. Then move these ROMS into the game files inside of retro like when preparing the game files after the initial cloning of the repo. Once inside that repo each state should be zipped independently of one another. Once this happens the extension will now be .zip, remove this from the extension so that the extension still remains .state. The states are now ready to be loaded by the agent. Every time you load up the emulator decrement all the way back to zero again. 

---
# Further Help

If you have any further questions on how to use or modify this project feel free to open up an issue so that others can see the discussion and benifit from the answer. However before asking any issues please check to see if your issue has been answered before to avoid redundancy. If you have any questions regarding contributing please refer to the contributing guidelines for more information. 

---
## References:
https://github.com/openai/retro/issues/33 (outdated but helpful)   
https://medium.com/aureliantactics/integrating-new-games-into-retro-gym-12b237d3ed75 (Very helpful for writing the json files) 
https://github.com/keon/deep-q-learning (Someones basic implementation of DeepQ in python) 

https://www.youtube.com/watch?v=JgvyzIkgxF0 (reinforcement learning intro video)   
https://www.youtube.com/watch?v=0Ey02HT_1Ho (more advanced techniques)   
http://karpathy.github.io/2016/05/31/rl/ (good article on basic reinforcement learning)   
https://towardsdatascience.com/reinforcement-learning-lets-teach-a-taxi-cab-how-to-drive-4fd1a0d00529 (article on deep q learning for learning atari games)   
