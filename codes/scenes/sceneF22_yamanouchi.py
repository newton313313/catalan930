"""
Scene F22 —— 反格字（Yamanouchi 字）與 LR 斜表（Fulton《Young Tableaux》§5.2，書 p.63–66）

    倒著開票的選舉：w 從字尾往前讀，任何時刻 1 的個數 ≥ 2 的個數 ≥ 3 的個數 ≥ …
        2132121 是反格字；1232121 不是：倒著開到第 6 票，2 號 3 票、1 號 2 票（書 p.63）
    LR 斜表＝字是反格字的斜表；例 S = ((·,·,1),(·,1,2),(2,3)) 在 (3,3,2)/(2,1) 上，字 23121，
        滑到底得 U(2,2,1) = 11/22/3（第 i 列全是 i）
    引理 2：基本 Knuth 變換不改變「是不是反格字」：23121 → 23211 → 32211 = w(U(μ))，兩步都是
        k (k+1) k ↔ (k+1) k k 的關鍵情形（最右邊的 k 先開票，替 k 墊了一票）
    引理 1：內容 μ 的斜表是 LR 斜表 ⟺ Rect = U(μ)；命題 3：c^ν_{λμ} = ν/λ 上內容 μ 的 LR 斜表個數
        回到 F20：(3,2,1)/(2,1) 內容 (2,1) 的 3 個斜表，字 211 ✓、121 ✓、112 ✗ → c = 2，不必滑動

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。
滑動動畫借用 sceneF07_jeu_de_taquin 的 board 工具。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF22_yamanouchi.py SceneF22Yamanouchi
"""
import sys
from collections import Counter
from itertools import product as cartesian
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from scenes.sceneF07_jeu_de_taquin import anims_drop_cell, anims_move, anims_open_hole, board_as_skew, board_group, make_board
from utils.fulton_draw import SkewMob, WordMob, assert_apart, assert_in_frame, tuple_str, word_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed
from utils.tableaux import (
    CH5_RL_BAD,
    CH5_RL_GOOD,
    factorizations,
    is_reverse_lattice,
    jdt_steps,
    knuth_moves,
    knuth_path,
    lattice_tableau,
    lr_coefficient,
    lr_tableaux,
    partitions,
    rectify,
    rectifying_skews,
    skew_tableaux,
    ssyt,
    tableau_word,
)

N_ = None
FLIP_VOTE = 6                                          # 1232121 倒著開到第 6 票翻盤
LR_SHAPE = ((3, 3, 2), (2, 1))                         # (ν, λ)
LR_MU = (2, 2, 1)
LR_S = ((N_, N_, 1), (N_, 1, 2), (2, 3))
LR_WORD = (2, 3, 1, 2, 1)
KPATH = ((2, "K''", (2, 3, 2, 1, 1)), (0, "K''", (3, 2, 2, 1, 1)))
F20_SHAPE = ((3, 2, 1), (2, 1))
F20_MU = (2, 1)
F20_CANDS = (((N_, N_, 1), (N_, 1), (2,)), ((N_, N_, 1), (N_, 2), (1,)), ((N_, N_, 2), (N_, 1), (1,)))
F20_V = ((1, 2, 3), (4, 5), (6,))

CAND = {1: BLUE_C, 2: GREEN_C, 3: GOLD}


def first_violation(w):
    """倒著開票，第幾票時某個 k+1 號超過 k 號（沒有就 None）。"""
    cnt = Counter()
    for k, a in enumerate(reversed(w)):
        cnt[a] += 1
        if a > 1 and cnt[a] > cnt[a - 1]:
            return k + 1
    return None


def content_of(S):
    vals = [v for r in S for v in r if v is not None]
    return tuple(vals.count(k) for k in range(1, max(vals) + 1))


