"""
Scene F61 —— 把行重新排隊：鑰匙（Fulton §A.5，書 p.208–210）
執行（在 codes/ 內）：manimgl scenes/sceneF61_keys.py SceneF61Keys
"""
import sys
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import compact_skew, frank_tableau, keys
from utils.fulton_draw import SkewMob, assert_apart, assert_in_frame, tableau_mob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import rectify, shape, transpose

SLOW = 7.0
OK = "#7CE38B"
BAD = PINK
T = ((1, 1, 2, 2), (2, 3, 3), (4,))
BOOK_LENGTHS = (2, 3, 2, 1)
BOOK_COLS = ((1, 2), (1, 3, 4), (2, 3), (2,))
NAIVE = ((None, 1, 2, 2), (1, 2, 3), (3, 4))          # T 原來的行直接換位置
GALLERY = [(3, 2, 2, 1), (2, 3, 2, 1), (1, 3, 2, 2), (3, 1, 2, 2), (2, 1, 3, 2), (1, 2, 2, 3)]
LEFT_SETS = {1: (1,), 2: (1, 2), 3: (1, 2, 4)}
RIGHT_SETS = {1: (2,), 2: (2, 3), 3: (2, 3, 4)}
K_MINUS = ((1, 1, 1, 1), (2, 2, 2), (4,))
K_PLUS = ((2, 2, 2, 2), (3, 3, 3), (4,))
SMALL = ((1, 2), (3,))
LEN_COLOR = {1: GOLD, 2: TEAL, 3: BLUE_C}
L_COLOR, R_COLOR = OK, ORANGE


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def columns(T):
    return [tuple(T[i][j] for i in range(len(T)) if j < len(T[i])) for j in range(len(T[0]))]


def frank_skew(T, lengths):
    """frank 斜表：(各行內容, 各行 (頂端列, 長度), 斜表的列寫法)。"""
    cols = frank_tableau(T, list(lengths))
    geo = compact_skew(list(lengths))
    grid = [[None] * len(geo) for _ in range(max(t + L for t, L in geo))]
    for j, ((t, L), col) in enumerate(zip(geo, cols)):
        for k in range(L):
            grid[t + k][j] = col[k]
    S = tuple(tuple(r[:max(j for j, v in enumerate(r) if v is not None) + 1]) for r in grid)
    return cols, geo, S


def set_str(c):
    return r"\{" + ",".join(map(str, c)) + r"\}"


def check_math():
    assert columns(T) == [(1, 2, 4), (1, 3), (2, 3), (2,)] and shape(T) == (4, 3, 1)
    cols, geo, S = frank_skew(T, BOOK_LENGTHS)
    assert cols == BOOK_COLS and geo == [(1, 2), (0, 3), (0, 2), (0, 1)] and rectify(S) == T
    assert rectify(NAIVE) == ((1, 1, 2, 2), (2, 3), (3, 4)) != T
    for L in set(permutations((3, 2, 2, 1))):                     # 推論 1：最左／最右只看長度
        cols, _, S = frank_skew(T, L)
        assert rectify(S) == T and cols[0] == LEFT_SETS[L[0]] and cols[-1] == RIGHT_SETS[L[-1]]
    for c in (1, 2):                                                # 推論 2：L_c ⊂ L_d
        assert set(LEFT_SETS[c]) < set(LEFT_SETS[c + 1]) and set(RIGHT_SETS[c]) < set(RIGHT_SETS[c + 1])
    assert keys(T) == (K_MINUS, K_PLUS)
    assert transpose(tuple(LEFT_SETS[len(c)] for c in columns(T))) == K_MINUS
    assert transpose(tuple(RIGHT_SETS[len(c)] for c in columns(T))) == K_PLUS
    assert all(a <= b <= c for ra, rb, rc in zip(K_MINUS, T, K_PLUS) for a, b, c in zip(ra, rb, rc))
    assert keys(SMALL) == (((1, 1), (3,)), ((2, 2), (3,)))
    assert frank_tableau(SMALL, [1, 2]) == ((1,), (2, 3)) and frank_tableau(SMALL, [2, 1]) == ((1, 3), (2,))


def paint(mob, geo, colors, opacity=0.35):
    for j, (t, L) in enumerate(geo):
        for k in range(L):
            mob.cell(t + k, j).set_fill(colors[j], opacity)
    return mob


def col_box(mob, geo, j, color, buff=0.04):
    t, L = geo[j]
    return SurroundingRectangle(VGroup(*[mob.cell(t + k, j) for k in range(L)]), buff=buff).set_stroke(color, 4)


