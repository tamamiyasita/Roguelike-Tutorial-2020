import arcade
from constants import *
from level_up_sys import check_flower_level
class LevelUpFlower:
    def __init__(self):
        self.level_bonus = None # flowerのステータスボーナス
        self.flowers = None # レベルアップするflowerのリスト
        self.add = {}

    def window_pop(self, viewports, engine):
        self.engine = engine
        self.flowers = check_flower_level(self.engine.player) 

        self.viewport_left = viewports[0]
        self.viewport_righit = viewports[1]
        self.viewport_bottom = viewports[2]
        self.viewport_top = viewports[3]

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

        
        if len(self.flowers) > 0:
            # from collections import Counter
            item = self.flowers[0]
            if self.key == arcade.key.ENTER:
                if self.add:# 追加skill
                    # if self.add in self.player.fighter.level_skills:
                    #     self.player.fighter.level_skills[self.add] += 1
                    # else:
                    #     self.player.fighter.level_skills.setdefault(self.add, 1)
                    # Counter(self.player.fighter.level_skills) + Counter(self.add)
                    if self.add in item.skill_bonus:
                        item.skill_bonus[self.add] += 1
                    else:
                        item.skill_bonus.setdefault(self.add, 1)
                item.level += 1
                self.level_bonus = None
                self.flowers.remove(item)
                self.key = None
                self.add = {}
                
            elif not self.level_bonus:
                self.level_bonus = level_up(item, item.level_up_weights)



            y = -10
            font_size =15

            item_text = f"{item.name}".replace("_", " ").title()

            arcade.draw_scaled_texture_rectangle(
                center_x=self.player.center_x,
                center_y=self.back_panel_top_left + (GRID_SIZE),
                texture=item.texture,
                scale=6
                )
                
            # 花名タイトル
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
            # STR,DEX,INTの表示
            font_color = (220, 208, 255)
            for k,v in item.states_bonus.items():
                if self.level_bonus and k == self.level_bonus[0]:
                    font_color = (250, 150, 159)
                else:
                    font_color = (220, 208, 255)

                arcade.draw_text(
                    text=f"{k}:{v}",
                    start_x=self.bottom_left_x + 10,
                    start_y=self.back_panel_top_left + y - (22) - ifs,
                    color=font_color,
                    font_size=font_size,
                    font_name="consola.ttf",
                    anchor_y="top"
                )
                ifs += 21
            # skillの表示
            for k, v in item.skill_bonus.items():
                arcade.draw_text(
                    text=f"{k} level {v}".replace("_", " ").title(),
                    start_x=self.bottom_left_x + 10,
                    start_y=self.back_panel_top_left + y - (22) - ifs,
                    color=arcade.color.CORNSILK,
                    font_size=font_size,
                    font_name="consola.ttf",
                    anchor_y="top"
                )
                ifs += 19
