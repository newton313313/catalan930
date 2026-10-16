"""
Scene F56 —— 拆積木：對偶字母與 evacuation（Fulton §A.1，書 p.183–186；§A.3 一句）
執行（在 codes/ 內）：manimgl scenes/sceneF56_evacuation.py SceneF56Evacuation
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_appendix import dual_word, evacuation, evacuation_steps
from utils.fulton_draw import WordMob, assert_apart, assert_in_frame, tableau_mob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import insert_word, shape

SLOW = 6.0
ACC = YELLOW
STAR = TEAL_B
N0 = 3
W0 = (3, 1, 2, 1)
T_SMALL = ((1, 2), (3,))
T_BOOK = ((1, 2, 2, 3), (2, 3, 5, 5), (4, 4, 6), (5, 6))
N_BOOK = 6


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def slide_moves(T):
    """拿掉左上角之後做一次 jeu de taquin：回傳 (移動 [(從, 到)], 空出的格子, 新表)。"""
    cells = {(i, j): v for i, r in enumerate(T) for j, v in enumerate(r)}
    del cells[(0, 0)]
    hole, moves = (0, 0), []
    while True:
        i, j = hole
        right, below = cells.get((i, j + 1)), cells.get((i + 1, j))
        if right is None and below is None:
            break
        src = (i, j + 1) if below is None or (right is not None and right < below) else (i + 1, j)
        cells[hole] = cells.pop(src)
        moves.append((src, hole))
        hole = src
    rows = []
    i = 0
    while (i, 0) in cells:
        rows.append(tuple(cells[(i, j)] for j in range(len(T[i])) if (i, j) in cells))
        i += 1
    return moves, hole, tuple(rows)


def star_rows(T, N):
    """T* 寫成 x* 的樣子：數字 y 就是 (N+1-y)*。"""
    return [[N + 1 - y for y in r] for r in T]


def check_math():
    assert dual_word(W0, N0) == (3, 2, 3, 1) and tuple(reversed(W0)) == (1, 2, 1, 3)
    for T, N in ((T_SMALL, N0), (T_BOOK, N_BOOK)):
        cur = T
        for nxt, b, v in evacuation_steps(T, N):
            moves, hole, new = slide_moves(cur) if sum(map(len, cur)) > 1 else ([], (0, 0), ())
            assert new == nxt and hole == b and v == N + 1 - cur[0][0]
            cur = nxt
    assert evacuation_steps(T_SMALL, N0)[0][:2] == (((2,), (3,)), (0, 1))
    assert evacuation(T_SMALL, N0) == ((1, 3), (2,)) and evacuation(((1, 3), (2,)), N0) == T_SMALL
    st = evacuation_steps(T_BOOK, N_BOOK)
    assert st[0][0] == ((2, 2, 2, 3), (3, 4, 5, 5), (4, 6, 6), (5,)) and st[0][1] == (3, 1) and st[0][2] == 6
    Ts = evacuation(T_BOOK, N_BOOK)
    assert Ts == ((1, 1, 2, 3), (2, 2, 3, 5), (4, 4, 5), (5, 6))
    assert star_rows(Ts, N_BOOK) == [[6, 6, 5, 4], [5, 5, 4, 2], [3, 3, 2], [2, 1]]
    assert shape(Ts) == shape(T_BOOK) and evacuation(Ts, N_BOOK) == T_BOOK
    P, Pd = insert_word(W0), insert_word(dual_word(W0, N0))
    assert P == ((1, 1), (2,), (3,)) and Pd == ((1, 3), (2,), (3,)) and evacuation(P, N0) == Pd
    # Knuth 關係 x z y ≡ z x y（x ≤ y < z）在 * 之下變成 y* z* x* ≡ y* x* z*（z* < y* ≤ x*）
    for x in range(1, 4):
        for y in range(x, 4):
            for z in range(y + 1, 4):
                a, b = dual_word((x, z, y), 3), dual_word((z, x, y), 3)
                assert a == (4 - y, 4 - z, 4 - x) and b == (4 - y, 4 - x, 4 - z)
                assert insert_word(a) == insert_word(b) and 4 - z < 4 - y <= 4 - x


# ---------------------------------------------------------------- 棋盤（evacuation 用）
class Board:
    def __init__(self, T, cs, top_left, fs=None):
        self.cs, self.fs = cs, fs or 60 * cs
        self.tl = np.array([top_left[0], top_left[1], 0.0])
        self.sq = {}
        for i, r in enumerate(T):
            for j in range(len(r)):
                self.sq[(i, j)] = Square(cs).set_stroke(GREY_B, 3).move_to(self.pos(i, j))
        self.ent = {(i, j): tex(str(v), self.fs).move_to(self.pos(i, j)) for i, r in enumerate(T)
                    for j, v in enumerate(r)}
        self.star = {}
        self.grid = VGroup(*self.sq.values())
        self.nums = VGroup(*self.ent.values())

    def pos(self, i, j):
        return self.tl + (j + 0.5) * self.cs * RIGHT + (i + 0.5) * self.cs * DOWN

    def group(self):
        return VGroup(self.grid, self.nums)


def evac_step(scene, b, cur, N, rt=1.0):
    x = cur[0][0]
    m = b.ent.pop((0, 0))
    scene.play(m.animate.set_color(ACC).scale(1.25), run_time=0.35 * rt)
    scene.play(FadeOut(m, shift=0.7 * b.cs * (LEFT + UP)), run_time=0.4 * rt)
    if sum(map(len, cur)) > 1:
        moves, hole, new = slide_moves(cur)
    else:
        moves, hole, new = [], (0, 0), ()
    for src, dst in moves:
        mob = b.ent.pop(src)
        b.ent[dst] = mob
        scene.play(mob.animate.move_to(b.pos(*dst)), run_time=0.4 * rt)
    s = tex("%d^*" % x, b.fs * 0.8, STAR).move_to(b.pos(*hole))
    b.star[hole] = (s, x)
    scene.play(FadeIn(s, scale=1.4), b.sq[hole].animate.set_fill(STAR, opacity=0.15), run_time=0.45 * rt)
    return new


def stars_to_numbers(scene, b, N, run_time=1.0):
    anims = []
    for cell, (s, x) in list(b.star.items()):
        t = tex(str(N + 1 - x), b.fs, STAR).move_to(s)
        anims.append(Transform(s, t))
    scene.play(*anims, run_time=run_time)


# ---------------------------------------------------------------- 1. 對偶字
def part_dual_word(scene):
    rule = mixed("$x^*=N+1-x$", "$N=3:\\ 1^*=3,\\ 2^*=2,\\ 3^*=1$", font_size=30, buff=0.9)
    rule.move_to(np.array([0, 2.5, 0]))
    wm = WordMob(W0, size=0.72, center=np.array([0.4, 1.25, 0]))
    wm2 = WordMob(W0, size=0.72, center=np.array([0.4, 1.25, 0]))
    lab = tex("w=", 40).next_to(wm, LEFT, buff=0.3)
    lab2 = tex("w^*=", 40).next_to(wm, LEFT, buff=0.3).shift(1.15 * DOWN)
    k1 = tex(r"x\,z\,y\ \equiv\ z\,x\,y\qquad (x\le y<z)", 36).move_to(np.array([0, -0.95, 0]))
    arr = tex(r"\Big\Downarrow\ {}^*", 36).move_to(np.array([0, -1.7, 0]))
    k2 = tex(r"y^*z^*x^*\ \equiv\ y^*x^*z^*\qquad (z^*<y^*\le x^*)", 36).move_to(np.array([0, -2.5, 0]))
    assert_in_frame(rule, wm, lab, lab2, k1, arr, k2)
    assert_apart(rule, wm, 0.2)
    assert_apart(wm.copy().shift(1.15 * DOWN), k1, 0.2)

    scene.say("問：把一個字倒過來讀、每個字母換成「對面」的字母，", wait=SLOW * 0.4)
    scene.say("它的表會變成什麼？", wait=SLOW * 0.3)
    scene.play(FadeIn(rule), run_time=0.8)
    scene.say("在 ", "$[N]$", " 上，", "$x$", " 的對面是 ", "$x^*=N+1-x$", "：大小顛倒", wait=SLOW * 0.5)
    scene.play(FadeIn(wm), FadeIn(wm2), Write(lab), run_time=0.8)
    scene.play(wm2.animate.shift(1.15 * DOWN), run_time=0.7)
    n = len(W0)
    tiles = list(wm2.tiles)
    scene.say("例：", "$w=3121$", "。第一步，倒過來讀：", "$1213$", wait=0.6)
    scene.play(*[t.animate(path_arc=PI / 2).move_to(wm2.slot(n - 1 - k)) for k, t in enumerate(tiles)],
               run_time=1.2)
    scene.wait(SLOW * 0.3)
    scene.say("第二步，每個字母換成對偶：", "$1\\mapsto 3,\\ 2\\mapsto 2$", wait=0.4)
    scene.play(*[Transform(t.label, tex(str(N0 + 1 - t.value), 0.72 * 56, STAR).move_to(t.label)) for t in tiles],
               *[t.square.animate.set_stroke(STAR).set_fill(STAR, opacity=0.15) for t in tiles],
               Write(lab2), run_time=1.0)
    scene.say("得到 ", "$w^*=3231$", "（", "$N=3$", "）", wait=SLOW * 0.4)
    scene.play(FadeIn(k1, shift=0.2 * DOWN), run_time=0.8)
    scene.say("Knuth 關係呢？", "$x\\,z\\,y\\equiv z\\,x\\,y$", " 兩邊同時取 ", "$*$", wait=SLOW * 0.3)
    scene.play(FadeIn(arr), FadeIn(k2, shift=0.2 * DOWN), run_time=0.9)
    scene.say("變成 ", "$y^*z^*x^*\\equiv y^*x^*z^*$", "：還是一條 Knuth 關係", wait=SLOW * 0.4)
    scene.say("所以 ", "$w\\equiv w'$", " 就推得 ", "$w^*\\equiv w'^*$", wait=SLOW * 0.4)


# ---------------------------------------------------------------- 2. evacuation：小例子
def part_small(scene):
    b = Board(T_SMALL, 1.0, (-5.0, 1.4))
    tlab = tex("T", 44).next_to(b.grid, UP, buff=0.3)
    steps = VGroup(
        mixed("1. 拿走左上角的 ", "$x$", font_size=28),
        mixed("2. 剩下的斜表滑成一般表 ", r"$\Delta T$", font_size=28),
        mixed("3. 空出的格子填 ", "$x^*$", font_size=28),
        mixed("4. 對 ", r"$\Delta T$", " 重複，直到拿完", font_size=28),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(np.array([2.6, 1.0, 0]))
    res = mixed("$T^*=$", tableau_mob(evacuation(T_SMALL, N0), cs=0.6), font_size=32)
    res.move_to(np.array([1.5, -1.9, 0]))
    back = mixed(r"$(T^*)^*=T$", font_size=30, color=MUTED_COLOR).next_to(res, RIGHT, buff=0.8)
    assert_in_frame(b.group(), tlab, steps, res, back)
    assert_apart(b.group(), steps, 0.4)
    assert_apart(steps, res, 0.2)

    scene.say("evacuation：把一張表一格一格「拆掉」，再按對偶填回去", wait=SLOW * 0.3)
    scene.play(FadeIn(b.group()), Write(tlab), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(s, shift=0.2 * RIGHT) for s in steps], lag_ratio=0.4), run_time=1.8)
    scene.say("小例子 ", "$T=12/3$", "，", "$N=3$", wait=SLOW * 0.2)
    cur = T_SMALL
    caps = [("拿走 ", "$1$", "；", "$2$", " 比 ", "$3$", " 小，滑到左邊；空格填 ", "$1^*$"),
            ("拿走 ", "$2$", "；", "$3$", " 往上滑；空格填 ", "$2^*$"),
            ("最後拿走 ", "$3$", "，填 ", "$3^*$")]
    for cap in caps:
        scene.say(*cap, wait=0.3)
        cur = evac_step(scene, b, cur, N0, rt=1.6)
        scene.wait(SLOW * 0.3)
    scene.say("把 ", "$x^*$", " 換回數字：", "$1^*=3,\\ 2^*=2,\\ 3^*=1$", wait=0.3)
    stars_to_numbers(scene, b, N0)
    scene.play(FadeIn(res, shift=0.2 * UP), run_time=0.8)
    scene.say("得到 ", "$T^*=13/2$", "：形狀沒變", wait=SLOW * 0.3)
    scene.play(FadeIn(back), run_time=0.6)
    scene.say("再做一次就回到 ", "$12/3$", "：", r"$(T^*)^*=T$", wait=SLOW * 0.4)


# ---------------------------------------------------------------- 3. 書上的例子
def part_book(scene):
    cs = 0.66
    b = Board(T_BOOK, cs, (-5.6, 2.0))
    tlab = tex("T", 40).next_to(b.grid, LEFT, buff=0.35)
    orig = tableau_mob(T_BOOK, cs=0.48).move_to(np.array([2.0, 1.15, 0]))
    olab = tex("T", 34).next_to(orig, UP, buff=0.2)
    first = mixed(r"$\Delta T=2223/3455/466/5$", font_size=28).move_to(np.array([2.6, -1.0, 0]))
    first2 = mixed("$1^*$", " 放在第 4 列第 2 格", font_size=28).next_to(first, DOWN, buff=0.3)
    Ts = evacuation(T_BOOK, N_BOOK)
    num = tableau_mob(Ts, cs=0.48, entry_color=STAR).move_to(np.array([5.3, 1.15, 0]))
    nlab = tex("T^*", 34).next_to(num, UP, buff=0.2)
    eq = tex("=", 40).move_to(np.array([3.65, 1.15, 0]))
    starlab = mixed(r"$T^*=6^*6^*5^*4^*/5^*5^*4^*2^*/3^*3^*2^*/2^*1^*$", font_size=24)
    starlab.move_to(np.array([-0.2, -2.55, 0]))
    assert_in_frame(b.group(), tlab, orig, olab, first, first2, num, nlab, starlab)
    assert_apart(b.group(), VGroup(orig, first, first2), 0.4)
    assert_apart(orig, num, 0.3)
    assert_apart(b.group(), starlab, 0.15)

    scene.say("書上的例子（p.184）：", "$N=6$", "，", "$x^*=7-x$", wait=SLOW * 0.3)
    scene.play(FadeIn(b.group()), Write(tlab), FadeIn(orig), FadeIn(olab), run_time=1.0)
    scene.say("第一步：拿走 ", "$1$", "，洞一路滑到右下", wait=0.2)
    cur = evac_step(scene, b, T_BOOK, N_BOOK, rt=1.5)
    scene.play(FadeIn(first), FadeIn(first2), run_time=0.8)
    scene.say("得到 ", r"$\Delta T$", "，", "$1^*$", " 落在第 4 列第 2 格", wait=SLOW * 0.4)
    scene.say("快轉：每一步都是拿走、滑動、填 ", "$x^*$", wait=0.2)
    scene.play(FadeOut(first), FadeOut(first2), run_time=0.4)
    while cur:
        cur = evac_step(scene, b, cur, N_BOOK, rt=0.4)
    scene.play(FadeIn(starlab), run_time=0.8)
    scene.say("拆完了：每一格都填好了 ", "$x^*$", wait=SLOW * 0.3)
    stars_to_numbers(scene, b, N_BOOK)
    scene.play(FadeIn(eq), FadeIn(num), FadeIn(nlab), run_time=0.8)
    scene.say("換成數字：", "$T^*=1123/2235/445/56$", "，形狀不變", wait=SLOW * 0.5)


# ---------------------------------------------------------------- 4. 對偶定理
def part_theorem(scene):
    title = zh("對偶定理", font_size=34, color=ACC).move_to(np.array([-4.6, 2.6, 0]))
    items = VGroup(
        mixed("(1) ", "$T^*$", " 和 ", "$T$", " 形狀相同", font_size=28),
        mixed("(2) ", r"$(T^*)^*=T$", font_size=28),
        mixed("(3) ", r"$P(w^*)=P(w)^*$", font_size=28),
        mixed("(4) ", r"$\omega\leftrightarrow(P,Q)\ \Rightarrow\ \omega^*\leftrightarrow(P^*,Q^*)$", font_size=28),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    items.next_to(title, DOWN, buff=0.4, aligned_edge=LEFT)
    pa = tableau_mob(insert_word(W0), cs=0.45)
    pb = tableau_mob(insert_word(dual_word(W0, N0)), cs=0.45, entry_color=STAR)
    arr = tex(r"\xrightarrow{\ *\ }", 40)
    ex = VGroup(pa, arr, pb).arrange(RIGHT, buff=0.45).move_to(np.array([4.4, 1.1, 0]))
    la = tex("P(3121)", 26).next_to(pa, DOWN, buff=0.22)
    lb = tex("P(3231)", 26).next_to(pb, DOWN, buff=0.22)
    app = mixed("應用：", r"$[T,U]\mapsto[U^*,T^*]$", " 給出 ", r"$c^\nu_{\lambda\mu}=c^\nu_{\mu\lambda}$",
                " 的一一對應", font_size=28).move_to(np.array([0, -1.75, 0]))
    a3 = mixed("§A.3：把這種對應推廣成「LR 對應」（形狀改變定理）", font_size=24, color=MUTED_COLOR)
    a3.next_to(app, DOWN, buff=0.35)
    assert_in_frame(title, items, ex, la, lb, app, a3)
    assert_apart(items, VGroup(ex, la, lb), 0.3)
    assert_apart(items, app, 0.2)

    scene.say("這些現象合起來就是對偶定理", wait=0.3)
    scene.play(Write(title), run_time=0.6)
    for k, it in enumerate(items):
        scene.play(FadeIn(it, shift=0.2 * RIGHT), run_time=0.6)
        if k == 2:
            scene.play(FadeIn(pa), FadeIn(la), run_time=0.6)
            scene.play(Write(arr), FadeIn(pb), FadeIn(lb), run_time=0.8)
            scene.say("例：", "$P(3121)=11/2/3$", "，", "$P(3231)=13/2/3$", "，正是 ", "$P(3121)^*$",
                      wait=SLOW * 0.6)
        elif k == 3:
            scene.say("陣列 ", r"$\omega$", " 也一樣：", r"$\omega^*$", " 對應到 ", "$(P^*,Q^*)$", wait=SLOW * 0.4)
        else:
            scene.wait(SLOW * 0.25)
    scene.play(FadeIn(app, shift=0.2 * UP), run_time=0.8)
    scene.say("應用：", r"$[T,U]\mapsto[U^*,T^*]$", " 把 ", r"$c^\nu_{\lambda\mu}$", " 和 ",
              r"$c^\nu_{\mu\lambda}$", " 的表一一對上", wait=SLOW * 0.5)
    scene.play(FadeIn(a3), run_time=0.6)
    scene.say("§A.3 把這種一一對應推廣成 LR 對應", wait=SLOW * 0.4)
    scene.say("收束：evacuation＝把字母表倒過來看同一張表", wait=SLOW * 0.6)


class SceneF56Evacuation(ChuScene):
    def construct(self):
        self.show_header("F56 拆積木：對偶字母與 evacuation")
        check_math()
        part_dual_word(self)
        self.clear_stage()
        part_small(self)
        self.clear_stage()
        part_book(self)
        self.clear_stage()
        part_theorem(self)
        self.wait(1.0)
