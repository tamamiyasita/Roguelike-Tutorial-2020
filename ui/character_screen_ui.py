import arcade
from constants import *
from data import *
import pyglet.gl as gl

class CharacterScreenUI:
    def __init__(self, engine):
        self.engine = engine
        self.player = engine.player
        self.font_name=UI_FONT
        

    def draw_character_screen(self, viewport, selected_item):
        self.selected_item = selected_item
        self.viewport_left = viewport[0] + GRID_SIZE*3
        self.viewport_right = viewport[1]
        self.viewport_bottom = viewport[2] + GRID_SIZE*3
        self.viewport_top = viewport[3]

        self.ui_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)


        # viewport_left = viewport_x+100
        # self.viewport_bottom = viewport_y+100
        self.panel_width = SCREEN_WIDTH-GRID_SIZE*6
        self.panel_height = SCREEN_HEIGHT-GRID_SIZE*6

        self.panel_top = self.viewport_bottom + self.panel_height
        self.panel_side = self.viewport_left + 18
        """背景"""
        cs = arcade.load_texture(r"image\chara_screen.png")
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=self.viewport_left,
            bottom_left_y=self.viewport_bottom,
            width=self.panel_width,
            height=self.panel_height,
            texture=cs
        )
        # キャラクターアイコン
        c = arcade.Sprite(filename=r"image\chara_sheet.png", scale=6,
                        center_x=self.viewport_left + 82,
                        center_y=self.panel_top - GRID_SIZE - 20)
        self.ui_sprites.append(c)
        


        """タイトル"""
        spacing = 1.65
        text_position_y = self.panel_top 
        text_position_x = self.panel_side+2
        text_size = 24 
        text_color = (186, 253, 143)

        
        arcade.draw_text(
            text="Character Screen",
            start_x=self.panel_side,
            start_y=self.panel_top-12,
            color=(255, 122, 248),
            font_size=text_size
        )

        """ステータス表示"""
        text_position_y -= text_size * spacing
        text_size = 16
        m = -2
        u = GRID_SIZE *2+18

        states_text = f"Race: {self.player.race}"
        arcade.draw_text(
            text=states_text,
            start_x=self.panel_side+u,
            start_y=text_position_y+m,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )

        text_position_y -= text_size * spacing
        states_text = f"Name: {self.player.name}"
        arcade.draw_text(
            text=states_text,
            start_x=self.panel_side+u,
            start_y=text_position_y+m,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )

        text_position_y -= text_size * spacing
        states_text = f"Lv  : {self.player.fighter.level}"
        arcade.draw_text(
            text=states_text,
            start_x=self.panel_side+u,
            start_y=text_position_y+m,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )
        text_position_y -= text_size * spacing
        states_text = f"Next: {self.player.experience_per_level[self.player.fighter.level+1]-self.player.fighter.current_xp}.exp"
        arcade.draw_text(
            text=states_text,
            start_x=self.panel_side+u,
            start_y=text_position_y+m,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )


        spacing = 1.78
        text_size = 15
        text_position_y -= text_size * spacing +8
        states_text ="[States]"
        arcade.draw_text(
            text=f"{states_text: ^14}",
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size-1,
            font_name=self.font_name,
        )
        text_position_y -= text_size * spacing
        states_text = f"MHP: {self.player.fighter.max_hp: >3}  +{self.player.equipment.states_bonus['max_hp']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )

        text_position_y -= text_size * spacing
        states_text = f"STR: {self.player.fighter.base_strength: >3}  +{self.player.equipment.states_bonus['STR']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )

        text_position_y -= text_size * spacing 
        states_text = f"DEX: {self.player.fighter.base_dexterity: >3}  +{self.player.equipment.states_bonus['DEX']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )

        text_position_y -= text_size * spacing
        states_text = f"INT: {self.player.fighter.base_intelligence: >3}  +{self.player.equipment.states_bonus['INT']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )
        text_position_y -= text_size * spacing
        states_text = f"DEF: {self.player.fighter.defense: >3}  +{self.player.equipment.states_bonus['defense']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )
        text_position_y -= text_size * spacing
        states_text = f"EVE: {self.player.fighter.defense: >3}  +{self.player.equipment.states_bonus['evasion']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )
        text_position_y -= text_size * spacing
        states_text = f"SPD: {self.player.fighter.speed: >3}  +{self.player.equipment.states_bonus['speed']: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=text_position_x,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )
        text_position_y -= text_size * spacing +7
        states_text = f"[Resistance]"
        arcade.draw_text(
            text=f"{states_text: ^14}",
            start_x=text_position_x-5,
            start_y=text_position_y,
            color=text_color,
            font_size=text_size,
            font_name=self.font_name
        )
        text_position_y -= text_size * spacing
        for r_key, r_val in self.player.fighter.resist.items():
            states_text = f"{r_key[:4]:<4}:  {r_val}  +{self.player.equipment.resist_bonus[r_key]: >3}"
            arcade.draw_text(
                text=states_text,
                start_x=self.panel_side+2,
                start_y=text_position_y,
                color=text_color,
                font_size=15,
                font_name=self.font_name
                )
            text_position_y -= text_size * spacing
        self.draw_flowers()
        self.ui_sprites.draw(filter=gl.GL_NEAREST)

    def draw_flowers(self):
        """スキルリストの表示"""
        left_position = self.viewport_left + GRID_SIZE*3+20
        top_position = self.panel_top-GRID_SIZE*2-25
        y = -20 # セパレート
        item_font_size = 15
        flowers = self.player.equipment.flower_slot
        skill_list = list(self.player.fighter.skill_list)
        skill_list = sorted(skill_list, key=lambda x: x.level, reverse=True)

        # arcade.draw_text(
        #     text="Flowers",
        #     start_x=left_position,
        #     start_y=top_position,
        #     color=(129, 255, 71),
        #     font_size=item_font_size,
        #     font_name=UI_FONT
        # )

        # First icon
        first_icon = arcade.load_texture(r"image\first.png")
        arcade.draw_texture_rectangle(
            center_x=left_position + 20,
            center_y=top_position + y-21,
            width=40,
            height=40,
            texture=first_icon
        )
        y -= 84        

        for i, flower in enumerate(flowers):


            item_text = f"{flower.name}".replace("_", " ").title()

            # TODO passive activeのiconの位置調整
            # TODO 最初のslot icon
            # TODO 全体的なiconのテキスト位置
            # TODO 選択枠のsprite
            # TODO 背景のsprite変更
            # 花アイコンには上に名前横にLV　HP/MHP　EXP





            # 二列目
            if i == 4:
                left_position += GRID_SIZE * 5
                y = -20
            
            
            # 上下移動出来る選択枠
            if i == self.selected_item:
                arcade.draw_lrtb_rectangle_outline(
                    left=left_position,
                    right=left_position + GRID_SIZE*3,
                    top=top_position + y,
                    bottom=top_position + y - (GRID_SIZE/2) - 9,
                    color=[252,250,20,255],
                    border_width=1
                )



            # タイトル
            arcade.draw_text(
                text=item_text,
                start_x=left_position,
                start_y=top_position + y,
                color=(129, 255, 81),
                font_size=item_font_size-4,
                # font_nameself.=UI_FONT2
            )

            
            # flower icon
            arcade.draw_texture_rectangle(
                center_x=left_position + 20,
                center_y=top_position + y-21,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )
            arcade.draw_texture_rectangle(
                center_x=left_position + 20,
                center_y=top_position + y-21,
                width=40,
                height=40,
                texture=flower.icon
            )
            # EXPの表示
            if flower.level < len(flower.experience_per_level):
                xp_to_next_level = flower.experience_per_level[flower.level+1]
                exp_text = f"XP {flower.current_xp: >4} / {xp_to_next_level: >4}"
            else:
                exp_text = f"XP {flower.current_xp}"
            arcade.draw_text(text=exp_text,
                            start_x=left_position + 43,
                            start_y=top_position + y-20,
                            color=(239,192,70),
                            font_size=9,
                            font_name=UI_FONT2
                            )
            # passviveとactiveでicon位置調整
            skill = flower.flower_skill
            # if Tag.passive in skill.tag:
            #     sx = GRID_SIZE*2
            # elif Tag.active in skill.tag:
            #     sx = GRID_SIZE*3
            sx = GRID_SIZE*2
            arcade.draw_texture_rectangle(
                center_x=left_position + 20 + sx,
                center_y=top_position + y-21,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )
            arcade.draw_texture_rectangle(
                center_x=left_position + 20 + sx,
                center_y=top_position + y-21,
                width=40,
                height=40,
                texture=skill.icon
            )
                
            # skill level
            arcade.draw_text(
                text=f"level {flower.level}",
                start_x=left_position + 43,
                start_y=top_position + y-2,
                color=(234, 255, 96),
                font_size=item_font_size-4,
                # font_name=self.UI_FONT2,
                anchor_y="top"
            )

            y -= 84        





