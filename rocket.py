import arcade
import math
import random
from arcade.hitbox import PymunkHitBoxAlgorithm


PRECISE_HIT_BOX = PymunkHitBoxAlgorithm(detail=1.0)

class Rocket(arcade.Sprite):
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
        
        self.moving = False
        self.steering_right = False
        self.steering_left = False
        
        self.record_motion_trail = False
        self.motion_trail = []

        self.mass = 1.0
        self.collision_radius = max(self.width, self.height) * 0.33
        self.collision_restitution = 0.55
        self.collision_friction = 0.18
        self.collision_static = False
        self.collision_enabled = True
    
    @property
    def speed(self):
        return math.sqrt(
            self.move_x ** 2 + self.move_y ** 2
        )
    
    def move(self, speed):
        rad = math.radians(self.dir)
        self.move_x += math.sin(rad) * speed
        self.move_y += math.cos(rad) * speed

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
        
        drift = 0.99
        self.move_x *= drift
        self.move_y *= drift
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
        
        if self.record_motion_trail:
            self.motion_trail.append((self.x, self.y, self.dir))
            self.motion_trail = self.motion_trail[-200:]

        self.sync_view_position()
            
        return super().update(delta_time, *args, **kwargs)

    def draw_motion_trail(self):
        add_y = -33
        
        for add_x in [-35, 35]:
            for i in range(len(self.motion_trail) - 1):
                x1, y1, dir1 = self.motion_trail[i]
                x2, y2, dir2 = self.motion_trail[i + 1]
                offset_x = (
                    self.game.width / 2 -
                    self.game.player.move_x * self.game.camera_offset -
                    self.game.player.x
                )
                offset_y = (
                    self.game.height / 2 -
                    self.game.player.move_y * self.game.camera_offset -
                    self.game.player.y
                )
                rad1_y = math.radians(dir1)
                rad1_x = math.radians(dir1 + 90)
                add_x1 = math.sin(rad1_y) * add_y + math.sin(rad1_x) * add_x
                add_y1 = math.cos(rad1_y) * add_y + math.cos(rad1_x) * add_x
                rad2_y = math.radians(dir2)
                rad2_x = math.radians(dir2 + 90)
                add_x2 = math.sin(rad2_y) * add_y + math.sin(rad2_x) * add_x
                add_y2 = math.cos(rad2_y) * add_y + math.cos(rad2_x) * add_x
                a = 255
                color = (a, a, a, (
                    20 * (i / len(self.motion_trail))
                ))
                arcade.draw_line(
                    offset_x + x1 + add_x1,
                    offset_y + y1 + add_y1,
                    offset_x + x2 + add_x2,
                    offset_y + y2 + add_y2,
                    color, 5
                )

class Player(Rocket):
    def __init__(self, game):
        super().__init__(game, "./Assets/player.png")
        self.x = 100
        self.y = -100
        self.dir = 0
        self.move_x = -2
        self.move_y = 2
        self.speed_dir = -0.5
        self.record_motion_trail = True
        self.mass = 2.6
        self.collision_radius *= 0.95
        self.collision_restitution = 0.4
        self.collision_friction = 0.3

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
        self.mass = 1.4
        self.collision_restitution = 0.65
        self.collision_friction = 0.12

if __name__ == "__main__":
    import game
    game.main()
