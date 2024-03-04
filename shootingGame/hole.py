import pygame
from pygame.locals import Rect
from random import randint

class Hole:
    #画面の
    W_HEIGHT = 0
    #壁の横幅（クラス変数へ移動）
    WALL_WIDTH = 10
    
    #壁の角度の最大値
    ANGLE_MAX = 6
    #1段階ごとに穴が狭くなるサイズ
    NARROW_SIZE = 10
    #最小の穴のサイズ
    MIN_HOLE_SIZE = 100
    
    
    #穴のずれる角度
    hole_angle = 1
    #レベル
    level = 1
    
    #コンストラクタ
    def __init__(self, x):
        self.rect = Rect(x, 20, Hole.WALL_WIDTH, 560)
    
    #穴の設定
    def set_hole(self, top, height):
        self.rect.top = top
        self.rect.height = height
        
    #穴のサイズを算出する
    def calc_hole_size(self):
        self.hole_size = self.rect.height
        self.hole_size -= Hole.NARROW_SIZE
        #穴のサイズが最小値を下回ったら、最小限にする
        if self.hole_size < Hole.MIN_HOLE_SIZE:
            self.hole_size = Hole.MIN_HOLE_SIZE

    #角度分移動する
    def move_angle(self):
        #穴をコピーして、一度動かしてみる
        check_rect = self.rect.copy()
        check_rect.move_ip(0, Hole.hole_angle)
        #移動後の位置が、上の端に達していたら新しい角度（下向き）を設定する
        if check_rect.top <= 0:
            Hole.hole_angle = randint(1, Hole.ANGLE_MAX)
            #穴のサイズを算出
            self.calc_hole_size()
            #穴のサイズを計算後の値にする
            self.rect.height = self.hole_size
            #レベルを１増やす
            Hole.level += 1
            
        #移動後の位置が、下の端に達していたら新しい角度（上向き）を設定する
        elif check_rect.bottom >= Hole.W_HEIGHT:
            Hole.hole_angle = randint(1, Hole.ANGLE_MAX) * -1
            
            #穴のサイズを算出
            self.calc_hole_size()
            #穴のサイズを計算後の値にして、穴の上端をずらす
            self.rect.height = self.hole_size
            self.rect.top -= Hole.hole_angle

        #穴を角度だけ移動する
        self.rect.move_ip(0, Hole.hole_angle)

    #左に移動する
    def move_left(self):
        self.rect.move_ip(-1 * Hole.WALL_WIDTH, 0)

        
        
        
        