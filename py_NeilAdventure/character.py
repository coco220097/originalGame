from game import Game
from pygame import Rect

# キャラクタークラス（アニメーションするものが継承するクラス）
class Character:

    # コンストラクタ
    def __init__(self, image_list, change_image_interval):
        # 画像リスト
        self.image_list = image_list
        # 画像番号は最初は０を設定
        self.img_no = 0
        self.image = self.image_list[self.img_no]
        # 画像変更間隔
        self.change_image_interval = change_image_interval
        # 画像変更タイミング
        self.next_img_count = Game.count + self.change_image_interval
        # 画面上の位置
        self.pos_x, self.pos_y = 0, 0
                
    # キャラクターの画像（アニメーション）設定
    def set_chara_animation(self):
        # 画像を変えるタイミングの場合、画像を変更
    
        if self.next_img_count <= Game.count:
            # 画像番号を１加算して、画像の数を超えた場合０に戻す
            self.img_no += 1
            self.img_no = self.img_no if self.img_no < len(self.image_list) else 0
            # 次の画像変更タイミングを設定
            self.next_img_count = Game.count + self.change_image_interval

    # 画面に描画
    def draw(self, pos):
        # 画面に描画
        self.image = self.image_list[self.img_no]
        Game.surface.blit(self.image, pos)

    # 四角を取得
    def get_rect(self):
        # 位置を設定
        width = self.image.get_width()
        height = self.image.get_height()
        return Rect(self.pos_x, self.pos_y, width, height)
    
    # 四角を取得(ブロックのみ)
    def get_rectforblock(self):
        # 位置を設定
        width = self.image.get_width()
        height = self.image.get_height()
        return Rect(self.pos_x, self.pos_y, width, height)
    
