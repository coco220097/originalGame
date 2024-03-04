import pygame
from game import Game
from character import Character

# プレイヤークラス
class Player(Character):

    # 画像を変える間隔
    CHANGE_IMAGE_INTERVAL = 5
    
    # コンストラクタ
    def __init__(self):
        self.image_list = (pygame.image.load("image/player-r1hamu.png"),
                           pygame.image.load("image/player-r2hamu.png"),
                           pygame.image.load("image/player-r3hamu.png"))
  
        
        # 親クラスのコンストラクタを実行
        super().__init__(self.image_list, Player.CHANGE_IMAGE_INTERVAL)
        # 画面上の位置
        self.pos_x = 150
        self.pos_y = 425
        # キャラが右に進んだ距離
        self.forward_len = 0
        # ジャンプ中フラグ
        self.is_jump = False
        # 空中フラグ
        self.in_air = False
        # ジャンプ距離
        self.jump_len = 0
        # ライフ
        self.life = 3
        self.max_life = 3
        # 次のヒット判定カウント
        self.next_hit_count = 0
        # ゴール判定カウント
        self.goal_count = -1
        # ラグーン 判定カウント
        self.lagoon_count = -1
  
######################
    # 右移動処理
    def right_move(self, step):
        move_step = 0               # 進める距離
        pos_x_base = self.pos_x     # 移動前の位置
        # 移動距離だけ繰り返し
        for i in range(step):
            # 右に１だけ、画面上の距離を移動
            self.pos_x += 1
            move_step += 3  #was 1
            # ブロックとぶつかった場合
            if self.block_check() > 0:
                move_step -= 1
                break
        # 画面上の位置を戻す
        self.pos_x = pos_x_base
        # 進める距離分進ませる
        self.forward_len += move_step
        
    # 左移動処理
    def left_move(self, step):
        move_step = 0 
        pos_x_base = self.pos_x     # 移動前の位置
        # 移動距離だけ繰り返し
        for i in range(step):
            # 左に１だけ移動
            self.pos_x -= 1
            move_step += 3
            
            # # 通りぬけられないブロックとぶつかった場合のｘ軸
            # if self.block_check() > 0:
            #     # 元の位置に戻して、Falseを返却
            #     self.pos_x += 1
            #     return False
        # 通常に戻ったらTrueを返却
        return True

    # 上移動処理
    def up_move(self, step):
        # 移動距離だけ繰り返し
        for i in range(step):
            # 上に１だけ移動
            self.pos_y -= 1
            # # 通りぬけられないブロックとぶつかった場合のｙ軸
            # if self.block_check() > 0:
            #     # 元の位置に戻して、Falseを返却
            #     self.pos_y += 1
            #     return False
        # 通常に上昇できたらTrueを返却
        return True

    # 下移動処理
    def down_move(self, step):
        # 移動距離だけ繰り返し
        for i in range(step):
            # 下に１だけ移動
            self.pos_y += 1
            # 下限位置、または、何らかのブロックとぶつかった場合
            if self.pos_y >= 425 or self.block_check() >= 0:
                # 元の位置に戻して、Falseを返却
                self.pos_y -= 1
                return False
        # 通常に下降できたらTrueを返却
        return True  
