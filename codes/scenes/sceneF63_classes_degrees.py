"""
Scene F63 —— 交點就是乘法：子簇的類與次數（Fulton §B.3，書 p.219–222；§B.1 的性質；練習 8）
執行（在 codes/ 內）：manimgl scenes/sceneF63_classes_degrees.py SceneF63ClassesDegrees
"""
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import plucker_degree
from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.scene_base import ChuScene
from utils.schubert import box_product, plucker
from utils.schubert_draw import BoxDiagramMob
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import standard_tableaux

SLOW = 8.0
OK = "#7CE38B"
H_COLOR, C_COLOR = TEAL, PINK
LEFT_C, RIGHT_C = np.array([-3.5, 0.45, 0]), np.array([3.5, 0.45, 0])
ELL = (1.7, 1.0)                       # 圓錐曲線 x²/a² + y²/b² = 1（相對座標）
LINE = (0.3, 0.35)                     # 直線 y = 0.3x + 0.35
ELL_A, ELL_B = (1.75, 0.85), (0.85, 1.6)
GRASS = [(2, 4), (2, 5), (3, 6)]
SYT22 = [((1, 2), (3, 4)), ((1, 3), (2, 4))]


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def line_conic_points():
    (a, b), (m, c) = ELL, LINE
    xs = np.roots([1 / a ** 2 + m ** 2 / b ** 2, 2 * m * c / b ** 2, c ** 2 / b ** 2 - 1])
    return [np.array([x.real, m * x.real + c, 0]) for x in xs if abs(x.imag) < 1e-9]


def conic_conic_points():
    (a1, b1), (a2, b2) = ELL_A, ELL_B
    M = np.array([[1 / a1 ** 2, 1 / b1 ** 2], [1 / a2 ** 2, 1 / b2 ** 2]])
    X2, Y2 = np.linalg.solve(M, np.ones(2))
    return [np.array([sx * np.sqrt(X2), sy * np.sqrt(Y2), 0]) for sx in (1, -1) for sy in (1, -1)]


def sigma_powers(k):
    out, cur = [], {(1,): 1}
    out.append(cur)
    for _ in range(k - 1):
        nxt = {}
        for lam, c in cur.items():
            for nu, d in box_product(lam, (1,), 2, 2).items():
                nxt[nu] = nxt.get(nu, 0) + c * d
        cur = {tuple(x for x in nu if x): c for nu, c in nxt.items()}
        out.append(cur)
    return out


def trunc_mul(f, g):
    """Z[h1,h2]/(h1², h2²) 裡的乘法。"""
    out = {}
    for (a, b), c in f.items():
        for (p, q), d in g.items():
            if a + p < 2 and b + q < 2:
                out[(a + p, b + q)] = out.get((a + p, b + q), 0) + c * d
    return out


def check_math():
    (a, b) = ELL
    pts = line_conic_points()
    assert len(pts) == 2 == 1 * 2
    assert all(abs(p[0] ** 2 / a ** 2 + p[1] ** 2 / b ** 2 - 1) < 1e-9 for p in pts)
    q = conic_conic_points()
    assert len(q) == 4 == 2 * 2
    for (a1, b1) in (ELL_A, ELL_B):
        assert all(abs(p[0] ** 2 / a1 ** 2 + p[1] ** 2 / b1 ** 2 - 1) < 1e-9 for p in q)
    pw = sigma_powers(4)
    assert pw[1] == {(2,): 1, (1, 1): 1} and pw[2] == {(2, 1): 2} and pw[3] == {(2, 2): 2}
    assert sorted(standard_tableaux((2, 2))) == sorted(SYT22)
    assert [plucker_degree(r, m) for r, m in GRASS] == [2, 5, 42]
    assert [len(standard_tableaux((m - r,) * r)) for r, m in GRASS] == [2, 5, 42]
    assert [comb(m, r) - 1 for r, m in GRASS] == [5, 9, 19] and [r * (m - r) for r, m in GRASS] == [4, 6, 9]
    x = plucker([[1, 2, 0, 1], [0, 1, 3, 2]])
    assert x[(1, 2)] * x[(3, 4)] - x[(1, 3)] * x[(2, 4)] + x[(1, 4)] * x[(2, 3)] == 0
    h = {(1, 0): 1, (0, 1): 1}
    assert trunc_mul(h, h) == {(1, 1): 2}                                    # (h1+h2)^2 = 2 h1 h2
    for (p0, p1), (r0, r1) in (((1, 2), (3, 5)), ((2, -1), (4, 7))):          # Segre 的像在 xw = yz 上
        X, Y, Z, W = p0 * r0, p0 * r1, p1 * r0, p1 * r1
        assert X * W == Y * Z


