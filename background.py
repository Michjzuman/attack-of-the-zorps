import arcade
import math
import random

class Star(arcade.Sprite):
    def __init__(self, game):
        self.type = random.choices(
            [1, 2, 3, 4],
            weights = [200, 50, 20, 1]
        )[0]
        self.distance = random.random()
        super().__init__(f"./Assets/star{self.type}.png")
        self.scale = 0.15
        self.game = game
        
        self.x = random.randint(-1000, 1000)
        self.y = random.randint(-1000, 1000)
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        distance = (8 - (self.type + self.distance)) * 4 + 1
        
        camera_offset_x = (
            self.game.player.speed_x * self.game.camera_offset +
            self.game.player.x / distance
        ) 
        camera_offset_y = (
            self.game.player.speed_y * self.game.camera_offset +
            self.game.player.y / distance
        )
        
        self.center_x = self.game.width / 2 - camera_offset_x + self.x
        self.center_y = self.game.height / 2 - camera_offset_y + self.y
        
        return super().update(delta_time, *args, **kwargs)


if __name__ == "__main__":
    import game
    game.main()