#####################################  
  
    # １フレームごとにする画像・処理
    def frame_process_img(self):
        
        # 右キーが押されている間、キャラを右に進ませる
        # （背景を左に移動させる）
        if Game.on_rightkey():
            self.image_list = (pygame.image.load("image/player-r1hamu.png"),
                                pygame.image.load("image/player-r2hamu.png"),
                                pygame.image.load("image/player-r3hamu.png"))               
            self.pos_x += 3
            self.forward_len += 1
            self.right_move(1)    #←コレ主人公の速さが1フレームに：(1)1歩進む、(2)2歩進む、(3)３歩遠くにジャンプしたり歩いたりする
            
            #キャラ(self)が左の壁と接触したばあい
            if self.pos_x > 600-75:  #(800//2+200-75:画面サイズ//2+200-75)
                self.pos_x = 600-75
            
            ####################    
                
            
        elif Game.on_leftkey():
            self.image_list = (pygame.image.load("image/player-l1hamu.png"),
                               pygame.image.load("image/player-l2hamu.png"),
                               pygame.image.load("image/player-l3hamu.png"))
            
            self.pos_x -= 3
            self.forward_len -= 3   #was 1
            #キャラ(self)が右の壁と接触したばあい
            if self.pos_x < 75:
                self.pos_x = 75
            
        # ジャンプ中でなく、スペースキーが押されたら、
        # ジャンプを開始する
        if Game.on_spacekey() and not self.in_air:
            self.is_jump = True
            self.in_air = True
            self.jump_len = 0
        
        # ジャンプ中の場合
        if self.is_jump:
            # ジャンプの長さが80までは上昇する
            if self.jump_len < 80:  #was 80
                #self.pos_y -= 4
                # 上昇できなかった場合
                if not self.up_move(6):     #was (4)
                    # ジャンプの長さを80にする（打ち切る）
                    self.jump_len = 15
            # ジャンプの長さが110まではそのまま
            elif self.jump_len < 20:
                pass
            # # ジャンプの長さが190までは下降する
            # elif self.jump_len < 190:
            #     self.pos_y += 4
            
            # それらが終わったらジャンプ終了
            else:
                self.is_jump = False
            # ジャンプの長さを１増やす
            self.jump_len += 5
        else:   # ジャンプ中でない場合
            # 下に移動、移動できたら空中扱い
            if self.down_move(6):     #was (4)
                self.in_air = True
            else:
                self.in_air = False            

        # キャラクターの画像設定
        self.set_chara_animation()
    
    # 画面に描画
    def draw(self):
        super().draw((self.pos_x, self.pos_y))
    
    # 敵との当たり判定
    def hit_check(self):
        # 当たり判定を行わないカウンタの場合、残りカウントに応じてTrue/Falseを返却
        if self.next_hit_count > Game.count:
            return 4 if self.next_hit_count - Game.count > 150 else 3
            # return True if self.next_hit_count - Game.count > 150 else False
        is_hit = False
        is_item = False
        # プレイヤー画像の四角を取得
        player_rect = self.get_rect()
        
        # 敵の数だけ繰り返し
        for enemy in Game.enemy_list:
            enemy_rect = enemy.get_rect()
            if player_rect.colliderect(enemy_rect):
                is_hit = True

                if enemy.enemy_type < 3:
                    self.life -= 1
                    is_item = False
                else:
                    self.life += 1
                    is_item = True
                    if self.life > 3:
                        self.life = 3
            
        if is_hit:
            self.next_hit_count = Game.count + 200
        
        if is_hit and is_item:
            return 1
        elif is_hit and not is_item:
            return 2
        else:
            return 3
    
    # ゴールとの当たり判定
    def goal_check(self):
        # すでにゴール済みの場合は判定をしない
        if 0 < self.goal_count:
            return
        # プレイヤー画像の四角を取得
        player_rect = self.get_rect()
        # ゴール（右）の四角を取得
        goal_rect = Game.goal_list[1].get_rect()
        # ゴール（右）と触れたら、一定時間後にゲームクリアとする
        if player_rect.colliderect(goal_rect):
            self.goal_count = Game.count + 80
            
    # ラグーンとの当たり判定
    def lagoon_check(self):
        # すでにゴール済みの場合は判定をしない
        if 0 < self.lagoon_count:
            return
        # プレイヤー画像の四角を取得
        player_rect = self.get_rect()
        # ラグーン（右）の四角を取得
        lagoon_rect = Game.lagoon_list[0].get_rect()
        # ラグーン（右）と触れたら、一定時間後にゲームクリアとする
        if player_rect.colliderect(lagoon_rect):
           self.lagoon_count = Game.count + 10           
     
    # ブロックとの当たり判定
    def block_check(self):
        # ヒットチェック結果
        # -1:ヒットなし、数値：ヒットあり（大きい方のブロック種別を返却）
        hit_result = -1
        # プレイヤー画像の四角を取得
        player_rectforblock = self.get_rectforblock()
        for block in Game.block_list:
            # ブロックの四角を取得
            block_rect = block.get_rectforblock()
            # ブロックと触れたら、今までの結果の中で一番大きなブロック種別を設定
            if player_rectforblock.colliderect(block_rect):
                hit_result = max(hit_result, int(block.block_type))
 

        # ヒットしたブロック種別を返却
        return hit_result     
                
    # Charactorクラスのget_rectをオーバーライド
    def get_rect(self):
        rect = super().get_rect()
        # 当たり判定をやや小さくする
        rect.x += rect.width * 0.1
        rect.y += rect.height * 0.1
        rect.width *= 0.8
        rect.height *= 0.8
        return rect
    
    # Charactorクラスのget_rectforblockを「浮くblockだけ」再度オーバーライド
    def get_rectforblock(self):
        rectforblock = super().get_rectforblock()
        # 当たり判定をやや小さくする
        rectforblock.x += rectforblock.width * 0.1 + 2
        rectforblock.y += rectforblock.height * 0.1 + 65
        rectforblock.width *= 0.6
        rectforblock.height *= 0.01
        return rectforblock
            
    # 当たり領域表示
    def draw_hit_area(self):
        if Game.debug_mode:
            # ラグーン画像の四角を取得
            lagoon_rect = self.get_rect()
            pygame.draw.rect(Game.surface, (255,0,125), lagoon_rect, 5)
            
            # プレイヤー画像の四角を取得（ブロック以外の当たり）
            player_rect = self.get_rect()
            pygame.draw.rect(Game.surface, (255,0,125), player_rect, 5)
            
            # プレイヤー画像の四角を取得(ブロックのみ反応)
            player_rectforblock = self.get_rectforblock()
            pygame.draw.rect(Game.surface, (255,255,255), player_rectforblock, 5)
            
            # 敵の数だけ繰り返し
            for enemy in Game.enemy_list:
                enemy_rect = enemy.get_rect()
                pygame.draw.rect(Game.surface, (255,0,0), enemy_rect, 5)
                
            # ブロックの数だけ繰り返し
            for block in Game.block_list:
                block_rect = block.get_rect()
                pygame.draw.rect(Game.surface, (0,0,255), block_rect, 5)

  