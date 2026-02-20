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
        self.glows = arcade.SpriteList()
        self.players = arcade.SpriteList()
        
        self.camera_offset = 2
        self.world_size = 10000
        self.cull_margin = 120
        
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
        self.glows = background.create_default_glows(self)
        
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
        self._culled_lists = (
            self.glows,
            self.stars,
            self.aliens,
            self.rocks,
            self.planets,
            self.players,
        )
        self._update_visibility()

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        self.glows.draw()
        background.draw_grid(self)
        self.stars.draw()
        self.aliens.draw()
        self.rocks.draw()
        self.planets.draw()
        self.player.draw_motion_trail()
        self.players.draw()

    def on_update(self, delta_time):
        self.glows.update()
        self.players.update()
        self.aliens.update()
        self.rocks.update()
        self.planets.update()
        self.physics_engine.update()
        self.stars.update()
        self._update_visibility()
        self.frame += 1

    def _update_visibility(self):
        left = -self.cull_margin
        right = self.width + self.cull_margin
        bottom = -self.cull_margin
        top = self.height + self.cull_margin

        for sprite_list in self._culled_lists:
            for sprite in sprite_list:
                half_w = sprite.width * 0.5
                half_h = sprite.height * 0.5
                sprite.visible = (
                    sprite.center_x + half_w >= left
                    and sprite.center_x - half_w <= right
                    and sprite.center_y + half_h >= bottom
                    and sprite.center_y - half_h <= top
                )

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
