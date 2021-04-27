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
        # self.flowers = check_flower_level(self.engine.player) 
        self.flowers = self.engine.player.equipment.flower_slot.values()

        self.viewport_left = viewports[0]
        self.viewport_righit = viewports[1]
        self.viewport_bottom = viewports[2]
        self.viewport_top = viewports[3]
        self.window_width = SCREEN_WIDTH - 924
        self.window_height = SCREEN_HEIGHT - 800

        self.bottom_left_x=self.viewport_left+GRID_SIZE*7
        self.bottom_left_y=self.viewport_bottom+GRID_SIZE*8
        self.back_panel_top_left = self.viewport_top - (GRID_SIZE*4)

        # 最下部の基本枠
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.bottom_left_x,
            bottom_left_y=self.bottom_left_y,
            width=(GRID_SIZE*5),
            height=(GRID_SIZE*3),
            color=[232, 55, 25, 100]
        )
        # flowerアイコン
        arcade.draw_rectangle_filled(
            center_x=self.player.center_x,
            center_y=self.back_panel_top_left + (GRID_SIZE),
            width=100,
            height=100,
            color=(250,250,250,150)
        )

        
        if self.key == arcade.key.ENTER:
            # self.flowers[0].level += 1
            # self.flowers[0].current_xp = 0
            self.level_bonus = None
            self.flowers.remove(self.flowers[0])
            self.key = None
                
        if len(self.flowers) < 1:
            self.player.equipment.equip_update()
            self.engine.game_state = GAME_STATE.NORMAL
        
        # if len(self.flowers) > 0:
        else:

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
            title = self.bottom_left_x+10
            arcade.draw_text(
                text=f"LEVEL UP!",
                start_x=title,
                start_y=self.back_panel_top_left-10,
                color=arcade.color.BLUE_GREEN,
                font_size=font_size,
                # font_name=UI_FONT2,
                anchor_y="top"
            )
            f_name = title + 80
            arcade.draw_text(
                text=f" {item_text} ",
                start_x=f_name,
                start_y=self.back_panel_top_left-10,
                color=arcade.color.PEARL,
                font_size=font_size,
                # font_name=UI_FONT2,
                anchor_y="top"
            )
            l = "level"
            arcade.draw_text(
                text=f"{l:16}",
                start_x=self.bottom_left_x + 33,
                start_y=self.back_panel_top_left-35,
                color=arcade.color.AERO_BLUE,
                font_size=font_size,
                font_name=UI_FONT2,
                anchor_y="top"
            )
            arcade.draw_text(
                text=f"+ {item.level:6}",
                start_x=self.bottom_left_x + GRID_SIZE*2.5,
                start_y=self.back_panel_top_left-35,
                color=arcade.color.AERO_BLUE,
                font_size=font_size,
                font_name=UI_FONT2,
                anchor_y="top"
            )

            ifs = 5

            # statesの表示
            font_color = (220, 208, 255)


            if self.level_bonus:
                for k,v in self.level_bonus.items():

                    font_color = (50, 150, 55)
                    if k == f"max_hp":
                        font_color = (75, 15, 15)
                    if k in ["STR", "DEX", "INT"]:
                        font_color = (190, 55, 55)
                    if k in ["evasion", "defense"]:
                        font_color = (250, 55, 155)
                    if k in self.player.fighter.resist:
                        font_color = (150, 10, 250)
                    if "speed" in k:
                        font_color = (250, 250, 50)


                    arcade.draw_text(
                        text=f"{k:16}",
                        start_x=self.bottom_left_x + 33,
                        start_y=self.back_panel_top_left + y - (52) - ifs,
                        color=font_color,
                        font_size=font_size,
                        font_name=UI_FONT2,
                        anchor_y="top"
                    )
                    arcade.draw_text(
                        text=f"+ {v:6}",
                        start_x=self.bottom_left_x + GRID_SIZE*2.5,
                        start_y=self.back_panel_top_left + y - (52) - ifs,
                        color=arcade.color.WHITE,
                        font_size=font_size,
                        font_name=UI_FONT2,
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
            #         font_name=UI_FONT2,
            #         anchor_y="top"
            #     )
            #     ifs += 19


