
import arcade
from constants import *

class NormalUI:
    """GameState=Normal時に描画するUI
    """
    def __init__(self, player, viewport_x, viewport_y,selected_item, messages, mouse_position):
        self.player = player
        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
        self.selected_item = selected_item
        self.messages = messages
        self.mouse_position = mouse_position


    def draw_in_normal_state(self):
        """mainに渡すメソッドをまとめる"""
        self.draw_hp_and_status_bar()
        self.draw_inventory()
        self.draw_messages_handle()


    def draw_hp_and_status_bar(self):
        """ステータスパネルとHPバー"""
        # パネル用変数
        hp_font_size = 13
        hp_bar_width = hp_font_size * 5  # HPバーの幅
        hp_bar_height = hp_font_size - 2  # HPバーの太さ
        hp_bar_margin = self.viewport_y + STATES_PANEL_HEIGHT - 7  # パネル上端からのHPバーの位置
        left_margin = self.viewport_x + 25  # 画面左からのHPとバーの位置
        top_hp_margin = hp_bar_margin - 23  # パネル上端からのHPの位置
        top_exp_margin = top_hp_margin - 15  # top_hp_marginからのEXPの位置

        # HP/MAXHPの表示
        hp_text = f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}"

        arcade.draw_text(text=hp_text,
                         start_x=left_margin,
                         start_y=top_hp_margin,
                         color=COLORS["status_panel_text"],
                         font_size=hp_font_size
                         )

        # EXPの表示
        if self.player.fighter.level < len(EXPERIENCE_PER_LEVEL):
            xp_to_next_level = EXPERIENCE_PER_LEVEL[self.player.fighter.level - 1]
            exp_text = f"XP: {self.player.fighter.current_xp} / {xp_to_next_level}"
        else:
            exp_text = f"XP: {self.player.fighter.current_xp}"

        arcade.draw_text(text=exp_text,
                         start_x=left_margin,
                         start_y=top_exp_margin,
                         color=arcade.color.BAZAAR
                         )

        # レベルの表示
        level_text = f"Level:{self.player.fighter.level}"

        arcade.draw_text(text=level_text,
                         start_x=left_margin,
                         start_y=top_exp_margin - 20,
                         color=arcade.color.BITTERSWEET
                         )

        # HPバーの描画
        draw_status_bar(center_x=hp_bar_width / 2 + left_margin,
                        center_y=hp_bar_margin,
                        width=hp_bar_width,
                        height=hp_bar_height,
                        current_value=self.player.fighter.hp,
                        max_value=self.player.fighter.max_hp
                        )
    
    
    def draw_inventory(self):
        """インベントリの表示"""
        item_left_position = self.viewport_x + SCREEN_WIDTH / 2.3 # パネル左からの所持アイテム表示位置の調整に使う変数
        item_top_position = self.viewport_y + STATES_PANEL_HEIGHT - 22 # パネル上端からの所持アイテム表示位置の調整に使う変数
        separate_size = 1.5  # アイテム名の表示間隔の調整に使う変数
        margin = 3 # 選択したアイテムのアウトライン線の位置調整に使う変数
        item_font_size = 12
        outline_size = 2
        capacity = self.player.inventory.capacity
        selected_item = self.selected_item  # ボタン押下で選択したアイテムオブジェクト
        field_width = SCREEN_WIDTH / (capacity + 1) / separate_size  # アイテム表示感覚を決める変数

        # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
        # TODO 複数行にする処理を考える（５回ループしたら縦と横の変数に増減するなど）
        for item in range(capacity):
            items_position = item * field_width + item_left_position  # パネル左からの所持アイテムの表示位置
            if item == selected_item:
                arcade.draw_lrtb_rectangle_outline(
                        left=items_position - margin,
                        right=items_position + field_width - margin,
                        top=item_top_position + item_font_size + margin*2,
                        bottom=item_top_position - margin,
                        color=arcade.color.BLACK,
                        border_width=outline_size
                        )

            if self.player.inventory.bag[item]:
                item_name = self.player.inventory.bag[item].name
            else:
                item_name = ""

            item_text = f"{item+1}: {item_name}"

            arcade.draw_text(
                        text=item_text,
                        start_x=items_position,
                        start_y=item_top_position,
                        color=COLORS["status_panel_text"],
                        font_size=item_font_size
                        )


    def draw_messages_handle(self):
        """メッセージ表示領域"""
        margin = 3
        message_top_position = 19 # パネル上端からのメッセージ表示位置
        message_left_position = self.viewport_x -margin + 125 # 画面左からのメッセージ表示位置
        message_panel_width = (SCREEN_WIDTH / 2.3) - 125 - margin # メッセージパネル幅
        message_panel_height = STATES_PANEL_HEIGHT # メッセージパネル高
        message_first_position = self.viewport_y + STATES_PANEL_HEIGHT - message_top_position # 最初の行
        
        arcade.draw_xywh_rectangle_filled(
                        bottom_left_x=message_left_position,
                        bottom_left_y=self.viewport_y,
                        width=message_panel_width,
                        height=message_panel_height,
                        color=arcade.color.SHAMPOO
                        )

        for message in self.messages:
            arcade.draw_text(
                        text=message,
                        start_x=message_left_position,
                        start_y=message_first_position,
                        color=COLORS["status_panel_text"]
                        )

            # 文字送り
            message_first_position -= message_top_position


def draw_status_bar(center_x, center_y, width, height, current_value, max_value):
    """ステータスバーの実体"""
    arcade.draw_rectangle_filled(
        center_x, center_y, width, height, color=COLORS.get("status_bar_background"))
    states_width = (current_value / max_value) * width
    arcade.draw_rectangle_filled(center_x - (width / 2 - states_width / 2),
                                 center_y, states_width, height, COLORS["status_bar_foreground"])