def check_math():
    assert is_reverse_lattice(CH5_RL_GOOD) and first_violation(CH5_RL_GOOD) is None
    assert not is_reverse_lattice(CH5_RL_BAD) and first_violation(CH5_RL_BAD) == FLIP_VOTE
    nu, lam = LR_SHAPE
    assert LR_S in lr_tableaux(nu, lam, LR_MU) and tableau_word(LR_S) == LR_WORD
    assert rectify(LR_S) == lattice_tableau(LR_MU)
    assert tuple(knuth_path(LR_WORD, tableau_word(lattice_tableau(LR_MU)))) == KPATH
    assert all(is_reverse_lattice(w) for _, _, w in KPATH)
    for i, _, _ in KPATH:                               # 兩步都是 k (k+1) k → (k+1) k k
        w = LR_WORD if i == KPATH[0][0] else KPATH[0][2]
        a, b, c = w[i:i + 3]
        assert a == c and b == a + 1
    # 引理 1（一般的表）：字是反格字 ⟺ 第 i 列全是 i
    for n in range(1, 7):
        for p in partitions(n):
            good = [T for T in ssyt(p, len(p)) if is_reverse_lattice(tableau_word(T))]
            assert good == [lattice_tableau(p)]
    # 引理 2：長度 ≤ 6、字母 ≤ 3 的字全部檢查
    for n in range(3, 7):
        for w in cartesian((1, 2, 3), repeat=n):
            r = is_reverse_lattice(w)
            assert all(is_reverse_lattice(w2) == r for _, _, w2 in knuth_moves(w))
    # 命題 3：滑成 U(μ) 的斜表＝LR 斜表
    for (nu_, lam_), mu_ in ((LR_SHAPE, LR_MU), (F20_SHAPE, F20_MU)):
        assert rectifying_skews(nu_, lam_, lattice_tableau(mu_)) == lr_tableaux(nu_, lam_, mu_)
    cands = tuple(S for S in skew_tableaux(*F20_SHAPE, 2) if content_of(S) == F20_MU)
    assert cands == F20_CANDS
    assert [is_reverse_lattice(tableau_word(S)) for S in cands] == [True, True, False]
    assert lr_coefficient(F20_MU, F20_MU, F20_SHAPE[0]) == 2 == len(factorizations(F20_V, F20_MU, F20_MU))


def check_mark(fs=40):
    return Tex(r"\checkmark", font_size=fs, fill_color=OK_COLOR)


def cross_mark(fs=44):
    return Tex(r"\times", font_size=fs, fill_color=RED)


def word_colors(w):
    return {k: CAND[a] for k, a in enumerate(w)}


# =============================================================================
# 第 1 段：倒著開票的選舉
# =============================================================================
PILE_X = {1: -4.7, 2: -3.3, 3: -1.9}
BASE_Y, BS = -2.05, 0.5


def run_election(scene, wm, w, rt=0.55):
    """倒著開票，每一票飛到候選人的票堆；翻盤時停下。回傳 (票堆, 翻盤的票數或 None)。"""
    counts, blocks = Counter(), VGroup()
    piles = {a: VGroup() for a in CAND}
    for k in range(len(w)):
        p = len(w) - 1 - k
        a = w[p]
        sq = Square(side_length=BS * 0.92, stroke_color=WHITE, stroke_width=2).set_fill(CAND[a], opacity=0.6)
        blk = VGroup(sq, Tex(str(a), font_size=28))
        blk.move_to([PILE_X[a], BASE_Y + (counts[a] + 0.5) * BS, 0])
        counts[a] += 1
        piles[a].add(blk)
        blocks.add(blk)
        scene.play(TransformFromCopy(wm.tiles[p], blk), wm.tiles[p].animate.set_opacity(0.3), run_time=rt)
        if a > 1 and counts[a] > counts[a - 1]:
            scene.play(piles[a].animate.set_color(RED), Indicate(piles[a], color=RED), run_time=0.7)
            return blocks, k + 1
    return blocks, None


