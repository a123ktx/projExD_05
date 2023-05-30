import pygame as pg
import sys
import random
import time

WIDTH = 800  # ディスプレイの横幅
HEIGHT = 600  # ディスプレイの縦幅

class Bird(pg.sprite.Sprite):
    """
    ゲームキャラクター(こうかとん)に関するクラス
    """
    def __init__(self, num: int,x : int):
        """
        こうかとんの初期化
        引数1 num: こうかとん画像ファイル名の番号
        引数2 x: こうかとんのx座標
        """
        super().__init__()
        self.mode = 0  # 移動方向の判別 0: 右, 1: 左
        self.jump = 0  # こうかとんの飛び判定 0: 飛んでいない, 1: 飛んでいる
        self.cnt = 0  # こうかとんが飛んだときに頂上で浮遊している時間
        self.j_h = 0  # こうかとんが飛ぶときの高さの設定
        self.num=num
        self.img = pg.image.load(f"ex05/fig/{self.num}.png")
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.bottom = 500
        self.life = 2
       
    def update(self,screen: pg.Surface, mode: int, on_grd: bool,bird_h: int):
        """
        こうかとんの行動と描画を設定
        引数1 screen: 描画の時につかうpg.Surface
        引数2 mode: ゲームの状態を判定 0: ゲーム中, 1: ゲームオーバー, 2: ゴール
        引数3 on_grd: こうかとんが接地しているか判定 0: 接地している, 1:接地していない
        引数4 bird_h: こうかとんのbottomがどの高さにあるか判定
        """
        if mode == 0:
            if self.mode == 0:
                screen.blit(self.img,self.rect)
            elif self.mode == 1:
                screen.blit(pg.transform.flip(self.img,True,False),self.rect)
            if on_grd:
                if self.jump == 1:
                    self.rect.bottom -=5  # 5づつ上昇する
                    self.j_h = bird_h - 150  # こうかとんのbottomから150上の位置まで飛ぶようにする
                    if self.rect.bottom <= self.j_h:
                        self.cnt +=1
                        self.rect.bottom += 5  # 5の上昇と打消しでその場に留まる
                        if self.cnt >=20:
                            self.jump = 0
                            self.cnt = 0
                if self.jump == 0:
                    self.rect.bottom += 5  # 5づつ降下する
        elif mode == 1:
            self.num = 8  # こうかとんの画像を8番に変更
            self.img = pg.image.load(f"ex05/fig/{self.num}.png")
            screen.blit(self.img,self.rect)
            font1 = pg.font.SysFont(None, 80)
            text1 = font1.render("GAME OVER",True,(0,0,0))  
            screen.blit(text1, (240,200)) # GAME OVER テキストを表示
        elif mode == 2:
            self.num = 6  # こうかとんの画像を6番に変更
            self.img = pg.image.load(f"ex05/fig/{self.num}.png")
            font1 = pg.font.SysFont(None, 80)
            text1 = font1.render("GAME CLEAR",True,(255,215,0)) 
            screen.blit(self.img,self.rect) 
            screen.blit(text1, (220,200)) # GAMECLEAテキストを表示


class Background:
    """
    背景に関するクラス
    """
    def __init__(self, screen: pg.Surface):
        """
        背景の初期化
        引数1 screen: 描画の時につかうpg.Surface
        """
        self.x=0  # 背景の移動距離self.xを0に初期化
        self.bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
        self.bg_img_fl = pg.transform.flip(self.bg_img,True,False)
        screen.blit(self.bg_img_fl,[-800,0])

    def update(self, screen: pg.Surface, mode: int, wall: bool):
        """
        移動に応じた更新
        引数1 screen: 描画の時につかうpg.Surface
        引数2 mode: ゲームの状態を判定 0: ゲーム中, 1: ゲームオーバー, 2: ゴール
        引数3 wall: こうかとんが壁に当たっているか判定 0:当たっていない , 1:当たっている
        """
        if mode == 0:
            self.x%=3200  # 横幅が3200の背景を使いまわす為3200で割った余りにする
            screen.blit(self.bg_img,[800-self.x,0])
            screen.blit(self.bg_img_fl,[2400-self.x,0])
            screen.blit(self.bg_img_fl,[-800-self.x,0])
        elif mode == 1 or mode == 2 or wall:  # 背景を移動しないように設定
            screen.blit(self.bg_img,[800-self.x,0])
            screen.blit(self.bg_img_fl,[2400-self.x,0])
            screen.blit(self.bg_img_fl,[-800-self.x,0])


