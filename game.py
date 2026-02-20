import arcade
from arcade.types import Color
import os
import random

import background
import rocket
import planets
import effects
import physics

class Game(arcade.Window):
    def __init__(self):
        super().__init__(1200, 750, "Attack of the Zorps",
            resizable=True)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.planets = arcade.SpriteList()
        self.rocks = arcade.SpriteList()
        self.aliens = arcade.SpriteList()
        self.stars = arcade.SpriteList()
        self.players = arcade.SpriteList()
        
        self.camera_offset = 2
        self.world_size = 3000
        
        self.planets.append(
            planets.Earth(self)
        )
        self.planets.append(
            planets.Alien_Planet(self)
        )
    
        self.player = rocket.Player(self)
        self.players.append(self.player)
        
        for i in range(20):
            self.rocks.append(
                planets.Rock(self)
            )
        
        for _ in range(2000):
            self.stars.append(background.Star(self))
        
        self.frame = 0
        
        self.physics_engine = physics.WorldPhysicsEngine(
            self,
            [
                self.players,
                self.aliens,
                self.rocks,
            ],
            world_bounds=(
                -self.world_size / 2,
                self.world_size / 2,
                -self.world_size / 2,
                self.world_size / 2,
            ),
            iterations=4,
        )

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        background.draw_grid(self)
        self.stars.draw()
        self.aliens.draw()
        self.rocks.draw()
        self.planets.draw()
        self.player.draw_motion_trail()
        self.players.draw()

    def on_update(self, delta_time):
        self.players.update()
        self.aliens.update()
        self.rocks.update()
        self.planets.update()
        self.physics_engine.update()
        self.stars.update()
        self.frame += 1

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]:
            self.player.moving = True
        if key in [arcade.key.RIGHT, arcade.key.D]:
            self.player.steering_right = True
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.player.steering_left = True

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]:
            self.player.moving = False
        if key in [arcade.key.RIGHT, arcade.key.D]:
            self.player.steering_right = False
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.player.steering_left = False
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

def main():
    Game()
    arcade.run()

if __name__ == "__main__":
    main()