def part_election(scene):
    rule = VGroup(mixed("反格字（Yamanouchi 字）：", font_size=26),
                  mixed("從字尾往前開票，開到任何時候", font_size=24),
                  mixed("$\\#1\\ge\\#2\\ge\\#3\\ge\\cdots$", font_size=26)
                  ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([0.6, 2.2, 0], aligned_edge=LEFT)
    wg = WordMob(CH5_RL_GOOD, size=0.6, colors=word_colors(CH5_RL_GOOD), center=[-3.3, 2.0, 0])
    wb = WordMob(CH5_RL_BAD, size=0.6, colors=word_colors(CH5_RL_BAD), center=[-3.3, 2.0, 0])
    arr = Arrow([-1.0, 1.35, 0], [-5.6, 1.35, 0], buff=0, stroke_width=3, fill_color=GREY_B)
    alab = mixed("開票順序", font_size=20, color=MUTED_COLOR).next_to(arr, DOWN, buff=0.08)
    base = Line([-5.4, BASE_Y, 0], [-1.2, BASE_Y, 0], stroke_color=GREY_B, stroke_width=3)
    names = VGroup(*[mixed(f"{a} 號", font_size=22, color=CAND[a]).move_to([PILE_X[a], BASE_Y - 0.3, 0])
                     for a in CAND])
    res_g = VGroup(word_tex(CH5_RL_GOOD, font_size=36), check_mark()).arrange(RIGHT, buff=0.3)
    res_b = VGroup(word_tex(CH5_RL_BAD, font_size=36), cross_mark(),
                   mixed(f"第 {FLIP_VOTE} 票：2 號超前", font_size=22, color=RED)).arrange(RIGHT, buff=0.3)
    VGroup(res_g, res_b).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0.8, -0.3, 0], aligned_edge=LEFT)
    tall = VGroup(*[Square(side_length=BS).move_to([PILE_X[a], BASE_Y + (h + 0.5) * BS, 0])
                    for a in CAND for h in range(3)])
    assert_in_frame(rule, wg, arr, alab, base, names, res_g, res_b, tall)
    assert_apart(VGroup(wg, arr, alab), VGroup(rule, res_g, res_b), gap=0.3)
    assert_apart(VGroup(wg, arr, alab), tall, gap=0.2)
    assert_apart(VGroup(tall, base, names), VGroup(rule, res_g, res_b), gap=0.3)
    assert_apart(rule, res_g, gap=0.3)

    scene.say("想像一場選舉：字裡每個字母是一張票，寫著候選人的號碼")
    scene.play(FadeIn(wg, shift=0.1 * DOWN), FadeIn(base), FadeIn(names), run_time=0.9)
    scene.wait(0.4)
    scene.say("倒著開票：1 號不能落後 2 號，2 號不能落後 3 號……")
    scene.play(GrowArrow(arr), FadeIn(alab), FadeIn(rule, shift=0.1 * LEFT), run_time=1.0)
    scene.wait(1.8)
    scene.say("開票：", "$" + r"\ ".join(map(str, CH5_RL_GOOD)) + "$")
    blocks, flip = run_election(scene, wg, CH5_RL_GOOD)
    assert flip is None
    scene.say("開完都沒有人超前：這是反格字")
    scene.play(FadeIn(res_g, shift=0.1 * LEFT), run_time=0.6)
    scene.wait(1.6)
    scene.say("換一個字：", "$" + r"\ ".join(map(str, CH5_RL_BAD)) + "$", "，再開一次")
    scene.play(FadeOut(blocks), FadeOut(wg), FadeIn(wb), run_time=0.7)
    blocks, flip = run_election(scene, wb, CH5_RL_BAD)
    assert flip == FLIP_VOTE
    scene.say(f"第 {FLIP_VOTE} 票開出來，2 號有 3 票、1 號只有 2 票：翻盤！不是反格字")
    scene.play(FadeIn(res_b, shift=0.1 * LEFT), run_time=0.6)
    scene.wait(2.4)


# =============================================================================
# 第 2 段：LR 斜表，滑到底就是 U(μ)
# =============================================================================
def slide_board(scene, board, S, rt=0.4):
    for corner, path, _ in jdt_steps(S):
        scene.play(*anims_open_hole(board, corner), run_time=rt)
        for src in path[1:]:
            scene.play(*anims_move(board, src), run_time=rt)
        scene.play(*anims_drop_cell(board), run_time=rt * 0.8)


