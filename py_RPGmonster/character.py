from game import Game
from square import Square

# キャラクタークラス（プレイヤーとモンスターの共通的な部分のクラス）
class Character(Square):
    
    # 画像を変える間隔
    CHANGE_IMAGE_INTERVAL = 10
    # キャラクターの移動距離
    MOVE_STEP = 16   ###オリジナルは16だよ###
    
    # コンストラクタ
    def __init__(self):
        # 親クラスのコンストラクタを呼び出し
        super().__init__()
        # 画像リスト
        self.image_list = None
        # 画像変更タイミング
        self.next_img_count = Game.count + Character.CHANGE_IMAGE_INTERVAL
        

    # 画像リスト設定
    def set_images(self, image_list):
        self.image_list = image_list    #画像リスト
        self.img_no = 0               #画像番号
        
        # 画像を設定
        self.set_image(self.image_list[self.img_no])

    # キャラクターの位置を計算
    def calc_chara_pos(self, posx, posy, dx, dy):
        # スクエアに対する端数が１スクエア分を超える
        # またはマイナスになる場合に値を調整
        if dx < 0:
            posx -= 1
            dx += Game.SQ_LEN
        elif dx >= Game.SQ_LEN:
            posx += 1
            dx = dx - Game.SQ_LEN
        if dy < 0:
            posy -= 1
            dy += Game.SQ_LEN
        elif dy >= Game.SQ_LEN:
            posy += 1
            dy = dy - Game.SQ_LEN
            
        return posx, posy, dx, dy
    

    # キャラクター移動チェック
    def check_chara_move(self, posx, posy, dx, dy, unmovable_chip_list):
        check_pos_list = []         # チェック位置リスト
        # チェック対象に、移動先のposx, posyを追加
        check_pos_list.append((posx, posy))
        # もし、上下方向にずれがある場合、ひとつ下のマスもチェック対象に追加
        if dy !=0:
            check_pos_list.append((posx, posy +1))
        # もし、左右方向にずれがある場合、ひとつ右のマスもチェック対象に追加
        if dx !=0:
            check_pos_list.append((posx +1, posy))
        # もし、両方にずれがある場合、右下のマスもチェック対象に追加
        if dx != 0 and dy != 0:
            check_pos_list.append((posx +1, posy +1))
        # フィールドクラスのチェックを実施し、その結果を戻り値に設定
        return Game.field.check_movable(check_pos_list, unmovable_chip_list)

    # キャラクターの画像（アニメーション）設定
    def set_chara_animation(self):
        # 画像を変えるタイミングの場合、画像を変更
        if self.next_img_count <= Game.count:
            # 画像番号を１加算して、画像の数を超えた場合０に戻す
            self.img_no += 1
            self.img_no = self.img_no if self.img_no < len(self.image_list) else 0
            # 親クラス（Square）の画像を設定
            self.set_image(self.image_list[self.img_no])
            # 次の画像変更タイミングを設定
            self.next_img_count = Game.count + Character.CHANGE_IMAGE_INTERVAL
            