def len_labels(mob, geo, fs=28):
    y = mob.get_bottom()[1] - 0.3
    return VGroup(*[tex(str(L), fs, LEN_COLOR[L]).move_to(np.array([mob.cell(t, j).get_center()[0], y, 0]))
                    for j, (t, L) in enumerate(geo)])


# ---------------------------------------------------------------- 1. 問題與命題 7
def part_frank(scene):
    tgeo = [(0, len(c)) for c in columns(T)]
    tab = paint(tableau_mob(T, cs=0.7).move_to(np.array([3.6, 0.6, 0])), tgeo, [LEN_COLOR[L] for _, L in tgeo])
    tlab = len_labels(tab, tgeo)
    tname = tex("T", 40).next_to(tab, UP, buff=0.3)
    cols, geo, S = frank_skew(T, BOOK_LENGTHS)
    sk = paint(SkewMob(S, cs=0.7, show_mu=False).move_to(np.array([-3.6, 0.6, 0])), geo,
               [LEN_COLOR[L] for L in BOOK_LENGTHS])
    slab = len_labels(sk, geo)
    sname = tex(r"(2,3,2,1)", 34, MUTED_COLOR).next_to(sk, UP, buff=0.3)
    nv = paint(SkewMob(NAIVE, cs=0.7, show_mu=False).move_to(sk.get_center()), geo,
               [LEN_COLOR[L] for L in BOOK_LENGTHS])
    arrow = Arrow(np.array([-1.5, 0.6, 0]), np.array([1.5, 0.6, 0]), buff=0).set_color(GREY_B)
    alab = zh("rectify", font_size=26, color=MUTED_COLOR).next_to(arrow, UP, buff=0.12)
    wrong = tableau_mob(rectify(NAIVE), cs=0.5).move_to(np.array([0, -1.8, 0]))
    wlab = mixed("$\\ne T$", font_size=28, color=BAD).next_to(wrong, RIGHT, buff=0.3)
    rule = zh("緊湊形式：相鄰兩行，左邊長就頂端對齊，右邊長就底端對齊", font_size=26, color=MUTED_COLOR)
    rule.move_to(np.array([0, 2.75, 0]))
    assert_in_frame(tab, tlab, tname, sk, slab, sname, arrow, wrong, wlab, rule)
    assert_apart(sk, arrow, 0.2)
    assert_apart(arrow, tab, 0.2)
    assert_apart(VGroup(sname, tname), rule, 0.1)
    assert_apart(wrong, VGroup(slab, tlab, arrow), 0.15)

    scene.say("問：一張表的各行換個順序排，還能 rectify 回原來的表嗎？", wait=SLOW * 0.6)
    scene.play(FadeIn(tab), Write(tname), run_time=1.0)
    scene.play(FadeIn(tlab), run_time=0.6)
    scene.say("$T=1122/233/4$", " 的四行：", "$124,\\ 13,\\ 23,\\ 2$", "，長度 ", "$3,2,2,1$", wait=SLOW * 0.6)
    scene.say("把長度排成 ", "$(2,3,2,1)$", "：先試試直接把原來的行搬過去", wait=SLOW * 0.3)
    scene.play(FadeIn(nv), FadeIn(slab), Write(sname), run_time=1.0)
    scene.play(GrowArrow(arrow), FadeIn(alab), run_time=0.8)
    scene.play(TransformFromCopy(nv, wrong), run_time=1.2)
    scene.play(FadeIn(wlab), run_time=0.5)
    scene.say("滑回去得到 ", "$1122/23/34$", "，形狀都不對：行的內容必須換", wait=SLOW * 0.6)
    scene.play(FadeOut(wrong), FadeOut(wlab), FadeOut(nv), FadeIn(rule), run_time=0.8)
    scene.say("形狀先固定：", "$(2,3,2,1)$", " 的緊湊斜形", wait=SLOW * 0.4)
    scene.play(FadeIn(sk.cells), run_time=0.8)
    scene.say("命題 7：恰有一種填法，讓這個斜表 rectify 成 ", "$T$", wait=SLOW * 0.5)
    scene.play(LaggedStartMap(FadeIn, sk.entries, lag_ratio=0.12), run_time=1.6)
    scene.play(Indicate(tab, color=OK, scale_factor=1.05), run_time=1.0)
    scene.say("各行是 ", "$12,\\ 134,\\ 23,\\ 2$", "（書 p.209）：叫做 ", "$T$", " 的 frank 斜表", wait=SLOW * 0.7)
    scene.say("長度的每一種排列都有唯一的 frank 斜表；", "$(3,2,2,1)$", " 就是 ", "$T$", " 自己", wait=SLOW * 0.5)