def part_lr_tableau(scene):
    nu, lam = LR_SHAPE
    title = mixed("LR 斜表：字是反格字的斜表", font_size=28, color=YELLOW).move_to([-6.2, 2.55, 0], aligned_edge=LEFT)
    board = make_board(LR_S, 0.62, (-6.2, 1.75, 0), 34)
    bg = board_group(board)
    shape_lab = Tex(tuple_str(nu) + "/" + tuple_str(lam), font_size=26, fill_color=MUTED_COLOR)
    shape_lab.next_to(bg, DOWN, buff=0.2)
    wm = WordMob(LR_WORD, size=0.6, colors=word_colors(LR_WORD))
    wlab = Tex("w(S)=", font_size=36)
    wrow = VGroup(wlab, wm).arrange(RIGHT, buff=0.25).move_to([-1.0, 1.0, 0], aligned_edge=LEFT)
    wck = check_mark().next_to(wm, RIGHT, buff=0.3)
    read = [(i, j) for i in reversed(range(len(LR_S))) for j, v in enumerate(LR_S[i]) if v is not None]
    assert tuple(board["vals"][b] for b in read) == LR_WORD
    u_lab = mixed("$U(\\mu)$", "：第 ", "$i$", " 列全是 ", "$i$", "，", "$\\mu=" + tuple_str(LR_MU) + "$", font_size=24)
    u_lab.move_to([-1.0, -0.15, 0], aligned_edge=LEFT)
    l1 = mixed("引理 1：", "$S$", " 是內容 ", "$\\mu$", " 的 LR 斜表 ", "$\\Longleftrightarrow$", "$\\mathrm{Rect}(S)=U(\\mu)$",
               font_size=26)
    l2 = mixed("一般的表：倒著開的第一票是第 1 列最右格，只能是 1，所以第 1 列全是 1；第 2 列同理……",
               font_size=20, color=MUTED_COLOR)
    lem = VGroup(l1, l2).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-6.2, -1.75, 0], aligned_edge=LEFT)
    lfr = SurroundingRectangle(lem, buff=0.15, color=YELLOW, stroke_width=2.5)
    assert_in_frame(title, bg, shape_lab, wrow, wck, u_lab, lfr)
    assert_apart(title, VGroup(bg, wrow), gap=0.2)
    assert_apart(VGroup(bg, shape_lab), VGroup(wrow, wck, u_lab), gap=0.4)
    assert_apart(VGroup(wrow, wck), u_lab, gap=0.3)
    assert_apart(VGroup(bg, shape_lab, u_lab), lfr, gap=0.1)

    scene.say("斜表的字：由最下面一列讀到最上面，每列由左到右")
    scene.play(FadeIn(title), FadeIn(bg), FadeIn(shape_lab), FadeIn(wlab), run_time=0.8)
    for k, b in enumerate(read):
        scene.play(TransformFromCopy(board["nums"][b], wm.tiles[k]), run_time=0.4)
    scene.say("倒著開票：1、2、1、3、2，沒有人超前：這是 LR 斜表")
    scene.play(FadeIn(wck, scale=1.4), run_time=0.5)
    scene.wait(1.4)
    scene.say("把它滑到底（rectify），看看會變成什麼")
    slide_board(scene, board, LR_S)
    assert board_as_skew(board) == lattice_tableau(LR_MU)
    scene.say("第 1 列全是 1、第 2 列全是 2、第 3 列是 3：正是 ", "$U(\\mu)$")
    scene.play(*[board["nums"][b].animate.set_fill(CAND[v]) for b, v in board["vals"].items()],
               FadeOut(shape_lab), FadeIn(u_lab), run_time=0.8)
    scene.wait(1.4)
    scene.say("引理 1：LR 斜表滑到底一定是 ", "$U(\\mu)$", "，反之亦然")
    scene.play(FadeIn(lem), ShowCreation(lfr), run_time=0.8)
    scene.wait(2.6)


