"""
Scene F60 —— 填格子遊戲：0-1 矩陣與 Gale–Ryser（Fulton §A.4.3，書 p.203–208；練習 19、20）
執行（在 codes/ 內）：manimgl scenes/sceneF60_zero_one.py SceneF60ZeroOne
"""
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import column_insert, dual_rsk, gale_ryser, lex_sort, matrix_to_pairs, zero_one_matrices
from utils.fulton_draw import TwoRowArray, assert_apart, assert_in_frame, tuple_str
from utils.rep_draw import MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import conjugate, kostka, partitions, shape

SLOW = 10.5
ACC = YELLOW
BUMP = PINK
UCOL = ORANGE
VCOL = BLUE_B
OK = "#7CE38B"
BAD = "#E05AA0"
ONE = TEAL_B
PZ1 = ((3, 2, 1), (2, 2, 2))
PZ2 = ((3, 3), (3, 1, 1, 1))
M0 = [[0, 1, 1], [1, 0, 1], [1, 0, 1]]


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def is_ssyt(T):
    rows = all(a <= b for r in T for a, b in zip(r, r[1:]))
    cols = all(T[i][j] < T[i + 1][j] for i in range(len(T) - 1) for j in range(len(T[i + 1])))
    return rows and cols


def n_ssyt(nu, k):
    """形狀 ν、數字 ≤ k 的半標準表個數。"""
    return sum(kostka(nu, a) for a in product(range(sum(nu) + 1), repeat=k) if sum(a) == sum(nu))


def ex19_terms(lam, mu):
    return [(nu, kostka(conjugate(nu), lam), kostka(nu, mu)) for nu in partitions(sum(lam))
            if kostka(conjugate(nu), lam) * kostka(nu, mu)]


def partial(seq, length):
    s = list(seq) + [0] * (length - len(seq))
    return [sum(s[:k + 1]) for k in range(length)]


def check_math():
    u, v = lex_sort(*zip(*matrix_to_pairs(M0)))
    assert (u, v) == ((1, 1, 2, 2, 3, 3), (2, 3, 1, 3, 1, 3))
    P, Q = dual_rsk(M0)
    assert P == ((1, 1, 2), (3, 3, 3)) and Q == ((1, 1), (2, 2), (3, 3)) and shape(Q) == conjugate(shape(P))
    seen = set()
    for bits in product((0, 1), repeat=9):
        if not any(bits):
            continue
        B = [list(bits[0:3]), list(bits[3:6]), list(bits[6:9])]
        P2, Q2 = dual_rsk(B)
        assert shape(Q2) == conjugate(shape(P2)) and is_ssyt(P2) and is_ssyt(Q2)
        assert max(x for r in P2 for x in r) <= 3 and max(x for r in Q2 for x in r) <= 3
        seen.add((P2, Q2))
    total = sum(n_ssyt(nu, 3) * n_ssyt(conjugate(nu), 3) for n in range(1, 10) for nu in partitions(n)
                if len(nu) <= 3 and nu[0] <= 3)
    assert len(seen) == 511 == total
    assert len(zero_one_matrices(*PZ1)) == 3 and len(zero_one_matrices(*PZ2)) == 0
    assert sum(a * b for _, a, b in ex19_terms(*PZ1)) == 3 and ex19_terms(*PZ2) == []
    assert ex19_terms(*PZ1) == [((3, 2, 1), 1, 2), ((2, 2, 2), 1, 1)]
    assert gale_ryser(*PZ1) and not gale_ryser(*PZ2)
    assert conjugate(PZ1[0]) == (3, 2, 1) and conjugate(PZ2[0]) == (2, 2, 2)
    assert partial(PZ1[1], 3) == [2, 4, 6] and partial(conjugate(PZ1[0]), 3) == [3, 5, 6]
    assert partial(PZ2[1], 4)[0] == 3 and partial(conjugate(PZ2[0]), 4)[0] == 2


