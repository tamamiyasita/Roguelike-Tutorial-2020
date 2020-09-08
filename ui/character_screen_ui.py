from viewport import viewport
import arcade
from constants import *
from data import *


class CharacterScreen:
    def __init__(self, player):
        self.player = player
        self.character_sheet_buttons = arcade.SpriteList()

    def draw_character_screen(self, viewport_x, viewport_y):
        self.viewport_left = viewport_x
        self.viewport_bottom = viewport_y

        """背景"""
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=0+self.viewport_left,
            bottom_left_y=0+self.viewport_bottom,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            color=COLORS["status_panel_background"]
        )

        """タイトル"""
        spacing = 1.8
        text_position_y = SCREEN_HEIGHT - 50 + self.viewport_bottom
        text_position_x = 10 + self.viewport_left
        text_size = 24
        screen_title = "Character Screen"
        text_color = arcade.color.AFRICAN_VIOLET
        arcade.draw_text(
            text=screen_title,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )

        """ステータス表示"""
        text_position_y -= text_size * spacing
        text_size = 20
        states_text = f"Attack: {self.player.fighter.base_strength} + {self.player.equipment.states_bonus['str']}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )

        text_position_y -= text_size * spacing  # TODO ゼロならボーナス非表示にしよう
        states_text = f"Defense: {self.player.fighter.base_defense} + {self.player.equipment.states_bonus['defense']}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )

        text_position_y -= text_size * spacing
        states_text = f"HP: {self.player.fighter.hp} / {self.player.fighter.max_hp}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )

        text_position_y -= text_size * spacing
        states_text = f"Level: {self.player.fighter.level}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size
        )

        """ボタンのスプライト"""
        spacing = 37
        sheet_y = self.viewport_bottom + SCREEN_HEIGHT - 75
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_left + 200
        button.center_y = sheet_y
        button.name = "Attack"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_left + 200
        button.center_y = sheet_y
        button.name = "Defense"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_left + 200
        button.center_y = sheet_y
        button.name = "HP"
        self.character_sheet_buttons.append(button)

        self.draw_button()

    def draw_button(self):
        """ボタンの描画"""
        self.character_sheet_buttons = arcade.SpriteList()

        spacing = 37
        sheet_y = self.viewport_bottom + SCREEN_HEIGHT - 75
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_left + 200
        button.center_y = sheet_y
        button.name = "Attack"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_left + 200
        button.center_y = sheet_y
        button.name = "Defense"
        self.character_sheet_buttons.append(button)

        sheet_y -= spacing
        button = arcade.Sprite(r"image\plus_button.png")
        button.center_x = self.viewport_left + 200
        button.center_y = sheet_y
        button.name = "HP"
        self.character_sheet_buttons.append(button)

        if self.player.fighter.ability_points > 0:
            self.character_sheet_buttons.draw()

    def buttons_click(self, x, y):
        if self.player.fighter.ability_points > 0:
            buttons_clicked = arcade.get_sprites_at_point(
                point=(x, y),
                sprite_list=self.character_sheet_buttons
            )
            for buttons in buttons_clicked:
                if buttons.name == "Attack":
                    self.player.fighter.base_strength += 1
                    self.player.fighter.ability_points -= 1
                elif buttons.name == "Defense":
                    self.player.fighter.base_defense += 1
                    self.player.fighter.ability_points -= 1
                elif buttons.name == "HP":
                    self.player.fighter.base_max_hp += 15
                    self.player.fighter.max_hp += 15
                    self.player.fighter.ability_points -= 1

#
