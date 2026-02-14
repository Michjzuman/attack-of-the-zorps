import arcade
import math

class Rocket(arcade.Sprite):
    def __init__(self, window, image):
        super().__init__(image)
        self.scale = 0.15
        self.window = window
        
        self.x = 0
        self.y = 0
        self.dir = 0
        
        self.speed_x = 0
        self.speed_y = 100
        self.speed_dir = 0
        
        self.moving = False
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        camera_offset_x = self.speed_x * 10
        camera_offset_y = self.speed_y * 10
        
        self.center_x = self.window.width / 2 - camera_offset_x
        self.center_y = self.window.height / 2 - camera_offset_y
        self.angle = self.dir
        
        self.x += self.speed_x
        self.y += self.speed_y
        self.dir += self.speed_dir
        
        drift = 0.99
        self.speed_x *= drift
        self.speed_y *= drift
        self.speed_dir *= drift
        
        if self.moving:
            self.speed_x += math.sin(self.dir) * 0.2
            self.speed_y += math.cos(self.dir) * 0.2
            
        return super().update(delta_time, *args, **kwargs)


if __name__ == "__main__":
    import game
    game.main()