# =============================================================================
# 第 3 段：引理 2——Knuth 變換保持反格性（看關鍵的那一票）
# =============================================================================
def part_knuth(scene):
    ys = (1.9, 0.55, -0.8)
    starts = (LR_WORD, LR_WORD, KPATH[0][2])            # 每一列開始時的字（之後在該列做一步變換）
    wms = [WordMob(w, size=0.6, colors=word_colors(w), center=[-3.0, y, 0]) for w, y in zip(starts, ys)]
    checks = [check_mark().next_to(wm, RIGHT, buff=0.3) for wm in wms]
    labs = [Tex("w(S)", font_size=30).next_to(wms[0], LEFT, buff=0.3),
            Tex(r"w(U(\mu))", font_size=30).next_to(wms[2], LEFT, buff=0.3)]
    k0 = mixed("引理 2：基本 Knuth 變換", font_size=26, color=YELLOW)
    k0b = mixed("不改變「是不是反格字」", font_size=26, color=YELLOW)
    k1 = Tex(r"k\ (k{+}1)\ k\ \longleftrightarrow\ (k{+}1)\ k\ k", font_size=34)
    k2 = mixed("倒著開票時，最右邊那個 ", "$k$", " 最先開出", font_size=22)
    k3 = mixed("它先替 ", "$k$", " 墊了一票：", "$k{+}1$", " 怎麼排都追不上", font_size=22)
    k4 = mixed("其他情形：誰多誰少根本不受影響", font_size=20, color=MUTED_COLOR)
    panel = VGroup(k0, k0b, k1, k2, k3, k4).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    panel.move_to([0.9, 0.55, 0], aligned_edge=LEFT)
    k1.shift(0.3 * RIGHT)
    left = VGroup(*wms, *checks, *labs)
    assert_in_frame(left, panel)
    assert_apart(left, panel, gap=0.3)
    for a, b in zip(wms, wms[1:]):
        assert_apart(a, b, gap=0.6)

    scene.say("為什麼？滑動的每一步，字都只做了基本 Knuth 變換")
    scene.play(FadeIn(wms[0]), FadeIn(labs[0]), FadeIn(checks[0]), run_time=0.7)
    scene.play(FadeIn(k0), FadeIn(k0b), run_time=0.7)
    scene.wait(1.0)
    for step, ((i, rule, w_new), src, dst, ck) in enumerate(zip(KPATH, wms, wms[1:], checks[1:])):
        assert src.letters == dst.letters
        scene.play(*[TransformFromCopy(x, y) for x, y in zip(src.tiles, dst.tiles)], run_time=0.6)
        k = dst.letters[i]
        scene.say("關鍵的一票：最右邊的 ", f"${k}$", "，倒著開時它最先開出" if step == 0 else "，同樣先開出")
        key = SurroundingRectangle(dst.tiles[i + 2], buff=0.06, color=YELLOW, stroke_width=4)
        scene.play(ShowCreation(key), run_time=0.5)
        if step == 0:
            scene.play(FadeIn(k1), FadeIn(k2), run_time=0.7)
        dst.apply_move(scene, i, rule, run_time=0.7)
        assert dst.letters == w_new
        scene.play(FadeOut(key), FadeIn(ck, scale=1.4), run_time=0.5)
        if step == 0:
            scene.say("交換的是 ", f"${k}$", " 和 ", f"${k + 1}$", "：前面已墊了一票，", f"${k + 1}$", " 不會超前")
            scene.play(FadeIn(k3), run_time=0.6)
            scene.wait(1.6)
    assert wms[2].letters == tableau_word(lattice_tableau(LR_MU))
    scene.play(FadeIn(labs[1]), FadeIn(k4), run_time=0.6)
    scene.say("一路都是反格字，最後到達 ", "$U(\\mu)$", " 的字")
    scene.wait(2.4)


