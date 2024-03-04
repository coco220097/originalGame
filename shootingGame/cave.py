from ast import Delete
from itertools import starmap 
import sys
from xml.dom.pulldom import START_DOCUMENT
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE
from hole import Hole
import datetime


# ウインドウサイズ
W_WIDTH = 800
W_HEIGHT = 600
Hole.W_HEIGHT = W_HEIGHT

#ゲーム開始時の時機の位置
START_SHIP_X = 0
START_SHIP_Y = 250
#時機の上下方向の加速度
V_ACCELERATION = 1
#壁の横幅→クラスへ移動
#WALL_WIDTH = 10

pygame.init()   # pygameの初期化処理

# pygame の繰り返し処理の指定
# set_repeat（delay、interval）
# delay:最初の繰り返しの前のミリ秒数
# interval:その後、繰り返されるミリ秒数
pygame.key.set_repeat(5, 5)
surface = pygame.display.set_mode((W_WIDTH, W_HEIGHT))  # 画面表示
clock = pygame.time.Clock()                             # clock

#時機の位置
ship_pos = [START_SHIP_X, START_SHIP_Y]


#星の描画
star = pygame.image.load("image/bgimage.png")
star2 = pygame.image.load("image/bgimage.png")

# 爆発画像の読込
clash_image=[
    pygame.image.load("image/clash1.png"),
    pygame.image.load("image/clash2.png"),
    pygame.image.load("image/clash3.png"),
    pygame.image.load("image/clash4.png")]




#黒板スクロール
BGcolor = (00, 102, 153)

def draw_bg(x, scroll):
    width=800
    # surface.fill(BGcolor)
    for x in range(10): 
        surface.blit(star,((x * width) - scroll * 0.8, 0))
        surface.blit(star2,((x * width) - scroll * 0.4, 0)) 
        
running = True       
        
        
     
############################################
# #ゲームオーバーの場合、一枚爆発画像を上から描画する
# if is_gameover:
#     surface.blit(clash_image, (ship_pos[0]-15, ship_pos[1]-30))
############################################## 

#ゲームオーバーの場合、爆発画「clash_image0-3」をおきかえながら描画する
a = 0

def animation(surface):
 
    global a
    
    if a < 8:
        print(a%4)
        surface.blit(clash_image[a%4], (ship_pos[0]-15, ship_pos[1]-30))
        a += 1
        
    # if a == 4:
    #     # sys.quit()
    #     a = 0
           

        
       
            

# メイン処理
def main():
    scroll = 0
    scroll_speed = 10
    
    v_speed = 0     #時機の上下方向の速度
    is_gameover = False#ゲームオーバーフラグ
    score = 0   #スコア
    # "Arial"　→　"Helvetica"
    game_font = pygame.font.SysFont("Helvetica", 32)



    # #星の画像の読み込み
    # img_bg = pygame.image.load("image/bgimage.png")

    # 自機画像の読込
    ship_image = pygame.image.load("image/ship.png")
 
   
    
    
    #壁の穴のリスト
    holes = []
    #壁（穴）の数は、画面の横幅÷壁の横幅
    for x in range(W_WIDTH // Hole.WALL_WIDTH):
        #壁の穴を作成する
        holes.append(Hole(x * Hole.WALL_WIDTH))

    

    # ゲームのループ処理
    while True:
        is_space_down =False    #スペースキーが押されているかのフラグ

        # イベント処理
        for event in pygame.event.get():
            # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #スペースキー押下でフラグをTrueにする
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True
                    
        #プレイ中のみ、以下の処理をする
        if not is_gameover:
            
            
            #上下方向の時機の速度を計算する         
            if is_space_down:
                v_speed -= V_ACCELERATION
            else:
                v_speed += V_ACCELERATION
            #時機の位置を設定する  
            ship_pos[1] += v_speed 
            #位置は、一番右の穴の位置にする
            right_rect = holes[-1].rect
            new_hole = Hole(right_rect.x + Hole.WALL_WIDTH)
            #穴の位置とサイズを、一番右と同じにする
            new_hole.set_hole(right_rect.top, right_rect.height)
            #新しい穴を角度分ずらします
            new_hole.move_angle()
            #先頭の穴を削除して、新しい穴を追加する
            del holes[0]
            holes.append(new_hole)
            #すべての穴を１つ分左に移動
            for hole in holes:
                hole.move_left()
   
   
    

            #壁にぶつかったか判定する
            #「穴の上端より時機が上に行った場合」または
            #「穴の下端より時機が下にいった場合」にぶつかったとする
            if holes[0].rect.top > ship_pos[1] or holes[0].rect.bottom < ship_pos[1] + 60:
                is_gameover = True
                

            #壁の描画
        surface.fill((75, 44, 18))   
        
        #壁の穴の描画
        for hole in holes:
            pygame.draw.rect(surface, (0, 0, 0), hole.rect)

        draw_bg(x, scroll)
        scroll += scroll_speed
        
        if a <= 7:
            # 時機の位置に、自機を描画
            surface.blit(ship_image, ship_pos)
        
        
        if is_gameover:
            #surface.blit(clash_image[a], (ship_pos[0]-15, ship_pos[1]-30))
            
            ##ゲームオーバーになった時のアニメーションを実行
            animation(surface)
            # sys.exit()
        else:
        #ゲームオーバーでないとき、スコアを加算する
            score += 1



        
        #レベルとスコアを表示
        level_info = game_font.render(f"Level:{Hole.level:3}", True, (255, 0, 255))
        score_info = game_font.render(f"Score:{score:6}", True, (255, 0, 0))
        surface.blit(level_info, (480, 20))
        surface.blit(score_info, (620, 20))


        #アルファ設定（不透明度設定）
        s = pygame.Surface((280,40))  # the size of your rect
        s.set_alpha(150)                # alpha level
        s.fill((255,255,255))           # this fills the entire surface
        surface.blit(s, (480,60))    # (0,0) are the top-left coordinates
        nowdate = game_font.render(str(datetime.date.today()), True, (100, 0, 100))
        nowtime = game_font.render(datetime.datetime.now().strftime("%H:%M:%S"), True, (0, 0, 100))

        surface.blit(nowdate, [495, 60])    # 文字列の位置を指定
        surface.blit(nowtime, [635, 60])    # 文字列の位置を指定
        
        # ##時間を表示############
        # while True:
        #     #surface.fill((0, 255, 0))   # 背景（壁）を緑色で塗りつぶす
        #     s = pygame.Surface((270,40))  # the size of your rect
        #     s.set_alpha(50)                # alpha level
        #     s.fill((0,255,0))           # this fills the entire surface
        #     surface.blit(s, (480,60))    # (0,0) are the top-left coordinates
            
        #     nowdate = game_font.render(str(datetime.date.today()), True, (100, 0, 100))
        #     nowtime = game_font.render(datetime.datetime.now().strftime("%H:%M:%S"), True, (0, 0, 100))

        #     surface.blit(nowdate, [480, 60])    # 文字列の位置を指定
        #     surface.blit(nowtime, [620, 60])    # 文字列の位置を指定
        #     pygame.display.update()            # 画面更新
        #     # イベントを処理
        #     for event in pygame.event.get():
        #         if event.type == QUIT:  # 閉じるボタンが押されたら終了
        #             pygame.quit()       # Pygameの終了（画面を閉じる）
        #             sys.exit()          # プログラムの終了
            
        # ################              
           
       
        # 画面の更新
        pygame.display.update()
        # クロック（時間間隔）の設定
        clock.tick(15)

    
    
if __name__ == '__main__':
    main()