# ---------------------------------------------------------------- 格子
def sum_grid(rows, cols, cs, center):
    m, n = len(rows), len(cols)
    c = np.array([center[0], center[1], 0.0])
    sq = {}
    grid = VGroup()
    for i in range(m):
        for j in range(n):
            s = Square(cs).set_stroke(GREY_B, 2).move_to(c + np.array([(j - (n - 1) / 2) * cs, ((m - 1) / 2 - i) * cs, 0]))
            sq[(i, j)] = s
            grid.add(s)
    fs = 60 * cs
    rl = VGroup(*[tex(str(rows[i]), fs, UCOL).next_to(sq[(i, n - 1)], RIGHT, buff=0.18) for i in range(m)])
    cl = VGroup(*[tex(str(cols[j]), fs, VCOL).next_to(sq[(m - 1, j)], DOWN, buff=0.14) for j in range(n)])
    g = VGroup(grid, rl, cl)
    g.sq, g.grid, g.rl, g.cl, g.cs = sq, grid, rl, cl, cs
    return g


def ones(G, M, color=ONE):
    return VGroup(*[Square(G.cs * 0.72).set_stroke(width=0).set_fill(color, opacity=0.85).move_to(G.sq[(i, j)])
                    for i, r in enumerate(M) for j, a in enumerate(r) if a])


# ---------------------------------------------------------------- 會動的表
class LiveTab:
    def __init__(self, cs, top_left, fs=None):
        self.cs, self.fs = cs, fs or 60 * cs
        self.tl = np.array([top_left[0], top_left[1], 0.0])
        self.sq, self.ent = {}, {}

    def pos(self, i, j):
        return self.tl + (j + 0.5) * self.cs * RIGHT + (i + 0.5) * self.cs * DOWN

    def ghost(self, T):
        return VGroup(*[Square(self.cs).move_to(self.pos(i, j)) for i, r in enumerate(T) for j in range(len(r))])


def column_insert_anim(scene, lt, src, path, rt=1.0):
    inc = src.copy()
    scene.play(inc.animate.move_to(lt.pos(*path[0]) + LEFT * lt.cs).set_color(ACC).scale(lt.fs / 36),
               run_time=0.5 * rt)
    for k, cell in enumerate(path):
        if cell in lt.ent:
            y = lt.ent[cell]
            stage = lt.pos(*path[k + 1]) + 0.55 * lt.cs * LEFT
            scene.play(y.animate.set_color(BUMP), lt.sq[cell].animate.set_fill(ACC, opacity=0.25),
                       run_time=0.25 * rt)
            scene.play(inc.animate.move_to(lt.pos(*cell)), y.animate.move_to(stage), run_time=0.45 * rt)
            lt.ent[cell] = inc
            inc = y
        else:
            sq = Square(lt.cs).set_stroke(GREY_B, 3).move_to(lt.pos(*cell)).set_fill(ACC, opacity=0.25)
            lt.sq[cell] = sq
            scene.play(FadeIn(sq), inc.animate.move_to(lt.pos(*cell)), run_time=0.45 * rt)
            lt.ent[cell] = inc
    scene.play(*[lt.sq[c].animate.set_fill(BLACK, opacity=0) for c in path[:-1]],
               *[lt.ent[c].animate.set_color(WHITE) for c in path], run_time=0.25 * rt)


def place_anim(scene, lt, src, cell, rt=1.0):
    sq = Square(lt.cs).set_stroke(GREY_B, 3).move_to(lt.pos(*cell)).set_fill(ACC, opacity=0.25)
    m = src.copy()
    lt.sq[cell] = sq
    lt.ent[cell] = m
    scene.play(FadeIn(sq), m.animate.move_to(lt.pos(*cell)).set_color(UCOL).scale(lt.fs / 36), run_time=0.55 * rt)
    return sq


