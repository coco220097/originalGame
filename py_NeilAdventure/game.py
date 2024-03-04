import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP
from pygame.locals import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_SPACE, K_RETURN
from enum import Enum

# ゲームの基本情報クラス
class Game:
    
    # ========== クラス変数 ==========
    surface = None          # 表示するウィンドウ
    count = 0               # ゲームカウンタ
    phase = None            # 処理段階
    debug_mode = False      # デバッグモード
    keymap = []             # キー押下情報
    player = None           # プレイヤー
    enemy_list = []         # 敵リスト
    goal_list = []          # ゴールリスト（左・右）
    lagoon_list = []          # ラグーン
    block_list = []         # ブロックリスト
    ike_list = []         # 池リスト
    
    # クラスメソッド：イベントチェック処理
    @classmethod
    def check_event(cls):
        # イベント処理ループ
        for event in pygame.event.get():
            # 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # キーダウン処理
            elif event.type == KEYDOWN:
                if not event.key in Game.keymap:
                    Game.keymap.append(event.key)
            # キーアップ処理
            elif event.type == KEYUP:
                Game.keymap.remove(event.key)

    # クラスメソッド：キーチェック処理
    @classmethod
    def on_upkey(cls):
        return K_UP in Game.keymap
    @classmethod
    def on_downkey(cls):
        return K_DOWN in Game.keymap
    @classmethod
    def on_leftkey(cls):
        return K_LEFT in Game.keymap
    @classmethod
    def on_rightkey(cls):
        return K_RIGHT in Game.keymap
    @classmethod
    def on_spacekey(cls):
        return K_SPACE in Game.keymap
    @classmethod
    def on_enterkey(cls):
        return K_RETURN in Game.keymap

# 処理段階（列挙型クラス）
class Phase(Enum):
    TITLE = 1           # タイトル画面
    GAME_START = 2      # ゲーム開始
    
    MAIN_GAME = 11      # ゲーム中
    
    GAME_CLEAR = 21     # ゲームクリア
    
    GAME_OVER = 99      # ゲームオーバー