# ---------------------------------------------------------------- 2. 推論 1、2
def part_corollaries(scene):
    items = VGroup()
    data = []
    for k, L in enumerate(GALLERY):
        cols, geo, S = frank_skew(T, L)
        x, y = -5.0 + 2.45 * (k % 3), 1.05 - 2.55 * (k // 3)
        m = SkewMob(S, cs=0.42, show_mu=False).move_to(np.array([x, y, 0]))
        lab = tex(r"(%s)" % ",".join(map(str, L)), 26, MUTED_COLOR).move_to(np.array([x, y + 1.15, 0]))
        items.add(VGroup(m, lab))
        data.append((m, geo, L))
    lboxes = VGroup(*[col_box(m, geo, 0, L_COLOR) for m, geo, _ in data])
    rboxes = VGroup(*[col_box(m, geo, len(geo) - 1, R_COLOR) for m, geo, _ in data])
    lsets = VGroup(*[tex(r"\mathcal L_%d=%s" % (c, set_str(LEFT_SETS[c])), 32, L_COLOR) for c in (1, 2, 3)])
    rsets = VGroup(*[tex(r"\mathcal R_%d=%s" % (c, set_str(RIGHT_SETS[c])), 32, R_COLOR) for c in (1, 2, 3)])
    lsets.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(np.array([4.6, 1.6, 0]))
    rsets.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(np.array([4.6, -0.55, 0]))
    chain = VGroup(tex(r"\mathcal L_1\subset\mathcal L_2\subset\mathcal L_3", 30, YELLOW),
                   tex(r"\mathcal R_1\subset\mathcal R_2\subset\mathcal R_3", 30, YELLOW))
    chain.arrange(DOWN, buff=0.15).move_to(np.array([4.6, -2.3, 0]))
    assert_in_frame(items, lsets, rsets, chain)
    for a, b in zip(items, items[1:]):
        assert_apart(a, b, 0.2)
    assert_apart(items, VGroup(lsets, rsets), 0.3)
    assert_apart(lsets, rsets, 0.2)
    assert_apart(rsets, chain, 0.15)

    scene.say("把六種長度順序的 frank 斜表排在一起", wait=SLOW * 0.2)
    scene.play(LaggedStartMap(FadeIn, items, lag_ratio=0.15), run_time=2.2)
    scene.wait(SLOW * 0.3)
    scene.say("看最左邊那一行：長度一樣，內容就一樣", wait=SLOW * 0.2)
    scene.play(LaggedStartMap(ShowCreation, lboxes, lag_ratio=0.15), run_time=1.6)
    scene.say("推論 1：最左那一行只跟它的長度 ", "$c$", " 有關，記成 ", r"$\mathcal L_c$", wait=SLOW * 0.3)
    scene.play(LaggedStartMap(FadeIn, lsets, lag_ratio=0.3), run_time=1.4)
    scene.wait(SLOW * 0.4)
    scene.say("最右那一行也一樣：記成 ", r"$\mathcal R_c$", wait=SLOW * 0.2)
    scene.play(LaggedStartMap(ShowCreation, rboxes, lag_ratio=0.15), run_time=1.6)
    scene.play(LaggedStartMap(FadeIn, rsets, lag_ratio=0.3), run_time=1.4)
    scene.wait(SLOW * 0.4)
    scene.say("推論 2：", "$c<d$", " 時 ", r"$\mathcal L_c\subset\mathcal L_d$", "，", r"$\mathcal R_c\subset\mathcal R_d$", wait=SLOW * 0.2)
    scene.play(Write(chain), run_time=1.2)
    scene.wait(SLOW * 0.6)


# ---------------------------------------------------------------- 3. 鑰匙
def part_keys(scene):
    tgeo = [(0, len(c)) for c in columns(T)]
    colors = [LEN_COLOR[L] for _, L in tgeo]
    km = paint(tableau_mob(K_MINUS, cs=0.62).move_to(np.array([-4.4, 1.0, 0])), tgeo, [L_COLOR] * 4, 0.25)
    tb = paint(tableau_mob(T, cs=0.62).move_to(np.array([0, 1.0, 0])), tgeo, colors)
    kp = paint(tableau_mob(K_PLUS, cs=0.62).move_to(np.array([4.4, 1.0, 0])), tgeo, [R_COLOR] * 4, 0.25)
    names = VGroup(tex(r"K_-(T)", 36, L_COLOR).next_to(km, UP, buff=0.3), tex("T", 36).next_to(tb, UP, buff=0.3),
                   tex(r"K_+(T)", 36, R_COLOR).next_to(kp, UP, buff=0.3))
    lsub = VGroup(*[tex(r"\mathcal L_%d" % L, 26, L_COLOR).move_to(np.array([km.cell(0, j).get_center()[0],
                                                                          km.get_bottom()[1] - 0.3, 0]))
                    for j, (_, L) in enumerate(tgeo)])
    rsub = VGroup(*[tex(r"\mathcal R_%d" % L, 26, R_COLOR).move_to(np.array([kp.cell(0, j).get_center()[0],
                                                                          kp.get_bottom()[1] - 0.3, 0]))
                    for j, (_, L) in enumerate(tgeo)])
    leq = VGroup(tex(r"\le", 40, MUTED_COLOR).move_to(np.array([-2.2, 1.0, 0])),
                 tex(r"\le", 40, MUTED_COLOR).move_to(np.array([2.2, 1.0, 0])))
    sm = [tableau_mob(SMALL, cs=0.5), tableau_mob(((1, 1), (3,)), cs=0.5), tableau_mob(((2, 2), (3,)), cs=0.5)]
    small = VGroup(tex(r"K_-:", 30, L_COLOR), sm[1], tex(r"\longleftarrow", 34, MUTED_COLOR), sm[0],
                   tex(r"\longrightarrow", 34, MUTED_COLOR), sm[2], tex(r":K_+", 30, R_COLOR))
    small.arrange(RIGHT, buff=0.35).move_to(np.array([0, -1.75, 0]))
    assert_in_frame(km, tb, kp, names, lsub, rsub, small)
    assert_apart(km, tb, 0.4)
    assert_apart(tb, kp, 0.4)
    assert_apart(VGroup(lsub, rsub, km, tb, kp), small, 0.25)

    scene.say("把它們排成表：長度 ", "$c$", " 的行換成 ", r"$\mathcal L_c$", wait=SLOW * 0.2)
    scene.play(FadeIn(tb), Write(names[1]), run_time=0.9)
    scene.play(TransformFromCopy(tb, km), run_time=1.3)
    scene.play(Write(names[0]), FadeIn(lsub), run_time=0.8)
    scene.say("左鑰匙 ", r"$K_-(T)=1111/222/4$", "（", r"$124,\ 12,\ 12,\ 1$", "）", wait=SLOW * 0.6)
    scene.play(TransformFromCopy(tb, kp), run_time=1.3)
    scene.play(Write(names[2]), FadeIn(rsub), run_time=0.8)
    scene.say("右鑰匙 ", r"$K_+(T)=2222/333/4$", "（", r"$234,\ 23,\ 23,\ 2$", "）", wait=SLOW * 0.6)
    scene.say("推論 2 保證：鑰匙的每一行都包含它右邊那一行", wait=SLOW * 0.5)
    scene.play(FadeIn(leq), run_time=0.6)
    scene.say("這個例子裡逐格比較：", r"$K_-(T)\le T\le K_+(T)$", wait=SLOW * 0.5)
    scene.say("小例子 ", r"$T=12/3$", "：frank 斜表 ", r"$1\,|\,23$", " 與 ", r"$13\,|\,2$", wait=SLOW * 0.3)
    scene.play(FadeIn(small[3]), run_time=0.6)
    scene.play(FadeIn(small[2]), FadeIn(small[1]), FadeIn(small[0]), run_time=0.9)
    scene.play(FadeIn(small[4]), FadeIn(small[5]), FadeIn(small[6]), run_time=0.9)
    scene.say(r"$\mathcal L_1=\{1\},\ \mathcal L_2=\{1,3\}$", " 給 ", r"$K_-=11/3$", "；", r"$\mathcal R_1=\{2\},\ \mathcal R_2=\{2,3\}$",
              " 給 ", r"$K_+=22/3$", wait=SLOW * 0.8)
    scene.say("鑰匙用在旗流形的標準單項式（§10.5 末，Lascoux–Schützenberger）", wait=SLOW * 0.6)
    scene.say("收束：鑰匙是一張表「最靠左／最靠右」的影子", wait=SLOW * 0.7)


class SceneF61Keys(ChuScene):
    def construct(self):
        self.show_header("把行重新排隊：鑰匙")
        check_math()
        part_frank(self)
        self.clear_stage()
        part_corollaries(self)
        self.clear_stage()
        part_keys(self)
        self.wait(1.0)
