from pygame.locals import *
import pygame
import player
import maze 

class App:
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_player = None
        self._image_block = None
        self._image_flag = None
        self.maze = maze.Maze(10)
        self.player = player.Player(self.maze.Block_size, self.maze)
 
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
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        clock = pygame.time.Clock()
 
        while( self._running ):
            clock.tick(10)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            if (keys[K_LEFT]):
                self.player.moveLeft()
 
            if (keys[K_UP]):
                self.player.moveUp()
 
            if (keys[K_DOWN]):
                self.player.moveDown()
 
            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()