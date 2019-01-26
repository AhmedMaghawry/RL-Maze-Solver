from pygame.locals import *
import pygame
import player
import maze 
from grid import MazeMDP
import math
from tkinter import *
from tkinter import messagebox

import numpy as np

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_player = None
        self._image_block = None
        self._image_flag = None
        self._image_down = None
        self._image_right = None
        self._image_left = None
        self._image_up = None
        self._moves = []
        self.maze = maze.Maze(10)
        self.maze_mdp= None
        self.player = player.Player(self.maze.Block_size, self.maze)
        self.start = None
        self.utilty = None
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode([(self.maze.N + 2) * self.maze.Block_size,(self.maze.N + 2) * self.maze.Block_size])
        pygame.display.set_caption('Maze Runner')
        pygame.display.flip()
        self._running = True
        self._image_player = pygame.image.load('player.png')
        self._image_block = pygame.image.load('block.png')
        self._image_flag = pygame.image.load('flag.png')
        self._image_down = pygame.image.load('down.png')
        self._image_up = pygame.image.load('up.png')
        self._image_right = pygame.image.load('right.png')
        self._image_left = pygame.image.load('left.png')
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
 
    def on_render(self):
        self._display_surf.fill((255,255,255))
        self._display_surf.blit(self._image_player,(self.player.x,self.player.y))
        self.maze.draw(self._display_surf, self._image_block, self._image_flag, self._image_down, self._image_up, self._image_left, self._image_right)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
        
    def generate_MDP_grid(self):
        obstacle = []
        shape = (self.maze.N+2,self.maze.N+2)
        maze_2d = np.reshape(self.maze.maze, shape)
        for i in range (shape[0]):
            for j in range (shape[1]):
                if(maze_2d[i][j]==3): 
                    goal = (i,j)
                if(maze_2d[i][j]==1):   
                    obstacle.append((i,j))
                if(maze_2d[i][j]==2):   
                    self.start = (i,j)
        default_reward = 0
        goal_reward = 1
        reward_grid = np.zeros(shape) + default_reward
        reward_grid[goal] = goal_reward
        for i in range (len(obstacle)):
            reward_grid[obstacle[i]] = -0.1
        terminal_flag = np.zeros_like(reward_grid, dtype=np.bool)
        terminal_flag[goal] = True
        obstacle_flag = np.zeros_like(reward_grid, dtype=np.bool)
        obstacle_flag[1, 1] = True
        self.maze_mdp = MazeMDP(reward_grid=reward_grid,
                          obstacle_flag=obstacle_flag,
                          terminal_flag=terminal_flag,
                          action_probabilities=[
                              (-1, 0.1),
                              (0, 0.8),
                              (1, 0.1),
                          ],
                          no_action_probability=0.0)
    
        
    def solve_maze(self):
        mdp_solvers = {'Value Evalution': self.maze_mdp.value_evalution,
                       'Policy Evalution': self.maze_mdp.policy_evalution}
        global final_utlity
        for solver_name, solver_fn in mdp_solvers.items():
            print('Final result of {}:'.format(solver_name))
            policy_grids, utility_grids = solver_fn(iterations=30, discount=0.5)
            final_utlity = utility_grids[:, :, -1]
            final_policy = policy_grids[:, :, -1]
            print(final_utlity)
            print(final_policy)
        self.utilty = final_utlity
            
    def reach_goal(self):    
        print("Steps to reach to goal from start are :")
        stop_counter = len(self.utilty) * len(self.utilty)
        iterator = self.start
        while (self.utilty[iterator[0]][iterator[1]] != 1 and stop_counter != 0) :
            
            max_num = 0.0
            #0 : Down, 1 : Up, 2 : Left, 3 : Right
            direction = 0
            #Down
            if iterator[0] + 1 < len(self.utilty) and (self.utilty[iterator[0] + 1][iterator[1]] + 10) >= max_num :
                max_num = self.utilty[iterator[0] + 1][iterator[1]] + 10
                direction = 0
            #Up
            if iterator[0] - 1 >= 0 and (self.utilty[iterator[0] - 1][iterator[1]] + 10) >= max_num :
                max_num = self.utilty[iterator[0] - 1][iterator[1]] + 10
                direction = 1
            #Left
            if iterator[1] - 1 >= 0 and (self.utilty[iterator[0]][iterator[1] - 1] + 10) >= max_num :
                max_num = self.utilty[iterator[0]][iterator[1] - 1] + 10
                direction = 2
            #Right
            if iterator[1] + 1 < len(self.utilty) and (self.utilty[iterator[0]][iterator[1] + 1] + 10) >= max_num :
                max_num = self.utilty[iterator[0]][iterator[1] + 1] + 10
                direction = 3
            
            if direction == 0 :
                print("Move Down")
                #self._display_surf.blit(self._image_down,(iterator[0],iterator[1]))
                #self.player.moveDown()
                self._moves.append(0)
                iterator = [iterator[0] + 1,iterator[1]]
            elif direction == 1 :
                print("Move Up")
                #self._display_surf.blit(self._image_up,(iterator[0],iterator[1]))
                #self.player.moveUp()
                self._moves.append(1)
                iterator = [iterator[0] - 1,iterator[1]]
            elif direction == 2 :
                print("Move Left")
                #self._display_surf.blit(self._image_left,(iterator[0],iterator[1]))
                #self.player.moveLeft()
                self._moves.append(2)
                iterator = [iterator[0],iterator[1] - 1]
            else:
                print("Move Right")
                #self.player.moveRight()
                #self._display_surf.blit(self._image_right,(iterator[0],iterator[1]))
                self._moves.append(3)
                iterator = [iterator[0],iterator[1] + 1]
            stop_counter-=1
            
    def on_execute(self):
        
        if self.on_init() == False:
            self._running = False
        
        clock = pygame.time.Clock()
        
        iterat = 0
        flag = True
        
        while( self._running ):
            clock.tick(5)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if iterat < len(self._moves):
                if(self._moves[iterat] == 0):
                    self.player.moveDown()
                    #self._display_surf.blit(self._image_down,(self.player.x,self.player.y))
                    #self.player.maze.maze[convert_to_index(self.player.x, self.player.y, math.sqrt(len(self.maze.maze)), 50)] = 7
                elif(self._moves[iterat] == 1):
                    self.player.moveUp()
                    #self._display_surf.blit(self._image_up,(self.player.x,self.player.y))
                    #self.player.maze.maze[convert_to_index(self.player.x, self.player.y, math.sqrt(len(self.maze.maze)), 50)] = 5
                elif(self._moves[iterat] == 2):
                    self.player.moveLeft()
                    #self._display_surf.blit(self._image_left,(self.player.x,self.player.y))
                    #self.player.maze.maze[convert_to_index(self.player.x, self.player.y, math.sqrt(len(self.maze.maze)), 50)] = 6
                elif(self._moves[iterat] == 3):
                    self.player.moveRight()
                    #self._display_surf.blit(self._image_right,(self.player.x,self.player.y))
                    #self.player.maze.maze[convert_to_index(self.player.x, self.player.y, math.sqrt(len(self.maze.maze)), 50)] = 7
            elif flag :
                flag= False
                if (not isGoalExsist(self.player.maze.maze)) :
                    #Display reached to goal
                    print("Goal Reached")
                    Tk().wm_withdraw() #to hide the main window
                    messagebox.showinfo('Result','Player Reached to the Goal')
                else :
                    #Goal cant Reached
                    print("Goal Not Reached")
                    Tk().wm_withdraw() #to hide the main window
                    messagebox.showerror('Result','Player Cant Reached to the Goal')
            iterat += 1
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        

def isGoalExsist(maze_arr):
    return 3 in maze_arr

def convert_to_index(x, y, size, block):
    new_x = x / block
    new_y = y / block
    return int((new_y) * size + new_x)
 
if __name__ == "__main__" :
    theApp = App()
    theApp.generate_MDP_grid()
    theApp.solve_maze()
    theApp.reach_goal()
    theApp.on_execute()
    
   
    