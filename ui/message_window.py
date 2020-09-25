from keymap import choices_key
from random import choice
import arcade
from constants import *
from data import *
from keymap import choices_key


class MessageWindow:
    def __init__(self, engine):
        self.engine = engine
        self.choice = 0
        self.player_message = []

    def window_pop(self, viewports, choice):
        self.viewports = viewports
        self.actor = self.engine.messenger
        if self.actor.npc_state == NPC_state.REQUEST:
            self.other_message = self.actor.message_event["request"]
            self.player_message = self.actor.message_event["reply"]
        elif self.actor.npc_state == NPC_state.WAITING:
            self.other_message = self.actor.message_event["waiting"]
            self.player_message = self.actor.message_event["accepted"]
        elif self.actor.npc_state == NPC_state.REWARD:
            self.other_message = self.actor.message_event["reward"]
            self.player_message = self.actor.message_event["ok"]


        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        self.panel_left_x=self.viewport_left+200
        self.panel_left_y=self.viewport_bottom+200


        self.panel_ui(choice)

    def panel_ui(self, c):
        f = arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left+200,
            bottom_left_y=self.viewport_bottom+200,
            width=SCREEN_WIDTH - 400,
            height=SCREEN_HEIGHT - 400,
            color=[255, 255, 255, 150]
        )
        arcade.draw_texture_rectangle(self.panel_left_x+50, self.panel_left_y+510, GRID_SIZE, GRID_SIZE, self.actor.texture)
        arcade.draw_texture_rectangle(self.panel_left_x+1030, self.panel_left_y+50, GRID_SIZE*1.5, GRID_SIZE*1.5, IMAGE_ID["player"][1])
        y = 45
        for m in self.other_message:
            arcade.draw_text(
            text=m,
            start_x=self.panel_left_x+100,
            start_y=self.panel_left_y+380+y,
            color=arcade.color.AIR_FORCE_BLUE,
            font_size=45)
            y -= 45


        if isinstance(c, int):
            self.choice = c
    
            arcade.draw_rectangle_filled((self.viewport_left+self.viewport_righit)/2, self.panel_left_y+100+(self.choice*45),SCREEN_WIDTH-410,45,[153,21,111,150])
        y=0
        for r in self.player_message:
            arcade.draw_text(
            text=r,
            start_x=self.panel_left_x+990,
            start_y=self.panel_left_y+100-y,
            color=arcade.color.ORIOLES_ORANGE,
            anchor_x="right",
            anchor_y="center",
            font_size=30)
            y -= 45

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