def region(center, w=6.2, h=3.7):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.2).set_stroke(GREY_C, 2).set_fill(GREY_E, 0.25)
    return r.move_to(center)


# ---------------------------------------------------------------- 1. 交點＝乘積
def part_bezout(scene):
    top = tex(r"H^*(\mathbb P^2)=\mathbb Z[h]/(h^3),\qquad h^2=[\mathrm{pt}]", 34).move_to(np.array([0, 2.85, 0]))
    r1, r2 = region(LEFT_C), region(RIGHT_C)
    (a, b), (m, c) = ELL, LINE
    conic = Ellipse(width=2 * a, height=2 * b).set_stroke(C_COLOR, 4).move_to(LEFT_C)
    line = Line(LEFT_C + np.array([-2.8, -2.8 * m + c, 0]), LEFT_C + np.array([2.8, 2.8 * m + c, 0])).set_stroke(H_COLOR, 4)
    dots1 = VGroup(*[Dot(LEFT_C + p, radius=0.09).set_color(YELLOW) for p in line_conic_points()])
    lh = tex("h", 32, H_COLOR).next_to(line.get_end(), UP, buff=0.12)
    lc = tex("2h", 32, C_COLOR).move_to(LEFT_C + np.array([0.0, -b - 0.35, 0]))
    e1 = Ellipse(width=2 * ELL_A[0], height=2 * ELL_A[1]).set_stroke(C_COLOR, 4).move_to(RIGHT_C)
    e2 = Ellipse(width=2 * ELL_B[0], height=2 * ELL_B[1]).set_stroke(BLUE_B, 4).move_to(RIGHT_C)
    dots2 = VGroup(*[Dot(RIGHT_C + p, radius=0.09).set_color(YELLOW) for p in conic_conic_points()])
    f1 = mixed(r"$h\cdot 2h=2h^2=2$", " 個點", font_size=28).move_to(np.array([-3.5, -1.95, 0]))
    f2 = mixed(r"$2h\cdot 2h=4h^2=4$", " 個點", font_size=28).move_to(np.array([3.5, -1.95, 0]))
    bez = mixed("Bézout：", "$d$", " 次與 ", "$e$", " 次曲線交 ", "$de$", " 點", font_size=28, color=OK)
    bez.move_to(np.array([0, -2.62, 0]))
    assert_in_frame(top, r1, r2, line, lh, lc, f1, f2, bez)
    assert_apart(top, VGroup(r1, r2), 0.1)
    assert_apart(r1, r2, 0.3)
    assert_apart(VGroup(r1, r2), VGroup(f1, f2), 0.1)
    assert_apart(VGroup(f1, f2), bez, 0.1)

    scene.say("問：直線和圓錐曲線交幾點？平面裡兩條曲線呢？", wait=SLOW * 0.5)
    scene.play(FadeIn(r1), FadeIn(r2), run_time=0.7)
    scene.play(ShowCreation(conic), run_time=1.0)
    scene.play(ShowCreation(line), run_time=0.8)
    scene.play(LaggedStartMap(FadeIn, dots1, scale=2.0, lag_ratio=0.4), run_time=0.9)
    scene.say("子簇 ", "$V$", " 給出上同調裡的類 ", "$[V]$", "：直線的類叫 ", "$h$", wait=SLOW * 0.3)
    scene.play(Write(top), run_time=1.2)
    scene.play(FadeIn(lh), FadeIn(lc), run_time=0.7)
    scene.say("圓錐曲線是 2 次：", r"$[\text{conic}]=2h$", wait=SLOW * 0.3)
    scene.say("性質 (9)：橫截相交時，", r"$[V]\cdot[W]$", " 就是交點的類", wait=SLOW * 0.4)
    scene.play(Write(f1), run_time=1.0)
    scene.play(Indicate(dots1, color=YELLOW, scale_factor=1.6), run_time=0.9)
    scene.say(r"$h\cdot 2h=2h^2$", "：兩個點", wait=SLOW * 0.3)
    scene.play(ShowCreation(e1), ShowCreation(e2), run_time=1.2)
    scene.play(LaggedStartMap(FadeIn, dots2, scale=2.0, lag_ratio=0.3), run_time=1.0)
    scene.play(Write(f2), run_time=1.0)
    scene.say("兩條圓錐曲線：", r"$2h\cdot 2h=4h^2$", "，四個點", wait=SLOW * 0.4)
    scene.play(FadeIn(bez, shift=0.2 * UP), run_time=0.7)
    scene.say("一般地 ", r"$dh\cdot eh=de\,h^2$", "：Bézout 定理變成一行乘法", wait=SLOW * 0.6)


