"""
Scene F57 —— 打擂台：行插入（Fulton §A.2，書 p.186–189；命題 1、練習 6）
執行（在 codes/ 內）：manimgl scenes/sceneF57_column_bumping.py SceneF57ColumnBumping
"""
import sys
from itertools import permutations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import column_insert, column_insert_word, dual_word
from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob, word_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import insert_word, row_insert, rsk, transpose

SLOW = 7.0
ACC = YELLOW
BUMP = PINK
OK = "#7CE38B"
T0 = ((1, 3), (2,))
W = (2, 4, 1, 3, 5)
WREV = tuple(reversed(W))
P_W = ((1, 3, 5), (2, 4))


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def tstr(T):
    return "/".join("".join(map(str, r)) for r in T)


def describe(x, T, path):
    """字幕用：x 擠掉了哪些數（由路徑算出）。"""
    bumped = [T[i][j] for i, j in path[:-1]]
    if not bumped:
        return ["$%d$" % x, " 直接放進新格子"]
    return ["$%d$" % x, " 擠掉 ", "$" + "\\to ".join(map(str, bumped)) + "$"]


def check_math():
    assert column_insert(T0, 1) == (((1, 1, 3), (2,)), [(0, 0), (0, 1), (0, 2)], (0, 2))
    assert column_insert(T0, 2) == (((1, 2, 3), (2,)), [(1, 0), (0, 1), (0, 2)], (0, 2))
    assert insert_word(W) == P_W and column_insert_word(WREV) == P_W
    assert WREV == (5, 3, 1, 4, 2)
    assert insert_word(WREV) == ((1, 2), (3, 4), (5,)) == transpose(P_W)
    for w in permutations(range(1, 6)):
        assert column_insert_word(tuple(reversed(w))) == insert_word(w)
        assert insert_word(tuple(reversed(w))) == transpose(insert_word(w))
        assert transpose(rsk(tuple(reversed(w)))[1]) == rsk(dual_word(w, 5))[1]
    assert rsk(WREV)[1] == ((1, 4), (2, 5), (3,)) and dual_word(W, 5) == (1, 3, 5, 2, 4)
    assert rsk(dual_word(W, 5))[1] == ((1, 2, 3), (4, 5))


# ---------------------------------------------------------------- 會動的表
class LiveTab:
    def __init__(self, T, cs, top_left, fs=None):
        self.cs, self.fs = cs, fs or 60 * cs
        self.tl = np.array([top_left[0], top_left[1], 0.0])
        self.sq, self.ent = {}, {}
        for i, r in enumerate(T):
            for j, v in enumerate(r):
                self.sq[(i, j)] = Square(cs).set_stroke(GREY_B, 3).move_to(self.pos(i, j))
                self.ent[(i, j)] = tex(str(v), self.fs).move_to(self.pos(i, j))

    def pos(self, i, j):
        return self.tl + (j + 0.5) * self.cs * RIGHT + (i + 0.5) * self.cs * DOWN

    def group(self):
        return VGroup(*self.sq.values(), *self.ent.values())


def animate_insert(scene, lt, x, path, mode, rt=1.0):
    """播放一次插入：mode = 'row'（列插入，從上面掉進來）或 'col'（行插入，從左邊推進來）。"""
    off = UP if mode == "row" else LEFT
    inc = tex(str(x), lt.fs, ACC).move_to(lt.pos(*path[0]) + off * lt.cs)
    scene.play(FadeIn(inc, shift=-0.3 * off), run_time=0.35 * rt)
    for k, cell in enumerate(path):
        if cell in lt.ent:
            y = lt.ent[cell]
            stage = lt.pos(*path[k + 1]) + 0.55 * lt.cs * off
            scene.play(y.animate.set_color(BUMP), lt.sq[cell].animate.set_fill(ACC, opacity=0.25),
                       run_time=0.25 * rt)
            scene.play(inc.animate.move_to(lt.pos(*cell)), y.animate.move_to(stage), run_time=0.5 * rt)
            lt.ent[cell] = inc
            inc = y
        else:
            sq = Square(lt.cs).set_stroke(GREY_B, 3).move_to(lt.pos(*cell)).set_fill(ACC, opacity=0.25)
            lt.sq[cell] = sq
            scene.play(FadeIn(sq), inc.animate.move_to(lt.pos(*cell)), run_time=0.5 * rt)
            lt.ent[cell] = inc
    scene.play(*[lt.sq[c].animate.set_fill(BLACK, opacity=0) for c in path],
               *[lt.ent[c].animate.set_color(WHITE) for c in path], run_time=0.3 * rt)