# ---------------------------------------------------------------- 1. 謎題
def part_puzzle(scene):
    G1 = sum_grid(*PZ1, 0.75, (-3.6, 0.7))
    G2 = sum_grid(*PZ2, 0.75, (3.2, 0.7))
    l1 = mixed("列和 ", "$(3,2,1)$", "，行和 ", "$(2,2,2)$", font_size=26).next_to(G1, DOWN, buff=0.4)
    l2 = mixed("列和 ", "$(3,3)$", "，行和 ", "$(3,1,1,1)$", font_size=26).next_to(G2, DOWN, buff=0.4)
    q1 = tex("?", 90, ACC).move_to(G1.grid)
    q2 = tex("?", 90, ACC).move_to(G2.grid)
    leg = mixed("每格填 ", "$0$", " 或 ", "$1$", font_size=26, color=MUTED_COLOR).move_to(np.array([0, 2.75, 0]))
    assert_in_frame(G1, G2, l1, l2, leg)
    assert_apart(VGroup(G1, l1), VGroup(G2, l2), 0.8)
    assert_apart(leg, VGroup(G1, G2), 0.2)

    scene.say("問：每格填 ", "$0$", " 或 ", "$1$", "，列和 ", "$(3,2,1)$", "、行和 ", "$(2,2,2)$", "，填得出來嗎？",
              wait=SLOW * 0.25)
    scene.play(FadeIn(leg), FadeIn(G1), run_time=0.9)
    scene.play(FadeIn(l1), FadeIn(q1, scale=0.6), run_time=0.7)
    scene.say("那列和 ", "$(3,3)$", "、行和 ", "$(3,1,1,1)$", " 呢？", wait=SLOW * 0.2)
    scene.play(FadeIn(G2), FadeIn(l2), FadeIn(q2, scale=0.6), run_time=0.9)
    scene.say("先猜猜看。答案在最後揭曉", wait=SLOW * 0.3)


# ---------------------------------------------------------------- 2. Knuth 的對應
def part_knuth(scene):
    M = MatrixMob(M0, font_size=36, center=np.array([-5.0, 1.6, 0]))
    ml = tex("A=", 36).next_to(M, LEFT, buff=0.15)
    u, v = lex_sort(*zip(*matrix_to_pairs(M0)))
    arr = TwoRowArray(u, v, font_size=36, center=np.array([1.2, 2.35, 0]), top_color=UCOL, bottom_color=VCOL)
    al = mixed("$u$", "$v$", font_size=28).arrange(DOWN, buff=0.28).next_to(arr, LEFT, buff=0.3)
    cs = 0.72
    Pt = LiveTab(cs, (-2.4, 0.85))
    Qt = LiveTab(cs, (2.3, 0.85))
    P, Q = dual_rsk(M0)
    gP, gQ = Pt.ghost(P), Qt.ghost(Q)
    stage = Square(cs).move_to(Pt.pos(1, -1))
    pl = mixed("$P$", "：依序行插入 ", "$v$", font_size=26).next_to(gP, DOWN, buff=0.3)
    pl.align_to(gP, LEFT)
    ql = mixed("$Q$", "：", "$u$", " 放在新格子的共軛位置", font_size=26).next_to(gQ, DOWN, buff=0.3)
    ql.align_to(gQ, LEFT)
    res = mixed("形狀 ", "$" + tuple_str(shape(P)) + "$", " 與 ", "$" + tuple_str(shape(Q)) + "$", " 互為共軛",
                font_size=28, color=ACC).move_to(np.array([0, -2.5, 0]))
    assert_in_frame(M, ml, arr, al, gP, gQ, stage, pl, ql, res)
    assert_apart(VGroup(M, ml), VGroup(stage, gP), 0.4)
    assert_apart(VGroup(arr, al), VGroup(gP, gQ), 0.3)
    assert_apart(VGroup(gP, pl), VGroup(gQ, ql), 0.3)
    assert_apart(VGroup(pl, ql), res, 0.15)

    scene.say("Knuth 的對應：0-1 矩陣就是「沒有重複」的陣列", wait=SLOW * 0.25)
    scene.play(FadeIn(M), Write(ml), run_time=0.8)
    scene.play(FadeIn(arr), FadeIn(al), run_time=0.9)
    scene.say("每個 ", "$1$", " 給一對 ", "$(i,j)$", "，排成字典序", wait=SLOW * 0.25)
    scene.play(FadeIn(pl), FadeIn(ql), run_time=0.7)
    scene.say("依序行插入 ", "$v_1,\\dots,v_6$", "；新格子在 ", "$(i,j)$", " 時，把 ", "$u$", " 放在 ", "$Q$", " 的 ",
              "$(j,i)$", wait=SLOW * 0.25)
    TP, TQ = (), ()
    for k in range(len(v)):
        rt = 1.6 if k < 2 else 1.0
        top, bot = arr.col(k)
        scene.play(top.animate.set_color(ACC), bot.animate.set_color(ACC), run_time=0.25)
        T0 = TP
        TP, path, nb = column_insert(TP, v[k])
        bumped = [T0[i][j] for i, j in path[:-1]]
        what = ("，擠掉 ", "$" + "\\to ".join(map(str, bumped)) + "$") if bumped else ()
        scene.say("行插入 ", "$v_%d=%d$" % (k + 1, v[k]), *what, "；新格子 ", "$(%d,%d)$" % (nb[0] + 1, nb[1] + 1),
                  "，", "$Q$", " 的 ", "$(%d,%d)$" % (nb[1] + 1, nb[0] + 1), " 寫 ", "$u_%d=%d$" % (k + 1, u[k]),
                  wait=0.2)
        column_insert_anim(scene, Pt, bot, path, rt=rt)
        sq = place_anim(scene, Qt, top, (nb[1], nb[0]), rt=rt)
        scene.play(sq.animate.set_fill(BLACK, opacity=0), Pt.sq[nb].animate.set_fill(BLACK, opacity=0),
                   top.animate.set_color(MUTED_COLOR), bot.animate.set_color(MUTED_COLOR), run_time=0.25)
        scene.wait(1.6 if k < 2 else 1.0)
    assert TP == P
    scene.play(FadeIn(res, shift=0.2 * UP), run_time=0.7)
    scene.say("結果 ", "$P=112/333$", "、", "$Q=11/22/33$", "：形狀互為共軛", wait=SLOW * 0.35)
    scene.say(r"$3\times3$", " 的 ", "$511$", " 個非零 0-1 矩陣，一一對應到這樣的表對（程式核對）", wait=SLOW * 0.35)


