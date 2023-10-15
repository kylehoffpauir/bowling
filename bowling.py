class Game():
    def __init__(self):
        self.gameScore = {1: [], 2: [], 3: [],
                     4: [], 5: [], 6: [],
                     7: [], 8: [], 9: [],
                     10: []}
        self.name = self.getUser()
        self.playGame()

    def getUser(self):
        name = input("What is your name? ")
        print("Hello " + name + "!")
        return name

    def playGame(self):
        print("---- STARTING A NEW GAME ----")
        # 10 frames
        for frame in range(1, 12):
            print("Frame " + str(frame))
            # 2 throws per frame
            self.throwBall(frame)
            # print scoreboard after each frame
            self.printScore()
        print("---- GAME OVER ----")
        self.printScore()

    def throwBall(self, frame):
        # using this while loop instead of a for loop because we may need to repeat a throw on invalid input
        # TODO add 10th frame logic
        throw = 1
        while throw < 3:
            print("Throw " + str(throw) + " of 2")
            pinsKnocked = input("Enter score: ").upper()
            # validate input
            if not self.validateScore(pinsKnocked, throw):
                print("Invalid input, try again")
                continue
            # if we get a strike, we are done with the frame
            if pinsKnocked == "X" or pinsKnocked == 10:
                self.gameScore[frame].append("X")
                throw += 1
                break
            # only allow spare on second throw
            elif (pinsKnocked == "/") or (throw == 2 and self.gameScore[frame][0] + int(pinsKnocked) == 10):
                self.gameScore[frame].append("/")
                throw += 1
                break
            # otherwise, add score to frame as normal
            else:
                self.gameScore[frame].append(int(pinsKnocked))
                throw += 1

    def validateScore(self, score, throw):
        # valid inputs are only [X, /, 1-10] IFF / is a / on the second throw
        #print(str(score in ["X", "/", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]) + " " + str(throw == 2 and score == "/"))
        return True if (throw == 2 and score == "/") \
            else (score in ["X", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

    # TODO fix the scoring for strikes and spares
    def calculateScore(self):
        totalScore = 0
        for x in self.gameScore:
            if len(self.gameScore[x]) == 0:
                continue
            if self.gameScore[x][0] == "X":
                # A strike earns 10 points plus the sum of your next two shots.
                if self.gameScore[x+1][0] and self.gameScore[x+1][1]:
                    totalScore += 10 + (self.gameScore[x+1][0] + self.gameScore[x+1][1])
                else:
                    totalScore += 10
            elif self.gameScore[x][1] == "/":
                # A spare earns 10 points plus the sum of your next one shot.
                if self.gameScore[x+1][0]:
                    totalScore += 10 + self.gameScore[x+1][0]
                else:
                    totalScore += 10
            elif len(self.gameScore[x]) > 2 and x == 10:
                totalScore += sum(self.gameScore[x])
            else:
                totalScore += self.gameScore[x][0] + self.gameScore[x][1]
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
        print("_________________________________________________________________________________________")
        for i in range(1, 12):
            print("|\t" + str(i) + "\t", end="")
        print("|")
        # print the results of each frame from the gameScore dictionary
        # updates in "real time" ie. after each throw - which is why we check the dict entry's array length
        for x in self.gameScore:
            print("| ", end = "")
            # if the frame is empty, print nothing for that frame
            if len(self.gameScore[x]) == 0:
                print("\t\t", end="")
            # if the frame is one element, either throw 1/2 or a strike, print that
            elif len(self.gameScore[x]) == 1:
                print(" " + str(self.gameScore[x][0]) + "\t", end="")
            # if the frame is two elements, print the score for each throw
            elif len(self.gameScore[x]) == 2:
                print(" " + str(self.gameScore[x][0]) + "-" + str(self.gameScore[x][1]) + "\t", end="")
            # the last thing to do is to print the right border (+ a newline)
            if x == 11:
                print("|")

        # this is embarassingly ugly but it makes the scoreboard look nice so
        print("| TOTAL = " + str(self.calculateScore()) + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t|")
        print("-----------------------------------------------------------------------------------------")


# start a new game on run
game = Game()
