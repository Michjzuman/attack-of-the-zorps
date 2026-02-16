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
        image = [
            "./Assets/star1.png",
            "./Assets/star2.png",
            "./Assets/star3.png",
            "./Assets/star4.png"
        ][self.type - 1]
        super().__init__(image)
        self.scale = 0.15
        self.game = game
        
        self.x = random.randint(-1400, 1400)
        self.y = random.randint(-1400, 1400)
    
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

def draw_grid(game):
    l = 10000
    lines = 100
    color = (10, 20, 10)
    
    start_x = (
        game.width / 2 - l / 2 - game.player.x -
        (game.player.speed_x * game.camera_offset)
    )
    
    start_y = (
        game.height / 2 - l / 2 - game.player.y -
        (game.player.speed_y * game.camera_offset)
    )
    
    arcade.draw_lbwh_rectangle_outline(
        start_x, start_y, l, l, color, 10
    )
    
    for i in range(lines):
        if i > 0:
            x = start_x + i * (l / lines)
            y = start_y
            arcade.draw_line(
                x, y,
                x, y + l,
                color, 3
            )
            x = start_x
            y = start_y + i * (l / lines)
            arcade.draw_line(
                x, y,
                x + l, y,
                color, 3
            )

if __name__ == "__main__":
    import game
    game.main()