class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラス
    """
    def __init__(self, screen: pg.Surface, e_x: int):
        """
        敵の初期化
        引数1 screen: 描画の時につかうpg.Surface
        引数2 e_x: 敵の初期x座標
        """
        super().__init__()
        self.e_x = e_x
        self.vx = 0  # こうかとんの動きに連動した動きを設定するself.vxを0に初期化
        self.ev = 3  # 敵の移動速度を3に初期化
        self.ene_img = pg.transform.rotozoom(pg.image.load("ex05/fig/monster11.png"),0,0.2)
        self.rect = self.ene_img.get_rect()
        self.rect.centerx = self.e_x
        self.rect.bottom = 500
        screen.blit(self.ene_img,self.rect)

    def update(self, screen: pg.Surface, vx: int, mode: int):
        """
        こうかとんの動きやゲームの状態に応じて更新
        引数1 screen: 描画の時につかうpg.Surface
        引数2 vx: こうかとんの動きに応じたx座標の移動速度
        引数3 mode: ゲームの状態を判定 0: ゲーム中, 1: ゲームオーバー, 2: ゴール
        """
        if mode == 0:
            self.vx = vx
            self.rect.move_ip(self.vx,0)
            self.rect.centerx -= self.ev
            screen.blit(pg.transform.flip(self.ene_img,True,False),self.rect)
        else:
            screen.blit(self.ene_img,self.rect)
        

class Goal(pg.sprite.Sprite):
    """
    ゴールに関するクラス
    """
    def __init__(self, screen: pg.Surface):
        """
        ゴールの初期化
        引数1 screen: 描画の時につかうpg.Surface
        """
        super().__init__()
        self.g_img = pg.transform.rotozoom(pg.image.load("ex05/fig/torinosu_egg.png"),0,0.2)
        self.rect = self.g_img.get_rect()
        self.rect.centerx = 3200
        self.rect.bottom = 500
        screen.blit(self.g_img, self.rect)

    def update(self, screen: pg.Surface, bg: Background, vx: int):
        """
        こうかとんの動きに応じてゴールの位置の更新
        引数1 screen: 描画の時につかうpg.Surface
        引数2 bg: Backgroundのself.xを利用するための引数
        引数3 vx: こうかとんの動きに応じたx座標の移動速度
        """
        self.rect.move_ip(vx,0)
        screen.blit(self.g_img, self.rect)


class Ground(pg.sprite.Sprite):
    """
    地面の描画、設定をするクラス
    """
    def __init__(self, screen: pg.Surface, start: int, end: int, height: int):
        """
        地面の初期化
        引数1 screen: 描画の時につかうpg.Surface
        引数2 start: 地面の左端のx座標
        引数3 end: 地面の右端のx座標
        引数4 height: 地面の高さ
        """
        super().__init__()
        self.grd = pg.Surface((end - start,height))
        self.grd.fill((102,51,14))  # 地面の色を茶色に設定
        self.rect = self.grd.get_rect()
        self.rect.left = start
        self.rect.top = 600 - height
        screen.blit(self.grd,self.rect)

    def update(self,screen: pg.Surface, bg: Background, vx: int):
        """
        こうかとんの動きに応じた地面の更新
        引数1 screen: 描画の時につかうpg.Surface
        引数2 bg: Backgroundのself.xを利用するための引数
        引数3 vx: こうかとんの動きに応じたx座標の移動速度
        """
        self.rect.move_ip(vx,0)
        screen.blit(self.grd,self.rect)


class Score:
    """
    スコアに関するクラス
    敵を上から踏みつけると10、ゴールすると100
    """
    def __init__(self):
        """
        スコアの初期化
        """
        self.score = 0
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 0)
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, 50
        self.whi = 700
        self.hei = 500
        self.rectcenter = self.whi, self.hei

    def update(self, screen:pg.Surface, zanki):
        """
        その時のスコアに応じた更新
        引数1 screen: 描画の時につかうpg.Surface
        """
        self.image = self.font.render(f"Score: {self.score} Zanki : {zanki}", 0, self.color)
        screen.blit(self.image, self.rect)


class TitleScreen:
    """
    # タイトル画面の背景色やテキストの処理
    """
    def __init__(self,screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_color = (175,238,238)  # 背景色
        self.text_color = (0,128,0) # テキストの色
        self.title_font = pg.font.Font(None, 100) # メインタイトルの設定
        self.subtitle_font = pg.font.Font(None, 50) # サブタイトルの設定
        self.title_text = self.title_font.render("Super Kokaton", True, self.text_color) 
        self.subtitle_text = self.subtitle_font.render("Press Space to Start", True, self.text_color) 

    def show(self,screen):
        screen.fill(self.background_color)
        screen.blit(self.title_text, (150,200)) # メインタイトルの描画
        screen.blit(self.subtitle_text, (240,300)) # サブタイトルの描画


class Time():
    """
    タイムに関するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.time = 60 #時間制限
        self.time_60 = 0
        self.image = self.font.render(f"Time: {self.time}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH - 125, 50 # Time表示位置

    def time_up(self, add: int, mode: int):
        self.time_60 += add 
        if self.time_60 == 60: # カウントが60になったら
            self.time_60 = 0 
            if mode == 0:
                self.time -= 1 

    def update(self, screen: pg.Surface):
        if self.time <= 10:
            self.color = (255, 0, 0)
        self.image = self.font.render(f"Time: {self.time}", 0, self.color)
        screen.blit(self.image, self.rect)


class Coin(pg.sprite.Sprite):
    """
    コインに関するクラス
    """
    def __init__(self, screen: pg.Surface, c_x: int, c_y: int):
        """
        引数1 c_x:コインのx座標
        引数2 x_y:コインのy座標
        """
        super().__init__()
        self.c_x = c_x
        self.c_y = c_y
        self.coin_img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/food_daizu_meet.png"), 0, 0.1)
        self.coin_immg = pg.image
        self.rect = self.coin_img.get_rect()
        self.rect.centerx = self.c_x
        self.rect.centery = self.c_y
        screen.blit(self.coin_img, self.rect)
    
    def update(self, screen: pg.Surface, vx: int):
        self.rect.move_ip(vx, 0)
        screen.blit(self.coin_img, self.rect)


def main():
    pg.display.set_caption("Super_Kokaton")
    screen = pg.display.set_mode((WIDTH,HEIGHT))

    bird = Bird(2,200)
    bg = Background(screen)
    enes = pg.sprite.Group()
    gls = pg.sprite.Group()
    grws = pg.sprite.Group()
    grds = pg.sprite.Group()
    coins = pg.sprite.Group()
    scr = Score()
    time = Time()

    for i in range(4):
        enes.add(Enemy(screen, i * 200 + 1000))
    enes.add(Enemy(screen, 2000))
    gl = Goal(screen)
    gls.add(gl)
    grd1 = Ground(screen, 3000, 4400, 101)  # spritecollideの処理は重なっていないと起きないので1を追加した数をheightにする
    grds.add(grd1)
    grd2 = Ground(screen, 0, 2000, 101)
    grds.add(grd2)
    grd3 = Ground(screen, 2000, 2200, 201)
    grds.add(grd3)
    grd4 = Ground(screen, 2400, 2500, 201)
    grds.add(grd4)
    grd5 = Ground(screen, 2750, 2850, 101)
    grds.add(grd5)
    for i in range(7):
        coins.add(Coin(screen,i*400+500,300))
 
    tmr = 0  # ゲームが終わった際の描画時間用タイマー
    life_tmr = 0
    mode = 0
    on_grd = False
    bird_h = 0
    wall = False
    clock = pg.time.Clock()
    game_state = 0
    title_screen = TitleScreen(WIDTH,HEIGHT)
    
    while True:
        vx = 0
        on_grd = True
        key_lst = pg.key.get_pressed()
        for  event in pg.event.get():
            if event.type == pg.QUIT: return
            if game_state == 0:
                title_screen.show(screen)
                pg.display.update()
            if key_lst[pg.K_SPACE]:
                game_state = 1
        if game_state == 1:
            if key_lst[pg.K_RIGHT] and mode == 0:  # 十字キー右を押した際の処理
                bird.mode = 0
                bg.x += 5
                vx = -5
            if key_lst[pg.K_LEFT] and mode == 0:  # 十字キー左を押した際の処理
                bird.mode = 1
                bg.x -= 5
                if bg.x > 0 :
                    vx = 5
            if bg.x <= 0:  # 初期値より左にはいけないような処理
                bg.x = 0
            if bird.rect.centerx >= gl.rect.centerx:  # ゴールより右にいけないような処理
                bg.x = 3000
                vx = 0
            for ground in pg.sprite.spritecollide(bird, grds, False):  # こうかとんが接地しているときの処理
                if bird.rect.bottom == ground.rect.top + 1:
                    on_grd = False
                if bird.rect.bottom != ground.rect.top + 1:
                    if bird.rect.right - (bird.rect.right % 10) == ground.rect.left:
                        wall = True
                        if key_lst[pg.K_RIGHT] and mode == 0:
                            bg.x -= 5
                            vx = 0
                            mode = 0
                    if bird.rect.left + (10 - bird.rect.left % 10) == ground.rect.right:
                        wall = True
                        if key_lst[pg.K_LEFT] and mode == 0:
                            bg.x += 5
                            vx = 0
                            mode = 0
            if not on_grd and key_lst[pg.K_UP]:  # 十字キー上を押したときの処理
                bird.jump = 1
                bird.rect.bottom -= 5
                bird_h = bird.rect.bottom
            for ene in pg.sprite.spritecollide(bird, enes, False):  # こうかとんと敵が接触したときの処理
                if bird.rect.bottom <= ene.rect.top + 5:  # 上から踏んだ時に踏んだ敵を消しスコアを10アップ
                    enes.remove(ene)
                    scr.score += 10
                    pass
                else:  # 上以外からぶつかった時ゲームオーバーになり、残り描画時間設定用のtmrが回り始める
                    if mode == 0:
                        if life_tmr == 0:
                            bird.life -= 1
                            life_tmr = 30
                        else:
                            life_tmr -= 1
                            if life_tmr < 0:
                                life_tmr = 0
                    if bird.life < 1:
                        tmr += 1
                        mode = 1
            if bird.rect.top > 600:  # 描画範囲より下に行った場合の処理
                font1 = pg.font.SysFont(None, 80)
                text1 = font1.render("GAME OVER",True,(0,0,0))  
                screen.blit(text1, (240,200)) # GAME OVER テキストを表示
                tmr += 1
                mode = 1
            for coin in pg.sprite.spritecollide(bird, coins, True):
                scr.score += 50
            if time.time <= 0:
                tmr += 1
                mode = 1
            for goal in pg.sprite.spritecollide(bird,gls,False):  # こうかとんがゴールに接触したときの処理
                tmr += 1
                mode = 2
                if tmr == 1:
                    scr.score += 100
            if tmr >= 150:  # ゲーム終了から150カウント進んだら終了するための処理
                return
            time.time_up(1, mode)
            bg.update(screen, mode, wall)
            grds.update(screen, bg, vx)
            bird.update(screen, mode, on_grd, bird_h)
            enes.update(screen, vx, mode)
            gls.update(screen, bg, vx)
            scr.update(screen, bird.life)
            time.update(screen)
            coins.update(screen, vx)

            pg.display.update()
            clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

