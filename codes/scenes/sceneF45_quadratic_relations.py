"""
Scene F45 —— 同一條二次關係，三個身分（Fulton §8.4，書 p.124–126；§7.4；原大綱卡 F803）
執行（在 codes/ 內）：manimgl scenes/sceneF45_quadratic_relations.py SceneF45QuadraticRelations

三欄並排：Specht 的交換關係、Schur 模的關係、2×4 矩陣的 2×2 子式（都是「第 2 行頂端輪流和第 1 行交換」）；
A = [[1,2,0,1],[0,1,3,2]]：p12 p34 − p13 p24 + p14 p23 = −3 − 9 + 12 = 0；
二次關係生成的理想，預告第 9 章 Grassmannian；總結第 7–8 章。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

A = ((1, 2, 0, 1), (0, 1, 3, 2))
PAIRS = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
P_EXPECT = {(1, 2): 1, (1, 3): 3, (1, 4): 2, (2, 3): 6, (2, 4): 3, (3, 4): -3}
T21 = ((1, 3), (2,))
T22 = ((1, 3), (2, 4))
SLOW = 3.6


def exchange_top(T):
    """兩列的表：第 2 行頂端依序和第 1 行的每個數交換（行內上下位置不變）→ [S1, S2]。"""
    r0, r1 = T
    S1 = ((r0[1], r0[0]) + r0[2:], r1)
    S2 = ((r0[0], r1[0]) + r0[2:], (r0[1],) + r1[1:])
    return [S1, S2]


def columns(T):
    r0, r1 = T
    return [(r0[j], r1[j]) if j < len(r1) else (r0[j],) for j in range(len(r0))]


def minor(M, i, j):
    """第 i、j 行（column，1 起算）的 2×2 子式；i > j 時自動變號。"""
    return M[0][i - 1] * M[1][j - 1] - M[0][j - 1] * M[1][i - 1]


def D(M, T):
    """(2,2) 形的表 → 兩行各取一個子式再相乘。"""
    out = 1
    for c in columns(T):
        out *= minor(M, *c)
    return out


def polytabloid21(T):
    (a, c), (b,) = T
    out = {}
    for s, (x, y) in ((1, (a, b)), (-1, (b, a))):
        key = (frozenset((x, c)), frozenset((y,)))
        out[key] = out.get(key, 0) + s
    return {k: v for k, v in out.items() if v}


def vec_sum(*vs):
    out = {}
    for v in vs:
        for k, c in v.items():
            out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}


def num(x):
    return "(%d)" % x if x < 0 else str(x)


def wedge_tex(T):
    (a, c), (b,) = T
    return r"(v_%d\wedge v_%d)\otimes v_%d" % (a, b, c)


def p_tex(T):
    return "".join("p_{%d%d}" % c for c in columns(T))


def check_math():
    p = {ij: minor(A, *ij) for ij in PAIRS}
    assert p == P_EXPECT
    assert all(x >= 0 for r in A for x in r)                       # 子式展開不需加括號
    plk = p[1, 2] * p[3, 4] - p[1, 3] * p[2, 4] + p[1, 4] * p[2, 3]
    assert (p[1, 2] * p[3, 4], p[1, 3] * p[2, 4], p[1, 4] * p[2, 3]) == (-3, 9, 12) and plk == 0
    assert (A[0][2], A[1][3], A[0][3], A[1][2]) == (0, 2, 1, 3)       # 字幕 p34 = 0·2 − 1·3
    G = ((2, 1), (1, 3))                                               # 換列的基底：子式全乘 det G
    GA = tuple(tuple(sum(G[r][k] * A[k][c] for k in range(2)) for c in range(4)) for r in range(2))
    assert all(minor(GA, *ij) == 5 * p[ij] for ij in PAIRS) and G[0][0] * G[1][1] - G[0][1] * G[1][0] == 5
    S1, S2 = exchange_top(T22)
    assert (S1, S2) == (((3, 1), (2, 4)), ((1, 2), (3, 4)))
    assert [p_tex(T) for T in (T22, S1, S2)] == ["p_{12}p_{34}", "p_{32}p_{14}", "p_{13}p_{24}"]
    rng = np.random.default_rng(8)
    for M in [A] + [tuple(map(tuple, rng.integers(-5, 6, (2, 4)))) for _ in range(20)]:
        assert D(M, T22) == D(M, S1) + D(M, S2)                    # 交換關係對任何 2×4 矩陣都成立
        assert minor(M, 3, 2) == -minor(M, 2, 3)
    R1, R2 = exchange_top(T21)
    assert (R1, R2) == (((3, 1), (2,)), ((1, 2), (3,)))
    assert polytabloid21(T21) == vec_sum(polytabloid21(R1), polytabloid21(R2))
    assert [wedge_tex(T) for T in (T21, R1, R2)][0] == r"(v_1\wedge v_2)\otimes v_3"


# ---------------------------------------------------------------- 1. 三欄並排
def part_three(scene):
    xs = (-4.6, 0.0, 4.6)
    ys = (1.45, 0.35, -0.75)
    heads = [zh(t, font_size=24, color=MUTED_COLOR).move_to(np.array([x, 2.55, 0]))
             for t, x in zip(("Specht 模（第 7 章）", "Schur 模（第 8 章）", "2×4 矩陣的子式（§8.4）"), xs)]
    lead = ("", "=", "+")
    c1, c2, c3 = VGroup(), VGroup(), VGroup()
    for k, (T, U) in enumerate(zip([T21] + exchange_top(T21), [T22] + exchange_top(T22))):
        sgn = [Tex(lead[k], font_size=40, fill_color=POS_COLOR if k == 2 else WHITE)] if k else []
        r1 = VGroup(*sgn, tableau_mob(T, cs=0.42)).arrange(RIGHT, buff=0.25)
        r2 = Tex(lead[k] + wedge_tex(T), font_size=34)
        r3 = VGroup(*[s.copy() for s in sgn], tableau_mob(U, cs=0.42),
                    Tex(r"\to " + p_tex(U), font_size=36)).arrange(RIGHT, buff=0.25)
        for grp, r, x in ((c1, r1, xs[0]), (c2, r2, xs[1]), (c3, r3, xs[2])):
            r.move_to(np.array([x, ys[k], 0]))
            grp.add(r)
    sweep = [SurroundingRectangle(VGroup(c1[k], c2[k], c3[k]), buff=0.12, color=OP_COLOR) for k in range(3)]
    flip = Tex(r"p_{32}=-p_{23}", font_size=36, fill_color=NEG_COLOR).move_to(np.array([4.6, -1.65, 0]))
    plucker = Tex(r"p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0", font_size=42, fill_color=POS_COLOR)
    plucker.move_to(np.array([0, -2.45, 0]))
    assert_in_frame(*heads, c1, c2, c3, flip, plucker, *sweep)
    assert_apart(c1, c2, 0.3)
    assert_apart(c2, c3, 0.3)
    assert_apart(flip, plucker)

    scene.say("F39 的交換關係，已經出現兩次；這一幕看它的第三個身分", wait=SLOW * 0.3)
    scene.play(FadeIn(heads[0]), LaggedStart(*[FadeIn(r) for r in c1], lag_ratio=0.25), run_time=1.4)
    scene.say("第 7 章：第 2 行頂端的 3，輪流和第 1 行交換", wait=SLOW * 0.8)
    scene.say("F39 靠它把任何 ", "$e_T$", " 改寫成標準表的組合", wait=SLOW * 0.8)
    scene.play(FadeIn(heads[1]), LaggedStart(*[FadeIn(r) for r in c2], lag_ratio=0.25), run_time=1.4)
    scene.say("第 8 章：同一條，數字換成向量、行換成外積", wait=SLOW * 0.8)
    scene.say("第三個身分：", "$2\\times4$", " 矩陣，", "$p_{ij}$", " 是第 ", "$i,j$", " 行（column）的子式", wait=SLOW * 0.3)
    scene.play(FadeIn(heads[2]), LaggedStart(*[FadeIn(r) for r in c3], lag_ratio=0.25), run_time=1.4)
    scene.say("形狀 (2,2) 的表：每一行取一個子式再相乘", wait=SLOW * 1.0)
    scene.say("三欄一列一列對齊：同樣的交換、同樣的加號", wait=SLOW * 0.2)
    for k in range(3):
        scene.play(ShowCreation(sweep[k]), run_time=0.6)
        scene.wait(SLOW * 0.4)
        scene.play(FadeOut(sweep[k]), run_time=0.4)
    scene.say("把 ", "$p_{32}$", " 換成 ", "$-p_{23}$", "，移項整理", wait=SLOW * 0.3)
    scene.play(FadeIn(flip, shift=0.2 * UP), run_time=0.8)
    scene.play(Write(plucker), run_time=1.4)
    scene.say("這就是 Plücker 關係：三個身分，同一條二次式", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 2. 用整數矩陣驗算
def part_numbers(scene):
    p = {ij: minor(A, *ij) for ij in PAIRS}
    mat = MatrixMob(A, font_size=40, h_buff=0.8, v_buff=0.6)
    lab = Tex("A=", font_size=42)
    am = VGroup(lab, mat).arrange(RIGHT, buff=0.2).move_to(np.array([-4.2, 1.6, 0]))
    idx = VGroup(*[Tex(str(j + 1), font_size=26, fill_color=MUTED_COLOR).next_to(mat.col(j), UP, buff=0.3)
                   for j in range(4)])
    vals = {}
    for k, ij in enumerate(PAIRS):
        x = 1.2 + 2.6 * (k // 3)
        y = 2.1 - 0.75 * (k % 3)
        vals[ij] = Tex(r"p_{%d%d}=%d" % (ij[0], ij[1], p[ij]), font_size=36,
                       fill_color=NEG_COLOR if p[ij] < 0 else WHITE).move_to(np.array([x, y, 0]))
    detail_pos = np.array([-4.2, 0.1, 0])
    prods = []
    for k, (a, b) in enumerate((((1, 2), (3, 4)), ((1, 3), (2, 4)), ((1, 4), (2, 3)))):
        v = p[a] * p[b]
        t = Tex(r"p_{%d%d}p_{%d%d}=%s\cdot%s=%d" % (a + b + (num(p[a]), num(p[b]), v)), font_size=34)
        t.move_to(np.array([(-4.4, 0.0, 4.4)[k], -1.15, 0]))
        prods.append(t)
    vs = [p[1, 2] * p[3, 4], p[1, 3] * p[2, 4], p[1, 4] * p[2, 3]]
    total = Tex(r"p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=%d-%d+%d=%d" % (vs[0], vs[1], vs[2], vs[0] - vs[1] + vs[2]),
                font_size=40, fill_color=POS_COLOR).move_to(np.array([0, -2.3, 0]))
    assert_in_frame(am, idx, *vals.values(), *prods, total)
    assert_apart(prods[0], prods[1], 0.2)
    assert_apart(prods[1], prods[2], 0.2)
    assert_apart(am, VGroup(*vals.values()), 0.3)

    scene.say("用一個整數矩陣實際算一次", wait=SLOW * 0.3)
    scene.play(FadeIn(am), FadeIn(idx), run_time=1.0)
    scene.say("取兩行（column），算 ", "$2\\times2$", " 行列式，共 6 個", wait=SLOW * 0.2)
    for k, (i, j) in enumerate(PAIRS):
        rect = VGroup(*[SurroundingRectangle(mat.col(c - 1), buff=0.12, color=OP_COLOR) for c in (i, j)])
        det = Tex(r"p_{%d%d}=%d\cdot%d-%d\cdot%d" % (i, j, A[0][i - 1], A[1][j - 1], A[0][j - 1], A[1][i - 1]),
                  font_size=36, fill_color=OP_COLOR).move_to(detail_pos)
        rt = 0.8 if k < 2 else 0.5
        scene.play(ShowCreation(rect), FadeIn(det), run_time=rt)
        scene.play(TransformFromCopy(det, vals[(i, j)]), run_time=rt)
        scene.wait(SLOW * (0.4 if k < 2 else 0.15))
        scene.play(FadeOut(rect), FadeOut(det), run_time=0.4)
    scene.say("注意 ", "$p_{34}=0\\cdot2-1\\cdot3=-3$", " 是負的，乘的時候要帶著", wait=SLOW * 0.8)
    scene.say("三個乘積：", "$-3$", "、", "$9$", "、", "$12$", wait=SLOW * 0.2)
    for t in prods:
        scene.play(Write(t), run_time=1.0)
        scene.wait(SLOW * 0.3)
    scene.say("帶上正負號：", "$-3-9+12=0$", "，正好相消", wait=SLOW * 0.2)
    scene.play(Write(total), run_time=1.4)
    scene.play(Indicate(total, color=POS_COLOR), run_time=1.0)
    scene.say("換任何 ", "$2\\times4$", " 矩陣都是 0：這是子式之間的恆等式", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 3. 理想與 Grassmannian（預告）
def part_preview(scene):
    ring = Tex(r"\mathbb C[p_{12},p_{13},p_{14},p_{23},p_{24},p_{34}]\,/\,I", font_size=44).move_to(np.array([0, 1.9, 0]))
    ideal = mixed(r"$I$", "：由這些二次關係生成的理想", font_size=28).next_to(ring, DOWN, buff=0.45)
    arrow = Arrow(ideal.get_bottom(), ideal.get_bottom() + 1.1 * DOWN, buff=0.15).set_color(OP_COLOR)
    gr = mixed("第 9 章預告：Grassmannian（", r"$\mathbb C^4$", " 裡所有 2 維子空間）", font_size=28, color=OP_COLOR)
    gr.next_to(arrow, DOWN, buff=0.2)
    assert_in_frame(ring, ideal, arrow, gr)

    scene.say(r"$2\times4$", " 矩陣的兩列（row）張成 ", r"$\mathbb C^4$", " 裡的一個平面；六個子式記下這個平面",
              wait=SLOW * 1.5)
    scene.say("換一組基底張成同一個平面，六個子式只差同一個倍數（行列式）", wait=SLOW * 1.2)
    scene.play(Write(ring), run_time=1.4)
    scene.play(FadeIn(ideal, shift=0.2 * UP), run_time=0.8)
    scene.say("這些二次關係生成一個理想 ", "$I$", "：§8.4 用它描述子式之間的關係", wait=SLOW * 1.2)
    scene.play(GrowArrow(arrow), FadeIn(gr, shift=0.2 * DOWN), run_time=1.0)
    scene.say("第 9 章會把它們看成 Grassmannian 的方程（細節留到第 9 章）", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 4. 總結第 7–8 章
def part_summary(scene):
    lines = VGroup(
        mixed("第 7 章：", r"$S^\lambda$", "，基底＝標準表，", r"$\dim=f^\lambda$", font_size=28),
        mixed("第 8 章：", r"$E^\lambda$", "，基底＝半標準表，", r"$\dim=d_\lambda(m)$", "，",
              r"$\operatorname{Char}=s_\lambda$", font_size=28),
        mixed("橋：", r"$E^{\otimes n}\cong\bigoplus_\lambda E^\lambda\otimes S^\lambda$", font_size=28),
        mixed("貫穿兩章：同一條交換關係（二次關係）", font_size=28),
    ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(np.array([0.3, 0.1, 0]))
    marks = VGroup(*[Dot(radius=0.07, fill_color=OP_COLOR).next_to(l, LEFT, buff=0.3) for l in lines])
    assert_in_frame(lines, marks)

    scene.say("總結第 7–8 章", wait=SLOW * 0.3)
    for l, m in zip(lines, marks):
        scene.play(FadeIn(m), FadeIn(l, shift=0.2 * RIGHT), run_time=0.9)
        scene.wait(SLOW * 0.9)
    scene.say("同一張楊圖、同一條關係：管 ", "$S_n$", "、管 ", r"$GL_m$", "，也管 Grassmannian 的方程", wait=SLOW * 1.8)


class SceneF45QuadraticRelations(ChuScene):
    def construct(self):
        self.show_header("同一條二次關係，三個身分")
        check_math()
        part_three(self)
        self.clear_stage()
        part_numbers(self)
        self.clear_stage()
        part_preview(self)
        self.clear_stage()
        part_summary(self)
        self.wait(1.0)
