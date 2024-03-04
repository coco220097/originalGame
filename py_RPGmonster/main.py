from cmath import phase
import pygame
from game import Game, Phase
from field import Field
from player import Player
from monster import Monster
from monsterlist import MonsterList
from battle import Battle
from title import Title

# Pythonの基本処理
pygame.init()
Game.surface = pygame.display.set_mode([960, 640])
clock = pygame.time.Clock()
pygame.display.set_caption("*** Sample RPG ***")

# 描画用フォント（等幅フォントを使用しているので、使えなかったら変えてください）
smallfont = pygame.font.SysFont("self", 36)   # 小さい文字用のフォント
midlefont = pygame.font.SysFont("self", 60)   # 中サイズ文字用のフォント
largefont = pygame.font.SysFont(None, 120)   # 大きい文字用のフォント



# ゲーム情報初期化処理
def init_game_info():
    # 各クラス変数に初期値を設定する
    is_gameover = False     # ゲームオーバーフラグ
    monsters = None         # モンスター
    # 仮に、フィールド表示をスタート状態とする（最終的にはタイトル画面にする）
    Game.phase = Phase.TITLE
    # フィールドクラスのインスタンスを作成して、ゲームクラスの変数に設定
    Game.field = Field(Game.START_FIELD)
    # プレイヤークラスのインスタンスを作成して、ゲームクラスの変数に設定
    Game.player = Player()
    # モンスター（初期配置）
    Game.monsters = []
    Game.monsters.append(Monster((8, 1), MonsterList.MON_NO_DOG))
    Game.monsters.append(Monster((2, 8), MonsterList.MON_NO_BEE))
    Game.monsters.append(Monster((2, 1), MonsterList.MON_NO_IKAKU))
    #戦闘画面
    Game.battle = Battle()
    #タイトル画面
    Game.title = Title()

# 基本描画処理
def basic_draw():
    # フィールドの描画
    Game.field.draw()
    # モンスター達の描画
    for monster in Game.monsters:
        monster.draw()
    # プレイヤーの描画
    Game.player.draw()
    
    bg2 = pygame.image.load("image/databg.jpg").convert_alpha()    
    rect_bg2 = bg2.get_rect()   # 右bg2画像を設定
    rect_bg2.center = (800, 320) # bg2画像の初期位置
    Game.surface.blit(bg2, rect_bg2)            # 背景2画像の描画
    
    # レベルの描画
    level_str = str(Game.player.level).rjust(5)     # 左空白埋めで５桁
    level_render =smallfont.render(f"Level:{level_str}",
                                   True, (255, 255, 255))
    Game.surface.blit(level_render, (680, 60))
    
    # HPの描画
    hp_str = str(Game.player.hp).rjust(5)     # 左空白埋めで５桁
    hp_render =smallfont.render(f"hp:{hp_str}",
                                   True, (255, 255, 255))
    Game.surface.blit(hp_render, (680, 110))
    
    
# メイン処理
def main():
    global speed, idx, tmr, floor, fl_max, welcome
    # ゲーム情報の初期化処理を実行
    init_game_info()
    
            
    idx = 1
            
    #ゲームプレイ中        
    if idx == 1:
                    
        # ゲームのメインループ
        while True:
            # ゲームのカウンタを１加算
            Game.count += 1
            # イベントチェック処理（終了、キー入力）を実行
            Game.check_event()
            
            Game.surface.fill((0, 0, 0))  # 画面を黒で塗りつぶす
            
           
            
            
            # pl_images5 = (Game.read_image_for_square("image/herodie1.png"),
            
            #     Game.player.set_images(pl_images5) # 画像を設定
            #     Game.player.set_chara_animation()

            if Game.phase == Phase.TITLE:
                Title.main()
                # GAME STARTメッセージの描画
                go_str = midlefont.render("PRESS ENTER",
                                            True, (255, 255, 255))
                Game.surface.blit(go_str, (340, 450))
                go_str2 = midlefont.render("TO PLAY",
                                            True, (255, 255, 255))
                Game.surface.blit(go_str2, (400, 500))
            # ===== ゲームフェーズによる処理段階分け =====
            # フィールド上の場合
            elif Game.phase == Phase.IN_FIELD:
                
                # プレイヤーの毎回処理
                Game.player.frame_process_img()
                # モンスターの毎回処理
                for monster in Game.monsters:
                    monster.frame_process_img()
                # 基本描画処理
                basic_draw()
                
            #戦闘中の場合
            elif Game.phase == Phase.IN_BATTLE:
                #戦闘中の毎回処理
                Game.battle.frame_process_btl()
                #基本描画処理
                basic_draw()
                #戦闘画面描画処理
                Game.battle.draw()
                
            # ゲームオーバーの場合
            elif Game.phase == Phase.GAME_OVER:
                pl_images5 = (Game.read_image_for_square("image/herodie1.png"),
                Game.read_image_for_square("image/herodie2.png")) 
                Game.player.set_images(pl_images5) # 画像を設定
                Game.player.set_chara_animation()
                # 基本描画処理
                basic_draw()
                # ゲームオーバーメッセージの描画
                go_str = largefont.render("GAME OVER...",
                                        True, (255, 0, 0))
                Game.surface.blit(go_str, (40, 300))

            pygame.display.update()     # 描画更新処理
            clock.tick(25)              # 一定時間処理

# メイン処理の呼び出し
if __name__ == '__main__':
    main()
