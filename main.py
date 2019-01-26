from pygame.locals import *
import pygame
import player
import maze 
from grid import MazeMDP

import numpy as np
import matplotlib.pyplot as plt

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_player = None
        self._image_block = None
        self._image_flag = None
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
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        pass
 
    def on_render(self):
        self._display_surf.fill((255,255,255))
        self._display_surf.blit(self._image_player,(self.player.x,self.player.y))
        self.maze.draw(self._display_surf, self._image_block, self._image_flag)
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
        plt.figure()
        self.maze_mdp.plot_policy(final_utlity,final_policy)
        self.utilty = final_utlity
        plt.show()
            
    def reach_goal(self):
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
                self.player.moveDown()
                iterator = [iterator[0] + 1,iterator[1]]
            elif direction == 1 :
                print("Move Up")
                self.player.moveUp()
                iterator = [iterator[0] - 1,iterator[1]]
            elif direction == 2 :
                print("Move Left")
                self.player.moveLeft()
                iterator = [iterator[0],iterator[1] - 1]
            else:
                print("Move Right")
                self.player.moveRight()
                iterator = [iterator[0],iterator[1] + 1]
            stop_counter-=1
            
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        clock = pygame.time.Clock()
        
        while( self._running ):
            clock.tick(10)
            
            pygame.event.pump()
            keys = pygame.key.get_pressed()
 
#            if (keys[K_RIGHT]):
#                self.player.moveRight()
# 
#            if (keys[K_LEFT]):
#                self.player.moveLeft()
# 
#            if (keys[K_UP]):
#                self.player.moveUp()
# 
#            if (keys[K_DOWN]):
#                self.player.moveDown()
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        
    
 
if __name__ == "__main__" :
    theApp = App()
    theApp.generate_MDP_grid()
    theApp.solve_maze()
    theApp.reach_goal()
    theApp.on_execute()
    
   
    