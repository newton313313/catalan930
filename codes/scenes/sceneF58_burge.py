"""
Scene F58 —— 反著排：Burge 對應（Fulton §A.4.1，書 p.197–201；作法 (1b)、命題 2）
執行（在 codes/ 內）：manimgl scenes/sceneF58_burge.py SceneF58Burge
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import antilex_sort, burge, column_insert, lex_sort, matrix_to_pairs, rsk_array
from utils.fulton_draw import TwoRowArray, assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.rep_draw import MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import shape

SLOW = 8.0
ACC = YELLOW
BUMP = PINK
UCOL = ORANGE
VCOL = BLUE_B
A = [[1, 2, 0], [0, 1, 1], [1, 1, 1]]
PAIRS = [(1, 1), (1, 2), (1, 2), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def check_math():
    assert matrix_to_pairs(A) == PAIRS
    u, v = zip(*PAIRS)
    assert lex_sort(u, v) == ((1, 1, 1, 2, 2, 3, 3, 3), (1, 2, 2, 2, 3, 1, 2, 3))
    assert antilex_sort(u, v) == ((3, 3, 3, 2, 2, 1, 1, 1), (1, 2, 3, 2, 3, 1, 2, 2))
    R, S = burge(A)
    assert R == ((1, 1, 2, 2, 2), (2, 3), (3,)) and S == ((1, 1, 1, 3, 3), (2, 2), (3,))
    assert shape(R) == shape(S) == (5, 2, 1)
    P, Q = rsk_array(u, v)
    assert P == ((1, 1, 2, 2, 2, 3), (2, 3)) and Q == ((1, 1, 1, 2, 2, 3), (3, 3)) and shape(P) == (6, 2)
    flat = lambda T: sorted(x for r in T for x in r)
    assert flat(R) == flat(P) == sorted(v) and flat(S) == flat(Q) == sorted(u)
    # 第三步：v_6=1 擠掉第一行的 2，2 再擠第二行的 2
    T = column_insert(column_insert((), 2)[0], 2)[0]
    _, path, _ = column_insert(T, 1)
    assert antilex_sort(u, v)[1][5] == 1 and [T[i][j] for i, j in path[:-1]] == [2, 2] and path[1][1] == 1


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


def column_insert_anim(scene, lt, src, path, rt=1.0):
    """行插入：src（陣列裡的數字）飛到第一行左邊，再一行一行擠過去。回傳新格子的方塊。"""
    off = LEFT
    inc = src.copy()
    scene.play(inc.animate.move_to(lt.pos(*path[0]) + off * lt.cs).set_color(ACC).scale(lt.fs / 36),
               run_time=0.5 * rt)
    for k, cell in enumerate(path):
        if cell in lt.ent:
            y = lt.ent[cell]
            stage = lt.pos(*path[k + 1]) + 0.55 * lt.cs * off
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


# ---------------------------------------------------------------- 1. 兩種排序
def part_arrays(scene):
    M = MatrixMob(A, font_size=40, center=np.array([-4.6, 1.3, 0]))
    ml = tex("A=", 40).next_to(M, LEFT, buff=0.2)
    pairs = tex(",".join("(%d,%d)" % p for p in PAIRS), 30).move_to(np.array([1.6, 2.55, 0]))
    u, v = zip(*PAIRS)
    lu, lv = lex_sort(u, v)
    au, av = antilex_sort(u, v)
    lex = TwoRowArray(lu, lv, font_size=36, center=np.array([1.8, 0.75, 0]))
    anti = TwoRowArray(au, av, font_size=36, center=np.array([1.8, -1.45, 0]))
    ll = mixed("字典序", "（R-S-K）", font_size=26).next_to(lex, UP, buff=0.2).align_to(lex, LEFT)
    la = mixed("反字典序", "（Burge）", font_size=26, color=ACC).next_to(anti, UP, buff=0.2).align_to(anti, LEFT)
    rule = mixed("上列由大到小；上列相同時，下列由小到大", font_size=24, color=MUTED_COLOR)
    rule.next_to(anti, DOWN, buff=0.3)
    assert_in_frame(M, ml, pairs, lex, anti, ll, la, rule)
    assert_apart(VGroup(M, ml), VGroup(pairs, lex, ll), 0.2)
    assert_apart(lex, anti, 0.4)
    assert_apart(VGroup(M, ml), la, 0.2)

    scene.say("問：R-S-K 用字典序；把陣列換成「上列由大到小」會發生什麼？", wait=SLOW * 0.4)
    scene.play(FadeIn(M), Write(ml), run_time=0.8)
    scene.say("書上的矩陣：第 ", "$i$", " 列第 ", "$j$", " 行的 ", "$a_{ij}$", " 就是 ", "$(i,j)$", " 的個數",
              wait=SLOW * 0.3)
    scene.play(Write(pairs), run_time=1.4)
    scene.say("八對：", "$(1,1),(1,2),(1,2),(2,2),\\dots$", wait=SLOW * 0.25)
    scene.say("例如 ", "$a_{12}=2$", "，所以 ", "$(1,2)$", " 出現兩次", wait=SLOW * 0.3)
    scene.play(FadeIn(lex), FadeIn(ll), run_time=0.9)
    scene.say("R-S-K 把它們排成字典序：上列由小到大", wait=SLOW * 0.3)
    scene.play(FadeIn(anti), FadeIn(la), run_time=0.9)
    scene.play(FadeIn(rule), run_time=0.6)
    scene.say("Burge 改用反字典序：上列遞減，同上列時下列遞增", wait=SLOW * 0.3)
    hi = [anti.col(k)[1] for k in range(3)]
    scene.play(*[h.animate.set_color(ACC) for h in hi], run_time=0.6)
    scene.say("例如上列都是 ", "$3$", " 的三對，下列是 ", "$1,2,3$", wait=SLOW * 0.35)


# ---------------------------------------------------------------- 2. 作法 (1b)
def part_build(scene):
    u, v = antilex_sort(*zip(*PAIRS))
    arr = TwoRowArray(u, v, font_size=36, center=np.array([0.6, 2.35, 0]), top_color=UCOL, bottom_color=VCOL)
    al = mixed("$u$", "$v$", font_size=28).arrange(DOWN, buff=0.28)
    al.next_to(arr, LEFT, buff=0.35)
    cs = 0.7
    R = LiveTab((), cs, (-5.2, 0.85))
    S = LiveTab((), cs, (1.3, 0.85))
    Rf, Sf = burge(A)
    ghostR = LiveTab(Rf, cs, (-5.2, 0.85)).group()
    ghostS = LiveTab(Sf, cs, (1.3, 0.85)).group()
    stage = Square(cs).move_to(R.pos(2, -1))
    rl = mixed("$R$", "：行插入 ", "$v$", font_size=28).next_to(ghostR, DOWN, buff=0.35).align_to(ghostR, LEFT)
    sl = mixed("$S$", "：在新格子放 ", "$u$", font_size=28).next_to(ghostS, DOWN, buff=0.35).align_to(ghostS, LEFT)
    assert_in_frame(arr, al, ghostR, ghostS, stage, rl, sl)
    assert_apart(VGroup(arr, al), VGroup(ghostR, ghostS), 0.3)
    assert_apart(VGroup(ghostR, stage), ghostS, 0.8)

    scene.say("作法 (1b)：從右往左，", "$v_8,\\dots,v_1$", " 依序行插入", wait=SLOW * 0.25)
    scene.play(FadeIn(arr), FadeIn(al), run_time=0.8)
    scene.play(FadeIn(rl), FadeIn(sl), run_time=0.6)
    scene.say("同時把 ", "$u_8,\\dots,u_1$", " 放進每次多出來的格子", wait=SLOW * 0.2)
    TR, TS = (), ()
    n = len(v)
    for k in range(n - 1, -1, -1):
        rt = 1.7 if k >= n - 3 else 1.0
        top, bot = arr.col(k)
        scene.play(top.animate.set_color(ACC), bot.animate.set_color(ACC), run_time=0.25)
        T0 = TR
        TR, path, nb = column_insert(TR, v[k])
        bumped = [T0[i][j] for i, j in path[:-1]]
        what = ("，擠掉 ", "$" + "\\to ".join(map(str, bumped)) + "$") if bumped else ("，直接放進新格子",)
        scene.say("第 %d 步：行插入 " % (n - k), "$v_%d=%d$" % (k + 1, v[k]), *what,
                  "；新格子寫 ", "$u_%d=%d$" % (k + 1, u[k]), wait=0.2)
        column_insert_anim(scene, R, bot, path, rt=rt)
        sq = place_anim(scene, S, top, nb, rt=rt)
        scene.play(sq.animate.set_fill(BLACK, opacity=0), R.sq[nb].animate.set_fill(BLACK, opacity=0),
                   top.animate.set_color(MUTED_COLOR), bot.animate.set_color(MUTED_COLOR), run_time=0.25)
        scene.wait(2.0 if k >= n - 3 else 1.3)
        if k == n - 2:
            scene.say("每一步：", "$R$", " 多一格，", "$S$", " 就在同一格寫下 ", "$u$", wait=SLOW * 0.25)
    assert TR == Rf
    scene.say("結果：", "$R=11222/23/3$", "，", "$S=11133/22/3$", wait=SLOW * 0.35)
    scene.say("兩張表同形狀 ", "$(5,2,1)$", "；", "$S$", " 也是半標準表", wait=SLOW * 0.35)


# ---------------------------------------------------------------- 3. 和 R-S-K 對照
def part_compare(scene):
    R, S = burge(A)
    P, Q = rsk_array(*zip(*PAIRS))
    cs = 0.55
    row1 = VGroup(tableau_mob(R, cs=cs), tableau_mob(S, cs=cs, entry_color=UCOL)).arrange(RIGHT, buff=0.8,
                                                                                        aligned_edge=UP)
    row2 = VGroup(tableau_mob(P, cs=cs), tableau_mob(Q, cs=cs, entry_color=UCOL)).arrange(RIGHT, buff=0.8,
                                                                                        aligned_edge=UP)
    row1.move_to(np.array([0.6, 1.55, 0]))
    row2.move_to(np.array([0.6, -0.95, 0]))
    row2.align_to(row1, LEFT)
    l1 = mixed("Burge：", "$(R,S)$", font_size=28, color=ACC).next_to(row1, LEFT, buff=0.6)
    l2 = mixed("R-S-K：", "$(P,Q)$", font_size=28).next_to(row2, LEFT, buff=0.6).align_to(l1, LEFT)
    s1 = tex(tuple_str(shape(R)), 32).next_to(row1, RIGHT, buff=0.5)
    s2 = tex(tuple_str(shape(P)), 32).next_to(row2, RIGHT, buff=0.5)
    prop = mixed("命題 2：(2b) 列插入＋滑動、(3b) 矩陣球（NW 序）也給出同一對 ", "$(R,S)$",
                 font_size=22, color=MUTED_COLOR).move_to(np.array([0, -2.55, 0]))
    assert_in_frame(row1, row2, l1, l2, s1, s2, prop)
    assert_apart(row1, row2, 0.4)
    assert_apart(row2, prop, 0.2)

    scene.say("對照：同一個 ", "$A$", " 用 R-S-K 得到什麼？", wait=SLOW * 0.2)
    scene.play(FadeIn(row1), FadeIn(l1), FadeIn(s1), run_time=0.9)
    scene.play(FadeIn(row2), FadeIn(l2), FadeIn(s2), run_time=0.9)
    scene.say("R-S-K：", "$P=112223/23$", "，", "$Q=111223/33$", "，形狀 ", "$(6,2)$", wait=SLOW * 0.45)
    scene.play(Indicate(s1), Indicate(s2), run_time=1.0)
    scene.say("同一個矩陣，兩種不同的表對——連形狀都不一樣", wait=SLOW * 0.45)
    scene.say("兩邊的內容一樣：", "$R,P$", " 裝的是 ", "$v$", "（行號），", "$S,Q$", " 裝的是 ", "$u$", "（列號）",
              wait=SLOW * 0.4)
    scene.play(FadeIn(prop), run_time=0.7)
    scene.say("命題 2：列插入＋滑動、或矩陣球（從 NW 編號）也得到同一對 ", "$(R,S)$", wait=SLOW * 0.5)
    scene.say("收束：換一個排序，就換一個對應", wait=SLOW * 0.5)


class SceneF58Burge(ChuScene):
    def construct(self):
        self.show_header("F58 反著排：Burge 對應")
        check_math()
        part_arrays(self)
        self.clear_stage()
        part_build(self)
        self.clear_stage()
        part_compare(self)
        self.wait(1.0)