# ---------------------------------------------------------------- 1. 規則
def part_rule(scene):
    rule = VGroup(
        mixed("行插入：", "$x$", " 在第一行擠掉最上面的 ", r"$\ge x$", " 的數，", font_size=28),
        mixed("被擠的數去下一行；沒有就放在該行底部", font_size=28),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(np.array([0, 2.3, 0]))
    A = LiveTab(T0, 0.85, (-4.6, 1.0))
    B = LiveTab(T0, 0.85, (1.8, 1.0))
    ra = mixed("$1\\to 13/2$", "$=113/2$", font_size=28).move_to(np.array([-3.4, -1.3, 0]))
    rb = mixed("$2\\to 13/2$", "$=123/2$", font_size=28).move_to(np.array([3.0, -1.3, 0]))
    note = mixed("對照：列插入擠掉第一個 ", "$>x$", " 的數；行插入擠掉第一個 ", r"$\ge x$", " 的數",
                 font_size=24, color=MUTED_COLOR).move_to(np.array([0, -2.4, 0]))
    assert_in_frame(rule, A.group(), B.group(), ra, rb, note)
    assert_apart(rule, VGroup(A.group(), B.group()), 0.5)
    assert_apart(A.group(), B.group(), 1.5)
    assert_apart(VGroup(ra, rb), note, 0.2)

    scene.say("問：第 1 章的列插入換成「一行一行地擠」，", wait=SLOW * 0.3)
    scene.say("會得到不同的表嗎？", wait=SLOW * 0.25)
    scene.play(FadeIn(rule[0]), FadeIn(rule[1]), run_time=1.0)
    scene.say("規則：在第一行找最上面的 ", r"$\ge x$", " 的數，擠掉它", wait=SLOW * 0.3)
    scene.play(FadeIn(A.group()), FadeIn(B.group()), run_time=0.8)
    scene.say("例一：把 ", "$1$", " 行插入 ", "$13/2$", wait=0.3)
    nT, path, nb = column_insert(T0, 1)
    animate_insert(scene, A, 1, path, "col", rt=2.2)
    scene.play(FadeIn(ra), run_time=0.6)
    scene.say("第一行的 ", "$1\\ge 1$", " 被擠走；它擠掉第二行的 ", "$3$", "；", "$3$", " 開新的一行", wait=SLOW * 0.4)
    scene.say("例二：把 ", "$2$", " 行插入 ", "$13/2$", wait=0.3)
    nT, path, nb = column_insert(T0, 2)
    animate_insert(scene, B, 2, path, "col", rt=2.2)
    scene.play(FadeIn(rb), run_time=0.6)
    scene.say("第一行最上面的 ", r"$\ge 2$", " 是 ", "$2$", "（在底下）；它再擠掉 ", "$3$", wait=SLOW * 0.4)
    scene.play(FadeIn(note), run_time=0.6)
    scene.say("注意：相等的數也會被擠走", wait=SLOW * 0.3)


# ---------------------------------------------------------------- 2. 擂台
def part_arena(scene):
    wl = mixed("$w=24135$", font_size=34).move_to(np.array([0, 2.7, 0]))
    tl = zh("列插入", font_size=30, color=BLUE_B).move_to(np.array([-4.0, 1.95, 0]))
    tr = zh("行插入（倒著）", font_size=30, color=ORANGE).move_to(np.array([3.0, 1.95, 0]))
    sl = word_tex(W, font_size=36).next_to(tl, DOWN, buff=0.25)
    sr = word_tex(WREV, font_size=36).next_to(tr, DOWN, buff=0.25)
    L = LiveTab((), 0.75, (-5.1, 0.35))
    R = LiveTab((), 0.75, (1.9, 0.35))
    ghostL = LiveTab(P_W, 0.75, (-5.1, 0.35)).group()
    ghostR = LiveTab(P_W, 0.75, (1.9, 0.35)).group()
    stageL = Square(0.75).move_to(L.pos(-1, 2))
    stageR = Square(0.75).move_to(R.pos(0, -1))
    vs = tex(r"\Leftrightarrow", 48).move_to(np.array([-0.4, -0.4, 0]))
    prop = mixed("命題 1：依序行插入 ", "$v_r,\\dots,v_1$", " 得到同一個 ", "$P$", font_size=28)
    prop.move_to(np.array([0, -2.35, 0]))
    assert_in_frame(wl, tl, tr, sl, sr, ghostL, ghostR, stageL, stageR, vs, prop)
    assert_apart(VGroup(sl, sr), VGroup(ghostL, ghostR, stageL, stageR), 0.1)
    assert_apart(VGroup(ghostL, stageL), VGroup(ghostR, stageR), 1.0)
    assert_apart(VGroup(ghostL, ghostR), prop, 0.3)

    scene.say("擂台：同一個字 ", "$w=24135$", "，兩種插入法", wait=SLOW * 0.25)
    scene.play(FadeIn(wl), FadeIn(tl), FadeIn(tr), FadeIn(sl), FadeIn(sr), run_time=1.0)
    scene.say("左邊列插入 ", "$2,4,1,3,5$", "；右邊行插入 ", "$5,3,1,4,2$", "（倒著）", wait=SLOW * 0.3)
    TL, TR = (), ()
    n = len(W)
    for k in range(n):
        rt = 1.3 if k < 2 else 1.0
        scene.play(sl[k].animate.set_color(ACC), sr[k].animate.set_color(ACC), run_time=0.25)
        TL0, TR0 = TL, TR
        TL, pL, _ = row_insert(TL, W[k])
        TR, pR, _ = column_insert(TR, WREV[k])
        scene.say("列：", *describe(W[k], TL0, pL), "；行：", *describe(WREV[k], TR0, pR), wait=0.2)
        animate_insert(scene, L, W[k], pL, "row", rt=rt)
        animate_insert(scene, R, WREV[k], pR, "col", rt=rt)
        scene.play(sl[k].animate.set_color(MUTED_COLOR), sr[k].animate.set_color(MUTED_COLOR), run_time=0.25)
        scene.wait(2.2)
    assert TL == TR == P_W
    boxL = SurroundingRectangle(L.group(), buff=0.15).set_stroke(OK, 3)
    boxR = SurroundingRectangle(R.group(), buff=0.15).set_stroke(OK, 3)
    scene.play(ShowCreation(boxL), ShowCreation(boxR), FadeIn(vs), run_time=0.8)
    scene.say("兩邊都得到 ", "$P=135/24$", "！", wait=SLOW * 0.4)
    scene.play(FadeIn(prop, shift=0.2 * UP), run_time=0.7)
    scene.say("命題 1：對任何字都成立——中間的表不同，最後的表一樣", wait=SLOW * 0.5)


# ---------------------------------------------------------------- 3. 倒過來與轉置
def part_transpose(scene):
    A = LiveTab(P_W, 0.75, (-5.4, 2.6))
    la = tex("P(24135)", 32).next_to(A.group(), DOWN, buff=0.3)
    Bt = transpose(P_W)
    B = LiveTab(Bt, 0.75, (-0.4, 2.6))
    lb = tex("P(53142)", 32).next_to(B.group(), DOWN, buff=0.3)
    arr = tex(r"\xrightarrow{\ T\ }", 40).move_to(np.array([-1.8, 1.85, 0]))
    cond = mixed("字母相異時：", r"$P(w^{\rm rev})=P(w)^T$", font_size=26).move_to(np.array([4.2, 1.6, 0]))
    qa = tableau_mob(rsk(WREV)[1], cs=0.5)
    qb = tableau_mob(rsk(dual_word(W, 5))[1], cs=0.5)
    qrow = VGroup(tex(r"Q(w^{\rm rev})=", 30), qa, tex(r"\quad\overset{T}{\longleftrightarrow}\quad", 30),
                  tex("Q(w^*)=", 30), qb).arrange(RIGHT, buff=0.2).move_to(np.array([0, -1.45, 0]))
    ex6 = mixed("練習 6：", "$w^*=13524$", font_size=24, color=MUTED_COLOR).next_to(qrow, DOWN, buff=0.25)
    assert_in_frame(A.group(), la, B.group(), lb, arr, cond, qrow, ex6)
    assert_apart(A.group(), arr, 0.15)
    assert_apart(arr, B.group(), 0.15)
    assert_apart(VGroup(B.group(), lb), cond, 0.3)
    assert_apart(VGroup(la, lb), qrow, 0.2)

    scene.say("那麼，倒過來的字 ", "$53142$", " 用列插入會得到什麼？", wait=SLOW * 0.3)
    scene.play(FadeIn(A.group()), FadeIn(la), run_time=0.7)
    scene.play(Write(arr), run_time=0.6)
    copies = [m.copy() for m in A.ent.values()]
    sqs = [A.sq[c].copy() for c in A.sq]
    scene.play(*[c.animate.move_to(B.pos(j, i)) for c, (i, j) in zip(copies, A.ent.keys())],
               *[s.animate.move_to(B.pos(j, i)) for s, (i, j) in zip(sqs, A.sq.keys())], run_time=1.4)
    scene.play(FadeIn(lb), run_time=0.5)
    scene.say("列和行對調：", "$P(53142)=12/34/5$", "，正是 ", "$135/24$", " 的轉置", wait=SLOW * 0.4)
    scene.play(FadeIn(cond), run_time=0.7)
    scene.say("字母都不同時，", r"$P(w^{\rm rev})=P(w)^T$", wait=SLOW * 0.4)
    scene.say("理由：命題 1 說它等於把 ", "$24135$", " 依序行插入；", wait=SLOW * 0.3)
    scene.say("字母相異時，行插入就是轉置過來的列插入", wait=SLOW * 0.4)
    scene.play(FadeIn(qrow), FadeIn(ex6), run_time=0.9)
    scene.say("命題 1 的 ", "$Q$", " 用「滑進來」得到，和 R-S-K 一樣", wait=SLOW * 0.3)
    scene.say("練習 6：", r"$Q(w^{\rm rev})$", " 與 ", "$Q(w^*)$", " 互為轉置", wait=SLOW * 0.4)
    scene.say("收束：列插入與行插入是同一個對應的兩種寫法", wait=SLOW * 0.6)


class SceneF57ColumnBumping(ChuScene):
    def construct(self):
        self.show_header("F57 打擂台：行插入")
        check_math()
        part_rule(self)
        self.clear_stage()
        part_arena(self)
        self.clear_stage()
        part_transpose(self)
        self.wait(1.0)
