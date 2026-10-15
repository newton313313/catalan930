"""
Scene F54 —— 排序遊戲：Bruhat 序（Fulton §10.5，書 p.173–177；Lemma 11、命題 7、練習 8）
執行（在 codes/ 內）：manimgl scenes/sceneF54_bruhat.py SceneF54Bruhat
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.schubert import (bruhat_chain, bruhat_covers, bruhat_leq, bruhat_leq_tableau, bruhat_levels, length,
                            perm_str, perms)
from utils.scene_base import ChuScene
from utils.schubert_draw import HasseMob
from utils.styles import MUTED_COLOR, mixed, zh

SLOW = 4.4
ACCENT = YELLOW
OK = "#7CE38B"
BAD = PINK
DOT = TEAL_B
U3, V3 = (1, 3, 2), (3, 1, 2)
GAME_U, GAME_V = (2, 1, 4, 3), (4, 2, 3, 1)
INC_A, INC_B = (1, 4, 2, 3), (3, 1, 2, 4)
CH_V = (6, 7, 9, 2, 5, 1, 8, 3, 4)
CH_U = (4, 2, 8, 3, 6, 1, 7, 9, 5)
CH_U2 = (4, 2, 8, 6, 7, 1, 9, 5, 3)


def fit(m, w):
    if m.get_width() > w:
        m.set_width(w)
    return m


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def rank(w):
    return [[sum(1 for i in range(p) if w[i] <= q) for q in range(1, len(w) + 1)] for p in range(1, len(w) + 1)]


def attempt(u, v):
    """Lemma 11 的下樓梯，走不下去就停：回傳 (經過的置換, 卡住的位置 j（1 起算）或 None)。"""
    seq = [tuple(v)]
    while seq[-1] != tuple(u):
        x = seq[-1]
        j = next(i for i in range(len(u)) if u[i] != x[i])
        ks = [k for k in range(j + 1, len(u)) if x[j] > x[k] >= u[j]]
        if x[j] < u[j] or not ks:
            return seq, j + 1
        y = list(x)
        y[j], y[ks[0]] = y[ks[0]], y[j]
        seq.append(tuple(y))
    return seq, None


def prefix_rows(u, v):
    """練習 8：每個 p，排好序的前綴與逐項比較的結果。"""
    return [(sorted(u[:p]), sorted(v[:p]), all(a <= b for a, b in zip(sorted(u[:p]), sorted(v[:p]))))
            for p in range(1, len(u))]


def check_math():
    assert rank(U3) == [[1, 1, 1], [1, 1, 2], [1, 2, 3]] and rank(V3) == [[0, 0, 1], [1, 1, 2], [1, 2, 3]]
    from utils.schubert import rank_matrix
    assert all(rank(w) == rank_matrix(w) for w in perms(4))
    assert bruhat_leq(U3, V3) and not bruhat_leq(V3, U3)
    assert [(p, q) for p in range(3) for q in range(3) if rank(U3)[p][q] > rank(V3)[p][q]] == [(0, 0), (0, 1)]
    assert rank(U3)[1][1] == 1 and rank(V3)[1][1] == 1
    assert all(bruhat_leq((1, 2, 3), w) and bruhat_leq(w, (3, 2, 1)) for w in perms(3))
    assert prefix_rows(GAME_U, GAME_V) == [([2], [4], True), ([1, 2], [2, 4], True), ([1, 2, 4], [2, 3, 4], True)]
    assert bruhat_leq(GAME_U, GAME_V) and bruhat_leq_tableau(GAME_U, GAME_V)
    assert prefix_rows(INC_A, INC_B)[:2] == [([1], [3], True), ([1, 4], [1, 3], False)]
    assert prefix_rows(INC_B, INC_A)[0] == ([3], [1], False)
    assert not bruhat_leq(INC_A, INC_B) and not bruhat_leq(INC_B, INC_A)
    for u in perms(4):
        for v in perms(4):
            assert bruhat_leq(u, v) == bruhat_leq_tableau(u, v)
    assert len(bruhat_covers(3)) == 8
    assert [len(lv) for lv in bruhat_levels(4)] == [1, 3, 5, 6, 5, 3, 1]
    seq, stuck = attempt(CH_U, CH_V)
    assert stuck is None and seq == bruhat_chain(CH_U, CH_V)
    assert [perm_str(x) for x in seq] == ["679251834", "579261834", "479261835", "429761835", "428761935",
                                          "428671935", "428371965", "428361975", "428361795"]
    assert [length(x) for x in seq] == list(range(22, 13, -1))
    for a, b in zip(seq, seq[1:]):
        assert sum(x != y for x, y in zip(a, b)) == 2
    assert bruhat_leq(CH_U, CH_V)
    seq2, stuck2 = attempt(CH_U2, CH_V)
    assert [perm_str(x) for x in seq2] == ["679251834", "579261834", "479261835", "429761835", "428761935",
                                           "428671935"]
    assert stuck2 == 8 and seq2[-1][7] == 3 and CH_U2[7] == 5 and bruhat_chain(CH_U2, CH_V) is None
    assert not bruhat_leq(CH_U2, CH_V) and not bruhat_leq(CH_V, CH_U2) and length(CH_U2) == 18


# ---------------------------------------------------------------- 1. 秩矩陣
def perm_grid(w, cs, center):
    m = len(w)
    sq = VGroup(*[Square(cs).move_to(center + np.array([(q - (m - 1) / 2) * cs, ((m - 1) / 2 - p) * cs, 0]))
                  for p in range(m) for q in range(m)]).set_stroke(GREY_C, 1.5)
    dots = VGroup(*[Dot(sq[p * m + w[p] - 1].get_center(), radius=0.11).set_color(DOT) for p in range(m)])
    g = VGroup(sq, dots)
    g.sq, g.dots, g.cs, g.m = sq, dots, cs, m
    return g


def corner_rect(g, p, q):
    tl = g.sq[0].get_corner(UL)
    return Rectangle(width=q * g.cs, height=p * g.cs).move_to(tl, aligned_edge=UL).set_stroke(ACCENT, 3).set_fill(
        ACCENT, 0.12)


def num_grid(M, sp, center, fs=34):
    m = len(M)
    nums = VGroup(*[tex(str(M[p][q]), fs).move_to(center + np.array([(q - (m - 1) / 2) * sp, ((m - 1) / 2 - p) * sp, 0]))
                    for p in range(m) for q in range(m)])
    h, w = m * sp, m * sp
    br = VGroup(
        VGroup(Line(UP * h / 2, DOWN * h / 2), Line(UP * h / 2, UP * h / 2 + RIGHT * 0.12),
               Line(DOWN * h / 2, DOWN * h / 2 + RIGHT * 0.12)).shift(center + LEFT * (w / 2 + 0.02)),
        VGroup(Line(UP * h / 2, DOWN * h / 2), Line(UP * h / 2, UP * h / 2 + LEFT * 0.12),
               Line(DOWN * h / 2, DOWN * h / 2 + LEFT * 0.12)).shift(center + RIGHT * (w / 2 + 0.02)),
    ).set_stroke(WHITE, 2)
    g = VGroup(br, nums)
    g.nums, g.br = nums, br
    return g


def part_rank(scene):
    defn = tex(r"r_w(p,q)=\#\{\,i\le p:\ w(i)\le q\,\}", 44).move_to(np.array([0, 2.5, 0]))
    blocks = []
    for w, gx, mx in ((U3, -5.0, -2.6), (V3, 1.7, 4.1)):
        g = perm_grid(w, 0.6, np.array([gx, 0.55, 0]))
        M = num_grid(rank(w), 0.55, np.array([mx, 0.55, 0]))
        lg = tex("w=" + perm_str(w), 32).next_to(g, UP, buff=0.25)
        lm = tex(r"r_{%s}" % perm_str(w), 32).next_to(M, UP, buff=0.25)
        blocks.append((g, M, lg, lm))
    res = mixed(r"$r_{132}\ge r_{312}$", "（逐格）", r"$\Rightarrow\ 132\le 312$", font_size=30)
    res.move_to(np.array([0, -1.35, 0]))
    note = mixed("秩越大越「小」：", "$123$", " 最小、", "$321$", " 最大", font_size=26, color=MUTED_COLOR)
    note.move_to(np.array([0, -2.25, 0]))
    rect = corner_rect(blocks[0][0], 2, 2)
    allm = [m for b in blocks for m in b]
    assert_in_frame(defn, *allm, res, note, rect)
    assert_apart(VGroup(*blocks[0]), VGroup(*blocks[1]), 0.4)
    assert_apart(defn, VGroup(*allm), 0.15)
    assert_apart(VGroup(*allm), res, 0.2)

    scene.say("問：胞腔 ", r"$X^\circ_u$", " 什麼時候落在 ", "$X_v$", " 的邊界上？", wait=SLOW * 0.6)
    scene.say("答案要一個比大小的方法：秩矩陣", wait=SLOW * 0.2)
    scene.play(Write(defn), run_time=1.4)
    g, M, lg, lm = blocks[0]
    scene.play(FadeIn(g.sq), FadeIn(lg), run_time=0.7)
    scene.play(LaggedStart(*[GrowFromCenter(d) for d in g.dots], lag_ratio=0.3), run_time=0.9)
    scene.say("第 ", "$i$", " 列在第 ", "$w(i)$", " 行放一個點；", "$r_w(p,q)$", " 數左上角 ", r"$p\times q$", " 裡的點", wait=SLOW * 0.2)
    scene.play(FadeIn(M.br), FadeIn(lm), FadeIn(rect), run_time=0.8)
    scene.play(FadeIn(M.nums[4], scale=1.4), run_time=0.6)
    scene.say("例如 ", "$r_{132}(2,2)=1$", "：左上 ", r"$2\times2$", " 只有一個點", wait=SLOW * 0.6)
    scene.play(FadeOut(rect), LaggedStart(*[FadeIn(n) for k, n in enumerate(M.nums) if k != 4], lag_ratio=0.1),
               run_time=1.2)
    g, M, lg, lm = blocks[1]
    scene.play(FadeIn(g.sq), FadeIn(lg), LaggedStart(*[GrowFromCenter(d) for d in g.dots], lag_ratio=0.3), run_time=1.0)
    scene.play(FadeIn(M.br), FadeIn(lm), LaggedStart(*[FadeIn(n) for n in M.nums], lag_ratio=0.1), run_time=1.2)
    scene.say("$312$", " 也照做。定義：", r"$u\le v\iff r_u\ge r_v$", "（每一格都要）", wait=SLOW * 0.5)
    hi = [blocks[0][1].nums[0], blocks[0][1].nums[1], blocks[1][1].nums[0], blocks[1][1].nums[1]]
    scene.play(*[n.animate.set_color(ACCENT) for n in hi], run_time=0.6)
    scene.say("只有第一列的兩格不一樣：1 比 0 大，其餘相等", wait=SLOW * 0.5)
    scene.play(FadeIn(res, shift=0.2 * UP), run_time=0.8)
    scene.wait(SLOW * 0.5)
    scene.play(FadeIn(note), run_time=0.6)
    scene.say("單位置換 ", "$123$", " 是最底層，", "$321$", " 是最頂層", wait=SLOW * 0.7)


# ---------------------------------------------------------------- 2. 排序遊戲
def game_rows(u, v, x, n=None):
    rows = VGroup()
    for p, (a, b, ok) in enumerate(prefix_rows(u, v)[:n], start=1):
        sym = r"\le" if ok else r"\not\le"
        s = r"p=%d:\quad \{%s\}\ %s\ \{%s\}" % (p, ",".join(map(str, a)), sym, ",".join(map(str, b)))
        t = tex(s, 34)
        mark = tex(r"\checkmark", 36, OK) if ok else tex(r"\times", 36, BAD)
        rows.add(VGroup(t, mark.next_to(t, RIGHT, buff=0.3)))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(np.array([x, 0.65, 0]))
    return rows


def part_game(scene):
    t1 = tex(r"2143\ \le\ 4231\ ?", 40).move_to(np.array([-3.4, 2.45, 0]))
    r1 = game_rows(GAME_U, GAME_V, -3.4)
    c1 = tex(r"2143\le 4231", 38, OK).move_to(np.array([-3.4, -1.2, 0]))
    t2 = tex(r"1423\ \text{ vs }\ 3124", 40).move_to(np.array([3.4, 2.45, 0]))
    r2 = game_rows(INC_A, INC_B, 3.4, n=2)
    r3 = game_rows(INC_B, INC_A, 3.4, n=1)
    lab_a = tex(r"1423\le 3124\,?", 28, MUTED_COLOR)
    lab_b = tex(r"3124\le 1423\,?", 28, MUTED_COLOR)
    VGroup(lab_a, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([3.4, 1.1, 0]))
    VGroup(lab_b, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([3.4, -0.75, 0]))
    c2 = mixed("$1423$", " 和 ", "$3124$", " 不可比", font_size=30, color=BAD).move_to(np.array([3.4, -1.9, 0]))
    assert_in_frame(t1, r1, c1, t2, r2, r3, lab_a, lab_b, c2)
    assert_apart(VGroup(t1, r1, c1), VGroup(t2, r2, r3, lab_a, lab_b, c2), 0.3)
    assert_apart(r1, c1, 0.2)
    assert_apart(r2, lab_b, 0.15)
    assert_apart(r3, c2, 0.15)

    scene.say("比秩矩陣要算一大張表；練習 8 給了更快的「排序遊戲」", wait=SLOW * 0.3)
    scene.play(FadeIn(t1), run_time=0.6)
    scene.say("每個前綴各自排好序，再逐項比較：上面的每一項都不能比較大", wait=SLOW * 0.3)
    for k, row in enumerate(r1):
        scene.play(FadeIn(row[0], shift=0.2 * RIGHT), run_time=0.7)
        scene.play(FadeIn(row[1], scale=1.5), run_time=0.4)
        scene.wait(SLOW * 0.35)
    scene.play(Write(c1), run_time=0.8)
    scene.say("三個前綴都過關：", r"$2143\le 4231$", wait=SLOW * 0.6)
    scene.play(FadeIn(t2), FadeIn(lab_a), run_time=0.7)
    for row in r2:
        scene.play(FadeIn(row[0], shift=0.2 * RIGHT), run_time=0.7)
        scene.play(FadeIn(row[1], scale=1.5), run_time=0.4)
        scene.wait(SLOW * 0.25)
    scene.say("$1<3$", " 過關，但 ", r"$\{1,4\}$", " 對 ", r"$\{1,3\}$", "：第二項 ", "$4>3$", wait=SLOW * 0.4)
    scene.play(FadeIn(lab_b), FadeIn(r3[0][0], shift=0.2 * RIGHT), run_time=0.8)
    scene.play(FadeIn(r3[0][1], scale=1.5), run_time=0.4)
    scene.say("反過來第一步就輸：", "$3>1$", wait=SLOW * 0.4)
    scene.play(FadeIn(c2, shift=0.2 * UP), run_time=0.7)
    scene.say("兩個方向都不成立：Bruhat 序不是全序", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 3. Hasse 圖
def part_hasse(scene):
    h3 = HasseMob(bruhat_levels(3), bruhat_covers(3), dx=1.6, dy=1.2, font_size=30).move_to(np.array([-4.5, 0.0, 0]))
    h4 = HasseMob(bruhat_levels(4), bruhat_covers(4), dx=1.02, dy=0.76, font_size=22).move_to(np.array([2.3, 0.0, 0]))
    h3.edges.set_stroke(GREY_B, 2)
    h4.edges.set_stroke(GREY_C, 1)
    counts = VGroup()
    for k, lv in enumerate(bruhat_levels(4)):
        y = h4.node[lv[0]].get_center()[1]
        counts.add(tex(str(len(lv)), 28, ACCENT).move_to(np.array([6.3, y, 0])))
    l3 = tex("S_3", 34, MUTED_COLOR).next_to(h3, UP, buff=0.3)
    l4 = tex("S_4", 34, MUTED_COLOR).move_to(np.array([-1.0, 2.4, 0]))
    assert_in_frame(h3, h4, counts, l3, l4)
    assert_apart(h3, h4, 0.4)
    assert_apart(h4, counts, 0.15)

    scene.say("把覆蓋關係畫出來：", "$S_3$", " 有 6 個點、8 條邊", wait=SLOW * 0.2)
    scene.play(FadeIn(l3), FadeIn(h3.nodes), run_time=0.8)
    scene.play(LaggedStart(*[ShowCreation(e) for e in h3.edges], lag_ratio=0.15), run_time=1.6)
    scene.say("每往上一層長度多 1；中間交叉的那幾條，不是相鄰對調", wait=SLOW * 0.6)
    scene.play(FadeIn(l4), FadeIn(h4.nodes), run_time=1.0)
    scene.play(LaggedStart(*[ShowCreation(e) for e in h4.edges], lag_ratio=0.02), run_time=2.2)
    scene.play(LaggedStart(*[FadeIn(c, shift=0.2 * LEFT) for c in counts], lag_ratio=0.1), run_time=0.9)
    scene.say("$S_4$", "：每層 1, 3, 5, 6, 5, 3, 1 個，正是 F50 數過的胞腔", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 4. 下樓梯（Lemma 11）
def digits(w, color_at=None, fs=30):
    color_at = color_at or {}
    return VGroup(*[tex(str(a), fs, color_at.get(k, WHITE)) for k, a in enumerate(w)]).arrange(RIGHT, buff=0.12)


def chain_column(seq, x, y0, dy=0.5):
    rows = VGroup()
    for k, w in enumerate(seq):
        cols = {}
        if k:
            cols = {i: ACCENT for i in range(len(w)) if w[i] != seq[k - 1][i]}
        d = digits(w, cols).move_to(np.array([x, y0 - dy * k, 0]))
        lab = tex(r"\ell=%d" % length(w), 24, MUTED_COLOR).next_to(d, RIGHT, buff=0.35)
        rows.add(VGroup(d, lab))
    return rows


def part_chain(scene):
    seq, _ = attempt(CH_U, CH_V)
    seq2, stuck = attempt(CH_U2, CH_V)
    left = chain_column(seq, -3.7, 2.0)
    right = chain_column(seq2, 2.7, 2.0)
    tu = VGroup(tex("u=", 30, MUTED_COLOR), digits(CH_U, fs=30)).arrange(RIGHT, buff=0.15)
    tu.next_to(left[0], UP, buff=0.3).align_to(left[0][0], LEFT).shift(LEFT * 0.62)
    tu2 = VGroup(tex("u=", 30, MUTED_COLOR), digits(CH_U2, {stuck - 1: BAD}, fs=30)).arrange(RIGHT, buff=0.15)
    tu2.next_to(right[0], UP, buff=0.3).align_to(right[0][0], LEFT).shift(LEFT * 0.62)
    hit = SurroundingRectangle(left[-1][0], buff=0.08).set_stroke(OK, 2.5)
    bad_digit = right[-1][0][stuck - 1]
    stop = SurroundingRectangle(bad_digit, buff=0.06).set_stroke(BAD, 2.5)
    msg = mixed("第 8 位 ", "$3<5$", "：卡住", font_size=28, color=BAD).next_to(right[-1], DOWN, buff=0.45)
    ans = mixed("$428671953$", " 和 ", "$679251834$", " 不可比", font_size=26, color=BAD).next_to(msg, DOWN, buff=0.3)
    assert_in_frame(left, right, tu, tu2, hit, msg, ans, stop)
    assert_apart(VGroup(left, tu), VGroup(right, tu2, msg, ans), 0.3)

    scene.say("書上的大例子（Lemma 11）：", "$S_9$", " 裡從 ", "$v$", " 一步步走下樓梯到 ", "$u$", wait=SLOW * 0.2)
    scene.play(FadeIn(tu), FadeIn(left[0]), run_time=0.8)
    scene.say("找第一個和 ", "$u$", " 不同的位置 ", "$j$", "，往右找第一個 ", "$k$", "：", r"$u(j)\le x(k)<x(j)$", "，交換",
              wait=SLOW * 0.4)
    for k in range(1, len(left)):
        scene.play(TransformFromCopy(left[k - 1][0], left[k][0]), FadeIn(left[k][1]), run_time=0.55)
        if k == 2:
            scene.say("每一步長度剛好減 1：22, 21, 20, …", wait=SLOW * 0.2)
    scene.play(ShowCreation(hit), run_time=0.6)
    scene.say("八步到達 ", "$u$", "：所以 ", r"$u\le v$", "，而且中間每一層都有一個", wait=SLOW * 0.7)
    scene.say("換成 ", "$u=428671953$", " 再走一次", wait=SLOW * 0.2)
    scene.play(FadeIn(tu2), FadeIn(right[0]), run_time=0.8)
    for k in range(1, len(right)):
        scene.play(TransformFromCopy(right[k - 1][0], right[k][0]), FadeIn(right[k][1]), run_time=0.55)
    scene.play(ShowCreation(stop), FadeIn(msg, shift=0.2 * UP), run_time=0.8)
    scene.say("前五步一樣，第六行在第 8 位遇到 ", "$3<5$", "：往下換只會更小，走不下去", wait=SLOW * 0.7)
    scene.play(FadeIn(ans), run_time=0.6)
    scene.say("卡住就表示 ", r"$u\not\le v$", "；長度又比 ", "$v$", " 短，所以兩者不可比", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 5. 命題 7
def part_prop(scene):
    p7 = fit(tex(r"u\le v\quad\iff\quad X_u\subset X_v\quad\iff\quad\Omega_u\supset\Omega_v", 46, ACCENT), 12.6).move_to(np.array([0, 1.9, 0]))
    xw = tex(r"X_w=\{E_\bullet:\ \dim(E_p\cap F_q)\ge r_w(p,q)\ \text{for all } p,q\}", 38).move_to(np.array([0, 0.6, 0]))
    fit(xw, 12.4)
    ans = mixed("胞腔 ", r"$X^\circ_u$", " 落在 ", "$X_v$", " 裡", r"$\iff u\le v$", font_size=32)
    ans.move_to(np.array([0, -0.8, 0]))
    sl = zh("比大小，只要排序", font_size=34, color=OK).move_to(np.array([0, -2.0, 0]))
    assert_in_frame(p7, xw, ans, sl)
    assert_apart(p7, xw, 0.2)
    assert_apart(xw, ans, 0.2)

    scene.say("命題 7：Bruhat 序就是 Schubert 簇的包含關係", wait=SLOW * 0.2)
    scene.play(Write(p7), run_time=1.6)
    scene.wait(SLOW * 0.5)
    scene.say("因為 ", "$X_w$", " 正是由秩條件切出來的", wait=SLOW * 0.2)
    scene.play(FadeIn(xw, shift=0.2 * UP), run_time=1.0)
    scene.say("秩越大，條件越嚴，簇越小：", "$r_u\\ge r_v$", " 就推出 ", r"$X_u\subset X_v$", wait=SLOW * 0.8)
    scene.play(FadeIn(ans, shift=0.2 * UP), run_time=0.8)
    scene.say("回答開頭的問題：", r"$X^\circ_u$", " 在 ", "$X_v$", " 的邊界上，恰好當 ", "$u<v$", wait=SLOW * 0.9)
    scene.play(FadeIn(sl, scale=1.1), run_time=0.8)
    scene.say("比大小只要排序", wait=SLOW * 1.0)


class SceneF54Bruhat(ChuScene):
    def construct(self):
        self.show_header("排序遊戲：Bruhat 序")
        check_math()
        part_rank(self)
        self.clear_stage()
        part_game(self)
        self.clear_stage()
        part_hasse(self)
        self.clear_stage()
        part_chain(self)
        self.clear_stage()
        part_prop(self)
        self.wait(1.0)
