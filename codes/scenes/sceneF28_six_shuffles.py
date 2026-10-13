"""
Scene F28 —— 三張卡片、六種排列（Fulton 第 7 章章首與 §7.2 前導，書 p.83–86；原大綱卡 F700、F701）
執行（在 codes/ 內）：manimgl scenes/sceneF28_six_shuffles.py SceneF28SixShuffles

洗三張卡 → S_3 的六個元素（依循環型分三類）→ 卡片變成座標 t1,t2,t3，置換＝換座標（置換矩陣）
→ 共同變化（直線 Cz）與相對變化（零和平面 W）→ 穩定子空間、直和、不可約；Maschke（平均化投影）、Schur 一句
→ 預告：三個形狀、維度 1、2、1；兩個計數窗 3=1+2 與 6=1+2·2+1。
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import compose, cycle_type, load
from utils.rep_draw import OP_COLOR, POS_COLOR, MatrixMob, perm_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

S3 = load("character_S3")
SH = load("shape21")
SIX = [tuple(r["rows"][0] + r["rows"][1]) for r in SH["all_numberings"]]   # 六個編號攤平＝S_3 的六個一行記法
SWAP12, SWAP23 = (2, 1, 3), (1, 3, 2)
X0 = (4, 1, 1)
Z_COLOR, W_COLOR = TEAL, PURPLE_B
SHAPES = [((3,), "3", "平凡"), ((2, 1), "21", "零和平面"), ((1, 1, 1), "111", "sign")]

# 斜投影的「三維」座標：t1 往左下、t2 往右、t3 往上
O3 = np.array([-3.5, -0.6, 0.0])
E3 = [np.array([-0.62, -0.50, 0.0]), np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])]
UNIT = 0.55


def p3(x):
    return O3 + UNIT * sum(c * e for c, e in zip(x, E3))


def perm_matrix(p):
    """ρ(σ)：第 j 欄是 σ(t_j) = t_{σ(j)}。"""
    n = len(p)
    return [[1 if p[j] == i + 1 else 0 for j in range(n)] for i in range(n)]


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def permute_coords(p, x):
    """σ·(Σ x_i t_i) = Σ x_i t_{σ(i)}。"""
    y = [0] * len(x)
    for i, v in enumerate(x):
        y[p[i] - 1] = v
    return tuple(y)


def mean_split(x):
    m = sum(x) // len(x)
    assert m * len(x) == sum(x)
    return m, tuple(v - m for v in x)


def check_math():
    assert len(SIX) == 6 and len(set(SIX)) == 6
    by_type = Counter(cycle_type(p) for p in SIX)
    assert [by_type[tuple(t)] for t in S3["types"]] == S3["sizes"] == [1, 3, 2]
    assert permute_coords(SWAP12, X0) == (1, 4, 1)
    assert perm_matrix(SWAP12) == [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
    for s in SIX:
        for t in SIX:
            assert perm_matrix(compose(s, t)) == mat_mul(perm_matrix(s), perm_matrix(t))
    assert mean_split(X0) == (2, (2, -1, -1))
    assert mean_split((1, 4, 1)) == (2, (-1, 2, -1))
    dims = [S3["specht"][k][0] for k in ("3", "21", "111")]
    assert dims == [1, 2, 1]
    chi_m, sizes = S3["permutation"]["21"], S3["sizes"]
    mult = [sum(chi_m[c] * S3["specht"][k][c] * sizes[c] for c in range(3)) // 6 for k in ("3", "21", "111")]
    assert mult == [1, 1, 0] and chi_m[0] == 3 == dims[0] + dims[1]
    assert S3["regular_multiplicities"] == S3["regular_dimensions"] == dims
    assert sum(m * d for m, d in zip(dims, dims)) == 6 == S3["squared_dimension_sum"]


def make_card(v, w=1.0, h=1.35, fs=60):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=GREY_A, stroke_width=3)
    box.set_fill(GREY_E, opacity=1.0)
    return VGroup(box, Tex(str(v), font_size=fs))


def mini_row(word):
    return VGroup(*[make_card(v, 0.42, 0.56, 30) for v in word]).arrange(RIGHT, buff=0.08)


# =============================================================================
def part_cards(scene):
    cards = VGroup(*[make_card(v) for v in (1, 2, 3)]).arrange(RIGHT, buff=0.4).move_to(0.6 * UP)
    scene.play(LaggedStartMap(FadeIn, cards, shift=0.3 * UP, lag_ratio=0.3), run_time=1.2)
    scene.say("洗三張卡：每洗一次，卡片的順序就換一次", wait=2.0)
    order = [0, 1, 2]
    label = None
    for p, (i, j) in ((SWAP12, (0, 1)), (SWAP23, (1, 2))):
        new = Tex(perm_tex(p), font_size=48, fill_color=OP_COLOR).next_to(cards, UP, buff=0.45)
        scene.play(FadeIn(new) if label is None else ReplacementTransform(label, new), run_time=0.5)
        label = new
        scene.play(Swap(cards[order[i]], cards[order[j]]), run_time=1.0)
        order[i], order[j] = order[j], order[i]
        scene.wait(1.0)
    scene.say("三張卡共有 ", "$3!=6$", " 種排法，也就是群 ", "$S_3$", " 的 6 個元素", wait=2.0)
    scene.play(FadeOut(cards), FadeOut(label), run_time=0.6)

    cols = VGroup()
    heads = ["e", "(a\\,b)", "(a\\,b\\,c)"]
    for t, size, head in zip(S3["types"], S3["sizes"], heads):
        rows = VGroup()
        for p in SIX:
            if cycle_type(p) == tuple(t):
                rows.add(VGroup(mini_row(p), Tex(perm_tex(p), font_size=30, fill_color=OP_COLOR)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        title = VGroup(Tex(head, font_size=34), zh(f"共 {size} 個", font_size=24, color=MUTED_COLOR)).arrange(RIGHT, buff=0.2)
        cols.add(VGroup(title, rows).arrange(DOWN, buff=0.35))
    cols.arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(0.4 * UP)
    assert_in_frame(cols)
    scene.play(LaggedStartMap(FadeIn, cols, lag_ratio=0.35), run_time=2.0)
    scene.say("依循環型分成三類：大小 1、3、2", wait=4.5)
    scene.say("三個類，待會兒會對上三個形狀", wait=3.0)
    scene.say("先不寫 6 個矩陣，而是問：排列怎麼作用在向量上？", wait=3.0)


def make_axes():
    axes = VGroup()
    for k, e in enumerate(E3):
        unit = np.zeros(3)
        unit[k] = 4.6
        neg = -unit * 0.25
        axes.add(Line(p3(neg), O3, stroke_color=GREY_C, stroke_width=2))
        arr = Arrow(O3, p3(unit), buff=0, thickness=2.5, fill_color=GREY_A)
        lab = Tex(f"t_{k + 1}", font_size=40).next_to(arr.get_end(), [LEFT + DOWN, RIGHT, UP][k], buff=0.12)
        axes.add(arr, lab)
    return axes


def part_axes(scene):
    axes = make_axes()
    assert_in_frame(axes)
    scene.play(ShowCreation(axes), run_time=1.5)
    scene.say("卡片只是標籤：三張卡變成三個獨立的座標方向", wait=3.0)
    f1 = Tex(r"x=x_1t_1+x_2t_2+x_3t_3", font_size=44).move_to(np.array([3.3, 2.5, 0]))
    scene.play(Write(f1), run_time=1.0)
    scene.wait(1.5)
    dot = Dot(p3(X0), radius=0.09, fill_color=YELLOW)
    lab = Tex(r"(4,1,1)", font_size=34, fill_color=YELLOW).next_to(dot, LEFT, buff=0.15)
    scene.say("例如 ", "$x=4t_1+t_2+t_3$", "，座標是 ", "$(4,1,1)$", wait=0.5)
    scene.play(FadeIn(dot, scale=0.5), FadeIn(lab), run_time=0.8)
    scene.wait(1.5)

    f2 = Tex(r"(1\,2):(x_1,x_2,x_3)\mapsto(x_2,x_1,x_3)", font_size=40, fill_color=OP_COLOR)
    f2.next_to(f1, DOWN, buff=0.5)
    scene.play(Write(f2), run_time=1.0)
    scene.say("把卡 1、2 對調，就是把第 1、2 個座標對調", wait=1.0)
    x1 = permute_coords(SWAP12, X0)
    lab2 = Tex(r"(1,4,1)", font_size=34, fill_color=YELLOW).next_to(p3(x1), UP, buff=0.25)
    scene.play(dot.animate.move_to(p3(x1)), ReplacementTransform(lab, lab2), run_time=1.2)
    scene.wait(1.5)

    mat = VGroup(Tex(r"\rho\big((1\,2)\big)=", font_size=40), MatrixMob(perm_matrix(SWAP12), font_size=36, h_buff=0.6))
    mat.arrange(RIGHT, buff=0.2).next_to(f2, DOWN, buff=0.5)
    scene.play(FadeIn(mat), run_time=1.0)
    scene.say("寫成矩陣：第 ", "$j$", " 欄是 ", "$t_j$", " 的去處，每欄只有一個 1", wait=3.5)
    f3 = Tex(r"\rho(\sigma\tau)=\rho(\sigma)\rho(\tau)", font_size=44, fill_color=POS_COLOR).next_to(mat, DOWN, buff=0.5)
    assert_in_frame(f1, f2, mat, f3)
    assert_apart(VGroup(f1, f2, mat, f3), axes)
    scene.play(Write(f3), run_time=1.0)
    scene.say("先做 ", "$\\tau$", " 再做 ", "$\\sigma$", "，矩陣就相乘：這叫做一個表示", wait=5.0)
    return axes, dot, lab2, VGroup(f1, f2, mat, f3)


def part_line_plane(scene, axes, dot, lab, panel):
    scene.play(FadeOut(panel), FadeOut(lab), run_time=0.6)
    zline = Line(p3((-2, -2, -2)), p3((4.5, 4.5, 4.5)), stroke_color=Z_COLOR, stroke_width=4)
    zlab = Tex(r"\mathbb{C}z", font_size=40, fill_color=Z_COLOR).next_to(zline.get_end(), UR, buff=0.1)
    u, w = np.array([1, -1, 0]), np.array([1, 1, -2])
    plane = Polygon(*[p3(a * u + b * w) for a, b in ((2.2, 1.0), (-2.2, 1.0), (-2.2, -1.0), (2.2, -1.0))],
                    stroke_color=W_COLOR, stroke_width=2, fill_color=W_COLOR, fill_opacity=0.18)
    wlab = Tex("W", font_size=40, fill_color=W_COLOR).next_to(plane, DOWN, buff=0.1)
    assert_in_frame(zline, zlab, plane, wlab)
    scene.play(ShowCreation(zline), FadeIn(zlab), run_time=1.2)
    scene.say("三個座標一起升降：方向 ", "$z=t_1+t_2+t_3$", "，每個排列都不動它", wait=3.5)
    scene.play(FadeIn(plane), FadeIn(wlab), run_time=1.2)
    scene.say("只看彼此差多少：座標和為 0 的零和平面 ", "$W$", wait=3.5)

    m, rest = mean_split(X0)
    eq1 = Tex(r"(4,1,1)=2(1,1,1)+(2,-1,-1)", font_size=40).move_to(np.array([3.2, 2.2, 0]))
    eq0 = Tex(r"x=\bar{x}\,z+(x-\bar{x}\,z)", font_size=40).next_to(eq1, UP, buff=0.35)
    a_x = Arrow(O3, p3(X0), buff=0, thickness=2.5, fill_color=YELLOW)
    a_z = Arrow(O3, p3((m, m, m)), buff=0, thickness=3, fill_color=Z_COLOR)
    a_w = Arrow(p3((m, m, m)), p3(X0), buff=0, thickness=3, fill_color=W_COLOR)
    scene.play(dot.animate.move_to(p3(X0)), run_time=0.8)
    scene.play(Write(eq0), run_time=1.0)
    scene.play(GrowArrow(a_x), run_time=0.8)
    scene.play(GrowArrow(a_z), GrowArrow(a_w), Write(eq1), run_time=1.5)
    scene.say("平均值乘 ", "$z$", "，加上零和部分：", "$\\bar{x}=2$", wait=3.5)

    x1 = permute_coords(SWAP12, X0)
    m1, rest1 = mean_split(x1)
    assert m1 == m and sum(rest1) == 0 == sum(rest)
    eq2 = Tex(r"(1\,2):\ (1,4,1)=2(1,1,1)+(-1,2,-1)", font_size=40, fill_color=OP_COLOR).next_to(eq1, DOWN, buff=0.45)
    assert_in_frame(eq0, eq1, eq2)
    a_x1 = Arrow(O3, p3(x1), buff=0, thickness=2.5, fill_color=YELLOW)
    a_w1 = Arrow(p3((m, m, m)), p3(x1), buff=0, thickness=3, fill_color=W_COLOR)
    scene.play(dot.animate.move_to(p3(x1)), Transform(a_x, a_x1), Transform(a_w, a_w1), Write(eq2), run_time=1.5)
    scene.play(Indicate(a_z, color=Z_COLOR), run_time=1.0)
    scene.say("交換之後：平均值還是 2，零和部分仍然留在 ", "$W$", " 裡", wait=5.0)


def part_theory(scene):
    l1 = mixed("穩定子空間 ", "$U$", "：對每個 ", "$\\sigma$", " 都有 ", "$\\sigma U\\subseteq U$", font_size=30)
    l2 = mixed("例：", "$\\mathbb{C}z$", " 和 ", "$W$", " 都穩定，而且 ", "$M=\\mathbb{C}z\\oplus W$", font_size=30)
    l3 = mixed("不可約：除了 ", "$0$", " 和自己，沒有別的穩定子空間", font_size=30)
    l4 = mixed("注意：", "$z$", " 不動，不代表整個表示是平凡的", font_size=26, color=MUTED_COLOR)
    block = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(1.4 * UP)
    scene.play(FadeIn(l1, shift=0.2 * UP), run_time=0.8)
    scene.say("子空間每次被作用後都還在裡面，才叫穩定", wait=3.0)
    scene.play(FadeIn(l2, shift=0.2 * UP), run_time=0.8)
    scene.say("三維空間拆成兩塊穩定的子空間：直和", wait=3.0)
    scene.play(FadeIn(l3, shift=0.2 * UP), FadeIn(l4), run_time=0.8)
    scene.say("拆到不能再拆的，叫不可約", wait=3.0)

    mas = Tex(r"P_G=\frac{1}{|G|}\sum_{g\in G}\rho(g)\,P\,\rho(g)^{-1}", font_size=40)
    mas_note = zh("有限群、複數係數：平均化後的投影是等變的", font_size=24, color=MUTED_COLOR)
    mas_box = VGroup(zh("Maschke", font_size=28, color=OP_COLOR), mas, mas_note).arrange(DOWN, buff=0.2)
    mas_box.move_to(np.array([-3.3, -1.55, 0]))
    v1 = mixed("$S^{(3)}$", font_size=30)
    v2 = mixed("$S^{(2,1)}$", font_size=30)
    b1, b2 = (SurroundingRectangle(v, buff=0.2, color=GREY_B) for v in (v1, v2))
    c1, c2 = VGroup(b1, v1), VGroup(b2, v2)
    VGroup(c1, c2).arrange(RIGHT, buff=1.6)
    arr = Arrow(c1.get_right(), c2.get_left(), buff=0.1, thickness=2.5, fill_color=GREY_B)
    zero = Tex(r"\varphi=0", font_size=34, fill_color=OP_COLOR).next_to(arr, UP, buff=0.1)
    schur = VGroup(zh("Schur", font_size=28, color=OP_COLOR), VGroup(c1, c2, arr, zero)).arrange(DOWN, buff=0.3)
    schur.move_to(np.array([3.4, -1.55, 0]))
    assert_in_frame(block, mas_box, schur)
    assert_apart(block, mas_box)
    assert_apart(mas_box, schur)
    scene.play(FadeIn(mas_box), run_time=1.0)
    scene.say("Maschke：把任一投影對整個群平均，穩定子空間就有穩定的補空間", wait=5.0)
    scene.play(FadeIn(schur), run_time=1.0)
    scene.say("Schur：兩個不同的不可約之間，等變映射只有 0；同一個則只有純量倍", wait=5.0)


def part_preview(scene):
    cards = VGroup()
    for lam, key, name in SHAPES:
        d = YoungDiagramMob(lam, cell_size=0.38)
        dim = Tex(r"\dim=" + str(S3["specht"][key][0]), font_size=32)
        cards.add(VGroup(d, dim, zh(name, font_size=24, color=MUTED_COLOR)).arrange(DOWN, buff=0.18))
    cards.arrange(RIGHT, buff=1.6, aligned_edge=DOWN).move_to(1.65 * UP)
    scene.play(LaggedStartMap(FadeIn, cards, lag_ratio=0.3), run_time=1.5)
    scene.say("三個形狀，三種不可約模式：維度 1、2、1", wait=3.5)

    def window(title, pieces, labels, center, width):
        row = VGroup(*[Tex(p, font_size=52) for p in pieces]).arrange(RIGHT, buff=0.22)
        labs = VGroup()
        for k, t in labels.items():
            labs.add(Tex(t, font_size=32, fill_color=MUTED_COLOR).next_to(row[k], DOWN, buff=0.3))
        body = VGroup(title, VGroup(row, labs)).arrange(DOWN, buff=0.3)
        frame = Rectangle(width=width, height=2.4, stroke_color=GREY_B, stroke_width=2).move_to(center)
        body.move_to(frame)
        for a, b in zip(labs, labs[1:]):
            assert_apart(a, b)
        return VGroup(frame, body), row

    t1 = VGroup(Tex(r"M^{(2,1)}", font_size=36), zh("三維", font_size=24, color=MUTED_COLOR)).arrange(RIGHT, buff=0.2)
    w1, r1 = window(t1, ["3", "=", "1", "+", "2"], {2: r"S^{(3)}", 4: r"S^{(2,1)}"}, np.array([-3.6, -1.45, 0]), 5.0)
    t2 = VGroup(Tex(r"\mathbb{C}[S_3]", font_size=36), zh("六維", font_size=24, color=MUTED_COLOR)).arrange(RIGHT, buff=0.2)
    w2, r2 = window(t2, ["6", "=", "1", "+", r"2\cdot 2", "+", "1"],
                    {2: r"S^{(3)}", 4: r"\big(S^{(2,1)}\big)^{\oplus 2}", 6: r"S^{(1^3)}"},
                    np.array([2.9, -1.45, 0]), 6.6)
    assert_in_frame(cards, w1, w2)
    assert_apart(w1, w2)
    assert_apart(cards, VGroup(w1, w2))
    scene.play(FadeIn(w1), run_time=1.0)
    scene.say("第一個計數窗：三維的 ", "$M^{(2,1)}$", " 拆成 ", "$3=1+2$", wait=4.0)
    scene.play(FadeIn(w2), run_time=1.0)
    scene.say("第二個計數窗：六維的群代數，", "$S^{(2,1)}$", " 出現兩次", wait=5.0)
    scene.play(Indicate(r2[4], color=OP_COLOR), run_time=1.0)
    sq = Tex(r"=1^2+2^2+1^2", font_size=40, fill_color=POS_COLOR)
    sq.next_to(w2, UP, buff=0.15).align_to(w2, RIGHT)
    if sq.get_top()[1] > cards.get_bottom()[1] - 0.05:
        sq.next_to(w2[0], DOWN, buff=0.08)
    assert_in_frame(sq)
    scene.play(Write(sq), run_time=1.0)
    scene.say("每種不可約出現的次數＝它的維度：", "$1^2+2^2+1^2=6$", "（本章將解釋）", wait=5.0)
    scene.say("不是 ", "$6=1+2+1$", "；而三維的 ", "$M^{(2,1)}$", " 裡也沒有 sign", wait=5.0)
    scene.clear_stage()

    qs = VGroup(
        zh("① 形狀怎麼造出模組？", font_size=34),
        zh("② 為什麼基底是標準表？", font_size=34),
        zh("③ 交換的矩陣怎麼算？", font_size=34),
    ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(0.3 * UP)
    scene.play(LaggedStartMap(FadeIn, qs, shift=0.2 * RIGHT, lag_ratio=0.4), run_time=1.8)
    scene.say("接下來幾幕，一題一題回答", wait=4.0)


class SceneF28SixShuffles(ChuScene):
    def construct(self):
        self.show_header("三張卡片、六種排列")
        check_math()
        part_cards(self)
        self.clear_stage()
        axes, dot, lab, panel = part_axes(self)
        part_line_plane(self, axes, dot, lab, panel)
        self.clear_stage()
        part_theory(self)
        self.clear_stage()
        part_preview(self)
        self.wait(1.0)
