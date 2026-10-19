import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんまたは爆弾のRect
    戻り値:タプル (横方向判定結果,縦方向関係結果)
    画面内ならTrue/画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の画像と加速度のリストを作成する
    戻り値：爆弾画像のリスト、加速度のリスト
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動方向に対応するこうかとん画像の辞書を作成する
    """
    kk_imgs = {}
    for x in [-5, 0, 5]:
        for y in [-5, 0, 5]:
            kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), -x*9, 0.9)
            kk_imgs[(x, y)] = kk_img
    return kk_imgs


def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が着弾した際に、画面をブラックアウトし、
    泣いているこうかとん画像と「Game Over」を表示して5秒間停止する
    引数 screen: 画面Surface
    """
    black_out = pg.Surface((WIDTH, HEIGHT))
    black_out.fill((0,0,0))
    black_out.set_alpha(150)

    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH // 2, HEIGHT // 2)

    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_kk_rct1 = cry_kk_img.get_rect()
    cry_kk_rct2 = cry_kk_img.get_rect()

    cry_kk_rct1.center = (txt_rct.left - 50, HEIGHT // 2)
    cry_kk_rct2.center = (txt_rct.right + 50, HEIGHT // 2)

    black_out.blit(txt, txt_rct)
    black_out.blit(cry_kk_img, cry_kk_rct1)
    black_out.blit(cry_kk_img, cry_kk_rct2)

    screen.blit(black_out, [0, 0])
    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # 練習4：kkとbbのrectが重なっていたら
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
                
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_rct.move_ip(avx, avy)
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_rct.size = bb_img.get_rect().size
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
