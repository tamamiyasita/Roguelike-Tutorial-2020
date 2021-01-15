import arcade
from constants import *
from util import grid_to_pixel, Bresenham
from itertools import chain



class SelectUI:
    def __init__(self, engine):
        self.engine = engine
        self.buttom_panel_width = SCREEN_WIDTH-STATES_PANEL_WIDTH
        self.panel_line_width = 4

        self.grid_sprites = arcade.SpriteList()
        self.d_time = 120
        self.x, self.y = 0, 0
        self.dx, self.dy = 0, 0
        self.grid_press = None
        self.grid_select = [0,0]
        self.sprite_list = []
        self.number = 0

    def nearby_actor(self, engine):
        result = []
        enemy_list = [enemy for enemy in engine.cur_level.actor_sprites if Tag.enemy in enemy.tag]
        e_len = len(enemy_list)
        for i in range(e_len):
            sprite = arcade.get_closest_sprite(engine.player, enemy_list)[0]
            if sprite.is_visible:
                result.append(sprite)
                enemy_list.remove(sprite)
        return result


    def draw_in_select_ui(self, viewports, engine):
        if len(self.sprite_list) <= self.number:
            self.number = 0
        try:
            self.sprite_list = self.nearby_actor(engine)
            sprite = self.sprite_list[self.number]
                      
            self.dx, self.dy = sprite.x, sprite.y
        except:    
            self.dx, self.dy = engine.player.x, engine.player.y

        self.viewports = viewports
        self.viewport_left = self.viewports[0]
        self.viewport_righit = self.viewports[1]
        self.viewport_bottom = self.viewports[2]
        self.viewport_top = self.viewports[3]

        self.panel_ui()
        self.grid_cursor()
        self.update()

    def update(self):

        self.d_time -= 2
        if -40 > self.d_time:
            self.d_time = 120

            #############

            ##ターゲットシステムの構想　fireシステムに渡す、またはターゲットSkill使用時に呼び出される？　actor.spritesをループし、visibleならカーソルをそのアクターに合わせる
            # その際に問題となる点。キー押下で決定　または次のターゲットにするのと近くのターゲットに最初にカーソルを合わせる方法
            # ていうかfireシステムから機能をうまく分離すれば良さそうな感じだ
            # あとファイアボールスクロールクラスからターゲット選択中の一時停止処理を借りれば
        try:
            for line in Bresenham((self.engine.player.x, self.engine.player.y),(self.dx, self.dy)):
                line = grid_to_pixel(*line)
                arcade.draw_rectangle_filled(line[0],line[1], GRID_SIZE, GRID_SIZE, [100,100,10,100,])
        except:
            pass
        # try:
        #     p = arcade.has_line_of_sight((self.engine.player.center_x, self.engine.player.center_y),(self.x, self.y), self.engine.cur_level.wall_sprites)
        #     if p:
        #         print(p)
                # arcade.draw_rectangle_filled(self.x,self.y,GRID_SIZE,GRID_SIZE,arcade.color.BLACK_BEAN)
        # except:
        #     pass

        #########
    def panel_ui(self):
        # 画面下のパネルをarcadeの四角形を描画する変数で作成
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left,
            bottom_left_y=self.viewport_bottom,
            width=self.buttom_panel_width,
            height=STATES_PANEL_HEIGHT,
            color=COLORS["status_panel_background"]
        )

        # 下パネルの周りの線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_left+self.panel_line_width*0.5,
            bottom_left_y=self.viewport_bottom+self.panel_line_width*0.5,
            width=self.buttom_panel_width-self.panel_line_width,
            height=STATES_PANEL_HEIGHT,
            color=arcade.color.ORANGE,
            border_width=self.panel_line_width
        )

        # 画面横のパネル
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH,
            bottom_left_y=self.viewport_bottom,
            width=STATES_PANEL_WIDTH,
            height=SCREEN_HEIGHT,
            color=arcade.color.LIBERTY
        )

        # 横パネルの周りの線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH -
            STATES_PANEL_WIDTH + self.panel_line_width*0.5,
            bottom_left_y=self.viewport_bottom + self.panel_line_width*0.5,
            width=STATES_PANEL_WIDTH - self.panel_line_width,
            height=SCREEN_HEIGHT - self.panel_line_width-231,
            color=arcade.color.LEMON_CHIFFON,
            border_width=self.panel_line_width
        )

        # ミニマップ囲い線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_left + SCREEN_WIDTH -
            STATES_PANEL_WIDTH + self.panel_line_width*0.5,
            bottom_left_y=self.viewport_bottom + SCREEN_HEIGHT - 228,
            width=STATES_PANEL_WIDTH - self.panel_line_width,
            height=225,
            color=arcade.color.BABY_BLUE,
            border_width=self.panel_line_width
        )

    def grid_cursor(self):
        self.sprites = [self.engine.cur_level.actor_sprites,
                        self.engine.cur_level.item_sprites]

        self.dx += self.grid_select[0]
        self.dy += self.grid_select[1]

        self.x, self.y = grid_to_pixel(self.dx, self.dy)
        if self.x < self.viewport_left:
            print(f"{self.x=} {self.viewport_left=}")


        # グリッド囲い線の描写
        arcade.draw_rectangle_outline(
            center_x=self.x,
            center_y=self.y,
            width=SPRITE_SIZE*SPRITE_SCALE,
            height=SPRITE_SIZE*SPRITE_SCALE,
            color=arcade.color.LIGHT_BLUE,
            border_width=2
        )
        # 点滅するグリッド内部
        arcade.draw_rectangle_filled(
            center_x=self.x,
            center_y=self.y,
            width=SPRITE_SIZE*SPRITE_SCALE-2,
            height=SPRITE_SIZE*SPRITE_SCALE-2,
            color=[255, 255, 255, self.d_time]
        )
        try:

            # グリッド囲い線の中にあるオブジェクトの情報の表示
            actor_at_point = arcade.get_sprites_at_exact_point(
                (self.x, self.y), self.sprites[0])
            item_at_point = arcade.get_sprites_at_exact_point(
                (self.x, self.y), self.sprites[1])
            if actor_at_point or item_at_point:
                y = 20
                for actor in chain(actor_at_point, item_at_point):
                    if actor.ai:
                        arcade.draw_text(
                            text=f"{actor.name.capitalize()}\n{actor.fighter.hp}/{actor.fighter.max_hp}",
                            start_x=self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH + 10,
                            start_y=self.viewport_bottom + SCREEN_HEIGHT - 400 - y,
                            color=arcade.color.RED_PURPLE,
                            font_size=20,
                        )
                        y += 20

                    y += 10

                    if not actor.ai:
                        arcade.draw_text(
                            text=f"{actor.__class__.__name__}",
                            start_x=self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH + 10,
                            start_y=self.viewport_bottom + SCREEN_HEIGHT - 400 - y,
                            color=arcade.color.GREEN_YELLOW,
                            font_size=20,
                        )
                        y += 30

                    if actor.explanatory_text:
                        arcade.draw_text(
                            text=f"{actor.explanatory_text}",
                            start_x=self.viewport_left + SCREEN_WIDTH - STATES_PANEL_WIDTH + 10,
                            start_y=self.viewport_bottom + SCREEN_HEIGHT - 400 - y,
                            color=arcade.color.WHITE,
                            font_size=14,
                        )
                        y += 20
        except:
            pass