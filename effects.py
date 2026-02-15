import arcade
import math

def draw_speed_lines(game):
    dis = 20
    rad = math.radians(game.player.dir)
    rad_plus_90 = math.radians(game.player.dir + 90)
    l = math.sqrt(
        game.player.speed_x ** 2 +
        game.player.speed_y ** 2
    ) * 50 - 100 + 500
    dis_x = math.sin(rad) * l
    dis_y = math.cos(rad) * l
    color = arcade.color.WHITE
    lw = 2
    start = math.sqrt(
        (game.width / 2) ** 2 +
        (game.height / 2) ** 2
    )
    
    for i in range(5):
        x = (
            game.width / 2 - math.sin(rad) * start +
            (math.sin(rad_plus_90) * dis) * i
        )
        y = (
            game.height / 2 - math.cos(rad) * start +
            (math.cos(rad_plus_90) * dis) * i
        )
        arcade.draw_line(
            x, y,
            x + dis_x, y + dis_y,
            color, lw
        )


if __name__ == "__main__":
    import game
    game.main()