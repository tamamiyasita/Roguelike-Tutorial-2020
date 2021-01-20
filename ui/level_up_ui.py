from random import choice
from typing import Tuple
import arcade
from constants import *
from data import *
from actor.skills.leaf_blade import LeafBlade
from actor.skills.branch_baton import BranchBaton
from actor.skills.healing import Healing
from actor.skills.seed_shot import SeedShot
from level_up_sys import check_experience_level, level_up

from enum import Enum, auto
from collections import deque


class Select(Enum):
    ability = auto()
    delay = auto()
    open_skill = auto()

leaf_blade = LeafBlade()
branch_baton = BranchBaton()
healing = Healing()
seed_shot = SeedShot()

class LevelupUI:
    def __init__(self):
        self.up_str = ""
        self.up_dex = ""
        self.up_int = ""
        self.tmp_states = None
        self.ui_state = Select.delay
        self.skill_queue = deque([healing, seed_shot, (leaf_blade, branch_baton), healing ])
        self.skill_result = []
        self.get_skill = None
        self.select_skill = True
        self.level_bonus = None

        self.window_width = SCREEN_WIDTH - 924
        self.window_height = SCREEN_HEIGHT - 800

    def states_choices(self, key):
        self.key = key
        if self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            if self.player.fighter.ability_points >= 1:
                if key == arcade.key.S:
                    self.player.fighter.base_strength += 1
                    self.player.fighter.ability_points -= 1
                    self.tmp_states = "STR"
                elif key == arcade.key.D:
                    self.player.fighter.base_dexterity += 1
                    self.player.fighter.ability_points -= 1
                    self.tmp_states = "DEX"
                elif key == arcade.key.I:
                    self.player.fighter.base_intelligence += 1
                    self.player.fighter.ability_points -= 1
                    self.tmp_states = "INT"
                self.ui_state = Select.open_skill

            

    def window_pop(self, viewports, engine):
        """Levelup時に出現するwindow"""
            
        self.engine = engine
        self.player = engine.player
        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        self.bottom_left_x=self.viewport_left+(MAIN_PANEL_X/2) -(self.window_width/2)
        self.bottom_left_y=self.viewport_bottom+500
        self.back_panel_top_left = self.viewport_top - (GRID_SIZE*4)


        if self.engine.game_state == GAME_STATE.LEVEL_UP_WINDOW:
            self.draw_base_window()
            self.draw_ability_select()

            if self.ui_state == Select.open_skill or self.get_skill:
                self.draw_skill_get_window()
        
        #flowerのlevel画面
        elif self.engine.game_state == GAME_STATE.LEVEL_UP_FLOWER:
            self.flower_level_up_window(engine)

    def flower_level_up_window(self, engine):
            # check_experience_level(self.player, engine)
            # engine.game_state = GAME_STATE.NORMAL

        # 最下部の基本枠
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left + (GRID_SIZE*5),
            bottom_left_y=self.back_panel_top_left- (GRID_SIZE*3),
            width=(GRID_SIZE*5),
            height=(GRID_SIZE*3),
            color=[255, 255, 255, 60]
        )
        arcade.draw_rectangle_filled(
            center_x=self.player.center_x,
            center_y=self.back_panel_top_left + (GRID_SIZE),
            width=100,
            height=100,
            color=(150,150,150,150)
        )
        item = None
        for item in self.player.equipment.item_slot:
            xp_to_next_level = item.experience_per_level[item.level+1]
            if item.current_xp >= xp_to_next_level and item.max_level >= item.level:
                if self.key == arcade.key.ENTER:
                    item.level += 1
                    self.level_bonus = None
                    check_experience_level(self.player, engine)
                    
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
                    text=f"LEVEL UP {item_text}",
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
                # スキルの表示
                for k, v in item.skill_add.items():
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
                
                break
            # else:
            #     engine.game_state = GAME_STATE.NORMAL
            #     self.level_bonus = None




            








    def draw_base_window(self):
        # 最下部の基本枠
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.bottom_left_x,
            bottom_left_y=self.bottom_left_y,
            width=self.window_width,
            height=self.window_height,
            color=[255, 255, 255, 190]
        )

        # テキストに使う変数
        spacing = 30
        self.text_position_x = self.bottom_left_x + 10
        self.text_position_y = self.bottom_left_y + 160
        text_size = 24

        # 最上段のタイトル
        screen_title = "Level UP!"
        text_color = arcade.color.GREEN_YELLOW
        arcade.draw_text(
            text=screen_title,
            start_x=self.text_position_x-10,
            start_y=self.text_position_y,
            color=text_color,
            font_size=text_size
        )

        # ability point表示
        text_color = arcade.color.PALATINATE_PURPLE
        arcade.draw_text(
            text=f"ability point: {self.player.fighter.ability_points}",
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )
        STR = f"STR: {self.player.fighter.base_strength} {self.up_str}"
        DEX = f"DEX: {self.player.fighter.base_dexterity} {self.up_dex}"
        INT = f"INT: {self.player.fighter.base_intelligence} {self.up_int}"

        # 以下ステータスpointの表示
        self.text_position_y -= spacing
        text_color = arcade.color.RED_ORANGE

        arcade.draw_text(
            text=STR,
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        self.text_position_y -= spacing
        text_color = arcade.color.BLUEBERRY
        arcade.draw_text(
            text=DEX,
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

        self.text_position_y -= spacing
        text_color = arcade.color.BLACK_LEATHER_JACKET
        arcade.draw_text(
            text=INT,
            start_x=self.text_position_x,
            start_y=self.text_position_y - spacing,
            font_name="consola.ttf",
            color=text_color,
            font_size=text_size-7
        )

    def draw_ability_select(self):
        # ability pointがゼロ、かつstateがabilityで選択文が出る
        if self.player.fighter.ability_points == 0 and self.ui_state == Select.ability:
            self.up_str = ""
            self.up_dex = ""
            self.up_int = ""
            arcade.draw_text(
                text=f"It's OK? ( YES : key[y]   NO : key[n] )",
                start_x=self.text_position_x+10,
                start_y=self.text_position_y-60,
                # font_name="consola.ttf",
                color=arcade.color.OLD_BURGUNDY,
                font_size=15
            )

            # Yボタンが押されたらgame stateをノーマルに戻し終了
            if self.key == arcade.key.Y:
                self.player.fighter.skill_list.extend(self.skill_result)
                self.get_skill = None
                self.select_skill = True
                self.skill_result = []
                self.player.equipment.passive_sprite_on(self.engine.cur_level.equip_sprites)

                # 花も同時にレベルが上がっていた場合に備えてのチェック
                self.f_list = check_experience_level(self.player, self.engine)
                # self.engine.game_state = GAME_STATE.NORMAL # ← すぐ上の関数に移動した


            # Nボタンならability pointを戻し再選択させる
            elif self.key == arcade.key.N or self.key == arcade.key.ESCAPE:
                self.player.fighter.ability_points += 1
                if self.tmp_states == "STR":
                    self.player.fighter.base_strength -= 1
                elif self.tmp_states == "DEX":
                    self.player.fighter.base_dexterity -= 1
                elif self.tmp_states == "INT":
                    self.player.fighter.base_intelligence -= 1

        elif self.player.fighter.ability_points != 0:
            self.up_str = "(key press S + 1)"
            self.up_dex = "(key press D + 1)"
            self.up_int = "(key press I + 1)"

    
    def get_skill_queue(self, get_skill):
        if get_skill is None and self.skill_queue:
            skill = self.skill_queue.popleft()
            return skill
        else:
            return get_skill


    def draw_skill_get_window(self):
        # ability pointがゼロかつスキル取得レベルなら追加で窓を表示する
        if self.player.fighter.ability_points < 1:
            if 0 < len(self.skill_queue) and self.select_skill:
                self.get_skill = self.skill_queue.popleft()
                self.select_skill = False
  
            if isinstance(self.get_skill, Tuple):
                skill_A = self.get_skill[0]
                skill_B = self.get_skill[1]

                # ベーススキル窓
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.bottom_left_x,
                    bottom_left_y=self.bottom_left_y-170,
                    width=self.window_width,
                    height=self.window_height+10,
                    color=[59, 125, 29, 170]
                )

                # スキル枠A
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.bottom_left_x+12,
                    bottom_left_y=self.bottom_left_y-160,
                    width=128,
                    height=128,
                    color=[25, 25, 45, 190]
                )


                # スキル枠Aのスキルアイコン
                arcade.draw_texture_rectangle(
                    self.bottom_left_x+76,
                    self.bottom_left_y-96,
                    64, 64,
                    texture=skill_A.icon
                )


                # スキル枠B
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.bottom_left_x+152,
                    bottom_left_y=self.bottom_left_y-160,
                    width=128,
                    height=128,
                    color=[55, 25, 25, 190]
                )



                # スキル枠Bのスキルアイコン
                arcade.draw_texture_rectangle(
                    self.bottom_left_x+216,
                    self.bottom_left_y-96,
                    64, 64,
                    texture=skill_B.icon
                )

                # スキル選択テキスト
                skill_explanatory_text = ""
                if self.ui_state == Select.open_skill:


                    arcade.draw_text(
                        text=f"key press A",
                        start_x=self.bottom_left_x+12,
                        start_y=self.text_position_y-98,
                        # font_name="consola.ttf",
                        color=arcade.color.WHITE,
                        font_size=16
                    )
                    arcade.draw_text(
                        text=f"key press B",
                        start_x=self.bottom_left_x+152,
                        start_y=self.text_position_y-98,
                        # font_name="consola.ttf",
                        color=arcade.color.WHITE,
                        font_size=16
                    )

                # スキル枠Aのタイトル
                arcade.draw_text(
                    text=skill_A.name.replace("_", " ").title(),
                    start_x=self.bottom_left_x+15,
                    start_y=self.text_position_y-123,
                    # font_name="consola.ttf",
                    color=arcade.color.GREEN_YELLOW,
                    font_size=15
                )
                # arcade.draw_text(
                #     text=skill_A.explanatory_text,
                #     start_x=self.bottom_left_x+15,
                #     start_y=self.text_position_y-223,
                #     # font_name="consola.ttf",
                #     color=arcade.color.GREEN_YELLOW,
                #     font_size=10
                # )

                # スキル枠Bのタイトル
                arcade.draw_text(
                    text=skill_B.name.replace("_", " ").title(),
                    start_x=self.bottom_left_x+155,
                    start_y=self.text_position_y-123,
                    # font_name="consola.ttf",
                    color=arcade.color.PALE_GOLD,
                    font_size=15
                )

                # スキル選択でui_stateをabilityにして決定の確認に進む
                if self.key == arcade.key.A:
                    self.skill_result = []
                    self.skill_result.append(skill_A)

                    arcade.draw_xywh_rectangle_outline(
                        bottom_left_x=self.bottom_left_x+12,
                        bottom_left_y=self.bottom_left_y-160,
                        width=128,
                        height=128,
                        color=arcade.color.GREEN_YELLOW,
                        border_width=1
                    )
                    arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=self.bottom_left_x+152,
                        bottom_left_y=self.bottom_left_y-160,
                        width=128,
                        height=128,
                        color=[255, 255, 255, 185])
                        
                    skill_explanatory_text = f"{skill_A.name} {skill_A.explanatory_text}".replace("_", " ")

                    # playerのskill listに追加し、装備更新をチェックさせる
                    self.ui_state = Select.ability

                elif self.key == arcade.key.B:
                    self.skill_result = []
                    self.skill_result.append(skill_B)

                    arcade.draw_xywh_rectangle_outline(
                        bottom_left_x=self.bottom_left_x+152,
                        bottom_left_y=self.bottom_left_y-160,
                        width=128,
                        height=128,
                        color=arcade.color.PALE_GOLD,
                        border_width=1
                    )
                    arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=self.bottom_left_x+12,
                        bottom_left_y=self.bottom_left_y-160,
                        width=128,
                        height=128,
                        color=[255, 255, 255, 185],
                    )

                    skill_explanatory_text = f"{skill_B.name} {skill_B.explanatory_text}".replace("_", " ")
                    self.ui_state = Select.ability

                arcade.draw_text(
                    text=f"{skill_explanatory_text}",
                    start_x=self.bottom_left_x+(self.window_width//2),
                    start_y=self.text_position_y-98,
                    color=arcade.color.WHITE,
                    anchor_x="center",
                    font_size=13
                )
                

            elif self.get_skill:
                # ベーススキル窓
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.bottom_left_x,
                    bottom_left_y=self.bottom_left_y-185,
                    width=self.window_width,
                    height=self.window_height+25,
                    color=[25, 25, 29, 170]
                )

                # スキル枠
                arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=self.bottom_left_x+82,
                    bottom_left_y=self.bottom_left_y-160,
                    width=128,
                    height=128,
                    color=[255, 250, 250, 190]
                )
                arcade.draw_xywh_rectangle_outline(
                    bottom_left_x=self.bottom_left_x+82,
                    bottom_left_y=self.bottom_left_y-160,
                    width=128,
                    height=128,
                    color=[135, 50, 50, 190]
                )
        
                # スキルアイコン
                arcade.draw_texture_rectangle(
                    self.bottom_left_x+146,
                    self.bottom_left_y-96,
                    64, 64,
                    texture=self.get_skill.icon
                )



                arcade.draw_text(
                    text=f"Get Skill",
                    start_x=self.bottom_left_x+82,
                    start_y=self.text_position_y-98,
                    font_name="consola.ttf",
                    color=arcade.color.WHITE,
                    font_size=16
                )
                arcade.draw_text(
                    text=f"{self.get_skill.name} {self.get_skill.explanatory_text}".replace("_", " "),
                    start_x=self.bottom_left_x+(self.window_width//2),
                    start_y=self.text_position_y-250,
                    color=arcade.color.WHITE,
                    anchor_x="center",
                    font_size=13
                )

                # スキル枠のタイトル
                arcade.draw_text(
                    text=self.get_skill.name.replace("_", " ").title(),
                    start_x=self.bottom_left_x+88,
                    start_y=self.text_position_y-123,
                    font_name="consola.ttf",
                    color=arcade.color.BLUE_VIOLET,
                    font_size=15
                )

                self.skill_result = []
                self.skill_result.append(self.get_skill)

                # playerのskill listに追加し、装備更新をチェックさせる
                self.ui_state = Select.ability
            

            else:
                self.ui_state = Select.ability


        else:
            # スキル取得レベルで無ければスキル窓表示をスキップ
            self.ui_state = Select.ability