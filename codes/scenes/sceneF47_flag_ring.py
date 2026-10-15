"""
Scene F47 —— 點在線上：旗流形與它的座標環（Fulton §9.1 Lemma 2、命題 1；§9.2；§9.3；書 p.134–145）
執行（在 codes/ 內）：manimgl scenes/sceneF47_flag_ring.py SceneF47FlagRing

P^2 的旗 = (點 ⊂ 線)：v1 = (1,2,3)、v2 = (0,1,1)，線的座標 (y12,y13,y23) = (1,1,−1)；
關聯方程 x1y23 − x2y13 + x3y12 = 0（v1 代入得 0，(1,0,0) 代入得 −1）；命題 1：Fl(C^3) ⊂ P^2×P^2；
座標環 S(3;1,2) 雙次數 (a,b) 的維數 = C(a+2,2)C(b+2,2) − C(a+1,2)C(b+1,2) = dim E^{(a+b,b)}；
一句不變量（§9.2）、一句 Borel–Weil（§9.3）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *
from math import comb

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.schubert import flag_ring_dim, plucker
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import hook_content_count

V1, V2 = (1, 2, 3), (0, 1, 1)
Y = (1, 1, -1)                         # (y12, y13, y23)
OFF = (1, 0, 0)
DIMS = {(0, 0): 1, (1, 0): 3, (0, 1): 3, (2, 0): 6, (1, 1): 8, (0, 2): 6, (2, 1): 15, (1, 2): 15, (2, 2): 27}
ORDER = [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (2, 1), (1, 2), (2, 2)]
SLOW = 4.4


def incidence(x, y):
    return x[0] * y[2] - x[1] * y[1] + x[2] * y[0]


def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def fit(mob, w):
    if mob.get_width() > w:
        mob.set_width(w)
    return mob


def shape_mob(lam, cs=0.16):
    """小 Young 圖（只看形狀）；空的形狀畫成 ∅。"""
    if not any(lam):
        return Tex(r"\emptyset", font_size=26).set_color(MUTED_COLOR)
    g = VGroup()
    for i, r in enumerate(lam):
        for j in range(r):
            g.add(Square(cs).move_to(np.array([j * cs, -i * cs, 0.0])).set_stroke(WHITE, 1.2).set_fill(BLUE_C, 0.55))
    return g


def check_math():
    y = plucker((V1, V2))
    assert tuple(y.values()) == Y and list(y) == [(1, 2), (1, 3), (2, 3)]
    assert (V1[0] * Y[2], V1[1] * Y[1], V1[2] * Y[0]) == (-1, 2, 3) and incidence(V1, Y) == 0
    assert incidence(V2, Y) == 0 and incidence(OFF, Y) == -1
    for x in (V1, OFF, (2, -1, 5)):                                # 關聯式 = det(x; v1; v2)
        assert incidence(x, Y) == det3((x, V1, V2))
    for (a, b), d in DIMS.items():
        assert flag_ring_dim(a, b) == d == hook_content_count((a + b, b), 3)
    assert comb(3, 2) * comb(3, 2) - 1 == 8 == flag_ring_dim(1, 1)
    assert len(ORDER) == len(DIMS) == len(set(ORDER))


# ---------------------------------------------------------------- 1. 點在線上：一條方程
def part_incidence(scene):
    box = Rectangle(width=4.2, height=4.6).set_stroke(GREY_D, 2).move_to(np.array([-4.35, 0.15, 0]))
    p2 = Tex(r"\mathbb P^2", font_size=32).set_color(MUTED_COLOR).next_to(box.get_corner(UL), DR, buff=0.15)
    a, b = np.array([-6.1, -1.5, 0]), np.array([-2.8, 1.7, 0])
    line = Line(a, b).set_stroke(TEAL_B, 4)
    lab_l = Tex(r"\ell", font_size=36).set_color(TEAL_B).move_to(b + np.array([0.3, -0.3, 0]))
    p1 = Dot(a + 0.32 * (b - a), radius=0.09).set_color(OP_COLOR)
    q1 = Dot(a + 0.72 * (b - a), radius=0.07).set_color(WHITE)
    l1 = Tex(r"[v_1]", font_size=30).set_color(OP_COLOR).next_to(p1, UL, buff=0.1)
    l2 = Tex(r"[v_2]", font_size=30).next_to(q1, UL, buff=0.1)
    off = Dot(np.array([-3.4, -1.3, 0]), radius=0.09).set_color(NEG_COLOR)
    loff = Tex(r"(1,0,0)", font_size=28).set_color(NEG_COLOR).next_to(off, DOWN, buff=0.12)
    pic = VGroup(box, p2, line, lab_l, p1, q1, l1, l2, off, loff)

    cx = 2.4
    vv = Tex(r"v_1=(1,2,3),\quad v_2=(0,1,1)", font_size=34).move_to(np.array([cx, 2.5, 0]))
    mat = MatrixMob((V1, V2), font_size=36, h_buff=0.75, v_buff=0.55).move_to(np.array([cx, 1.5, 0]))
    ym = Tex(r"(y_{12},y_{13},y_{23})=(1,1,-1)", font_size=34).set_color(TEAL_B).move_to(np.array([cx, 0.45, 0]))
    inc = Tex(r"x_1y_{23}-x_2y_{13}+x_3y_{12}=0", font_size=38).set_color(POS_COLOR)
    inc.move_to(np.array([cx, -0.5, 0]))
    e1 = Tex(r"x=v_1:\quad1\cdot(-1)-2\cdot1+3\cdot1=0", font_size=32).set_color(OP_COLOR)
    e1.move_to(np.array([cx, -1.4, 0]))
    e2 = Tex(r"x=(1,0,0):\quad1\cdot(-1)-0\cdot1+0\cdot1=-1\neq0", font_size=32).set_color(NEG_COLOR)
    e2.move_to(np.array([cx, -2.25, 0]))
    for m in (vv, ym, inc, e1, e2):
        fit(m, 8.0)
    right = VGroup(vv, mat, ym, inc, e1, e2)
    assert_in_frame(pic, right)
    assert_apart(pic, right, 0.3)
    for u, v in ((vv, mat), (mat, ym), (ym, inc), (inc, e1), (e1, e2)):
        assert_apart(u, v, 0.1)
    d = b - a                                                      # 不在線上的點離直線夠遠
    assert abs(np.cross(d[:2], (off.get_center() - a)[:2])) / np.linalg.norm(d) > 0.8

    scene.say("問：「一個點落在一條線上」要幾條方程？", wait=SLOW * 0.8)
    scene.play(ShowCreation(box), FadeIn(p2), run_time=0.8)
    scene.play(ShowCreation(line), FadeIn(lab_l), run_time=1.0)
    scene.play(FadeIn(p1, scale=0.5), FadeIn(l1), run_time=0.7)
    scene.say("$\\mathbb P^2$", " 裡的一個旗：一個點放在一條線上", wait=SLOW * 0.7)
    scene.play(FadeIn(q1, scale=0.5), FadeIn(l2), FadeIn(vv), run_time=0.9)
    scene.say("點是 ", "$[v_1]$", "；線 ", "$\\ell$", " 由 ", "$v_1$", " 和 ", "$v_2$", " 張成", wait=SLOW * 0.6)
    scene.play(FadeIn(mat), run_time=0.8)
    scene.say("線也有 Plücker 座標：", "$2\\times3$", " 矩陣的三個 ", "$2\\times2$", " 子式", wait=SLOW * 0.2)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        rect = VGroup(*[SurroundingRectangle(mat.col(c - 1), buff=0.1, color=TEAL_B) for c in (i, j)])
        scene.play(ShowCreation(rect), run_time=0.5)
        scene.wait(SLOW * 0.15)
        scene.play(FadeOut(rect), run_time=0.3)
    scene.play(FadeIn(ym, shift=0.2 * DOWN), run_time=0.8)
    scene.say("線的座標：", "$y_{12},y_{13},y_{23}=1,1,-1$", wait=SLOW * 0.6)
    scene.play(Write(inc), run_time=1.2)
    scene.say("Lemma 2：點 ", "$x$", " 在線上 ", "$\\Leftrightarrow$", " 這一條關聯方程成立", wait=SLOW * 0.8)
    scene.play(FadeIn(e1, shift=0.2 * DOWN), Indicate(p1, color=OP_COLOR), run_time=1.0)
    scene.say("代入 ", "$v_1$", "：", "$-1-2+3=0$", "，點確實在線上", wait=SLOW * 0.7)
    scene.play(FadeIn(off, scale=0.5), FadeIn(loff), FadeIn(e2, shift=0.2 * DOWN), run_time=1.0)
    scene.say("換一個不在線上的點 ", "$(1,0,0)$", "：得到 ", "$-1\\neq0$", wait=SLOW * 0.8)
    scene.say("其實它就是 ", "$3\\times3$", " 行列式 ", "$\\det(x;v_1;v_2)$", " 沿第一列展開", wait=SLOW * 0.9)
    scene.say("答案：一條；", "$x$", " 一次、", "$y$", " 一次——又是一條二次關係", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 2. 命題 1 與座標環的維數
def part_ring(scene):
    fl = Tex(r"Fl(\mathbb C^3)=\{x_1y_{23}-x_2y_{13}+x_3y_{12}=0\}\subset\mathbb P^2\times\mathbb P^2",
             font_size=34).move_to(np.array([0, 2.6, 0]))
    ring = Tex(r"S(3;1,2)=\operatorname{Sym}(E\oplus\textstyle\bigwedge^2E)/(x_1y_{23}-x_2y_{13}+x_3y_{12})",
               font_size=34).set_color(TEAL_B).move_to(np.array([0, 1.85, 0]))
    f1 = Tex(r"\dim S_{(a,b)}=\binom{a+2}2\binom{b+2}2-\binom{a+1}2\binom{b+1}2", font_size=32)
    f1.move_to(np.array([-3.6, 0.45, 0]))
    f3 = Tex(r"=\dim E^{(a+b,b)}", font_size=34).set_color(OP_COLOR)
    ex = Tex(r"(1,1):\quad3\cdot3-1\cdot1=8", font_size=32).set_color(POS_COLOR).move_to(np.array([-3.6, -1.35, 0]))
    for m in (fl, ring):
        fit(m, 12.8)
    fit(f1, 5.9)
    f3.next_to(f1, DOWN, buff=0.35).align_to(f1, RIGHT)

    xs = [1.5 + 1.75 * b for b in range(3)]
    ys = [0.4 - 1.2 * a for a in range(3)]
    col_h = VGroup(*[Tex("b=%d" % b, font_size=28).set_color(MUTED_COLOR).move_to(np.array([x, 1.15, 0]))
                     for b, x in zip(range(3), xs)])
    row_h = VGroup(*[Tex("a=%d" % a, font_size=28).set_color(MUTED_COLOR).move_to(np.array([0.2, y, 0]))
                     for a, y in zip(range(3), ys)])
    cells = {}
    for (a, b), d in DIMS.items():
        n = Tex(str(d), font_size=38).move_to(np.array([xs[b] - 0.38, ys[a], 0]))
        s = shape_mob((a + b, b)).move_to(np.array([xs[b] + 0.42, ys[a], 0]))
        cells[(a, b)] = VGroup(n, s)
    grid = VGroup(col_h, row_h, *cells.values())
    assert_in_frame(fl, ring, f1, f3, ex, grid)
    assert_apart(fl, ring, 0.1)
    assert_apart(ring, col_h, 0.1)
    assert_apart(VGroup(f1, f3, ex), grid, 0.3)
    assert_apart(f3, ex, 0.2)
    for (a, b), c in cells.items():
        if (a, b + 1) in cells:
            assert_apart(c, cells[(a, b + 1)], 0.2)
        if (a + 1, b) in cells:
            assert_apart(c, cells[(a + 1, b)], 0.2)

    scene.say("命題 1：", "$Fl(\\mathbb C^3)$", " 放進 ", "$\\mathbb P^2\\times\\mathbb P^2$", "，由這種二次方程切出", wait=SLOW * 0.2)
    scene.play(Write(fl), run_time=1.4)
    scene.wait(SLOW * 0.6)
    scene.say("座標環：", "$x_i$", " 和 ", "$y_{jk}$", " 的多項式，再除掉關係", wait=SLOW * 0.2)
    scene.play(Write(ring), run_time=1.4)
    scene.wait(SLOW * 0.6)
    scene.say("數維數遊戲：", "$x$", " 的次數 ", "$a$", "、", "$y$", " 的次數 ", "$b$", wait=SLOW * 0.2)
    scene.play(FadeIn(col_h), FadeIn(row_h), FadeIn(cells[(0, 0)]), run_time=0.9)
    scene.play(FadeIn(cells[(1, 0)]), FadeIn(cells[(0, 1)]), run_time=0.8)
    scene.say("$(1,0)$", "：", "$x_1,x_2,x_3$", " 三個；", "$(0,1)$", "：三個 ", "$y_{jk}$", wait=SLOW * 0.6)
    scene.play(FadeIn(cells[(2, 0)]), FadeIn(cells[(0, 2)]), run_time=0.8)
    scene.say("$(2,0)$", "、", "$(0,2)$", "：二次單項式各 6 個", wait=SLOW * 0.5)
    scene.play(FadeIn(ex, shift=0.2 * UP), FadeIn(cells[(1, 1)]), run_time=0.9)
    scene.say("$(1,1)$", "：", "$x_iy_{jk}$", " 有 9 個，關係式扣掉 1 個，剩 8", wait=SLOW * 0.8)
    scene.play(FadeIn(f1), run_time=1.0)
    scene.say("一般的公式：", "$(a,b)$", " 的單項式，扣掉關係乘上 ", "$(a-1,b-1)$", " 的部分", wait=SLOW * 0.8)
    scene.play(LaggedStart(*[FadeIn(cells[k]) for k in ((2, 1), (1, 2), (2, 2))], lag_ratio=0.4), run_time=1.4)
    scene.say("$15$", "、", "$15$", "、", "$27$", "……", wait=SLOW * 0.5)
    scene.play(Write(f3), run_time=1.0)
    scene.say("每一格正好是 ", "$GL_3$", " 的不可約表示 ", "$E^{(a+b,b)}$", " 的維數", wait=SLOW * 0.4)
    scene.play(LaggedStart(*[Indicate(cells[k][1], color=OP_COLOR) for k in ORDER[1:]], lag_ratio=0.15),
               run_time=1.8)
    scene.say("格子旁邊的小圖就是形狀 ", "$(a+b,b)$", "：最多兩列，每個形狀剛好一格", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 3. 不變量、Borel–Weil、收束
def part_bigger(scene):
    inv1 = mixed("§9.2 命題 2：", "$SL_n$", " 不變的多項式 ＝ 最大子式的多項式", font_size=28)
    inv2 = Tex(r"g\in SL_n:\quad\det(gA)=\det g\cdot\det A=\det A", font_size=34).set_color(MUTED_COLOR)
    bw1 = mixed("§9.3 Borel–Weil：", "$E^\\lambda$", " ＝ 旗流形上一個線叢的截面", font_size=28)
    bw2 = mixed("旗流形 ＝ 最高權重向量 ", "$[e_{U(\\lambda)}]$", " 在 ", "$\\mathbb P(E^\\lambda)$", " 裡的軌道",
                font_size=28)
    inv1.move_to(np.array([0, 2.5, 0]))
    inv2.move_to(np.array([0, 1.75, 0]))
    bw1.move_to(np.array([0, 0.75, 0]))
    bw2.move_to(np.array([0, 0.0, 0]))
    final = Tex(r"S(3;1,2)=\bigoplus_{a,b\ge0}E^{(a+b,b)}", font_size=46).set_color(POS_COLOR)
    final.move_to(np.array([0, -1.6, 0]))
    frame = SurroundingRectangle(final, buff=0.2, color=POS_COLOR)
    for m in (inv1, inv2, bw1, bw2):
        fit(m, 12.6)
    assert_in_frame(inv1, inv2, bw1, bw2, final, frame)
    for u, v in ((inv1, inv2), (inv2, bw1), (bw1, bw2), (bw2, frame)):
        assert_apart(u, v, 0.1)

    scene.say("兩句帶過的大定理", wait=SLOW * 0.2)
    scene.play(FadeIn(inv1, shift=0.2 * RIGHT), run_time=0.9)
    scene.say("哪些多項式在 ", "$SL_n$", " 作用下不變？正好是最大子式組成的多項式", wait=SLOW * 0.6)
    scene.play(FadeIn(inv2), run_time=0.8)
    scene.say("原因之一：", "$\\det g=1$", "，最大子式本身不會改變", wait=SLOW * 0.8)
    scene.play(FadeIn(bw1, shift=0.2 * RIGHT), run_time=0.9)
    scene.say("Borel–Weil：每個 ", "$E^\\lambda$", " 都可以實現成旗流形上某個線叢的截面", wait=SLOW * 0.8)
    scene.play(FadeIn(bw2, shift=0.2 * RIGHT), run_time=0.9)
    scene.say("反過來，旗流形就是最高權重向量在 ", "$\\mathbb P(E^\\lambda)$", " 裡的軌道", wait=SLOW * 0.9)
    scene.play(Write(final), ShowCreation(frame), run_time=1.4)
    scene.say("回到 ", "$m=3$", "：座標環拆開，正好是這些表示的直和", wait=SLOW * 0.8)
    scene.play(Indicate(final, color=POS_COLOR), run_time=1.0)
    scene.say("一個環把 ", "$GL_3$", " 的不可約表示一個不漏地裝進來（每個一次）", wait=SLOW * 1.2)


class SceneF47FlagRing(ChuScene):
    def construct(self):
        self.show_header("點在線上：旗流形與它的座標環")
        check_math()
        part_incidence(self)
        self.clear_stage()
        part_ring(self)
        self.clear_stage()
        part_bigger(self)
        self.wait(1.0)