# ---------------------------------------------------------------- 3. 對偶 Cauchy
def part_cauchy(scene):
    f1 = tex(r"\prod_{i,j}(1+x_iy_j)=\sum_\lambda s_\lambda(x)\,s_{\tilde\lambda}(y)", 48).move_to(np.array([0, 1.9, 0]))
    l1 = zh("對偶 Cauchy（Littlewood）", font_size=26, color=ACC).next_to(f1, UP, buff=0.3)
    f0 = tex(r"\prod_{i,j}\frac{1}{1-x_iy_j}=\sum_\lambda s_\lambda(x)\,s_\lambda(y)", 34).set_color(MUTED_COLOR)
    f0.move_to(np.array([0, 0.35, 0]))
    l0 = zh("對照 R-S-K：", font_size=24, color=MUTED_COLOR).next_to(f0, LEFT, buff=0.3)
    e19 = mixed("練習 19：列和 ", r"$\lambda$", "、行和 ", r"$\mu$", " 的 0-1 矩陣個數 ",
                r"$=\sum_\nu K_{\tilde\nu\lambda}K_{\nu\mu}$", font_size=28).move_to(np.array([0, -1.05, 0]))
    terms = ex19_terms(*PZ1)
    s = r",\quad ".join(r"\nu=%s:\ %d\cdot%d" % (tuple_str(nu), a, b) for nu, a, b in terms)
    tot = sum(a * b for _, a, b in terms)
    e19b = tex(r"\lambda=(3,2,1),\ \mu=(2,2,2):\quad " + s + r"\quad\Rightarrow\ %d" % tot, 30)
    e19b.next_to(e19, DOWN, buff=0.45)
    assert_in_frame(f1, l1, f0, l0, e19, e19b)
    assert_apart(f1, VGroup(f0, l0), 0.2)
    assert_apart(VGroup(f0, l0), e19, 0.2)

    scene.say("把每個 0-1 矩陣記成單項式 ", r"$\prod_{a_{ij}=1}x_iy_j$", "，全部加起來：",
              wait=SLOW * 0.2)
    scene.play(FadeIn(l1), Write(f1), run_time=1.6)
    scene.say("右邊的 ", r"$\tilde\lambda$", " 正是 ", "$Q$", " 的形狀：共軛", wait=SLOW * 0.35)
    scene.play(FadeIn(f0), FadeIn(l0), run_time=0.8)
    scene.say("對照 R-S-K 的 Cauchy 公式：沒有共軛、分母變成 ", "$1-x_iy_j$", wait=SLOW * 0.35)
    scene.play(FadeIn(e19, shift=0.2 * UP), run_time=0.8)
    scene.say("取係數：個數 ", r"$=\sum_\nu K_{\tilde\nu\lambda}K_{\nu\mu}$", wait=SLOW * 0.3)
    scene.play(FadeIn(e19b), run_time=0.8)
    scene.say("第一題：", r"$1\cdot2+1\cdot1=3$", " 個", wait=SLOW * 0.35)


