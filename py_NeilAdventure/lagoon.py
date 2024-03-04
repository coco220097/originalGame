from game import Game
from character import Character

# ゴールクラス
class Lagoon(Character):

    # 画像を変える間隔
    CHANGE_IMAGE_INTERVAL = 20
    
    # コンストラクタ
    def __init__(self, image_list):
        # 親クラスのコンストラクタを実行
        super().__init__(image_list, Lagoon.CHANGE_IMAGE_INTERVAL)
        # マップ全体での位置
        self.pos_x_in_map = 0
  
    # １フレームごとにする画像・処理
    def frame_process_img(self):
        # 表示位置を、プレイヤーの進んだ距離から算出
        self.pos_x = self.pos_x_in_map - Game.player.forward_len
    
    # 画面に描画
    def draw(self):
        super().draw((self.pos_x, self.pos_y))

        