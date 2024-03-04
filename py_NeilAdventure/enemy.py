import pygame
import random
from game import Game
from character import Character

# 敵キャラクタークラス
class Enemy(Character):

    # 画像を変える間隔
    CHANGE_IMAGE_INTERVAL = 20
    
    # コンストラクタ
    def __init__(self, enemy_type, image_list, change_image_interval):
        # 親クラスのコンストラクタを実行
        super().__init__(image_list, change_image_interval)
        # 敵種別を設定(0:車, 1:ボール, 2:鳥, 3:ハート, 4:item1, 5:item2)
        self.enemy_type = enemy_type
        # マップ全体での位置
        self.pos_x_in_map = 0
        self.pos_y_in_map = 0
        # 左方向の移動スピード
        self.y_speed = 3    #was 1
        # 下方向の移動スピード
        self.x_speed = 3    #was 1
        # 特殊移動フラグ
        self.sp_move = False
        # 特殊移動用カウンタ
        self.sp_move_count = 0
  
    # １フレームごとにする画像・処理
    def frame_process_img(self):
        if self.enemy_type == 0 or self.enemy_type ==1 or  self.enemy_type ==2:
            # 敵の位置を左に移動
            self.pos_x_in_map -= self.y_speed
            # 敵の表示位置を、プレイヤーの進んだ距離から算出
            self.pos_x = self.pos_x_in_map - Game.player.forward_len
            # 画面上の-1000 まで行ったら、現在位置+3000の位置に再設定
            if self.pos_x <= -1000:
                self.pos_x_in_map = Game.player.forward_len + 2000
                # ボールの場合は高さをランダムにする
                if self.enemy_type == 1:
                    self.pos_y = random.randint(100, 500)
           
        
        # 鳥の場合は、画面のx位置に対応して下降・上昇する
        if self.enemy_type == 2:
            if not self.sp_move and 400 <= self.pos_x <= 600:
                self.sp_move = True
                self.sp_move_count = 0
            if self.sp_move:
                # 移動が85までは下降する
                if self.sp_move_count < 85:
                    self.pos_y += 3
                # 移動が165まではそのまま
                elif self.sp_move_count < 165:
                    pass
                # 移動が250までは上昇する
                elif self.sp_move_count < 250:
                    self.pos_y -= 3
                # それらが終わったら特殊移動終了
                else:
                    self.sp_move = False
                self.sp_move_count += 1
        
        if self.enemy_type == 3 or self.enemy_type ==4 or self.enemy_type ==5:
        #3, 4, 5のアイテムを上から下に落とす
        # 敵の位置を左に移動
            self.pos_y_in_map += self.x_speed
            # 敵の表示位置を、プレイヤーの進んだ距離から算出
            self.pos_y = self.pos_y_in_map
            # 画面上の800 まで行ったら、現在位置-1600の位置に再設定
            if self.pos_y >= 800:
                self.pos_y_in_map = -800
                # ハートの場合は高さをランダムにする
                if self.enemy_type == 3:
                    self.pos_x = random.randint(100, 700)
            # print(self.pos_x, self.pos_y) #確認用

        # キノコの場合は、プレイヤーの位置に向かって移動する
        if self.enemy_type == 3:
            if Game.player.pos_y - self.pos_y < 0:
                self.pos_y -= 1
            elif Game.player.pos_y - self.pos_y > 0:
                self.pos_y += 1
            if Game.player.pos_x - self.pos_x < 0:
                self.pos_x_in_map -= 0.2
            elif Game.player.pos_y - self.pos_x > 0:
                self.pos_x_in_map += 1.2            
            
        # キャラクターの画像設定
        self.set_chara_animation()
    
    # 画面に描画
    def draw(self):
        super().draw((self.pos_x, self.pos_y))
        
    # Charactorクラスのget_rectをオーバーライド
    def get_rect(self):
        rect = super().get_rect()
        if self.enemy_type == 2:
            # 飛ぶ敵の場合、当たり判定を結構小さくする
            rect.x += rect.width * 0.3
            rect.y += rect.height * 0.1
            rect.width *= 0.4
            rect.height *= 0.8   
        else:
            # 他の場合、当たり判定をやや小さくする
            rect.x += rect.width * 0.1
            rect.y += rect.height * 0.1
            rect.width *= 0.8
            rect.height *= 0.8            
        return rect

        
