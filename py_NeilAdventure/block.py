from game import Game
from character import Character

# ブロッククラス
class Block(Character):

    # 画像を変える間隔
    CHANGE_IMAGE_INTERVAL = 20
    
    # コンストラクタ
    def __init__(self, block_type, image_list):
        # 親クラスのコンストラクタを実行
        super().__init__(image_list, Block.CHANGE_IMAGE_INTERVAL)
        # ブロック種別
        self.block_type = block_type
        # マップ全体での位置
        self.pos_x_in_map = 0
  
    # １フレームごとにする画像・処理
    def frame_process_img(self):
        # 表示位置を、プレイヤーの進んだ距離から算出
        self.pos_x = self.pos_x_in_map - Game.player.forward_len
    
    # 画面に描画
    def draw(self):
        super().draw((self.pos_x, self.pos_y))
        
    # blockクラスのget_rectをオーバーライド
    def get_rect(self):
        rect = super().get_rect()
        
        if self.block_type == 2:
            # 岩ブロックの場合、当たり判定を結構小さくする
            rect.x += rect.width * 0.1
            rect.y += rect.height * 0.1
            rect.width *= 0.8   
            rect.height *= 0.1 #was 0.8
            
        else:
            # 他の場合、当たり判定をやや小さくする(浮く岩)
            rect.x += rect.width * 0.1
            rect.y += rect.height * 0.1
            rect.width *= 0.8 
            rect.height *= 0.1  #was 0.8 #浮く岩Y軸当たり判定 
        return rect
    


        