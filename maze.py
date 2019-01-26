import random

class Maze:
    def __init__(self, size):
       self.N = size
       self.Block_size = 50
       tot = (size + 2) * (size + 2)
       flagx = random.randint(size,(size + 2) * (size + 2) - (size + 2) - 1)
       self.maze = generateMap(size, flagx)
    
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