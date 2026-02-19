import arcade
import random
import math
import rocket
from arcade.hitbox import PymunkHitBoxAlgorithm


PRECISE_HIT_BOX = PymunkHitBoxAlgorithm(detail=1.0)

class Planet(arcade.Sprite):
    def __init__(self, game, image):
        super().__init__(image, hit_box_algorithm=PRECISE_HIT_BOX)
        self.scale = 0.15
        self.game = game
        
        self.x = 0
        self.y = 0
        self.dir = 0
        
        self.move_x = 0
        self.move_y = 0
        self.speed_dir = 0
        
        self.pop_effect = 0
        
        self.spawner = False
        self.spawn_function = None

        self.mass = 9999
        self.collision_radius = max(self.width, self.height) * 0.45
        self.collision_restitution = 0.75
        self.collision_friction = 0.6
        self.collision_static = True
        self.collision_enabled = True

    def sync_view_position(self):
        camera_offset_x = self.game.player.move_x * self.game.camera_offset
        camera_offset_y = self.game.player.move_y * self.game.camera_offset
        self.center_x = (
            self.game.width / 2 - camera_offset_x -
            self.game.player.x + self.x
        )
        self.center_y = (
            self.game.height / 2 - camera_offset_y -
            self.game.player.y + self.y
        )
        self.angle = self.dir
    
    def update(self, delta_time = 1 / 60, *args, **kwargs):
        self.x += self.move_x
        self.y += self.move_y
        self.dir += self.speed_dir
        
        self.dir %= 360
        
        if self.spawner and self.spawn_function:
            self.spawn_function()

        self.sync_view_position()

class Earth(Planet):
    def __init__(self, game):
        super().__init__(game, "./Assets/earth.png")
        self.x = 300
        self.y = -300
        self.speed_dir = 0.1

class Egg(Planet):
    def __init__(self, game, x, y):
        super().__init__(game, "./Assets/egg.png")
        self.x = x
        self.y = y
        self.move_x = random.random() * 2 -1
        self.move_y = random.random() * 2 -1
        self.speed_dir = random.random() * 2 -1
        self.spawner = True
        self.spawn_function = self.spawn
        self.mass = 0.9
        self.collision_radius *= 0.68
        self.collision_restitution = 0.9
        self.collision_friction = 0.04
        self.collision_static = False
        self.sync_view_position()
    
    def spawn(self):
        return
        if random.choice(list(range(100))) == 0:
            self.game.aliens.append(rocket.Alien(self.game, self.x, self.y))

class Alien_Planet(Planet):
    def __init__(self, game):
        super().__init__(game, "./Assets/kepler67.png")
        self.x = -1000
        self.y = 1000
        self.speed_dir = -0.2
        self.spawner = True
        self.spawn_function = self.spawn
    
    def spawn(self):
        if random.choice(list(range(1000))) == 0:
            self.game.rocks.append(Egg(self.game, self.x, self.y))

if __name__ == "__main__":
    import game
    game.main()
