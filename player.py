import math

class Player:
    x = 50
    y = 50
    speed = 50
    maze = None

    def __init__(self, block_size, maze):
        self.x = block_size
        self.y = block_size
        self.speed = block_size
        self.maze = maze

    def moveRight(self):
        new_indx = convert_to_index(self.x + self.speed, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 :
            self.x = self.x + self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 0
            return 1
        elif self.maze.maze[new_indx] == 1 :
            return 0
        elif self.maze.maze[new_indx] == 3 :
            return 10
 
    def moveLeft(self):
        new_indx = convert_to_index(self.x - self.speed, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 :
            self.x = self.x - self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 0
            return 1
        elif self.maze.maze[new_indx] == 1 :
            return 0
        elif self.maze.maze[new_indx] == 3 :
            return 10
        
    def moveUp(self):
        new_indx = convert_to_index(self.x,self.y - self.speed, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 :
            self.y = self.y - self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 0
            return 1
        elif self.maze.maze[new_indx] == 1 :
            return 0
        elif self.maze.maze[new_indx] == 3 :
            return 10
 
    def moveDown(self):
        new_indx = convert_to_index(self.x,self.y + self.speed, math.sqrt(len(self.maze.maze)), self.speed)
        prev_indx = convert_to_index(self.x, self.y, math.sqrt(len(self.maze.maze)), self.speed)
        if self.maze.maze[new_indx] == 0 :
            self.y = self.y + self.speed
            self.maze.maze[new_indx] = 2
            self.maze.maze[prev_indx] = 0
            return 1
        elif self.maze.maze[new_indx] == 1 :
            return 0
        elif self.maze.maze[new_indx] == 3 :
            return 10

def convert_to_index(x, y, size, block):
    new_x = x / block
    new_y = y / block
    return int((new_y) * size + new_x)