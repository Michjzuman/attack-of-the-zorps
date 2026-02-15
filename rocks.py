import arcade
import random
import math

class Planet(arcade.Sprite):
    def __init__(self, game):
        super().__init__("./Assets/earth.png")
        self.scale = 0.15
        self.game = game
        
        self.x = 0
        self.y = 0
        self.dir = 0
        
        self.speed_x = 0.07
        self.speed_y = -0.05
        self.speed_dir = 0.1
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        camera_offset_x = self.game.player.speed_x * self.game.camera_offset
        camera_offset_y = self.game.player.speed_y * self.game.camera_offset
        
        self.center_x = (
            self.game.width / 2 - camera_offset_x -
            self.game.player.x + self.x
        )
        self.center_y = (
            self.game.height / 2 - camera_offset_y -
            self.game.player.y + self.y
        )
        self.angle = self.dir
        
        self.x += self.speed_x
        self.y += self.speed_y
        self.dir += self.speed_dir
        
        self.dir %= 360


if __name__ == "__main__":
    import game
    game.main()