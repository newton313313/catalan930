"""
Scene F48 —— 數星星：Grassmannian 的 Schubert 胞腔（Fulton §9.4，書 p.145–148）
執行（在 codes/ 內）：manimgl scenes/sceneF48_grass_cells.py SceneF48GrassCells

Gr(2,4)：列梯形矩陣第 i 列的 1 在第 n+i−λ_i 行（n=2），星號數 4−|λ| = 4,3,2,2,1,0；
[4 choose 2]_q = 1+q+2q²+q³+q⁴，q=1 → 6，q=2 → 35 = F_2^4 裡暴力數的平面數；
Ω_λ = {V : dim(V∩F_{n+i−λ_i}) ≥ i}，餘維 |λ|，包含 μ ⊇ λ 的胞腔（練習 13）；書上 r=5、n=7、λ=(5,3,2,2,1)：22 顆星。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.rep_draw import OP_COLOR, POS_COLOR
from utils.scene_base import ChuScene
from utils.schubert import count_subspaces_F2, gaussian_binomial, grass_cell_pattern
from utils.schubert_draw import STAR_COLOR, BoxDiagramMob, CellMatrixMob
from utils.styles import MUTED_COLOR, mixed, zh

R, N = 2, 2
LAMS = [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1), (2, 2)]
BIG_LAM, BIG_R, BIG_N = (5, 3, 2, 2, 1), 5, 7
OMEGAS = [((1, 0), r"\Omega_1:\ \dim(V\cap F_2)\ge1", OP_COLOR),
          ((2, 0), r"\Omega_2:\ F_1\subset V", PINK),
          ((1, 1), r"\Omega_{11}:\ V\subset F_3", TEAL_B)]
SLOW = 3.8


def stars(pattern):
    return sum(row.count("*") for row in pattern)


def contains(mu, lam):
    return all(m >= l for m, l in zip(mu, lam))


def lam_tex(lam):
    return r"\lambda=(%s)" % ",".join(map(str, lam))


def fit(mob, w):
    if mob.get_width() > w:
        mob.set_width(w)
    return mob


def check_math():
    pats = [grass_cell_pattern(l, R, N) for l in LAMS]
    assert [stars(p) for p in pats] == [4, 3, 2, 2, 1, 0] == [R * N - sum(l) for l in LAMS]
    for l, p in zip(LAMS, pats):
        assert [row.index("1") + 1 for row in p] == [N + i + 1 - l[i] for i in range(R)]
    p10 = grass_cell_pattern((1, 0), R, N)
    assert p10 == [["*", "1", "0", "0"], ["*", "0", "*", "1"]]
    assert [row.count("*") for row in p10] == [1, 2] == [N - 1, N - 0]
    gb = gaussian_binomial(4, 2)
    assert gb == [1, 1, 2, 1, 1] and sum(gb) == 6 == len(LAMS)
    assert [2 ** stars(p) for p in pats] == [16, 8, 4, 4, 2, 1]
    assert sum(c * 2 ** k for k, c in enumerate(gb)) == 35 == count_subspaces_F2(4, 2) == sum(2 ** stars(p) for p in pats)
    big = grass_cell_pattern(BIG_LAM, BIG_R, BIG_N)
    assert [row.count("*") for row in big] == [2, 4, 5, 5, 6] == [BIG_N - l for l in BIG_LAM]
    assert stars(big) == 22 == BIG_R * BIG_N - sum(BIG_LAM) == 35 - 13
    expect = {(1, 0): {(1, 0), (2, 0), (1, 1), (2, 1), (2, 2)}, (2, 0): {(2, 0), (2, 1), (2, 2)},
              (1, 1): {(1, 1), (2, 1), (2, 2)}}
    for lam, _, _ in OMEGAS:
        assert {mu for mu in LAMS if contains(mu, lam)} == expect[lam]
        assert [N + i + 1 - lam[i] for i in range(R)] == {(1, 0): [2, 4], (2, 0): [1, 4], (1, 1): [2, 3]}[lam]
    assert 2 + 2 - 3 >= 1                         # V ⊂ F_3 自動和 F_2 相交：Ω_11 只剩 V ⊂ F_3


# ---------------------------------------------------------------- 1. 一個胞腔放大看
def part_echelon(scene):
    flag = mixed("固定一個旗 ", "$F_1\\subset F_2\\subset F_3\\subset\\mathbb C^4$", font_size=28)
    flag.move_to(np.array([0, 2.55, 0]))
    mat = CellMatrixMob(grass_cell_pattern((1, 0), R, N), cs=0.75).move_to(np.array([-2.6, 0.75, 0]))
    cols = VGroup(*[Tex(str(j + 1), font_size=26).set_color(MUTED_COLOR).next_to(mat.cell(0, j), UP, buff=0.35)
                    for j in range(4)])
    rows = VGroup(*[Tex("i=%d" % (i + 1), font_size=28).set_color(MUTED_COLOR).next_to(mat, LEFT, buff=0.35)
                    .set_y(mat.cell(i, 0).get_y()) for i in range(2)])
    box = BoxDiagramMob((1, 0), R, N, cs=0.7).move_to(np.array([3.4, 0.75, 0]))
    blab = Tex(lam_tex((1, 0)), font_size=32).next_to(box, UP, buff=0.3)
    rule = mixed("第 ", "$i$", " 列的 1 在第 ", "$n+i-\\lambda_i$", " 行（", "$n=2$", "）", font_size=28)
    rule.move_to(np.array([0, -1.2, 0]))
    calc = Tex(r"i=1:\ 2+1-1=2,\qquad i=2:\ 2+2-0=4", font_size=32).set_color(OP_COLOR)
    calc.move_to(np.array([0, -2.05, 0]))
    assert_in_frame(flag, mat, cols, rows, box, blab, rule, calc)
    assert_apart(flag, cols, 0.1)
    assert_apart(VGroup(mat, rows), VGroup(box, blab), 0.5)
    assert_apart(mat, rule, 0.2)
    assert_apart(rule, calc, 0.1)

    scene.say("問：4 維的 ", "$Gr(2,4)$", " 能不能切成一塊塊「平地」", "$\\mathbb C^k$", "？", wait=SLOW * 0.8)
    scene.play(FadeIn(flag, shift=0.2 * DOWN), run_time=0.8)
    scene.say("先固定一個旗；每個 ", "$V$", " 都有唯一的列梯形矩陣", wait=SLOW * 0.5)
    scene.play(FadeIn(mat), FadeIn(cols), FadeIn(rows), run_time=1.0)
    scene.play(Indicate(mat.ones(), color=OP_COLOR), run_time=1.0)
    scene.say("每列有一個 1（黃）；1 的右邊、1 的下方都是 0", wait=SLOW * 0.8)
    scene.play(LaggedStart(*[Flash(s, color=STAR_COLOR) for s in mat.stars()], lag_ratio=0.3), run_time=1.2)
    scene.say("其餘的位置是星號：可以填任何複數", wait=SLOW * 0.7)
    scene.play(FadeIn(box), FadeIn(blab), run_time=0.9)
    scene.say("1 的位置由方框 ", "$2\\times2$", " 裡的 Young 圖 ", "$\\lambda$", " 決定", wait=SLOW * 0.3)
    scene.play(FadeIn(rule, shift=0.2 * UP), run_time=0.8)
    scene.play(Write(calc), run_time=1.2)
    scene.say("$\\lambda=(1,0)$", "：第 1 列的 1 在第 2 行，第 2 列的 1 在第 4 行", wait=SLOW * 0.8)
    scene.say("每列的星號數是 ", "$n-\\lambda_i$", "：這裡 ", "$1+2=3=4-|\\lambda|$", wait=SLOW * 0.8)
    scene.say("三顆星：這個胞腔就是 ", "$\\mathbb C^3$", wait=SLOW * 0.8)


# ---------------------------------------------------------------- 2. 六個胞腔、數點
def part_six(scene):
    xs, ys = (-4.4, 0.0, 4.4), (1.6, -0.6)
    panels, dims, pows = [], [], []
    for k, lam in enumerate(LAMS):
        c = np.array([xs[k % 3], ys[k // 3], 0])
        mat = CellMatrixMob(grass_cell_pattern(lam, R, N), cs=0.42).move_to(c + 0.55 * LEFT)
        box = BoxDiagramMob(lam, R, N, cs=0.3).move_to(c + 1.25 * RIGHT)
        lab = Tex(lam_tex(lam), font_size=28).move_to(c + 0.85 * UP)
        s = R * N - sum(lam)
        d = Tex(r"\dim=%d" % s, font_size=28).set_color(STAR_COLOR).move_to(c + 0.8 * DOWN)
        p = Tex(r"2^%d=%d" % (s, 2 ** s), font_size=28).set_color(POS_COLOR).move_to(d)
        panels.append(VGroup(lab, mat, box))
        dims.append(d)
        pows.append(p)
    qb = Tex(r"\begin{bmatrix}4\\2\end{bmatrix}_q=1+q+2q^2+q^3+q^4", font_size=36).move_to(np.array([0, -2.35, 0]))
    q2 = Tex(r"q=2:\quad16+8+4+4+2+1=35", font_size=34).set_color(POS_COLOR).move_to(np.array([-2.6, -2.35, 0]))
    brute = mixed("暴力數 ", "$\\mathbb F_2^4$", " 裡的平面：", "$35$", font_size=28).move_to(np.array([3.4, -2.35, 0]))
    assert_in_frame(*panels, *dims, *pows, qb, q2, brute)
    for k in range(6):
        if k % 3 < 2:
            assert_apart(VGroup(panels[k], dims[k]), VGroup(panels[k + 1], dims[k + 1]), 0.4)
        if k < 3:
            assert_apart(VGroup(panels[k], dims[k]), VGroup(panels[k + 3], dims[k + 3]), 0.1)
    assert_apart(VGroup(*panels[3:], *dims[3:]), qb, 0.15)
    assert_apart(q2, brute, 0.3)

    scene.say("方框 ", "$2\\times2$", " 裡的 Young 圖共有 6 個：6 個胞腔並排", wait=SLOW * 0.2)
    for k in range(6):
        scene.play(FadeIn(panels[k], shift=0.15 * UP), run_time=0.6)
    scene.wait(SLOW * 0.4)
    scene.say("數星星：星號數 ", "$4-|\\lambda|$", " 就是胞腔的維數", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(d) for d in dims], lag_ratio=0.2), run_time=1.4)
    scene.say("$4,3,2,2,1,0$", "：", "$Gr(2,4)=\\mathbb C^4\\sqcup\\mathbb C^3\\sqcup\\mathbb C^2\\sqcup\\mathbb C^2\\sqcup\\mathbb C^1\\sqcup\\mathbb C^0$",
              wait=SLOW * 1.0)
    scene.play(Write(qb), run_time=1.4)
    scene.say("每個胞腔記成 ", "$q^{\\dim}$", "，加起來是 Gauss 二項式", wait=SLOW * 0.8)
    scene.say("$q=1$", "：", "$1+1+2+1+1=6$", "，正好 6 個胞腔", wait=SLOW * 0.8)
    scene.say("$q=2$", "：在有限體 ", "$\\mathbb F_2$", " 上，", "$\\mathbb C^k$", " 換成 ", "$\\mathbb F_2^k$", "，有 ",
              "$2^k$", " 個點", wait=SLOW * 0.2)
    scene.play(*[ReplacementTransform(d, p) for d, p in zip(dims, pows)], run_time=1.2)
    scene.play(FadeOut(qb), FadeIn(q2, shift=0.2 * UP), run_time=0.9)
    scene.say("$16+8+4+4+2+1=35$", wait=SLOW * 0.6)
    scene.play(FadeIn(brute, shift=0.2 * LEFT), run_time=0.9)
    scene.say("電腦把 ", "$\\mathbb F_2^4$", " 裡的平面一個個列出來：也是 35 個", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 3. Schubert 簇：胞腔的閉包
def part_varieties(scene):
    om = Tex(r"\Omega_\lambda=\{V:\dim(V\cap F_{n+i-\lambda_i})\ge i\}", font_size=40).move_to(np.array([0, 2.5, 0]))
    pos = {(0, 0): (-5.6, 0.4), (1, 0): (-4.0, 0.4), (2, 0): (-2.4, 1.2), (1, 1): (-2.4, -0.4),
           (2, 1): (-0.8, 0.4), (2, 2): (0.8, 0.4)}
    nodes = {lam: BoxDiagramMob(lam, R, N, cs=0.35).move_to(np.array([x, y, 0])) for lam, (x, y) in pos.items()}
    edges = VGroup(*[Line(nodes[a].get_right(), nodes[b].get_left(), buff=0.12).set_stroke(GREY_B, 2)
                     for a, b in (((0, 0), (1, 0)), ((1, 0), (2, 0)), ((1, 0), (1, 1)), ((2, 0), (2, 1)),
                                  ((1, 1), (2, 1)), ((2, 1), (2, 2)))])
    codim = VGroup(*[Tex(str(k), font_size=26).set_color(MUTED_COLOR).move_to(np.array([x, -1.35, 0]))
                     for k, x in enumerate((-5.6, -4.0, -2.4, -0.8, 0.8))])
    clab = mixed("餘維數 ", "$|\\lambda|$", font_size=22, color=MUTED_COLOR).move_to(np.array([-2.4, -1.85, 0]))
    conds = [Tex(t, font_size=30).set_color(c).move_to(np.array([4.3, 1.1 - 0.85 * k, 0]))
             for k, (_, t, c) in enumerate(OMEGAS)]
    for t in conds:
        fit(t, 4.3)
    rects = [VGroup(*[SurroundingRectangle(nodes[mu], buff=0.08, color=c) for mu in LAMS if contains(mu, lam)])
             for lam, _, c in OMEGAS]
    graph = VGroup(*nodes.values(), edges, codim, clab)
    assert_in_frame(om, graph, *conds, *rects)
    assert_apart(om, graph, 0.15)
    assert_apart(VGroup(*rects[0]), VGroup(*conds), 0.4)
    for a, b in zip(conds, conds[1:]):
        assert_apart(a, b, 0.1)

    scene.say("Schubert 簇 ", "$\\Omega_\\lambda$", "：用 ", "$V$", " 和固定旗交出的維數來定義", wait=SLOW * 0.2)
    scene.play(Write(om), run_time=1.4)
    scene.wait(SLOW * 0.5)
    scene.play(LaggedStart(*[FadeIn(nodes[l]) for l in LAMS], lag_ratio=0.2), ShowCreation(edges), run_time=1.6)
    scene.play(FadeIn(codim), FadeIn(clab), run_time=0.7)
    scene.say("它是胞腔 ", "$\\Omega^\\circ_\\lambda$", " 的閉包，餘維數 ", "$|\\lambda|$", wait=SLOW * 0.8)
    intro = [("$\\Omega_1$", "：", "$V$", " 和 ", "$F_2$", " 至少交出一條直線，只有一個條件"),
             ("$\\Omega_2$", "：", "$V$", " 必須包含 ", "$F_1$"),
             ("$\\Omega_{11}$", "：", "$V$", " 落在 ", "$F_3$", " 裡（自動和 ", "$F_2$", " 相交）")]
    cover = [("$\\Omega_1$", " 包含所有 ", "$\\mu\\supseteq(1)$", " 的胞腔：5 個（練習 13）"),
             ("$\\Omega_2$", " 包含 ", "$(2)$", "、", "$(2,1)$", "、", "$(2,2)$", " 三個胞腔"),
             ("$\\Omega_{11}$", " 包含 ", "$(1,1)$", "、", "$(2,1)$", "、", "$(2,2)$", " 三個胞腔")]
    for k in range(len(OMEGAS)):
        scene.play(FadeIn(conds[k], shift=0.2 * LEFT), run_time=0.8)
        scene.say(*intro[k], wait=SLOW * 0.6)
        scene.play(ShowCreation(rects[k]), run_time=0.9)
        scene.say(*cover[k], wait=SLOW * 0.7)
        scene.play(FadeOut(rects[k]), run_time=0.5)
    scene.say("Young 圖越大，條件越多，Schubert 簇越小", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 4. 書上的大例子
def part_big(scene):
    head = Tex(r"r=5,\quad n=7,\quad\lambda=(5,3,2,2,1)", font_size=36).move_to(np.array([0, 2.5, 0]))
    mat = CellMatrixMob(grass_cell_pattern(BIG_LAM, BIG_R, BIG_N), cs=0.42).move_to(np.array([-2.4, 0.5, 0]))
    cnt = VGroup(*[Tex(str(BIG_N - l), font_size=30).set_color(STAR_COLOR)
                   .move_to(np.array([mat.get_right()[0] + 0.45, mat.cell(i, 0).get_y(), 0]))
                   for i, l in enumerate(BIG_LAM)])
    box = BoxDiagramMob(BIG_LAM, BIG_R, BIG_N, cs=0.3).move_to(np.array([4.3, 0.5, 0]))
    total = Tex(r"2+4+5+5+6=22=35-13", font_size=38).set_color(POS_COLOR).move_to(np.array([0, -1.75, 0]))
    assert_in_frame(head, mat, cnt, box, total)
    assert_apart(head, mat, 0.2)
    assert_apart(VGroup(mat, cnt), box, 0.4)
    assert_apart(mat, total, 0.3)

    scene.say("書上的大例子：", "$Gr$", " 的方框是 ", "$5\\times7$", wait=SLOW * 0.2)
    scene.play(FadeIn(head), FadeIn(mat), FadeIn(box), run_time=1.2)
    scene.say("每列的星號數 ", "$n-\\lambda_i$", "：", "$2,4,5,5,6$", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(c, shift=0.2 * LEFT) for c in cnt], lag_ratio=0.2), run_time=1.2)
    scene.wait(SLOW * 0.4)
    scene.play(Write(total), run_time=1.2)
    scene.say("共 22 顆星 ", "$=5\\cdot7-|\\lambda|$", "：維數 22、餘維數 13", wait=SLOW * 0.9)
    scene.play(Indicate(mat.stars(), color=STAR_COLOR), Indicate(box.cells, color=OP_COLOR), run_time=1.4)
    scene.say("星號＝自由度，方框裡的 Young 圖＝胞腔", wait=SLOW * 1.2)


class SceneF48GrassCells(ChuScene):
    def construct(self):
        self.show_header("數星星：Grassmannian 的 Schubert 胞腔")
        check_math()
        part_echelon(self)
        self.clear_stage()
        part_six(self)
        self.clear_stage()
        part_varieties(self)
        self.clear_stage()
        part_big(self)
        self.wait(1.0)
