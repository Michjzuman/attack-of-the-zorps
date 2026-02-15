import arcade
import math
import random

def draw_speed_lines(game):
    rays = 60
    dis = 20
    rad = math.radians(game.player.dir)
    rad_plus_90 = math.radians(game.player.dir + 90)
    l = math.sqrt(
        game.player.speed_x ** 2 +
        game.player.speed_y ** 2
    ) * 50 - 70
    color = arcade.color.WHITE
    lw = 2
    start = math.sqrt(
        (game.width / 2) ** 2 +
        (game.height / 2) ** 2
    )
    
    for i in range(rays):
        dis_x = math.sin(rad) * (l * random.random())
        dis_y = math.cos(rad) * (l * random.random())
        x = (
            game.width / 2 - math.sin(rad) * start +
            (math.sin(rad_plus_90) * dis) *
            (i + 0.5 - rays / 2)
        )
        y = (
            game.height / 2 - math.cos(rad) * start +
            (math.cos(rad_plus_90) * dis) *
            (i + 0.5 - rays / 2)
        )
        arcade.draw_line(
            x, y,
            x + dis_x, y + dis_y,
            color, lw
        )


if __name__ == "__main__":
    import game
    game.main()