# ---------------------------------------------------------------- 4. 揭曉與 Gale–Ryser
def part_reveal(scene):
    sols = zero_one_matrices(*PZ1)
    Gs = [sum_grid(*PZ1, 0.5, (-5.6 + 2.15 * k, 1.5)) for k in range(len(sols))]
    fills = [ones(G, B) for G, B in zip(Gs, sols)]
    c1 = mixed("$%d$" % len(sols), " 個", font_size=28, color=OK).next_to(VGroup(*Gs), UP, buff=0.25)
    G2 = sum_grid(*PZ2, 0.5, (3.9, 1.5))
    x2 = tex(r"\times", 90, BAD).move_to(G2.grid)
    c2 = mixed("$0$", " 個", font_size=28, color=BAD).next_to(G2, UP, buff=0.25)
    gr = mixed("Gale–Ryser（練習 20）：存在 ", r"$\Leftrightarrow$", " ", r"$\mu\trianglelefteq\tilde\lambda$",
               font_size=28).move_to(np.array([0, -0.45, 0]))
    lt1, lt2 = conjugate(PZ1[0]), conjugate(PZ2[0])
    a1, b1 = partial(PZ1[1], 3), partial(lt1, 3)
    cmp1 = r",\ ".join(r"%d\le%d" % (a, b) for a, b in zip(a1, b1))
    r1 = mixed("$" + tuple_str(PZ1[1]) + r"\trianglelefteq" + tuple_str(lt1) + "$", "：", "$" + cmp1 + "$",
               font_size=26, color=OK)
    a2, b2 = partial(PZ2[1], 4), partial(lt2, 4)
    r2 = mixed("$" + tuple_str(PZ2[1]) + r"\ \text{vs}\ " + tuple_str(lt2) + "$", "：", "$%d>%d$" % (a2[0], b2[0]),
               "（只有兩列，第一行放不下 3 個 1）", font_size=26, color=BAD)
    rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(gr, DOWN, buff=0.45)
    assert_in_frame(*Gs, c1, G2, c2, gr, rows)
    assert_apart(VGroup(*Gs), G2, 0.5)
    for a, b in zip(Gs, Gs[1:]):
        assert_apart(a, b, 0.2)
    assert_apart(VGroup(*Gs, G2), gr, 0.3)

    scene.say("揭曉：第一題有 ", "$%d$" % len(sols), " 個填法", wait=0.3)
    scene.play(*[FadeIn(G) for G in Gs], run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(f, scale=0.8) for f in fills], lag_ratio=0.3), FadeIn(c1), run_time=1.4)
    scene.wait(SLOW * 0.25)
    scene.say("第二題：一個都沒有", wait=0.3)
    scene.play(FadeIn(G2), FadeIn(c2), run_time=0.7)
    scene.play(Write(x2), run_time=0.6)
    scene.wait(SLOW * 0.2)
    scene.play(FadeIn(gr, shift=0.2 * UP), run_time=0.8)
    scene.say("Gale–Ryser：存在 ", r"$\Leftrightarrow$", " 行和 ", r"$\mu$", " 被列和的共軛 ", r"$\tilde\lambda$",
              " 支配", wait=SLOW * 0.35)
    scene.play(FadeIn(r1), run_time=0.7)
    scene.say("第一題：部分和 ", "$2\\le3,\\ 4\\le5,\\ 6\\le6$", "，成立", wait=SLOW * 0.35)
    scene.play(FadeIn(r2), run_time=0.7)
    scene.say("第二題：", r"$\tilde\lambda=(2,2,2)$", "，第一個部分和 ", "$3>2$", "，不成立", wait=SLOW * 0.35)
    scene.say("收束：能不能填，看支配序", wait=SLOW * 0.5)


class SceneF60ZeroOne(ChuScene):
    def construct(self):
        self.show_header("F60 填格子遊戲：0-1 矩陣與 Gale–Ryser")
        check_math()
        part_puzzle(self)
        self.clear_stage()
        part_knuth(self)
        self.clear_stage()
        part_cauchy(self)
        self.clear_stage()
        part_reveal(self)
        self.wait(1.0)
