from keymap import choices_key
from random import choice
import arcade
from constants import *
from data import *


class MessageWindow:
    def __init__(self, engine):
        self.engine = engine
        self.choice = 0
        self.player_message = []

    def window_pop(self, viewports, choice):
        self.actor = self.engine.messenger
        self.viewports = viewports

        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        self.panel_left=self.viewport_left+GRID_SIZE*3
        self.panel_right=self.viewport_righit-GRID_SIZE*3
        self.panel_bottom=self.viewport_bottom+GRID_SIZE*3
        self.panel_top=self.viewport_top-GRID_SIZE*3

        if self.actor.npc_state == NPC_state.REQUEST:
            self.other_message = self.actor.message_event["request"]
            self.player_message = self.actor.message_event["reply"]
        elif self.actor.npc_state == NPC_state.WAITING:
            self.other_message = self.actor.message_event["waiting"]
            self.player_message = self.actor.message_event["accepted"]
        elif self.actor.npc_state == NPC_state.REWARD:
            self.other_message = self.actor.message_event["reward"]
            self.player_message = self.actor.message_event["ok"]

        self.panel_ui(choice)

    def panel_ui(self, c):
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.panel_left,
            bottom_left_y=self.panel_bottom,
            width=MAIN_PANEL_X - GRID_SIZE * 2,
            height=MAIN_PANEL_Y - GRID_SIZE * 6,
            color=[255, 255, 255, 150]
        )
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.panel_right,
            bottom_left_y=self.viewport_bottom,
            width=GRID_SIZE * 2,
            height=MAIN_PANEL_Y,
            color=[0, 0, 0, 255]
        )
        
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.panel_left,
            bottom_left_y=self.panel_bottom,
            width=MAIN_PANEL_X - GRID_SIZE * 2,
            height=MAIN_PANEL_Y - GRID_SIZE * 6,
            color=[181, 159, 39, 190]
        )

        arcade.draw_texture_rectangle(self.panel_left+GRID_SIZE, self.panel_top-GRID_SIZE, GRID_SIZE*1.5, GRID_SIZE*1.5, self.actor.texture)
        arcade.draw_texture_rectangle(self.panel_right-GRID_SIZE, self.panel_bottom+GRID_SIZE, GRID_SIZE*1.5, GRID_SIZE*1.5, IMAGE_ID["Rou"][1])
        y = 0
        for m in self.other_message:
            arcade.draw_text(
            text=m,
            start_x=self.panel_left+GRID_SIZE*2,
            start_y=self.panel_top-GRID_SIZE*2+y,
            color=arcade.color.AIR_FORCE_BLUE,
            font_size=35,
            font_name=UI_FONT)
            y -= 40


        if isinstance(c, int):
            self.choice = c
    
            # arcade.draw_rectangle_filled(self.panel_right-GRID_SIZE*4, self.panel_bottom+(GRID_SIZE*2)+(self.choice*40),MAIN_PANEL_X-GRID_SIZE*5,45,[153,21,111,150])
            arcade.draw_lrtb_rectangle_filled(self.panel_left+GRID_SIZE*2, self.panel_right-GRID_SIZE*2, self.panel_bottom+(GRID_SIZE*2.3)+(self.choice*40), self.panel_bottom+(GRID_SIZE*1.7)+(self.choice*40),[153,21,111,150])
        y=0
        for r in self.player_message:
            arcade.draw_text(
            text=r,
            start_x=self.panel_right-GRID_SIZE*2,
            start_y=self.panel_bottom+GRID_SIZE*2-y,
            color=arcade.color.ORIOLES_ORANGE,
            anchor_x="right",
            anchor_y="center",
            font_size=26,
            font_name=UI_FONT)
            y -= 40

    def message_choices(self, key):
        choice = choices_key(key)
        # 選択枠を上下にループする
        if isinstance(choice, int):
            self.choice += choice
            if self.choice >= len(self.player_message):
                self.choice = 0
            if self.choice == -1:
                self.choice = len(self.player_message)-1
        # choice変数に"select"が入ると"self.choice"変数の値を読んで反応を返す
        elif choice == "select":
            if self.actor.npc_state == NPC_state.WAITING:
                self.engine.game_state = GAME_STATE.NORMAL
            if self.choice == 0:
                self.actor.npc_state = NPC_state.WAITING
            elif self.choice != 0:
                self.engine.game_state = GAME_STATE.NORMAL
        
        return self.choice