# ---------------------------------------------------------------- 2. 次數；Grassmannian
def part_degree(scene):
    defn = tex(r"V\subset\mathbb P^N,\ \dim V=k:\qquad \deg V=[V]\cdot h^{k}", 36, YELLOW).move_to(np.array([0, 2.75, 0]))
    emb = tex(r"Gr(2,4)\subset\mathbb P^5,\qquad h\mapsto\sigma_1", 34).move_to(np.array([-3.2, 1.75, 0]))
    pw = sigma_powers(4)
    chain = VGroup(tex(r"\sigma_1^2=\sigma_2+\sigma_{11}", 34), tex(r"\sigma_1^3=2\sigma_{21}", 34),
                   tex(r"\sigma_1^4=2\sigma_{22}=2\,[\mathrm{pt}]", 34, OK))
    chain.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(np.array([-3.4, 0.0, 0]))
    syt = VGroup(*[tableau_mob(t, cs=0.55) for t in SYT22]).arrange(RIGHT, buff=0.6).move_to(np.array([3.4, 0.3, 0]))
    sytl = zh("2×2 的標準表：2 張", font_size=26, color=MUTED_COLOR).next_to(syt, UP, buff=0.3)
    rel = tex(r"p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0", 34, C_COLOR).move_to(np.array([0, -2.1, 0]))
    assert_in_frame(defn, emb, chain, syt, sytl, rel)
    assert_apart(defn, VGroup(emb, sytl), 0.15)
    assert_apart(emb, chain, 0.15)
    assert_apart(chain, syt, 0.4)
    assert_apart(VGroup(chain, syt), rel, 0.2)
    assert pw[3] == {(2, 2): 2}

    scene.say("次數：", r"$V\subset\mathbb P^N$", " 和 ", "$k$", " 個一般的超平面交幾點", wait=SLOW * 0.3)
    scene.play(Write(defn), run_time=1.3)
    scene.say("例：圓錐曲線 ", r"$2h\cdot h=2$", "，次數 2", wait=SLOW * 0.4)
    scene.say(r"$Gr(2,4)$", " 用 Plücker 座標放進 ", r"$\mathbb P^5$", "：超平面的類拉回成 ", r"$\sigma_1$", wait=SLOW * 0.3)
    scene.play(FadeIn(emb), run_time=0.8)
    for k in range(3):
        scene.play(Write(chain[k]), run_time=0.9)
        scene.wait(0.4)
    scene.say("所以 ", r"$\deg Gr(2,4)=\sigma_1^4=2$", "（第 9 章的四條線）", wait=SLOW * 0.4)
    scene.play(FadeIn(syt), FadeIn(sytl), run_time=0.9)
    scene.say("係數 2 就是 ", r"$2\times2$", " 方框的標準表個數", wait=SLOW * 0.4)
    scene.play(Write(rel), run_time=1.2)
    scene.say("次數 2：正是一條二次方程——F46 的 Plücker 關係", wait=SLOW * 0.6)


def part_table(scene):
    cols = VGroup()
    for k, (r, m) in enumerate(GRASS):
        x = -4.4 + 4.4 * k
        box = BoxDiagramMob((m - r,) * r, r, m - r, cs=0.42).move_to(np.array([x, 1.35, 0]))
        name = tex(r"Gr(%d,%d)\subset\mathbb P^{%d}" % (r, m, comb(m, r) - 1), 32).move_to(np.array([x, -0.05, 0]))
        dim = tex(r"\dim=%d" % (r * (m - r)), 28, MUTED_COLOR).move_to(np.array([x, -0.65, 0]))
        deg = tex(r"\deg=%d" % plucker_degree(r, m), 40, OK).move_to(np.array([x, -1.45, 0]))
        cols.add(VGroup(box, name, dim, deg))
    note = zh("次數 ＝ 矩形的標準表個數（鉤長公式）", font_size=28, color=YELLOW).move_to(np.array([0, -2.45, 0]))
    assert_in_frame(cols, note)
    for a, b in zip(cols, cols[1:]):
        assert_apart(a, b, 0.3)
    assert_apart(cols, note, 0.15)

    scene.say("同樣的算法：", r"$\deg Gr(r,m)=\sigma_1^{r(m-r)}$", wait=SLOW * 0.3)
    for k in range(3):
        scene.play(FadeIn(cols[k][0]), FadeIn(cols[k][1]), FadeIn(cols[k][2]), run_time=0.8)
        scene.play(Write(cols[k][3]), run_time=0.7)
        if k == 1:
            scene.say(r"$Gr(2,5)$", "：次數 5", wait=SLOW * 0.2)
    scene.say(r"$Gr(3,6)$", "：次數 42", wait=SLOW * 0.2)
    scene.play(FadeIn(note), run_time=0.7)
    scene.say(r"$\sigma_1^{d}$", " 的係數數的是從空格子一格一格長成矩形的方法", wait=SLOW * 0.7)


