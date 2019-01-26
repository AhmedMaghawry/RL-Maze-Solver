import math

#Player Object represent the Agent and its position in the maze
class Player:
    # x-axis position for the agent default (1) 50 because of the size of the image
    x = 50
    # y-axis position for the agent default (1) 50 because of the size of the image
    y = 50
    # The step size of the agent default (1) 50 because of the size of the image
    speed = 50
    #The maze array consist of one the 8 numbers as follow : 
    # 0 : An empty cell
    # 1 : A block cell
    # 2 : The Player cell
    # 3 : The Flag(Goal) Cell
    # 4 : Previous move down
    # 5 : Previous move up
    # 6 : Previous move left
    # 7 : Previous move right
    maze = None

    def __init__(self, block_size, maze):
        self.x = block_size
        self.y = block_size
        self.speed = block_size
        self.maze = maze

    #Function to move the agent right and put the dirction on the previous cell
    def moveRight(self):
        new_indx = convert_to_index(self.x + self.speed, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 or self.maze.maze[new_indx] == 3:
            self.x = self.x + self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 7
 
    #Function to move the agent left and put the dirction on the previous cell
    def moveLeft(self):
        new_indx = convert_to_index(self.x - self.speed, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 or self.maze.maze[new_indx] == 3 :
            self.x = self.x - self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 6
        
    #Function to move the agent up and put the dirction on the previous cell
    def moveUp(self):
        new_indx = convert_to_index(self.x,self.y - self.speed, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 or self.maze.maze[new_indx] == 3 :
            self.y = self.y - self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 5
 
    #Function to move the agent down and put the dirction on the previous cell
    def moveDown(self):
        new_indx = convert_to_index(self.x,self.y + self.speed, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 or self.maze.maze[new_indx] == 3 :
            self.y = self.y + self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 4

#Convert the index with 2d to 1d to be accessable in the 1d maze
def convert_to_index(x, y, size, block):
    new_x = x / block
    new_y = y / block
    return int((new_y) * size + new_x)