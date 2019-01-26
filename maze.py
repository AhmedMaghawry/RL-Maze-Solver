import random

#Maze Object represent the Maze (The Environment)
class Maze:
    def __init__(self, size):
        #The size of the Maze
       self.N = size
       #The image size of the block
       self.Block_size = 50
       tot = (size + 2) * (size + 2)
       #Flag location (random in the last quartar in the maze)
       flagx = random.randint(size,(size + 2) * (size + 2) - (size + 2) - 1)
       #The 1d array of the maze which consist of :
       # 0 : An empty cell
       # 1 : A block cell
       # 2 : The Player cell
       # 3 : The Flag(Goal) Cell
       # 4 : Previous move down
       # 5 : Previous move up
       # 6 : Previous move left
       # 7 : Previous move right
       self.maze = generateMap(size, flagx)
    
    # This function takes as input :
    # 1- The game window surface.
    # 2- The player image
    # 3- The flag image
    # 4- The down image
    # 5- The up image
    # 6- The right image
    # 7- The left image
    def draw(self,display_surf,image_surf, image_flag, image_down, image_up, image_left, image_right):
       bx = 0
       by = 0
       for i in range(0,(self.N + 2)*(self.N + 2)):
           if self.maze[ bx + (by*(self.N + 2)) ] == 1:
               display_surf.blit(image_surf,( bx * self.Block_size , by * self.Block_size))
           elif self.maze[ bx + (by*(self.N + 2)) ] == 3:
               display_surf.blit(image_flag,( bx * self.Block_size , by * self.Block_size))
           elif self.maze[ bx + (by*(self.N + 2)) ] == 4:
               display_surf.blit(image_down,( bx * self.Block_size , by * self.Block_size))
           elif self.maze[ bx + (by*(self.N + 2)) ] == 5:
               display_surf.blit(image_up,( bx * self.Block_size , by * self.Block_size))
           elif self.maze[ bx + (by*(self.N + 2)) ] == 6:
               display_surf.blit(image_left,( bx * self.Block_size , by * self.Block_size))
           elif self.maze[ bx + (by*(self.N + 2)) ] == 7:
               display_surf.blit(image_right,( bx * self.Block_size , by * self.Block_size))
           bx = bx + 1
           if bx > (self.N + 1):
               bx = 0 
               by = by + 1


# Random maze generator which takes the size of the maze and the location of the flag
# The blocks are represent at most 1/4 of the maze
def generateMap(size, flag):
    s = size + 2
    res = [0]*s*s 
    for i in range(0, s * s) :
        if i == s + 1 :
            res[i] = 2
        elif i == flag :
            res[i] = 3
        elif i % s == 0 or (i % s) - s +1 == 0:
            res[i] = 1
        elif i < s or i >= (s*s - s): 
            res[i] = 1
        else :
            num = random.randint(0,12)
            if num % 4 == 1:
                res[i] = 1
            else:
                res[i] = 0
    return res