# ---------------------------------------------------------------- 3. 練習 8：Segre
def saddle(center, n=7, s=1.5):
    def P(u, v):
        return center + np.array([0.9 * (u - v), 0.32 * (u + v) + 0.45 * u * v, 0])
    us = np.linspace(-s, s, n)
    fam1 = VGroup(*[Line(P(u, -s), P(u, s)) for u in us]).set_stroke(H_COLOR, 3)
    fam2 = VGroup(*[Line(P(-s, v), P(s, v)) for v in us]).set_stroke(C_COLOR, 3)
    return fam1, fam2


def part_segre(scene):
    mp = tex(r"\mathbb P^1\times\mathbb P^1\to\mathbb P^3,\quad ([a:b],[c:d])\mapsto[ac:ad:bc:bd]", 34)
    mp.move_to(np.array([0, 2.75, 0]))
    fam1, fam2 = saddle(np.array([-3.6, -0.4, 0]))
    l1 = tex(r"h_1", 30, H_COLOR).next_to(fam1[0].get_center(), DL, buff=0.12)
    l2 = tex(r"h_2", 30, C_COLOR).next_to(fam2[0].get_center(), DR, buff=0.12)
    eqs = VGroup(tex(r"x_0x_3=x_1x_2", 34, YELLOW),
                 tex(r"H^*=\mathbb Z[h_1,h_2]/(h_1^2,h_2^2)", 32),
                 tex(r"h\mapsto h_1+h_2", 32),
                 tex(r"(h_1+h_2)^2=h_1^2+2h_1h_2+h_2^2=2h_1h_2", 32),
                 tex(r"\deg=2", 40, OK))
    eqs.arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(np.array([2.6, -0.2, 0]))
    assert_in_frame(mp, fam1, fam2, l1, l2, eqs)
    assert_apart(mp, VGroup(fam1, fam2, l1, l2, eqs), 0.15)
    assert_apart(VGroup(fam1, fam2, l1, l2), eqs, 0.2)

    scene.say("練習 8：Segre 嵌入", wait=SLOW * 0.2)
    scene.play(Write(mp), run_time=1.4)
    scene.play(ShowCreation(fam1), ShowCreation(fam2), run_time=1.5)
    scene.play(FadeIn(l1), FadeIn(l2), run_time=0.6)
    scene.play(Write(eqs[0]), run_time=0.8)
    scene.say("像是一個二次曲面，上面有兩族直線", wait=SLOW * 0.4)
    scene.play(FadeIn(eqs[1]), run_time=0.8)
    scene.play(FadeIn(eqs[2]), run_time=0.7)
    scene.say("超平面的類拉回成 ", "$h_1+h_2$", wait=SLOW * 0.3)
    scene.play(Write(eqs[3]), run_time=1.3)
    scene.say(r"$h_1^2=h_2^2=0$", "，只剩 ", "$2h_1h_2$", wait=SLOW * 0.4)
    scene.play(Write(eqs[4]), run_time=0.8)
    scene.say("次數 2：又是二次曲面", wait=SLOW * 0.4)
    scene.say("收束：拓撲把「數交點」變成多項式乘法", wait=SLOW * 0.7)


class SceneF63ClassesDegrees(ChuScene):
    def construct(self):
        self.show_header("交點就是乘法：子簇的類")
        check_math()
        part_bezout(self)
        self.clear_stage()
        part_degree(self)
        self.clear_stage()
        part_table(self)
        self.clear_stage()
        part_segre(self)
        self.wait(1.0)
