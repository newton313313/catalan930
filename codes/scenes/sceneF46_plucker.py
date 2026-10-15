"""
Scene F46 —— 六個數認出一個平面：Plücker 座標（Fulton §9.1，書 p.131–134）
執行（在 codes/ 內）：manimgl scenes/sceneF46_plucker.py SceneF46Plucker

A = [[1,2,0,1],[0,1,3,2]] 的 6 個 2×2 子式 1,3,2,6,3,−3；換列 g = [[1,1],[0,2]]：子式全部 ×det g = 2 → P^5 的一點；
Plücker 關係 p12p34 − p13p24 + p14p23 = 0：Gr(2,4) 是 P^5 裡的二次超曲面（維數 4）；Lemma 1；
練習 2：由 (1,2,1,1,2,3) 用式 (2) 還原 B = [[1,0,−1,−2],[0,1,2,1]]，ker B = ⟨(1,−2,1,0),(2,−1,0,1)⟩。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.schubert import plucker, plucker_from_coords
from utils.styles import MUTED_COLOR, mixed, zh

A = ((1, 2, 0, 1), (0, 1, 3, 2))
G = ((1, 1), (0, 2))
GA = ((1, 3, 3, 3), (0, 2, 6, 4))
PAIRS = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
P_A = (1, 3, 2, 6, 3, -3)
X = (1, 2, 1, 1, 2, 3)
B = ((1, 0, -1, -2), (0, 1, 2, 1))
KER = ((1, -2, 1, 0), (2, -1, 0, 1))
BAD = (1, 0, 0, 0, 0, 1)
SLOW = 3.6


def matmul(M, N):
    return tuple(tuple(sum(M[r][k] * N[k][c] for k in range(len(N))) for c in range(len(N[0])))
                 for r in range(len(M)))


def rel(p):
    """p 依 PAIRS 的順序：p12 p34 − p13 p24 + p14 p23。"""
    return p[0] * p[5] - p[1] * p[4] + p[2] * p[3]


def num(x):
    return "(%d)" % x if x < 0 else str(x)


def fit(mob, w):
    if mob.get_width() > w:
        mob.set_width(w)
    return mob


def row_tex(s):
    """式 (2) 的第 s 列（1 起算）：把 I=(1,2) 的第 s 個換成 t，t = 1..4。"""
    subs = [(t, 2) if s == 1 else (1, t) for t in range(1, 5)]
    lhs = r"a_{%d,t}=x_{%s}" % (s, "t2" if s == 1 else "1t")
    xs = ",".join("x_{%d%d}" % ij for ij in subs)
    vals = ",".join(str(v) for v in B[s - 1])
    return r"%s:\quad(%s)=(%s)" % (lhs, xs, vals)


def check_math():
    pa = plucker(A)
    assert list(pa) == PAIRS and tuple(pa.values()) == P_A
    assert matmul(G, A) == GA and G[0][0] * G[1][1] - G[0][1] * G[1][0] == 2
    assert tuple(plucker(GA).values()) == tuple(2 * v for v in P_A) == (2, 6, 4, 12, 6, -6)
    assert (P_A[0] * P_A[5], P_A[1] * P_A[4], P_A[2] * P_A[3]) == (-3, 9, 12) and rel(P_A) == 0
    assert all(v >= 0 for r in A for v in r)                      # 子式的算式不需加括號
    assert rel(BAD) == 1
    assert (X[0] * X[5], X[1] * X[4], X[2] * X[3]) == (3, 4, 1) and rel(X) == 0
    Bc = plucker_from_coords(dict(zip(PAIRS, X)), 2, 4)
    assert all(v.denominator == 1 for r in Bc for v in r)
    assert tuple(tuple(int(v) for v in r) for r in Bc) == B
    assert tuple(plucker(B).values()) == X
    assert all(sum(B[r][c] * v[c] for c in range(4)) == 0 for r in range(2) for v in KER)
    assert plucker(KER)[(3, 4)] != 0                               # 兩個向量線性獨立 → ker B 是 2 維
    assert 5 - 1 == 2 * 4 - 2 * 2 == 4
    assert row_tex(1).endswith("(1,0,-1,-2)") and row_tex(2).endswith("(0,1,2,1)")


# ---------------------------------------------------------------- 1. 六個子式、換列只差倍數
def part_minors(scene):
    mat = MatrixMob(A, font_size=36, h_buff=0.7, v_buff=0.55)
    am = VGroup(Tex("A=", font_size=40), mat).arrange(RIGHT, buff=0.2).move_to(np.array([-4.2, 1.5, 0]))
    idx = VGroup(*[Tex(str(j + 1), font_size=24).set_color(MUTED_COLOR).next_to(mat.col(j), UP, buff=0.3)
                   for j in range(4)])
    gmat = MatrixMob(GA, font_size=36, h_buff=0.7, v_buff=0.55)
    gam = VGroup(Tex("gA=", font_size=40), gmat).arrange(RIGHT, buff=0.2).move_to(np.array([0, -0.6, 0]))
    gam.shift((mat.get_center()[0] - gmat.get_center()[0]) * RIGHT)
    gdef = Tex(r"g=\begin{pmatrix}1&1\\0&2\end{pmatrix},\quad\det g=2", font_size=32)
    gdef.move_to(np.array([-4.2, -2.25, 0]))
    xs = [0.45 + 1.15 * k for k in range(6)]
    ya, yg = mat.get_center()[1], gmat.get_center()[1]
    heads = VGroup(*[Tex("p_{%d%d}" % ij, font_size=34).set_color(MUTED_COLOR).move_to(np.array([x, 2.6, 0]))
                     for ij, x in zip(PAIRS, xs)])
    vals_a = [Tex(str(v), font_size=38).set_color(NEG_COLOR if v < 0 else WHITE).move_to(np.array([x, ya, 0]))
              for v, x in zip(P_A, xs)]
    vals_g = [Tex(str(2 * v), font_size=38).set_color(NEG_COLOR if v < 0 else WHITE).move_to(np.array([x, yg, 0]))
              for v, x in zip(P_A, xs)]
    times = VGroup(*[Tex(r"\times2", font_size=26).set_color(OP_COLOR).move_to(np.array([x, (ya + yg) / 2, 0]))
                     for x in xs])
    detail_pos = np.array([3.3, (ya + yg) / 2, 0])
    point = Tex(r"[1:3:2:6:3:-3]\in\mathbb P^5", font_size=40).set_color(POS_COLOR)
    point.move_to(np.array([3.3, -1.95, 0]))
    frame = SurroundingRectangle(point, buff=0.15, color=POS_COLOR)
    assert_in_frame(am, idx, gam, gdef, heads, *vals_a, *vals_g, times, point, frame)
    assert_apart(am, heads, 0.3)
    assert_apart(gam, VGroup(*vals_g), 0.3)
    assert_apart(gdef, frame, 0.3)
    assert_apart(gam, gdef, 0.1)

    scene.say("問：", "$\\mathbb C^4$", " 裡的 2 維子空間，能不能用一串數字當身分證？", wait=SLOW * 0.8)
    scene.play(FadeIn(am), FadeIn(idx), run_time=1.0)
    scene.say("Fulton 的寫法：", "$2\\times4$", " 矩陣 ", "$A$", "，子空間 ", "$V=\\ker A$", wait=SLOW * 0.8)
    scene.say("對 ", "$A$", " 做列運算，", "$\\ker A$", " 不變：同一個 ", "$V$", " 有很多個 ", "$A$", wait=SLOW * 0.8)
    scene.say("身分證的候選：取兩行（column），算 ", "$2\\times2$", " 子式，共 ", "$\\binom42=6$", " 個",
              wait=SLOW * 0.3)
    scene.play(FadeIn(heads), run_time=0.8)
    for k, (i, j) in enumerate(PAIRS):
        rect = VGroup(*[SurroundingRectangle(mat.col(c - 1), buff=0.1, color=OP_COLOR) for c in (i, j)])
        det = Tex(r"p_{%d%d}=%d\cdot%d-%d\cdot%d" % (i, j, A[0][i - 1], A[1][j - 1], A[0][j - 1], A[1][i - 1]),
                  font_size=34).set_color(OP_COLOR).move_to(detail_pos)
        rt = 0.7 if k < 2 else 0.45
        scene.play(ShowCreation(rect), FadeIn(det), run_time=rt)
        scene.play(TransformFromCopy(det, vals_a[k]), run_time=rt)
        scene.wait(SLOW * (0.3 if k < 2 else 0.1))
        scene.play(FadeOut(rect), FadeOut(det), run_time=0.35)
    scene.say("六個數：", "$1,3,2,6,3,-3$", wait=SLOW * 0.5)
    scene.say("換一組列：左乘一個可逆的 ", "$2\\times2$", " 矩陣 ", "$g$", wait=SLOW * 0.2)
    scene.play(FadeIn(gdef, shift=0.2 * UP), run_time=0.8)
    scene.play(TransformFromCopy(am, gam), run_time=1.2)
    scene.say("同一個子空間：", "$\\ker(gA)=\\ker A$", wait=SLOW * 0.6)
    scene.say("新的六個子式：", "$2,6,4,12,6,-6$", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(v, shift=0.2 * DOWN) for v in vals_g], lag_ratio=0.15), run_time=1.4)
    scene.say("全部乘上同一個數 ", "$\\det g=2$", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(t) for t in times], lag_ratio=0.1), run_time=1.0)
    scene.wait(SLOW * 0.5)
    scene.say("所以只有比例有意義：", "$V$", " 對應 ", "$\\mathbb P^5$", " 的一個點", wait=SLOW * 0.2)
    scene.play(Write(point), ShowCreation(frame), run_time=1.2)
    scene.say("這六個數叫 ", "$V$", " 的 Plücker 座標", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 2. 二次關係：Gr(2,4) 是二次超曲面
def part_relation(scene):
    relm = Tex(r"p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0", font_size=44).set_color(POS_COLOR)
    relm.move_to(np.array([0, 2.45, 0]))
    ev = Tex(r"A:\quad1\cdot(-3)-3\cdot3+2\cdot6=-3-9+12=0", font_size=36).move_to(np.array([0, 1.55, 0]))
    bad = Tex(r"(1:0:0:0:0:1):\quad1\cdot1-0\cdot0+0\cdot0=1\neq0", font_size=36).set_color(NEG_COLOR)
    bad.move_to(np.array([0, 0.7, 0]))
    gr = Tex(r"Gr(2,4)=\{p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0\}\subset\mathbb P^5", font_size=38)
    gr.move_to(np.array([0, -0.35, 0]))
    dim = Tex(r"\dim Gr(2,4)=5-1=4=8-4", font_size=36).set_color(OP_COLOR).move_to(np.array([0, -1.3, 0]))
    lem = mixed("Lemma 1：一般的 ", "$Gr$", " 也由二次方程（Plücker 關係）切出", font_size=28)
    lem.move_to(np.array([0, -2.35, 0]))
    for m in (relm, ev, bad, gr, dim, lem):
        fit(m, 12.6)
    assert_in_frame(relm, ev, bad, gr, dim, lem)
    for a, b in ((relm, ev), (ev, bad), (bad, gr), (gr, dim), (dim, lem)):
        assert_apart(a, b, 0.1)

    scene.say("反過來：", "$\\mathbb P^5$", " 裡任取六個數，都是某個平面的座標嗎？", wait=SLOW * 0.8)
    scene.play(Write(relm), run_time=1.4)
    scene.say("不是：六個子式一定滿足 Plücker 關係（F45 看過）", wait=SLOW * 0.8)
    scene.play(FadeIn(ev, shift=0.2 * DOWN), run_time=0.9)
    scene.say("代入 ", "$A$", " 的六個子式：", "$-3-9+12=0$", wait=SLOW * 0.8)
    scene.play(FadeIn(bad, shift=0.2 * DOWN), run_time=0.9)
    scene.say("隨便取 ", "$(1:0:0:0:0:1)$", "：算出 1，不是任何平面的座標", wait=SLOW * 1.0)
    scene.play(Write(gr), run_time=1.4)
    scene.say("反之，滿足關係的點都來自一個平面（練習 2 會倒推回去）", wait=SLOW * 0.8)
    scene.say("所以 ", "$Gr(2,4)$", " 是 ", "$\\mathbb P^5$", " 裡一條二次方程的零點：二次超曲面", wait=SLOW * 0.8)
    scene.play(FadeIn(dim, shift=0.2 * DOWN), run_time=0.9)
    scene.say("一條方程降一維：", "$5-1=4$", wait=SLOW * 0.6)
    scene.say("另一種數法：", "$A$", " 有 8 個數，", "$g$", " 有 4 個數，", "$8-4=4$", wait=SLOW * 0.9)
    scene.play(FadeIn(lem, shift=0.2 * UP), run_time=0.9)
    scene.say("一般的 ", "$Gr$", "：二次關係不只一條，但全都是二次的", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 3. 練習 2：由座標還原矩陣
def part_inverse(scene):
    xm = Tex(r"(x_{12},x_{13},x_{14},x_{23},x_{24},x_{34})=(1,2,1,1,2,3)", font_size=36)
    xm.move_to(np.array([0, 2.5, 0]))
    chk = Tex(r"x_{12}x_{34}-x_{13}x_{24}+x_{14}x_{23}=3-4+1=0", font_size=36).set_color(POS_COLOR)
    chk.move_to(np.array([0, 1.75, 0]))
    rule = Tex(r"I=(1,2),\quad x_{ji}=-x_{ij},\quad x_{ii}=0", font_size=32).set_color(MUTED_COLOR)
    rule.move_to(np.array([0, 1.0, 0]))
    r1 = Tex(row_tex(1), font_size=32).move_to(np.array([0, 0.25, 0]))
    r2 = Tex(row_tex(2), font_size=32).move_to(np.array([0, -0.45, 0]))
    bmat = MatrixMob(B, font_size=36, h_buff=0.75, v_buff=0.55)
    bm = VGroup(Tex("B=", font_size=40), bmat).arrange(RIGHT, buff=0.2).move_to(np.array([-3.9, -1.85, 0]))
    minors = Tex(r"p_{ij}(B):\quad1,2,1,1,2,3", font_size=34).set_color(POS_COLOR)
    minors.move_to(np.array([2.5, -1.45, 0]))
    ker = Tex(r"\ker B=\langle(1,-2,1,0),(2,-1,0,1)\rangle", font_size=34).move_to(np.array([2.5, -2.3, 0]))
    for m in (xm, chk, rule, r1, r2):
        fit(m, 12.6)
    for m in (minors, ker):
        fit(m, 7.4)
    assert_in_frame(xm, chk, rule, r1, r2, bm, minors, ker)
    for a, b in ((xm, chk), (chk, rule), (rule, r1), (r1, r2), (r2, bm), (r2, minors), (minors, ker), (bm, ker),
                 (bm, minors)):
        assert_apart(a, b, 0.1)

    scene.say("練習 2：倒過來，給六個數，找回那個平面", wait=SLOW * 0.3)
    scene.play(Write(xm), run_time=1.4)
    scene.play(FadeIn(chk, shift=0.2 * DOWN), run_time=0.9)
    scene.say("先驗關係：", "$3-4+1=0$", "，確實是 ", "$Gr(2,4)$", " 的點", wait=SLOW * 0.8)
    scene.play(FadeIn(rule), run_time=0.8)
    scene.say("式 (2)：", "$x_{12}=1\\neq0$", "，把 ", "$I=(1,2)$", " 的第 ", "$s$", " 個數換成 ", "$t$",
              wait=SLOW * 0.8)
    scene.say("下標順序反過來要變號，下標重複就是 0", wait=SLOW * 0.7)
    scene.play(FadeIn(r1, shift=0.2 * RIGHT), run_time=0.9)
    scene.say("第 1 列：換掉 1，", "$x_{32}=-x_{23}=-1$", "、", "$x_{42}=-x_{24}=-2$", wait=SLOW * 0.9)
    scene.play(FadeIn(r2, shift=0.2 * RIGHT), run_time=0.9)
    scene.say("第 2 列：換掉 2，", "$x_{11}=0$", wait=SLOW * 0.6)
    scene.play(TransformFromCopy(VGroup(r1, r2), bm), run_time=1.3)
    scene.say("兩列合起來就是 ", "$B$", wait=SLOW * 0.5)
    scene.play(FadeIn(minors, shift=0.2 * LEFT), run_time=0.9)
    scene.say("驗算：", "$B$", " 的六個子式正好是 ", "$1,2,1,1,2,3$", wait=SLOW * 0.8)
    scene.play(FadeIn(ker, shift=0.2 * LEFT), run_time=0.9)
    scene.say("平面本身：", "$\\ker B$", " 由這兩個向量張成", wait=SLOW * 0.8)
    scene.play(Indicate(xm, color=POS_COLOR), Indicate(ker, color=POS_COLOR), run_time=1.2)
    scene.say("子空間 ", "$\\leftrightarrow$", " 滿足二次關係的一點", wait=SLOW * 1.2)


class SceneF46Plucker(ChuScene):
    def construct(self):
        self.show_header("六個數認出一個平面：Plücker 座標")
        check_math()
        part_minors(self)
        self.clear_stage()
        part_relation(self)
        self.clear_stage()
        part_inverse(self)
        self.wait(1.0)
