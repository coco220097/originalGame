import pygame
from pygame import Rect
from game import Game, Phase
from player import Player
from enemy import Enemy
import sys
import random
from goal import Goal
from lagoon import Lagoon
from block import Block

# 固定値を設定
pos_x = 800 
pos_y = 600  
MOISTURE_MAX = 300
moisture = MOISTURE_MAX 

# Pythonの基本処理
pygame.init()
Game.surface = pygame.display.set_mode([800, 600])
clock = pygame.time.Clock()
pygame.display.set_caption("******")

# 描画用フォント（等幅フォントを使用しているので、使えなかったら変えてください）
smallestfont = pygame.font.SysFont("self", 28)   # 最小さい文字用のフォント
smallfont = pygame.font.SysFont("self", 48)   # 小さい文字用のフォント
middlefont = pygame.font.SysFont("self", 60)   # 中くらい文字用のフォント
largefont = pygame.font.SysFont("None", 80)   # 大きい文字用のフォント
largefont_b = pygame.font.SysFont("None", 80, bold=True)   # 大きい文字用のフォント


# 背景読み込み
bg = None
# 難易度ごとの背景リストを作成
bg1 = (pygame.image.load("image/bg1.png"),pygame.image.load("image/bg1.png"))
bg2 = (pygame.image.load("image/bg2.png"),pygame.image.load("image/bg2.png"))
bg3 = (pygame.image.load("image/bg3.png"),pygame.image.load("image/bg3.png"))
bg_list = (bg1, bg2, bg3)

# 沼の読み込み
lagoon = None
# 難易度ごとの沼リストを作成
lagoon00 = pygame.image.load("image/lagoon00.png")
lagoon01 = pygame.image.load("image/lagoon01.png")
lagoon02 = pygame.image.load("image/lagoon02.png")
lagoon_list = (lagoon00, lagoon01, lagoon02)

# 画像読み込み
ui_image1 = pygame.image.load("image/bg1_alha1.png")    # alpha1板画像
ui_image2 = pygame.image.load("image/bg1_alha2.png")    # alpha2板画像
hit_image = pygame.image.load("image/bang.png") # ヒット画像
img_item2 = pygame.image.load('image/item2.png')  #降ってくるアイテム
img_item1 = pygame.image.load('image/item1.png')  #降ってくるアイテム
mes_rightmark = pygame.image.load('image/bg1_alha3_yajirushi.png')  #ui画像
mes_spacemark = pygame.image.load('image/bg1_alha3_jamp.png')  #ui画像

bg
# ゲームオーバー表示
overtex = pygame.image.load("image/over.png")   
rect_overtex = overtex.get_rect()
rect_overtex.center = (400, 300) # clear画像の初期位置

#ゲームクリア画像読み込み
cleartex = pygame.image.load("image/clear.png")   
rect_cleartex = cleartex.get_rect()
rect_cleartex.center = (400, 300) # clear画像の初期位置

# ライフ画像
life_image = pygame.image.load("image/heartred2.png")
life_image = pygame.transform.scale(life_image, (50, 50))   # 拡大縮小


# サウンドの読み込み
bgm_title = pygame.mixer.Sound('sound/s_title.mp3')
soundeffect_gameover = pygame.mixer.Sound('sound/fightfight_01.mp3')
# soundeffect_gameover = pygame.mixer.Sound('sound/s_game-over.mp3')
bgm_clear = pygame.mixer.Sound('sound/s_clear.mp3')
voi_clear2 = pygame.mixer.Sound('sound/kid_mama.wav')
bgm_ingame = pygame.mixer.Sound('sound/s_ingame.mp3')
soundeffect_enemy = pygame.mixer.Sound('sound/s_enemy1.mp3')
soundeffect_getitem = pygame.mixer.Sound('sound/s_getitem.mp3')

sound_num = 2

get_image_no = 0
hit_image_no = 0

#すべてのキャラクターをひとまとめにした画像を読みこむ
heart_image = pygame.image.load("image/hartani01.png")
star_image = pygame.image.load("image/kurukuru01.png")
    #画像表示用の小さな描画領域を作成する
    #pygame.SRCALPHAを指定すると、背景を透過できる
