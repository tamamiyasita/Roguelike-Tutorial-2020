# import arcade
# import arcade.gl as gl


# class MG(arcade.Window):
#     def __init__(self, width, height, title="cell"):
#         super().__init__(width, height, title)
#         self.window = arcade.get_window()
#         print(self.window.width)
        
        

#         arcade.set_background_color((200,200,200))



#     def on_draw(self):
#         arcade.start_render()

        
        
                   
#     def on_update(self, delta_time):
#         pass

#     def on_key_press(self, symbol: int, modifiers: int):
#         if symbol == arcade.key.ESCAPE:
#             arcade.close_window()

# def main():
#     gam = MG(600, 600)
#     arcade.run()

# if __name__ == "__main__":
#     main()

"""
This animation example shows how perform a radar sweep animation.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.radar_sweep
"""

import arcade
import math

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Radar Sweep Example"

# These constants control the particulars about the radar
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250


def on_draw(_delta_time):
    """ Use this function to draw everything to the screen. """

    # Move the angle of the sweep.
    on_draw.angle += RADIANS_PER_FRAME

    # Calculate the end point of our radar sweep. Using math.
    x = SWEEP_LENGTH * math.sin(on_draw.angle) + CENTER_X
    y = SWEEP_LENGTH * math.cos(on_draw.angle) + CENTER_Y

    # Start the render. This must happen before any drawing
    # commands. We do NOT need an stop render command.
    arcade.start_render()

    # Draw the radar line
    arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.OLIVE, 4)

    # Draw the outline of the radar
    arcade.draw_circle_outline(CENTER_X, CENTER_Y, SWEEP_LENGTH,
                               arcade.color.DARK_GREEN, 10)


# This is a function-specific variable. Before we
# use them in our function, we need to give them initial
# values.
on_draw.angle = 0  # type: ignore # dynamic attribute on function obj


def main():

    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BLACK)

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(on_draw, 1 / 80)

    # Run the program
    arcade.run()

    # When done running the program, close the window.
    arcade.close_window()


if __name__ == "__main__":
    main()