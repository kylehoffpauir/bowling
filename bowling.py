# import to save/load user data dictionary
import pickle

class Game():
    """
    possible improvements:
        add support for multiple players - this would be an extra loop after the frames but before the throws
                                           would be simple enough - when a new game is started, pass in players array
                                           and loop through each player between frames but before throws. Give each
                                           player a gameScore dict

        clean up ui, maybe even add a gui. If we go really crazy we could make this a webapp and have it run in a browser

        add a database to store scores and player names - right now just using python pickle library to save/load user info

        add a way to view previous games' entire scoreboards -- right now we can only see the high scores of users

        10th frame logic made things pretty messy. We could clean that up by only calling calculateScore() after the 10th
            frame is complete. This would require a little bit of refactoring, but would reduce the number of if statements
            in calculateScore() and would streamline the logic a bit.
            This comes at the cost of having a scoreboard that doesn't update until the 10th frame is complete, which
            is a little less user friendly. I think the current implementation is good, but it comes at the cost of
            some messy if checks littered throughout the code.
    """

    def __init__(self, user):
        self.gameScore = {1: [], 2: [], 3: [],
                     4: [], 5: [], 6: [],
                     7: [], 8: [], 9: [],
                     10: []}
        self.user = user
        self.name = user.getName()

    def playGame(self):
        print("---- STARTING A NEW GAME ----")
        # 10 frames
        for frame in range(1, 11):
            print("Frame " + str(frame))
            # 2 throws per frame, if it's the 10th handle a little differently.
            self.throwBall(frame, frame==10)
            # print scoreboard after each frame
            self.printScore()
        print("---- GAME OVER ----")
        self.printScore()
        return self.calculateScore()

    def throwBall(self, frame, tenthFrame=False):
        # using this while loop instead of a for loop because we may need to repeat a throw on invalid input
        throw = 1
        tenthThrow = 1
        while throw < 3:
            print("Throw " + str(throw) + " of 2")
            pinsKnocked = input("Enter score: ").upper()
            # validate input
            if not self.validateScore(pinsKnocked, throw):
                print("Invalid input, try again")
                continue
            if throw == 2 and self.convert(self.gameScore[frame][0]) + self.convert(pinsKnocked) > 10 and pinsKnocked != "/":
                print("Invalid input, try again")
                continue
            # if we get a strike, we are done with the frame
            if pinsKnocked == "X" or pinsKnocked == 10:
                self.gameScore[frame].append("X")
                # if we are on the 10th frame, we get a bonus throw
                if tenthFrame:
                    tenthThrow += 1
                    if tenthThrow > 3:
                        break
                    continue
                break
            # only allow spare on second throw
            elif (pinsKnocked == "/") or (throw == 2 and self.gameScore[frame][0] + int(pinsKnocked) == 10):
                self.gameScore[frame].append("/")
                # if we are on the 10th frame, we get a bonus throw
                if tenthFrame:
                    tenthThrow += 1
                    if tenthThrow > 4:
                        break
                    continue
                break
            # otherwise, add score to frame as normal
            else:
                self.gameScore[frame].append(int(pinsKnocked))
                if tenthFrame:
                    tenthThrow += 1
                    if tenthThrow > 4:
                        break
                throw += 1

    def validateScore(self, score, throw):
        # valid inputs are only [X, /, 0-10] IFF / is a / on the second throw
        # print(str(score in ["X", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]) + " " + str(throw == 2 and score == "/"))
        return True if (throw == 2 and score == "/") \
            else (score in ["X", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    def convert(self, score):
        if score == "X" or score == "/":
            return 10
        else:
            return int(score)

    def calculateScore(self):
        totalScore = 0
        for x in range(1, 11):  # Iterate through all 10 frames
            if len(self.gameScore[x]) == 0:
                continue
            # if we are on the 10th frame, we need to handle the bonus throws, sum the frame and add to total
            if x == 10:
                totalScore += sum(self.convert(element) for element in self.gameScore[x])
                if self.gameScore[ x -1][0] == "X" or self.gameScore[ x -1][1] == "/":
                    totalScore += sum(self.convert(element) for element in self.gameScore[x])
            # on a strike, add 10 + next two throws. if 9th frame, wait until 10th frame to add bonus throws
            elif self.gameScore[x][0] == "X":
                if x == 9:
                    totalScore += 10
                elif len(self.gameScore[x + 1]) >= 2:
                    totalScore += 10 + (self.convert(self.gameScore[x + 1][0]) + self.convert(self.gameScore[x + 1][1]))
                elif len(self.gameScore[x + 1]) == 1 and self.gameScore[x + 1][0] == "X":
                    if len(self.gameScore[x + 2]) > 0:
                        totalScore += 10 + \
                                    (self.convert(self.gameScore[x + 1][0]) + self.convert(self.gameScore[x + 2][0]))
                else:
                    totalScore += 10
            # on a spare, add 10 + next throw, if 9th frame, wait until 10th frame to add bonus throw
            elif self.gameScore[x][1] == "/":
                if x == 9:
                    totalScore += 10
                elif len(self.gameScore[x + 1]) > 0:
                    totalScore += 10 + self.convert(self.gameScore[x + 1][0])
                else:
                    totalScore += 10
            # on a normal two throw frame, add the sum of the frame
            else:
                totalScore += self.gameScore[x][0] + self.gameScore[x][1]
            # cap score at 300
            if totalScore >= 300:
                totalScore = 300
                print("\t\tPERFECT GAME!")
        return totalScore

    """
    http://www.fryes4fun.com/Bowling/scoring.htm
    Scoring Rules
    Strike
    
    If you knock down all 10 pins in the first shot of a frame, you get a strike.
    How to score: A strike earns 10 points plus the sum of your next two shots.
    
    Spare
    
    If you knock down all 10 pins using both shots of a frame, you get a spare.
    How to score: A spare earns 10 points plus the sum of your next one shot.
    
    Open Frame
    
    If you do not knock down all 10 pins using both shots of your frame (9 or fewer pins knocked down), you have an open frame.
    How to score: An open frame only earns the number of pins knocked down.
    
    The 10th Frame
    
    The 10th frame is a bit different:
    If you roll a strike in the first shot of the 10th frame, you get 2 more shots.
    If you roll a spare in the first two shots of the 10th frame, you get 1 more shot.
    If you leave the 10th frame open after two shots, the game is over and you do not get an additional shot.
    How to Score: The score for the 10th frame is the total number of pins knocked down in the 10th frame.
    """

    def printScore(self):
        # make output to look like a scoreboard for bowling
        print(self.name + "'s Scoreboard")
        print("_________________________________________________________________________________")
        for i in range(1, 11):
            print("|\t" + str(i) + "\t", end="")
        print("|")
        # print the results of each frame from the gameScore dictionary
        # updates in "real time" ie. after each throw - which is why we check the dict entry's array length
        for x in self.gameScore:
            print("| ", end="")
            # if the frame is empty, print nothing for that frame
            if len(self.gameScore[x]) == 0:
                print("\t\t", end="")
            # if the frame is one element, either throw 1/2 or a strike, print that
            elif len(self.gameScore[x]) == 1:
                print(" " + str(self.gameScore[x][0]) + "\t", end="")
            # if the frame is two elements, print the score for each throw
            elif len(self.gameScore[x]) == 2:
                print(" " + str(self.gameScore[x][0]) + "-" + str(self.gameScore[x][1]) + "\t", end="")
            # if the frame is more elements, print the score for each throw
            else:
                print("" + str(self.gameScore[x][0]) + "-" + str(self.gameScore[x][1]) + "-" + str(
                    self.gameScore[x][2]) + "", end="")

        # the last thing to do is to print the right border (+ a newline)
        print("|")
        # this is embarassingly ugly but it makes the scoreboard look nice so
        print("| TOTAL = " + str(self.calculateScore()) + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        print("---------------------------------------------------------------------------------")

class User():
    def __init__(self, name=None):
        self.name, self.highScore = self.getUser(name)

    def getName(self):
        return self.name

    def getHighScore(self):
        return self.highScore

    def getUser(self, name=None):
        if name is not None:
            name = input("What is your name? ")
            print("Checking saved data for: " + name)
        # check scorecard file for user entry
        # if user exists, load their scorecard and highest score
        # if user does not exist, create a new user entry
        try:
            with open('users.pkl', 'rb') as f:
                loaded_dict = pickle.load(f)
        except(FileNotFoundError):
            loaded_dict = {}
        if name in loaded_dict:
            print("Welcome back " + name + "!")
            print("High Score: " + str(loaded_dict[name]))
            return name, loaded_dict[name]
        else:
            print("Welcome " + name + "!")
            loaded_dict[name] = 0
        try:
            with open('users.pkl', 'wb') as f:
                pickle.dump(loaded_dict, f)
        except():
            print("Error saving user data")
        return name, 0

    def saveScore(self, score):
        # save the user's highest score
        try:
            with open('users.pkl', 'rb') as f:
                loaded_dict = pickle.load(f)
        except(FileNotFoundError):
            loaded_dict = {}
        if self.name in loaded_dict:
            if score > loaded_dict[self.name]:
                print("New High Score!")
                print("Saving new high score for " + self.name)
                loaded_dict[self.name] = score
        else:
            loaded_dict[self.name] = score
        try:
            with open('users.pkl', 'wb') as f:
                pickle.dump(loaded_dict, f)
        except():
            print("Error saving user data")


# start the game on run
# create a user
kyle = User("Kyle")
# create a game
game = Game(kyle)
# play the game
score = game.playGame()
print("Final Score: " + str(score))
# save the user's score
kyle.saveScore(score)
