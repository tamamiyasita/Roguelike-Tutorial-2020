import arcade
from constants import *
from level_up_sys import check_flower_level, Select_param


class LevelUpFlower:
    def __init__(self, engine):
        self.level_bonus = None # flowerのステータスボーナス
        self.flowers = None # レベルアップするflowerのリスト
        self.key = None
        self.engine = engine
        self.player = engine.player

    def states_choices(self, key):
        self.key = key


    def window_pop(self, viewports):
        self.flowers = check_flower_level(self.engine.player) 

        self.viewport_left = viewports[0]
        self.viewport_righit = viewports[1]
        self.viewport_bottom = viewports[2]
        self.viewport_top = viewports[3]
        self.window_width = SCREEN_WIDTH - 924
        self.window_height = SCREEN_HEIGHT - 800

        self.bottom_left_x=self.viewport_left+(MAIN_PANEL_X/2) -(self.window_width/2)
        self.bottom_left_y=self.viewport_bottom+500
        self.back_panel_top_left = self.viewport_top - (GRID_SIZE*4)

        # 最下部の基本枠
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left + (GRID_SIZE*5),
            bottom_left_y=self.back_panel_top_left- (GRID_SIZE*3),
            width=(GRID_SIZE*5),
            height=(GRID_SIZE*3),
            color=[255, 255, 255, 60]
        )
        # flowerアイコン
        arcade.draw_rectangle_filled(
            center_x=self.player.center_x,
            center_y=self.back_panel_top_left + (GRID_SIZE),
            width=100,
            height=100,
            color=(150,150,150,150)
        )

        
        if not self.flowers:
            self.engine.game_state = GAME_STATE.NORMAL
        
        if self.key == arcade.key.ENTER:
            self.flowers[0].level += 1
            self.level_bonus = None
            self.flowers.remove(self.flowers[0])
            self.key = None
                
        if len(self.flowers) > 0:

            item = self.flowers[0]
            level_bonus = Select_param(item)
            if not self.level_bonus:
                self.level_bonus = level_bonus.point_set()



            y = -10
            font_size =15

            item_text = f"{item.name}".replace("_", " ").title()

            arcade.draw_scaled_texture_rectangle(
                center_x=self.player.center_x,
                center_y=self.back_panel_top_left + (GRID_SIZE),
                texture=item.texture,
                scale=6
                )
                
            # タイトル
            arcade.draw_text(
                text=f"LEVEL UP {item_text} level {item.level+1}!",
                start_x=self.bottom_left_x + 10,
                start_y=self.back_panel_top_left-10,
                color=arcade.color.BLUE_GREEN,
                font_size=font_size+4,
                font_name="consola.ttf",
                anchor_y="top"
            )

            ifs = 5
            # statesの表示
            font_color = (220, 208, 255)
            if self.level_bonus:
                for k,v in self.level_bonus.items():

                    font_color = (250, 15, 15)

                    arcade.draw_text(
                        text=f"{k:15} + {v:4}",
                        start_x=self.bottom_left_x + 10,
                        start_y=self.back_panel_top_left + y - (22) - ifs,
                        color=font_color,
                        font_size=font_size,
                        font_name="consola.ttf",
                        anchor_y="top"
                    )
                    ifs += 23
            # の表示
            # for k, v in self.level_bonus.items():
            #     arcade.draw_text(
            #         text=f"{k} level {v}".replace("_", " ").title(),
            #         start_x=self.bottom_left_x + 10,
            #         start_y=self.back_panel_top_left + y - (22) - ifs,
            #         color=arcade.color.CORNSILK,
            #         font_size=font_size,
            #         font_name="consola.ttf",
            #         anchor_y="top"
            #     )
            #     ifs += 19


