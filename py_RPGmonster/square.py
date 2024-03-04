from game import Game
from pygame.locals import Rect

# スクエア（画面に表示する１マス）クラス
# 同サイズで描画するものは、すべてこのクラスを継承します
class Square:
    
    # コンストラクタ
    def __init__(self):
        self.image = None           #画像
        self.pos = [-100, -100]     #フィールド上の位置
        self.dxy = [0, 0]           #位置からのずれ

    # 画面に描画
    def draw(self):
        # 描画位置を設定
        x = self.pos[0] * Game.SQ_LEN + self.dxy[0]
        y = self.pos[1] * Game.SQ_LEN + self.dxy[1]
        # 画面に描画
        Game.surface.blit(self.image, (x, y),
                          (0, 0, Game.SQ_LEN, Game.SQ_LEN))

    # このスクエアの位置・サイズのRectを取得
    def get_rect(self):
        # 位置を設定
        x = self.pos[0] * Game.SQ_LEN + self.dxy[0]
        y = self.pos[1] * Game.SQ_LEN + self.dxy[1]
        return Rect(x, y, Game.SQ_LEN, Game.SQ_LEN)

    # 画像を設定
    def set_image(self, image):
        self.image = image
    # 位置を設定
    def set_pos(self, posx, posy):
        self.pos = [posx, posy]
    # 位置を取得
    def get_pos(self):
        return self.pos
    # ずれ位置を設定
    def set_dpos(self, dx, dy):
        self.dxy = [dx, dy]
    # ずれ位置を取得
    def get_dpos(self):
        return self.dxy
