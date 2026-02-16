import arcade
import math
import random

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
    
    def move(self, speed):
        rad = math.radians(self.dir)
        self.speed_x += math.sin(rad) * speed
        self.speed_y += math.cos(rad) * speed
    
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
        
        drift = 0.99
        self.speed_x *= drift
        self.speed_y *= drift
        self.speed_dir *= drift
        
        if self.moving:
            self.move(0.1)
        if self.steering_right:
            self.speed_dir += 0.02
            self.move(0.03)
        if self.steering_left:
            self.speed_dir -= 0.02
            self.move(0.03)
        
        self.dir %= 360
            
        return super().update(delta_time, *args, **kwargs)

class Player(Rocket):
    def __init__(self, game):
        super().__init__(game, "./Assets/player.png")
        self.x = 100
        self.y = -100
        self.dir = 0
        self.speed_x = -2
        self.speed_y = 2
        self.speed_dir = -0.5

class Alien(Rocket):
    def __init__(self, game, x, y):
        self.type = random.randint(1, 3)
        image = [
            "./Assets/alien1.png",
            "./Assets/alien2.png",
            "./Assets/alien3.png"
        ][self.type - 1]
        super().__init__(game, image)
        self.x = x
        self.y = y
        self.dir = random.random() * 360

if __name__ == "__main__":
    import game
    game.main()