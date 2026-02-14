import arcade
import math

class Rocket(arcade.Sprite):
    def __init__(self, game, image):
        super().__init__(image)
        self.scale = 0.15
        self.game = game
        
        self.x = 0
        self.y = 0
        self.dir = 0
        
        self.speed_x = 0
        self.speed_y = 0
        self.speed_dir = 0
        
        self.moving = False
        self.steering_right = False
        self.steering_left = False
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        camera_offset_x = self.speed_x * self.game.camera_offset
        camera_offset_y = self.speed_y * self.game.camera_offset
        
        self.center_x = self.game.width / 2 - camera_offset_x
        self.center_y = self.game.height / 2 - camera_offset_y
        self.angle = self.dir
        
        self.x += self.speed_x
        self.y += self.speed_y
        self.dir += self.speed_dir
        
        drift = 0.99
        self.speed_x *= drift
        self.speed_y *= drift
        self.speed_dir *= drift
        
        def move(speed):
            rad = math.radians(self.dir)
            self.speed_x += math.sin(rad) * speed
            self.speed_y += math.cos(rad) * speed
        
        if self.moving:
            move(0.5)
        if self.steering_right and not self.steering_left:
            self.speed_dir += 0.05
            move(0.5)
        elif self.steering_left:
            self.speed_dir -= 0.05
            move(0.2)
        
        self.dir %= 360
            
        return super().update(delta_time, *args, **kwargs)


if __name__ == "__main__":
    import game
    game.main()