# =============================================================================
# 第 4 段：命題 3——數 LR 斜表就得到 c
# =============================================================================
def part_prop3(scene):
    nu, lam = F20_SHAPE
    s1 = mixed("命題 3：", "$c^{\\nu}_{\\lambda\\mu}$", "＝", "$\\nu/\\lambda$", " 上內容 ", "$\\mu$",
               " 的 LR 斜表個數", font_size=30)
    s1.move_to([0, 2.45, 0])
    sfr = SurroundingRectangle(s1, buff=0.15, color=YELLOW, stroke_width=3)
    why = mixed("F20：", "$c$", "＝滑成 ", "$U_0$", " 的斜表數；取 ", "$U_0=U(\\mu)$", "，引理 1、2 ", "$\\Rightarrow$",
                " 就是 LR 斜表", font_size=22, color=MUTED_COLOR).move_to([0, 1.6, 0])
    xs = (-5.2, -2.8, -0.4)
    sks, ws, marks = [], [], []
    for S, x in zip(F20_CANDS, xs):
        sk = SkewMob(S, 0.55, center=[x, -0.1, 0])
        w = tableau_word(S)
        wt = word_tex(w, colors=word_colors(w), font_size=36).next_to(sk, DOWN, buff=0.35)
        mk = (check_mark() if is_reverse_lattice(w) else cross_mark()).next_to(wt, DOWN, buff=0.25)
        sks.append(sk)
        ws.append(wt)
        marks.append(mk)
    head = mixed("$\\nu/\\lambda=" + tuple_str(nu) + "/" + tuple_str(lam) + "$", "，", "$\\mu=" + tuple_str(F20_MU) + "$",
                 font_size=24).move_to([-2.8, 1.1, 0])
    n_lr = len(lr_tableaux(nu, lam, F20_MU))
    res = Tex(r"c^{" + tuple_str(nu) + "}_{" + tuple_str(F20_MU) + "," + tuple_str(F20_MU) + "}=" + str(n_lr),
              font_size=44, fill_color=YELLOW).move_to([4.2, -0.2, 0])
    rfr = SurroundingRectangle(res, buff=0.18, color=YELLOW, stroke_width=3)
    cols = [VGroup(s, w, m) for s, w, m in zip(sks, ws, marks)]
    assert_in_frame(sfr, why, head, *cols, rfr)
    assert_apart(sfr, why, gap=0.1)
    assert_apart(why, head, gap=0.1)
    assert_apart(head, VGroup(*sks), gap=0.1)
    for a, b in zip(cols, cols[1:]):
        assert_apart(a, b, gap=0.5)
    assert_apart(VGroup(*cols), rfr, gap=0.5)

    scene.say("合起來就是命題 3：LR 數可以直接數出來")
    scene.play(FadeIn(s1), ShowCreation(sfr), run_time=0.9)
    scene.wait(1.2)
    scene.say("理由：", "$c$", " 是滑成 ", "$U_0$", " 的斜表數，而滑成 ", "$U(\\mu)$", " 的恰好是 LR 斜表")
    scene.play(FadeIn(why), run_time=0.7)
    scene.wait(1.8)
    scene.say("回到 F20 的三個斜表：這次不用滑，只要讀字、倒著開票")
    scene.play(FadeIn(head), LaggedStart(*[FadeIn(s, shift=0.1 * DOWN) for s in sks], lag_ratio=0.25), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(w) for w in ws], lag_ratio=0.25), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.3), run_time=0.9)
    scene.wait(1.2)
    scene.say("兩個反格字、一個不是：", "$c=" + str(n_lr) + "$", "，和因數分解數出來的一樣")
    scene.play(FadeIn(res, scale=1.2), ShowCreation(rfr), cols[2].animate.set_opacity(0.35), run_time=0.9)
    scene.wait(2.6)


class SceneF22Yamanouchi(ChuScene):
    def construct(self):
        self.show_header("反格字與 LR 斜表")
        check_math()
        part_election(self)
        self.clear_stage()
        part_lr_tableau(self)
        self.clear_stage()
        part_knuth(self)
        self.clear_stage()
        part_prop3(self)
        self.wait(1.0)