get_images = (pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA),
                pygame.Surface((24, 24), pygame.SRCALPHA))
for i in range(9):
    get_images[i].blit(heart_image, (0, 0), Rect(24 * i, 0, 24, 24))
    
#画像表示用の小さな描画領域を作成する
#pygame.SRCALPHAを指定すると、背景を透過できる
hit_images = (pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA),
                pygame.Surface((48, 48), pygame.SRCALPHA))
for j in range(9):
    hit_images[j].blit(star_image, (0, 0), Rect(48 * j, 0, 48, 48))
    

# ゲーム情報初期化処理
def init_game_info():
    # コマンドライン引数の１つめが"1"の場合デバッグモード
    if len(sys.argv) > 1 and sys.argv[1] == "1":
        Game.debug_mode = True
    Game.phase = Phase.TITLE
    Game.player = Player()
    Game.enemy_list = []

# 基本描画処理
def basic_draw(is_hit, is_item, is_tutorial01, is_tutorial02):
    global get_image_no
    global hit_image_no
    Game.surface.fill((0, 0, 0))    # 画面を黒で塗りつぶす
    # 背景の描画（キャラクターが進んだ距離に合わせる）
    # 繋がった画像を２つ用意し、ＡＢＡという形で描画することで
    # つなぎ目が無く背景がスクロールできる
    x = Game.player.forward_len % 1600
    Game.surface.blit(bg[0], (-x, 0))
    Game.surface.blit(bg[1], (800-x, 0))
    Game.surface.blit(bg[0], (1600-x, 0))
    
    # lagoon00の描画
    Game.lagoon_list[0].draw()
    
    # ブロックの描画 
    for block in Game.block_list:
        block.draw()

    # 敵の描画    
    for enemy in Game.enemy_list:
        enemy.draw()
    # ※左→プレイヤー→右と描画することで、プレイヤーがゴールを通るようにする
    # ゴール（左）の描画
    Game.goal_list[0].draw()
    # プレイヤーの描画
    Game.player.draw()
    # ゴール（右）の描画
    Game.goal_list[1].draw()
    
    # ヒットマークの描画
    if is_hit:
        #ほしの描画 
        if not is_item:
            Game.surface.blit(hit_images[hit_image_no //4], (Game.player.pos_x + 30, Game.player.pos_y - 30))  #was //2
            hit_image_no = (hit_image_no + 1) % 36  #was 18
            
        else:
            #ハートの描画  
            Game.surface.blit(get_images[get_image_no // 1], (Game.player.pos_x + 30, Game.player.pos_y - 30))  #was //12
            get_image_no = (get_image_no + 1) % 9  #was 108
            
    # # ヒットマークの描画(60フレームの時)
    # if is_hit:
    #     #ほしの描画 
    #     if not is_item:
    #         Game.surface.blit(hit_images[hit_image_no //12], (Game.player.pos_x + 30, Game.player.pos_y - 30))  #was //4
    #         hit_image_no = (hit_image_no + 1) % 108  #was 36
            
    #     else:
    #         #ハートの描画  
    #         Game.surface.blit(get_images[get_image_no // 2], (Game.player.pos_x + 30, Game.player.pos_y - 30))
    #         get_image_no = (get_image_no + 1) % 18
        
    # ライフの描画
    for i in range(Game.player.max_life):
        if Game.player.life > i:
            Game.surface.blit(life_image, (730 - 60*i, 20))
    
    #uiデザイン画像や文字の表示
    Game.surface.blit(ui_image1, (0, 0)) #UIデザイン画像を表示する
    # write_msg("GO RIGHT", smallfont, (255, 255, 255),x=400,y=580)   # 白色の文字の表示
    
    # #uiデザイン画像や文字の表示
    if is_tutorial01:
        Game.surface.blit(mes_rightmark, (0, 0)) #UI「→にすすもう」画像を表示する
    if is_tutorial02:
        Game.surface.blit(mes_spacemark, (0, 0)) #UI「→にすすもう」画像を表示する    
    
            
    #時間制限バーの情報と表示        
    Game.surface.fill((220, 220, 0), (50, 30, moisture, 20))    #（黄；動く）
    if moisture <= 100:        
            # if Game.count % 100 >= 50:
            if Game.count % 10 >= 5:
                Game.surface.fill((255, 0, 0), (50, 30, moisture, 20))  #赤
            else:
                Game.surface.fill((255, 128, 128), (50, 30, moisture, 20))  # 黄
    
    #ui画像(時計マルの部分)
    Game.surface.blit(ui_image2, (0, 0)) #UIデザイン画像を表示する

# 文章を表示する関数
def write_msg(msg, font, color, x = 400, y = 300):
    # フォントからrenderを作成
    title_render = font.render(msg, True, color)
    # 画面の中心（または引数の値）を設定
    msg_rect = title_render.get_rect()
    msg_rect.center = (x, y)
    # 画面に描画
    Game.surface.blit(title_render, msg_rect.topleft)
    
# 敵情報設定処理
def set_enemy(selected_difficult):
    # 選択された難易度に対応する、敵データファイルを設定
    if selected_difficult == 1:
        enemy_file_path = "data/enemy_data1.txt"
    elif selected_difficult == 2:
        enemy_file_path = "data/enemy_data2.txt"
    else:
        enemy_file_path = "data/enemy_data0.txt"
    
    # 敵データファイルから読み込み
    with open(enemy_file_path, "r", encoding="utf-8") as enemy_file:
        # ファイル内の行だけ繰り返す
        for data in enemy_file:
            # 各行のデータをカンマで区切る（種類、横位置、縦位置）
            kind, x_in_map, y = data.split(",")
            
            enemy = None    # 一旦、敵データを空にする
            if kind == "0":     # スライムの場合
                image = pygame.image.load("image/slime1.png")
                image2 = pygame.image.load("image/slime2.png")
                # image = pygame.transform.flip(image, True, False)   # 左右反転
                # image = pygame.transform.scale(image, (120, 110))   # 拡大縮小
                image_list = (image, image2)
                enemy = Enemy(0, image_list, 100)
                #↓これ敵によって動きを変える為、noteに書いた
                # Game.enemy_list.append(Enemy(0, image_list, 100))
                # Game.enemy_list[1].pos_x_in_map = 1000
                # Game.enemy_list[1].pos_y = 470
                
            elif kind == "1":   # ボールモンスタの場合
                image = pygame.image.load("image/ballmon.png")
                image2 = pygame.transform.rotate(image, 90)     # 回転
                image3 = pygame.transform.rotate(image, 180)    # 回転
                image4 = pygame.transform.rotate(image, 270)    # 回転
                image_list = (image, image2, image3, image4)
                enemy = Enemy(1, image_list, 100)
                #↓これ敵によって動きを変える為、noteに書いた
                # Game.enemy_list.append(Enemy(1, image_list, 25))
                # Game.enemy_list[2].pos_x_in_map = 2000
                # Game.enemy_list[2].pos_y = 470  # was 350
                
            elif kind == "2":   # フライングモンスタの場合
                image = pygame.image.load("image/flyingmon.png")
                # image = pygame.transform.scale(image, (250, 120))   # 拡大縮小
                image_list = (image,)
                enemy = Enemy(2, image_list, 100)
                #↓これnoteに書いた
                # Game.enemy_list.append(Enemy(2, image_list, 100))
                # Game.enemy_list[0].pos_x_in_map = 3000
                # Game.enemy_list[0].pos_y = 100
                
            elif kind == "3":   # きのこの場合
                image = pygame.image.load("image/masu1.png")
                image2 = pygame.image.load("image/masu2.png")
                image_list = (image, image2)
                image_list = (image,)
                enemy = Enemy(3, image_list, 100)                

            # 敵データが有った場合
            if enemy != None:
                # 敵の位置を設定して、リストに追加
                enemy.pos_x_in_map = int(x_in_map)
                enemy.pos_y = int(y)
                Game.enemy_list.append(enemy)


    image = pygame.image.load("image/star1.png")
    image2 = pygame.image.load("image/star2.png")
    image_list = (image, image2)
    Game.enemy_list.append(Enemy(3, image_list, 25))
    Game.enemy_list[3].pos_x = random.randint(100, 500)
    Game.enemy_list[3].pos_y_in_map = random.randint(-1000, -100)
    
    image = pygame.image.load("image/item1.png")
    image_list = (image,)
    Game.enemy_list.append(Enemy(4, image_list, 25))
    Game.enemy_list[4].pos_x = random.randint(100, 500)
    Game.enemy_list[4].pos_y_in_map = random.randint(-800, -100)
    
    image = pygame.image.load("image/item2.png")
    image_list = (image,)
    Game.enemy_list.append(Enemy(5, image_list, 25))
    Game.enemy_list[5].pos_x = random.randint(100, 500)
    Game.enemy_list[5].pos_y_in_map = random.randint(-1300, -100)   


# ブロック情報設定処理
def set_block(selected_difficult):
    # 選択された難易度に対応する、敵データファイルを設定
    if selected_difficult == 1:
        block_file_path = "data/block_data1.txt"
    elif selected_difficult == 2:
        block_file_path = "data/block_data2.txt"
    else:
        block_file_path = "data/block_data0.txt"
    
    # ブロックデータファイルから読み込み
    with open(block_file_path, "r", encoding="utf-8") as block_file:
        # ファイル内の行だけ繰り返す
        for data in block_file:
            # 各行のデータをカンマで区切る（種類、横位置、縦位置、幅、高さ）
            kind, x_in_map, y, width, height = data.split(",")
            width, height = int(width), int(height)
            block = None    # 一旦、ブロックデータを空にする
            if kind == "0":     # パンの場合
                image = pygame.image.load("image/rock_inair2.png")
            elif kind == "1":   # 長丸岩
                image = pygame.image.load("image/rock_block.png")
            elif kind == "2":   # 四角ブロック
                image = pygame.image.load("image/sign_start.png")
            elif kind == "3":   # スタート看板
                image = pygame.image.load("image/sign_start2.png")
            elif kind == "4":   # スタート看板
                image = pygame.image.load("image/sign_start3.png")
            elif kind == "5":   # ゴールの家
                image = pygame.image.load("image/house2.png")
            else:
                # 他の種別の場合は処理をしない
                continue
            # ブロック画像の拡大縮小
            image = pygame.transform.scale(image, (width, height)) 
            image_list = (image,)
            # ブロックのインスタンスを作成
            block = Block(kind, image_list)

            # ブロックの位置を設定して、リストに追加
            block.pos_x_in_map = int(x_in_map)
            block.pos_y = int(y)
            Game.block_list.append(block)   
            
# ゴール情報設定処理
def set_goal(selected_difficult):
    # 現状は、どの難易度でもゴール位置は同じ
    image = pygame.image.load("image/mushgate.png")
    #ゴールは、左右２つの画像を作成する
    image_list = (image,)
    goal_l = Goal(image_list)
    goal_l.pos_x_in_map = 4000
    goal_l.pos_y = 455
    Game.goal_list.append(goal_l)
    goal_r = Goal(image_list)
    goal_r.pos_x_in_map = 4050
    goal_r.pos_y = 495
    Game.goal_list.append(goal_r)     
    
#ラグーンに当たった時の情報設定処理
def set_lagoon(selected_difficult):
    image = pygame.image.load("image/lagoon00.png")
    
    image_list = (image,)
    lagoon_r = Lagoon(image_list)
    lagoon_r.pos_x_in_map = 1600    #ラグーンのx位置決め
    lagoon_r.pos_y = 490
    Game.lagoon_list.append(lagoon_r)

            
# メイン処理
def main():
    global bg                   # 難易度に対応した背景（リスト）
    global moisture
    global sound_num
    selected_difficult = 0      # 選択中の難易度
    key_release = False         # キー離しフラグ
    start_count = 0             # ゲーム開始までのカウンター
    is_hit = False
    is_item = False
    is_tutorial01 = True    #チュートリアル01画像の表示
    is_tutorial02 = False    #チュートリアル02画像の表示

    # ゲーム情報の初期化処理を実行
    init_game_info()

    # ウィンドウを作成
    pygame.init()
    
    # ゲームのメインループ
    while True:
        # ゲームのカウンタを１加算
        Game.count += 1
        # イベントチェック処理（終了、キー入力）を実行
        Game.check_event()

        if sound_num == 2:
            pygame.mixer.stop()
            sound_num = 1
        # ===== ゲームフェーズによる処理段階分け =====
        # タイトル画面の場合
        if Game.phase == Phase.TITLE:
            #タイトルBGMを流す
            if sound_num == 1:
                bgm_title.play(-1)
                sound_num = 0
            # ゲームタイトル、難易度、メッセージを表示
            bg = pygame.image.load("image/title.png")   
            rect_bg = bg.get_rect()
        
            player = pygame.image.load("image/player-l1hamu.png")   
            rect_player = player.get_rect()
            
            rect_bg.center = (400, 300) # bg画像の初期位置
            rect_player.center = (460, 210) # プレイヤー画像の初期位置
            Game.surface.blit(bg, rect_bg)            # 背景画像の描画
            Game.surface.blit(player, rect_player)


            # write_msg("PRESS space TO PLAY", smallfont, (255, 255, 255), y=550)
            if Game.count % 100 >= 50:
                write_msg("PRESS SPACE TO PLAY", smallfont, (220, 220, 220), y=550)   # やや暗め色の文字
            else:
                write_msg("PRESS SPACE TO PLAY", smallfont, (255,255,255), y=550)   # やや明るい色の文字
            

            color = (127, 68, 40) if selected_difficult != 0 else (162, 197, 35)
            write_msg("EASY", middlefont, color, y=345)
            color = (127, 68, 40) if selected_difficult != 1 else (162, 197, 35)
            write_msg("NORMAL", middlefont, color, y=405)
            color = (127, 68, 40) if selected_difficult != 2 else (162, 197, 35)
            write_msg("HARD", middlefont, color, y=465)
            
            # スペースキーの場合
            if Game.on_spacekey():
                # ゲームを開始（20カウント後）
                Game.phase = Phase.GAME_START
                sound_num = 2
                start_count = Game.count + 20
                # 選択された難易度に応じて背景を設定
                bg = bg_list[selected_difficult]
                # 選択された難易度に応じて敵を設定
                set_enemy(selected_difficult)
                # 選択された難易度に応じてラグーンを設定
                set_lagoon(selected_difficult)
                # 選択された難易度に応じてゴールを設定
                set_goal(selected_difficult)
                # 選択された難易度に応じてブロックを設定
                set_block(selected_difficult)
                
                          
            # 上下キーの場合、選択難易度を変更
            elif Game.on_downkey() and key_release:
                selected_difficult += 1
                key_release = False
            elif Game.on_upkey() and key_release:
                selected_difficult -= 1
                key_release = False
            # 上下でループするように値を計算
            selected_difficult = selected_difficult % 3
            # 上下キーが離されない限り、選択難易度を移動しないようにする
            if not Game.on_downkey() and not Game.on_upkey():
                key_release = True

        # ゲーム開始時の場合（カウントが一定時間たったらゲーム開始）
        elif Game.phase == Phase.GAME_START:
            if start_count < Game.count:
                Game.phase = Phase.MAIN_GAME
                sound_num = 2
        # ゲーム中の場合
        elif Game.phase == Phase.MAIN_GAME:
            if sound_num == 1:
                bgm_ingame.play(-1)
                sound_num = 0

            # プレイヤーの毎回処理
            Game.player.frame_process_img()

            # 敵の数だけ敵の毎回処理を実施
            for enemy in Game.enemy_list:
                enemy.frame_process_img()
          
            # ゴールの数だけゴールの毎回処理を実施
            for goal in Game.goal_list:
                goal.frame_process_img()
            # ラグーンの数毎回処理を実施
            for lagoon in Game.lagoon_list:
                lagoon.frame_process_img()
            # ブロックの数だけブロックの毎回処理を実施
            for block in Game.block_list:
                block.frame_process_img()

            # プレイヤーと敵のヒットチェック
            hit_item = Game.player.hit_check()
            if hit_item == 1:
                is_hit = True
                is_item = True
            elif hit_item == 2:  
                is_hit = True
                is_item = False     
            elif hit_item == 3:  
                is_hit = False
                is_item = False 
            elif hit_item == 4:
                pass 
                     
            # ゴール判定
            Game.player.goal_check()
            
            # ラグーンと接触した時の判定
            Game.player.lagoon_check()
            
            # チュートリアル終了判定
            if Game.on_rightkey() and is_tutorial01:
                is_tutorial01 = False
                is_tutorial02 = True
            if Game.on_spacekey():
                is_tutorial02 = False 
            
            #時間制限の管理
            if selected_difficult == 0:
                moisture = moisture -0.05
            if selected_difficult == 1:
                moisture = moisture -0.1
            if selected_difficult == 2:
                moisture = moisture -0.2
           
            # 基本描画処理
            basic_draw(is_hit, is_item, is_tutorial01, is_tutorial02)
            # 当たり判定表示（デバッグモード用）
            Game.player.draw_hit_area()
            # 時間制限バーが０になったらゲームオーバーへ
            if moisture <= 0:
                Game.phase = Phase.GAME_OVER    # moistureが０になったらゲームオーバーへ
                sound_num = 2
            # ライフが０になったらゲームオーバーへ
            if Game.player.life <= 0:
                Game.phase = Phase.GAME_OVER
                sound_num = 2
            # ラグーン接触になったらゲームオーバーへ
            if 0 < Game.player.lagoon_count < Game.count:
                Game.phase = Phase.GAME_OVER
                sound_num = 2
            # ゴールカウントを超えたら、ステージクリアへ
            if 0 < Game.player.goal_count < Game.count:
                Game.phase = Phase.GAME_CLEAR
                sound_num = 2
                
        # ゲームクリアーの場合
        elif Game.phase == Phase.GAME_CLEAR:
            # 基本描画処理
            basic_draw(is_hit, is_item, is_tutorial01, is_tutorial02)
            # sound_num = 2
            #ゲームクリアBGMを流す
            if sound_num == 1:
                bgm_clear.play()
                voi_clear2.play()
                sound_num = 0
                
                
            
            # ステージクリアー表示
            Game.surface.blit(cleartex, rect_cleartex) 
 
        # ゲームオーバーの場合
        elif Game.phase == Phase.GAME_OVER:
            # 基本描画処理
            basic_draw(is_hit, is_item, is_tutorial01, is_tutorial02)

            #ゲームオーバーBGMを流す
            if sound_num == 1:
                soundeffect_gameover.play()
                sound_num = 0
            
            # ゲームオーバー表示
            overtex = pygame.image.load("image/over.png").convert_alpha()    
            rect_overtex = overtex.get_rect()
            rect_overtex.center = (400, 300) # clear画像の初期位置
            Game.surface.blit(overtex, rect_overtex)
            
            #Try Again タイトル画面へ
            write_msg("================", smallfont, (212, 247, 200), y=420)
            if Game.count % 100 >= 50:
                write_msg("PRESS ENTER TO TRY AGAIN!", smallestfont, (162, 197, 32), y=460)   # やや暗め色の文字
            else:
                write_msg("PRESS ENTER TO TRY AGAIN!", smallestfont, (212, 247, 200), y=460)   # やや明るい色の文字
            
            if Game.on_enterkey():
                # ゲーム情報の初期化処理を実行
                init_game_info()
                moisture = MOISTURE_MAX 
                Game.phase = Phase.TITLE
                
        #処理落ちしていないかをチェックしてみる。。。（結果：１フレーム45ぐらいで落ちてしまうので、一定処理時間は30がいい）    
        #print(clock.get_fps())

        pygame.display.update()     # 描画更新処理
        clock.tick(40)             # 一定時間処理

# メイン処理の呼び出し
if __name__ == '__main__':
    main()
