import arcade

import background
import rocket

class Game(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Attack of the Zorps",
            resizable=True)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.objects = arcade.SpriteList()
        self.stars = arcade.SpriteList()
        
        self.player = rocket.Rocket(self, "./Assets/player.png")
        
        self.objects.append(self.player)

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        self.objects.draw()

    def on_update(self, delta_time):
        self.objects.update()
        pass

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]:
            self.player.moving = True
        pass

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.W]:
            self.player.moving = False
        pass
    
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

def main():
    Game()
    arcade.run()

if __name__ == "__main__":
    main()