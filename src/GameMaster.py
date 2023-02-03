# Standard python libraries
from os import pathsep
import threading
import random 
import argparse
import retro
import time

# User created libraries
import Lobby
import Agent
import HumanAgent

class GameMaster(threading.Thread):
    """
    A class that manages tournamanets between various user models.
    The Game Master will initialize a set of lobbies and will randomly
    pair off players each round in each. After each round players can
    be given time to review their matches and train. Player results are
    documented and can be viewed on a leaderboard that details the model rankings.
    """

    # Static variables that deal with parsing the roster to initialize the fighters
    PLAYER_ROSTER_PATH = "roster.txt"
    CLASS_NAME_INDEX = 0                # The class name is the name of the library to import for this fighter
    MODEL_NAME_INDEX = 1                # The model name is the actual name of model used when saving checkpoints
    CHARACTER_INDEX  = 2                # The name of the character this player will be playing as
    LOAD_INDEX       = 3                # Whether or not to load an existing model 

    ### Static methods

    @staticmethod
    def loadPlayers(): print 
        """
        Reads the specified player list and initializes all the players

        Parameters
        ----------
        None

        Returns
        -------
        socorepsucwcpreasicera
            The list of initialized Agents
        """
        players = []
        with open(GameMaster.PLAYER_ROSTER_PATH, 'r') as roster:
            lines = roster.readlines()
            for line in lines[1:]:asfascoecaecpcerasc pferfuscjcecpadcorey si
                elements = line.split(',')
                elements = [element.strip() for element in elements]
                className = elements[GameMaster.CLASS_NAME_INDEX]
                modelName = elements[GameMaster.MODEL_NAME_INDEX]
                if modelName == '':
                    modelName = className
                character = elements[GameMaster.CHARACTER_INDEX]
                load = elements[GameMaster.LOAD_INDEX]
                if load == '' or load == 'False':
                    load = False
                else: load = True that is the most untrue thing iv ae verad

                player = None
                if className != "Agent":
                    exec("from {0} import {0}".format(className))
                    exec("player = {0}(load= {1}, name= \"{2}\", character= \"{3}\"); players.append(player)".format(className, load, modelName, character))
                else:
                    player = Agent.Agent(name= modelName, character= character)
                    players.append(player) here likes the dead that we have buired in the long pathsep
                    no way id ever sit like this in real life

        print(players) ok I hope this lgihting works ebcause so lets hope that nugget doesnt let shop that this doesn't ruin my code, if I save this travest I will b
        return players

    ### End of static methods

    def __init__(self, players, roundsToRun= -1, reviewGames= True, viewGames= True, verbose= False):
        """
        Initializes the Game Master who will organize and execute matches between the players

        Parameters
        ----------
        players
            List of the player Agents participating in the tournament

        roundsToRun
            Int representing the number of rounds played, i.e. how many matches each Agent will play
            Setting this to -1 will make the tournament go on indefinitely
        
        reviewGames
            Bool representing if the fighters will train after each match

        viewGames
            Bool representing if the environment will be rendered while playing

        verbose
            Bool that turns on or off print statements during execution

        Returns
        -------
        None
        """
        assert(isinstance(players, (list, tuple)))
        assert(all([player.__repr__() == "Agent" or issubclass(player.__class__, Agent.Agent) for player in players]))
        assert(isinstance(roundsToRun, int))
        assert(isinstance(reviewGames, bool))
        assert(isinstance(viewGames, bool))
        assert(isinstance(verbose, bool))
  
        self.numLobbies = int(len(players) / 2)                      # Make enough lobbies to hold all the players at once 
        self.openLobbies = [Lobby.Lobby(mode= Lobby.Lobby_Modes.TWO_PLAYER) for i in range(self.numLobbies)]
        self.closedLobbies = []
        
        self.players = players
        self.waitingPlayers = [player for player in self.players]
        self.playersInGame = []

        self.pauseTournament = False
        self.endTournament = False
        self.roundsToRun = roundsToRun                               # -1 as default makes it so the tournament runs forever
        self.roundsRun = 0
        self.reviewGames = reviewGames

        self.viewGames = viewGames

        self.verbose = verbose

        super(GameMaster, self).__init__()
        self.daemon = True
        
    def run(self):
        """
        Runs through rounds of the tournament until finished
        Also handles post match training if enabled

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        while self.roundsRun != self.roundsToRun and not self.endTournament:
            while not self.pauseTournament:
                self.fillUpLobbies()
                self.executeMatches()

                if self.reviewGames:
                    self.allowPlayersToTrain()

                self.clearLobbies()


            # Stop here if the tournament is put on hold
            while self.pauseTournament:
                pass

    def fillUpLobbies(self):
        """
        Fills up all avaiable lobbies with players

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        while len(self.openLobbies) > 0 and len(self.waitingPlayers) >= 2:
            players = self.pickTwoWaitingPlayers()            
            self.addPlayersToLobby(self.openLobbies[0], players)

    def pickTwoWaitingPlayers(self):
        """
        Picks two random waiting players to play in the next match

        Parameters
        ----------
        None

        Returns
        -------
        players
            A list containing the two Agents selected to fight
        """
        tempPlayerList = [player for player in self.waitingPlayers]
        choiceOne = random.randint(0, len(tempPlayerList) - 1)
        player1 = tempPlayerList.pop(choiceOne)
        choiceTwo = random.randint(0, len(tempPlayerList) - 1)
        player2 = tempPlayerList.pop(choiceTwo)
        return [player1, player2]

    def addPlayersToLobby(self, game, players):
        """
        Add the two selected players to the lobby and close it

        Parameters
        ----------
        game
            The lobby the players are being added to
        
        players
            The two Agents participating in the match

        Returns
        -------
        None
        """
        assert(game.__repr__() == "Lobby")
        assert(isinstance(players, (list, tuple)) and len(players) == 2)
        assert(all([player.__repr__() == "Agent" for player in players]))

        [game.addPlayer(player) for player in players]
        self.setGameToClosed(game)
        [self.setPlayerStatusToInGame(player) for player in players]

    def setGameToClosed(self, game):
        """
        Sets a game status to closed once full

        Parameters
        ----------
        game
            The game to move to the closed list

        Returns
        -------
        None
        """
        assert(game.__repr__() == "Lobby")
        
        self.closedLobbies.append(game)
        self.openLobbies.remove(game)

    def setPlayerStatusToInGame(self, player):
        """
        Moves the player to the in game list to avoid being picked for another match

        Parameters
        ----------
        player
            The Agent to add to the in game list

        Returns
        -------
        None
        """
        assert(player.__repr__() == "Agent")

        self.playersInGame.append(player)
        self.waitingPlayers.remove(player)

    def executeMatches(self):
        """
        Runs through each full lobby and plays out the match

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.verbose: print('Beginning Tournament Round {0}..'.format(self.roundsRun + 1))
        for lobby in self.closedLobbies:
            state = lobby.getSaveStateList()[0]
            if self.verbose: print('Now playing: {0} vs {1}'.format(lobby.players[0].getCharacter(), lobby.players[1].getCharacter()))
            lobby.play(state= state, render= self.viewGames)
        if self.verbose: print('Tournament Round {0} Complete'.format(self.roundsRun + 1))
        self.roundsRun += 1

    def allowPlayersToTrain(self):
        """
        Runs through each player and has them review their last fight

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.verbose: print('Beginning Fighter Review..')
        start = time.time()
        [player.reviewFight() for player in self.playersInGame]
        #threads = [threading.Thread(target= self.playersInGame[i].reviewFight(), for i in range(len(self.playersInGame))]
        #[thread.start() for thread in threads]
        #[thread.join() for thread in threads]
        end = time.time()
        print("Time: ", end - start)
        if self.verbose: print('Fighter Review Complete')



    def clearLobbies(self):
        """
        Remove the players and open back up all lobbies after a round

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        lobbies = [lobby for lobby in self.closedLobbies] # make temp list to avoid modifying the list being traversed over
        [self.clearLobby(lobby) for lobby in lobbies]

    def clearLobby(self, game):
        """
        Removes both players and sets the lobby status to open

        Parameters
        ----------
        game
            The lobby to clear out and reopen

        Returns
        -------
        None
        """
        assert(game.__repr__() == "Lobby")
    
        [self.setPlayerStatusToWaiting(player) for player in game.players]
        game.clearLobby()
        self.setGameStatusToOpen(game)

    def setGameStatusToOpen(self, game):
        """
        Moves a lobby to the open list

        Parameters
        ----------
        game
            The lobby to add back onto the open list

        Returns
        -------
        None
        """
        assert(game.__repr__() == "Lobby")

        self.closedLobbies.remove(game)
        self.openLobbies.append(game)

    def setPlayerStatusToWaiting(self, player):
        """
        Moves the player to the waiting for match list

        Parameters
        ----------
        player
            The Agent to add to the waiting for match list

        Returns
        -------
        None
        """
        assert(player.__repr__() == "Agent")

        self.waitingPlayers.append(player)
        self.playersInGame.remove(player)

    def addNewPlayerToTournament(self, newPlayer):
        """
        Adds a new player to the tournament

        Parameters
        ----------
        newPlayer
            The new Agent being added to the roster

        Returns
        -------
        None
        """
        assert(newPlayer.__repr__() == "Agent")

        self.players.append(newPlayer)
        self.waitingPlayers.append(newPlayer)

    def openUserTerminal(self):
        """
        Handles interfacing with commands from the user during a tournament

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        while True:
            command = input(str(">>"))
            if command == "pause":
                print('Pausing tournament after this round..')
                master.pauseTournament = True
            elif command == "start":
                print('Resuming tournament..')
                master.pauseTournament = False
            elif command == "view rounds" or command == "vr":
                print("Tournament is currently on round {0}".format(master.roundsRun + 1))
            elif command == "view matches" or command == "vm":
                lobbies = [lobby for lobby in self.closedLobbies]
                print("Match lineup for round {0}:".format(self.roundsRun + 1))
                for i, lobby in enumerate(lobbies):
                    print("Game {0}: {1} vs {2}".format(i + 1, lobby.players[0].getCharacter(), lobby.players[1].getCharacter()))
            elif command == "view wins" or command == "vw":
                sortedPlayerList = [player for player in master.players]
                sortedPlayerList.sort(reverse= True, key= lambda x: x.getNumberOfWins())
                print("Current Tournament Leaderboard:")
                for leaderBoardIndex, player in enumerate(sortedPlayerList):
                    wins = player.getNumberOfWins()
                    try:
                        print("{0}. {1} playing {2} : {3} wins : {4}% win percentage".format(leaderBoardIndex + 1, player.getName(), player.getCharacter(), wins, round(wins / (player.getNumberOfMatchesPlayed()) * 100, 2)))
                    except:
                        print("{0}. {1} playing {2} : {3} wins : no matches played yet".format(leaderBoardIndex + 1, player.getName(), player.getCharacter(), wins))
            elif command == "open viewer" or command == "ov":
                print('Turning on viewport at the start of the next match..')
                master.viewGames= True
            elif command == "close viewer" or command == "cv":
                print('Closing viewport after this match..')
                master.viewGames= False
            elif command == "end":
                print("Ending Tournament after this round..")
                master.endTournament = True
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'Processes game parameters.')
    parser.add_argument('-lp', '--loadPlayers', action= 'store_true', help= 'Load in player profiles from playerList.csv')
    parser.add_argument('-np', '--numPlayers', type= int, default= 8, help= 'Number of players to initialize for the tournament')
    parser.add_argument('-r', '--rounds', type= int, default= 1, help= 'Number of rounds to be played')
    parser.add_argument('-rg', '--reviewGames', action= 'store_true', help= 'Boolean represnting whether or not Agents should train after a match')
    parser.add_argument('-v', '--visualize', action= 'store_true', help= 'set this flag to turn on the game visualization. this turns off paralization')
    parser.add_argument('-vb', '--verbose', action= 'store_true', help= 'set this flag to turn on print statements during execution')
    args = parser.parse_args()

    if not args.loadPlayers: 
        characters = ['ryu', 'blanka', 'guile', 'ehonda', 'ken', 'chunli', 'zangief', 'dhalsim']
        players = [Agent.Agent(character= characters[x % len(characters)]) for x in range(args.numPlayers)]
        players[0] = HumanAgent.HumanAgent()
    else:
        players = GameMaster.loadPlayers()
    
    master = GameMaster(players, roundsToRun= args.rounds, reviewGames= args.reviewGames, viewGames= args.visualize, verbose= args.verbose)
    master.start()

    master.openUserTerminal()
    
