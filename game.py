import arcade
import os
import random

import background
import rocket
import rocks
import effects

class Game(arcade.Window):
    def __init__(self):
        super().__init__(1200, 750, "Attack of the Zorps",
            resizable=True)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.objects = arcade.SpriteList()
        self.stars = arcade.SpriteList()
        
        self.camera_offset = 2
        
        self.objects.append(rocks.Planet(self))
        
        self.player = rocket.Rocket(self, "./Assets/player.png")
        self.objects.append(self.player)
        
        for _ in range(4):
            self.objects.append(
                rocket.Alien(
                    self,
                    random.randint(-100, 100),
                    random.randint(-100, 100)
                )
            )
        
        for _ in range(1000):
            self.stars.append(background.Star(self))

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        self.stars.draw()
        self.objects.draw()
        effects.draw_speed_lines(self)

    def on_update(self, delta_time):
        self.objects.update()
        self.stars.update()

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