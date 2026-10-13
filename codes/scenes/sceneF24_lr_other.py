"""
Scene F24 —— LR 數的其他算法（Fulton《Young Tableaux》§5.3，書 p.68–70；練習 8）

    鉤子「換一副眼鏡看同一批東西」：同一個 LR 斜表，也可以看成 μ 上的一張標準表
    反格字 ↔ 標準表 U(w)：w = x_r…x_1，把 p 放進第 x_p 列（p.68 的例子 1123121 → 1367/25/4）
    反向編號：ν/λ 由上到下、每列由右往左編 1, 2, …（(5,4,3,2)/(3,3,1)）
    Remmel–Whitney（命題 4）：μ 上的標準表 U 要滿足
        (i)  k−1、k 在同一列 → U 裡 k 在 k−1 的右邊、不比它低
        (ii) k 在 j 的正下方 → U 裡 k 比 j 低、不比它右
        例：LR 斜表 S（內容 (4,2,1)）↔ U = 1245/37/6，格子 k 裡的數 = U 裡 k 所在的列
        對 (5,4,3,2)/(3,3,1)：9 種 μ 共 189 個標準表，過關的恰好 15 個（＝LR 斜表）
    Zelevinsky 的 picture 一句
    彩蛋（練習 8）：n 個 1、n 個 2 的反格字 ↔ 不跌破地面的山路，個數 1, 2, 5, 14, 42, 132 = 卡塔蘭數 C_n

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF24_lr_other.py SceneF24LROther
"""
import itertools
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import MU_COLOR, SkewMob, WordMob, assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH5_DECOMP,
    CH5_LAM,
    CH5_NU,
    is_partition,
    is_reverse_lattice,
    is_standard,
    lr_tableaux,
    remmel_whitney,
    reverse_numbering,
    shape,
    standard_tableaux,
    tableau_word,
    young_boxes,
)

NU, LAM = CH5_NU, CH5_LAM
EX_S = ((None, None, None, 1, 1), (None, None, None, 2), (None, 1, 1), (2, 3))     # 與 F23 同一個 LR 斜表
EX_MU = (4, 2, 1)
EX_U = ((1, 2, 4, 5), (3, 7), (6,))
BOOK_W = (1, 1, 2, 3, 1, 2, 1)                                                     # p.68
BOOK_U = ((1, 3, 6, 7), (2, 5), (4,))
REV_NUM = {(0, 4): 1, (0, 3): 2, (1, 3): 3, (2, 2): 4, (2, 1): 5, (3, 1): 6, (3, 0): 7}
ROW_PAIRS = ((1, 2), (4, 5), (6, 7))          # (k−1, k) 同一列
COL_PAIRS = ((2, 3), (5, 6))                  # (j, k)：k 在 j 正下方
F_TOTAL, LR_TOTAL = 189, 15
CAT_N = 3
CAT_WORDS = ((2, 1, 2, 1, 2, 1), (2, 1, 2, 2, 1, 1), (2, 2, 1, 1, 2, 1), (2, 2, 1, 2, 1, 1), (2, 2, 2, 1, 1, 1))
CAT_COUNTS = (1, 2, 5, 14, 42, 132)           # n = 1..6
NUM_COLORS = {1: BLUE_C, 2: GREEN_C, 3: GOLD}
ROW_C, COL_C = TEAL, PINK


def u_of_word(w):
    """U(w)：w = x_r…x_1，把 p 放進第 x_p 列（p = 1..r，書 p.68）。"""
    rows = {}
    for p, x in enumerate(reversed(w), start=1):
        rows.setdefault(x, []).append(p)
    return tuple(tuple(rows[i]) for i in range(1, max(rows) + 1))


def lattice_words(n):
    return tuple(sorted(w for w in set(itertools.permutations((1,) * n + (2,) * n)) if is_reverse_lattice(w)))


def check_math():
    # U(w)
    assert is_reverse_lattice(BOOK_W) and u_of_word(BOOK_W) == BOOK_U and is_standard(BOOK_U)
    c = Counter(BOOK_W)
    assert shape(BOOK_U) == tuple(c[i] for i in range(1, max(c) + 1)) == EX_MU
    for s in range(1, len(BOOK_W) + 1):        # 前 s 個數永遠排成 Young 圖
        assert is_partition(tuple(sum(v <= s for v in r) for r in BOOK_U if any(v <= s for v in r)))
    # 反向編號與兩種相鄰
    num = reverse_numbering(NU, LAM)
    assert num == REV_NUM
    assert tuple(sorted((num[(i, j + 1)], num[(i, j)]) for (i, j) in num if (i, j + 1) in num)) == ROW_PAIRS
    assert tuple(sorted((num[(i - 1, j)], num[(i, j)]) for (i, j) in num if (i - 1, j) in num)) == COL_PAIRS
    # S ↔ U：格子 k 裡的數 = U 裡 k 所在的列
    lr = lr_tableaux(NU, LAM)
    assert EX_S in lr and u_of_word(tableau_word(EX_S)) == EX_U
    rows_of = {v: i + 1 for i, r in enumerate(EX_U) for v in r}
    assert all(EX_S[i][j] == rows_of[k] for (i, j), k in REV_NUM.items())
    w = tableau_word(EX_S)
    assert all(w[::-1][k - 1] == EX_S[i][j] for (i, j), k in REV_NUM.items())
    assert EX_U in remmel_whitney(NU, LAM, EX_MU)
    for mu, cnt in CH5_DECOMP.items():
        rw = remmel_whitney(NU, LAM, mu)
        assert len(rw) == cnt
        assert set(rw) == {u_of_word(tableau_word(S)) for S in lr_tableaux(NU, LAM, mu)}
    assert sum(len(standard_tableaux(mu)) for mu in CH5_DECOMP) == F_TOTAL
    assert sum(CH5_DECOMP.values()) == LR_TOTAL == len(lr)
    # 練習 8
    assert lattice_words(CAT_N) == CAT_WORDS
    for n, cnt in enumerate(CAT_COUNTS, start=1):
        assert len(lattice_words(n)) == cnt == comb(2 * n, n) // (n + 1)
    assert sorted(u_of_word(w) for w in CAT_WORDS) == sorted(standard_tableaux((CAT_N, CAT_N)))


# =============================================================================
# 小工具
# =============================================================================
def colored_skew(S, cs, fs, **kw):
    t = SkewMob(S, cs=cs, fs=fs, **kw)
    for i, r in enumerate(S):
        for j, v in enumerate(r):
            if v:
                t.entry(i, j).set_fill(NUM_COLORS[v])
    return t


def make_glasses(color=TEAL_A):
    left = Circle(radius=0.45).set_stroke(color, width=5).set_fill(color, opacity=0.08)
    right = left.copy().shift(1.3 * RIGHT)
    bridge = ArcBetweenPoints(left.get_right(), right.get_left(), angle=-PI / 2).set_stroke(color, width=5)
    t1 = Line(left.get_left(), left.get_left() + 0.4 * LEFT + 0.18 * UP).set_stroke(color, width=5)
    t2 = Line(right.get_right(), right.get_right() + 0.4 * RIGHT + 0.18 * UP).set_stroke(color, width=5)
    return VGroup(left, right, bridge, t1, t2)


def dyck_path(w, x0, y0, step=0.22, color=TEAL):
    """從右往左讀：1 上坡、2 下坡；地面在 y0。"""
    pts, h = [np.array([x0, y0, 0.0])], 0
    for a in reversed(w):
        h += 1 if a == 1 else -1
        assert h >= 0
        pts.append(pts[-1] + step * RIGHT + (step if a == 1 else -step) * UP)
    ground = DashedLine(pts[0], pts[-1], dash_length=0.06).set_stroke(GREY_C, width=1.5)
    path = VMobject().set_points_as_corners(pts).set_stroke(color, width=3.5)
    return VGroup(ground, path)


# =============================================================================
# 第 1 段：鉤子——換一副眼鏡
# =============================================================================
def part_hook(scene):
    S = colored_skew(EX_S, 0.55, 30, center=np.array([-4.3, 0.4, 0]))
    U = tableau_mob(EX_U, 0.6, center=np.array([4.3, 0.4, 0]))
    sl = zh("LR 斜表", font_size=26).next_to(S, DOWN, buff=0.3)
    ul = mixed("$\\mu=" + tuple_str(EX_MU) + "$", " 上的標準表", font_size=26).next_to(U, DOWN, buff=0.3)
    g = make_glasses().move_to(S)
    assert_in_frame(S, U, sl, ul, g)
    assert_apart(VGroup(S, sl), VGroup(U, ul), gap=1.0)

    scene.say("換一副眼鏡，看同一批東西")
    scene.play(FadeIn(S), FadeIn(sl), run_time=0.7)
    scene.play(FadeIn(g, scale=1.3), run_time=0.6)
    scene.play(g.animate.move_to([0.0, 0.4, 0]), run_time=0.8)
    scene.play(FadeTransform(S.copy(), U), FadeIn(ul), run_time=1.2)
    scene.wait(0.6)
    scene.say("LR 斜表也能看成一張標準表；這一節換幾種眼鏡數同樣的 ", "$c^{\\nu}_{\\lambda\\mu}$")
    scene.play(WiggleOutThenIn(g), run_time=1.0)
    scene.wait(1.6)


# =============================================================================
# 第 2 段：反格字 ↔ 標準表 U(w)
# =============================================================================
def part_uw(scene):
    w = BOOK_W
    r = len(w)
    word = WordMob(w, size=0.6, colors=[NUM_COLORS[a] for a in w], center=np.array([-0.4, 2.15, 0]))
    plabs = VGroup(*[Tex(str(r - k), font_size=26, fill_color=MUTED_COLOR).next_to(word.tiles[k], DOWN, buff=0.12)
                     for k in range(r)])
    pname = Tex("p", font_size=28, fill_color=MUTED_COLOR).next_to(plabs, LEFT, buff=0.35)
    sh = shape(BOOK_U)
    d = YoungDiagramMob(sh, cell_size=0.7, top_left=np.array([-1.6, 0.75, 0]))
    rlabs = VGroup(*[zh(f"第 {i + 1} 列", font_size=22, color=NUM_COLORS[i + 1]).next_to(d.cell(i, 0), LEFT, buff=0.2)
                     for i in range(len(sh))])
    expl = VGroup(mixed("從右往左數，第 ", "$p$", " 個字母是 ", "$x$", font_size=24),
                  mixed("$\\Rightarrow$", " 把 ", "$p$", " 放進第 ", "$x$", " 列", font_size=24),
                  mixed("形狀＝內容 ", "$" + tuple_str(sh) + "$", font_size=24, color=OK_COLOR))
    expl.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.4, -0.15, 0], aligned_edge=LEFT)
    name = Tex("U(w)", font_size=36).next_to(d, DOWN, buff=0.3)
    nums, counts = [], Counter()
    for p in range(1, r + 1):
        k = r - p
        x = w[k]
        col = counts[x]
        counts[x] += 1
        assert BOOK_U[x - 1][col] == p
        nums.append((k, Tex(str(p), font_size=36).move_to(plabs[k]), d.cell_center(x - 1, col)))
    assert_in_frame(word, plabs, pname, d, rlabs, expl, name)
    for a, b in [(plabs, d), (plabs, rlabs), (rlabs, d), (d, expl), (pname, rlabs), (word, expl), (plabs, expl)]:
        assert_apart(a, b, gap=0.12)

    scene.say("先看字：", "$w=" + "".join(map(str, w)) + "$", " 是反格字（書上的例子）")
    scene.play(FadeIn(word), run_time=0.7)
    scene.play(FadeIn(plabs), FadeIn(pname), run_time=0.6)
    scene.wait(0.6)
    scene.say("從右往左：第 ", "$p$", " 個字母是幾，就把 ", "$p$", " 放進第幾列")
    scene.play(FadeIn(d), FadeIn(rlabs), FadeIn(expl[:2]), run_time=0.8)
    hl = SurroundingRectangle(word.tiles[-1], buff=0.05, color=YELLOW, stroke_width=3)
    scene.play(ShowCreation(hl), run_time=0.3)
    for k, t, target in nums:
        scene.play(hl.animate.move_to(word.tiles[k]), run_time=0.25)
        scene.play(t.animate.move_to(target), run_time=0.45)
    scene.play(FadeOut(hl), run_time=0.3)
    scene.say("反格字保證每一步都還是 Young 圖：得到標準表 ", "$U(w)$")
    scene.play(FadeIn(name), FadeIn(expl[2]), run_time=0.7)
    scene.wait(1.8)


# =============================================================================
# 第 3 段：反向編號、Remmel–Whitney 的兩條規則、S ↔ U
# =============================================================================
def part_rw(scene):
    pos = {k: b for b, k in REV_NUM.items()}
    cs = 0.62
    D = YoungDiagramMob(NU, cell_size=cs, top_left=np.array([-6.5, 2.3, 0]))
    D.fill_cells(young_boxes(LAM), MU_COLOR, opacity=0.35)
    nums = {b: Tex(str(k), font_size=32).move_to(D.cell_center(*b)) for b, k in REV_NUM.items()}
    nlab = zh("反向編號：由上而下，每列由右往左", font_size=22, color=MUTED_COLOR)
    nlab.next_to(D, DOWN, buff=0.25, aligned_edge=LEFT)
    row_rects = {pr: SurroundingRectangle(VGroup(D.cell(*pos[pr[0]]), D.cell(*pos[pr[1]])), buff=-0.05,
                                          color=ROW_C, stroke_width=3.5) for pr in ROW_PAIRS}
    col_rects = {pr: SurroundingRectangle(VGroup(D.cell(*pos[pr[0]]), D.cell(*pos[pr[1]])), buff=-0.12,
                                          color=COL_C, stroke_width=3.5) for pr in COL_PAIRS}
    flashes = {pr: rr.copy() for pr, rr in list(row_rects.items()) + list(col_rects.items())}
    r1 = mixed("(i) ", "$k-1,\\ k$", " 同一列 ", "$\\Rightarrow$", " ", "$U$", " 裡 ", "$k$", " 在 ", "$k-1$",
               " 右邊、不比它低", font_size=23, color=ROW_C)
    r2 = mixed("(ii) ", "$k$", " 在 ", "$j$", " 正下方 ", "$\\Rightarrow$", " ", "$U$", " 裡 ", "$k$", " 比 ", "$j$",
               " 低、不比它右", font_size=23, color=COL_C)
    rules = VGroup(r1, r2).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-2.7, 1.75, 0], aligned_edge=LEFT)
    link = mixed("格子 ", "$k$", " 裡填 ", "$x$", " ", "$\\Leftrightarrow$", " ", "$k$", " 在 ", "$U$", " 的第 ",
                 "$x$", " 列", font_size=24, color=YELLOW).move_to([-2.7, 0.55, 0], aligned_edge=LEFT)
    entries = {b: Tex(str(EX_S[b[0]][b[1]]), font_size=34, fill_color=NUM_COLORS[EX_S[b[0]][b[1]]])
               .move_to(D.cell_center(*b) + 0.06 * (RIGHT + DOWN)) for b in REV_NUM}
    for b, t in nums.items():
        t.generate_target()
        t.target.scale(0.62).set_fill(GREY_A).move_to(D.cell(*b).get_corner(UL) + 0.13 * (RIGHT + DOWN))
    slab = mixed("LR 斜表 ", "$S$", "，內容 ", "$" + tuple_str(EX_MU) + "$", font_size=22, color=MUTED_COLOR)
    slab.next_to(nlab, DOWN, buff=0.2, aligned_edge=LEFT)
    U = YoungDiagramMob(EX_MU, cell_size=cs, top_left=np.array([0.9, -0.1, 0]))
    ulabs = VGroup(*[zh(f"第 {i + 1} 列", font_size=20, color=NUM_COLORS[i + 1]).next_to(U.cell(i, 0), LEFT, buff=0.15)
                     for i in range(len(EX_MU))])
    uname = mixed("$U$", "：", "$\\mu$", " 上的標準表", font_size=22, color=MUTED_COLOR).next_to(U, RIGHT, buff=0.4)
    assert_in_frame(D, nlab, slab, rules, link, U, ulabs, uname)
    for a, b in [(D, rules), (D, link), (rules, link), (link, U), (link, ulabs), (D, nlab), (nlab, slab),
                 (slab, ulabs), (D, ulabs), (U, uname)]:
        assert_apart(a, b, gap=0.12)

    scene.say("換一副眼鏡：把 ", "$\\nu/\\lambda=" + tuple_str(NU) + "/" + tuple_str(LAM) + "$", " 的格子反向編號")
    scene.play(FadeIn(D), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(nums[pos[k]], scale=1.5) for k in sorted(pos)], lag_ratio=0.35),
               FadeIn(nlab), run_time=2.0)
    scene.wait(0.5)
    scene.say("Remmel–Whitney：", "$\\mu$", " 上的標準表 ", "$U$", " 只要守兩條規則")
    scene.play(*[ShowCreation(rr) for rr in row_rects.values()], FadeIn(r1), run_time=0.9)
    scene.wait(1.2)
    scene.play(*[ShowCreation(rr) for rr in col_rects.values()], FadeIn(r2), run_time=0.9)
    scene.wait(1.6)
    scene.say("戴上眼鏡看 LR 斜表：格子 ", "$k$", " 裡的數，就是 ", "$U$", " 裡 ", "$k$", " 所在的列")
    scene.play(*[MoveToTarget(t) for t in nums.values()], *[FadeIn(e) for e in entries.values()],
               *[FadeOut(rr) for rr in list(row_rects.values()) + list(col_rects.values())],
               FadeIn(slab), FadeIn(link), run_time=1.0)
    scene.play(FadeIn(U), FadeIn(ulabs), FadeIn(uname), run_time=0.6)
    hl = SurroundingRectangle(D.cell(*pos[1]), buff=0.02, color=YELLOW, stroke_width=4)
    scene.play(ShowCreation(hl), run_time=0.3)
    counts = Counter()
    for k in range(1, len(pos) + 1):
        i, j = pos[k]
        x = EX_S[i][j]
        col = counts[x]
        counts[x] += 1
        assert EX_U[x - 1][col] == k
        t = Tex(str(k), font_size=34).move_to(nums[pos[k]])
        anims = [t.animate.move_to(U.cell_center(x - 1, col)).set_fill(NUM_COLORS[x])]
        if k > 1:
            anims.append(hl.animate.move_to(D.cell(i, j)))
        for pr in ROW_PAIRS:
            if pr[1] == k:
                anims += [ShowCreationThenFadeOut(flashes[pr]), Indicate(r1, color=ROW_C, scale_factor=1.03)]
        for pr in COL_PAIRS:
            if pr[1] == k:
                anims += [ShowCreationThenFadeOut(flashes[pr]), Indicate(r2, color=COL_C, scale_factor=1.03)]
        scene.play(*anims, run_time=0.75)
    scene.play(FadeOut(hl), run_time=0.3)
    scene.say("斜表的「列不減」變成 (i)、「行遞增」變成 (ii)：兩邊一一對應")
    scene.wait(2.4)


# =============================================================================
# 第 4 段：每個 μ 數一數（同樣 15 個）；Zelevinsky
# =============================================================================
def part_count(scene):
    mus = list(CH5_DECOMP)
    xs = [-3.9 + 1.25 * k for k in range(len(mus))]
    title = mixed("$\\nu/\\lambda=" + tuple_str(NU) + "/" + tuple_str(LAM) + "$", "：每個 ", "$\\mu$",
                  " 的標準表逐一檢查 (i)(ii)", font_size=26).move_to(2.55 * UP)
    ys = (1.6, 0.85, 0.1)
    fvals = [len(standard_tableaux(mu)) for mu in mus]
    pvals = [len(remmel_whitney(NU, LAM, mu)) for mu in mus]
    assert F_TOTAL == sum(fvals) and LR_TOTAL == sum(pvals) and pvals == [CH5_DECOMP[mu] for mu in mus]
    heads = VGroup(Tex(r"\mu", font_size=30, fill_color=MUTED_COLOR),
                   zh("標準表", font_size=22, color=MUTED_COLOR), zh("過關", font_size=22, color=OK_COLOR))
    for h, y in zip(heads, ys):
        h.move_to([-6.6, y, 0], aligned_edge=LEFT)
    mrow = VGroup(*[Tex(tuple_str(mu), font_size=24).move_to([x, ys[0], 0]) for mu, x in zip(mus, xs)])
    frow = VGroup(*[Tex(str(f), font_size=30, fill_color=GREY_A).move_to([x, ys[1], 0]) for f, x in zip(fvals, xs)])
    prow = VGroup(*[Tex(str(c), font_size=34, fill_color=OK_COLOR).move_to([x, ys[2], 0]) for c, x in zip(pvals, xs)])
    hline = Line([-6.6, 1.25, 0], [6.7, 1.25, 0], stroke_color=GREY_C, stroke_width=2)
    total = mixed("共 ", f"${sum(fvals)}$", " 個標準表，過關的恰好 ", f"${sum(pvals)}$", " 個＝LR 斜表的個數",
                  font_size=28)
    total.move_to(1.05 * DOWN)
    tbox = SurroundingRectangle(total, buff=0.15, color=OK_COLOR, stroke_width=3)
    zel = mixed("Zelevinsky 的說法：", "$\\mu$", " 與 ", "$\\nu/\\lambda$", " 之間保持順序的對應（picture）也恰有 ",
                "$c^{\\nu}_{\\lambda\\mu}$", " 個", font_size=22, color=MUTED_COLOR).move_to(2.2 * DOWN)
    assert_in_frame(title, heads, mrow, frow, prow, hline, tbox, zel)
    for k in range(len(mus) - 1):
        assert_apart(mrow[k], mrow[k + 1], gap=0.1)
    for a, b in [(title, mrow), (heads, mrow), (heads, frow), (heads, prow), (prow, tbox), (tbox, zel)]:
        assert_apart(a, b, gap=0.12)

    scene.say("對每個 ", "$\\mu$", "，把 ", "$\\mu$", " 上所有標準表拿來檢查")
    scene.play(FadeIn(title), FadeIn(heads), ShowCreation(hline), FadeIn(mrow), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(t, shift=0.1 * DOWN) for t in frow], lag_ratio=0.1), run_time=1.0)
    scene.wait(0.6)
    scene.say("能過關的很少：個數正是 ", "$c^{\\nu}_{\\lambda\\mu}$")
    scene.play(LaggedStart(*[FadeIn(t, scale=1.5) for t in prow], lag_ratio=0.12), run_time=1.4)
    scene.wait(0.8)
    scene.say("合起來又是 ", f"${LR_TOTAL}$", "：和上一集機器找到的 LR 斜表一樣多")
    scene.play(FadeIn(total), ShowCreation(tbox), run_time=0.8)
    scene.wait(1.6)
    scene.say("還有一副眼鏡：Zelevinsky 的 picture，答案也一樣")
    scene.play(FadeIn(zel, shift=0.1 * UP), run_time=0.7)
    scene.wait(2.0)


# =============================================================================
# 第 5 段：彩蛋——練習 8，卡塔蘭數
# =============================================================================
def part_catalan(scene):
    title = mixed("彩蛋：只有 1 和 2、各 ", "$n$", " 個的反格字（練習 8）", font_size=28).move_to(2.6 * UP)
    hx = (-4.6, -1.85, 0.6)
    heads = VGroup(mixed("$n=" + str(CAT_N) + "$", " 的字", font_size=20, color=MUTED_COLOR),
                   zh("山路（從右往左：1 上、2 下）", font_size=20, color=MUTED_COLOR),
                   mixed("$U(w)$", font_size=20, color=MUTED_COLOR))
    for h, x in zip(heads, hx):
        h.move_to([x, 2.0, 0])
    rows = []
    for k, w in enumerate(CAT_WORDS):
        y = 1.4 - 0.78 * k
        wm = WordMob(w, size=0.36, colors=[NUM_COLORS[a] for a in w], center=np.array([hx[0], y, 0]))
        path = dyck_path(w, hx[1] - 0.66, y - 0.3)
        u = tableau_mob(u_of_word(w), 0.34, center=np.array([hx[2], y, 0]))
        rows.append(VGroup(wm, path, u))
    ns = range(1, len(CAT_COUNTS) + 1)
    x0, dx = 2.9, 0.62
    nrow = VGroup(Tex("n", font_size=28, fill_color=MUTED_COLOR).move_to([x0 - 0.7, 0.9, 0]),
                  *[Tex(str(n), font_size=28, fill_color=MUTED_COLOR).move_to([x0 + dx * (n - 1), 0.9, 0]) for n in ns])
    crow = VGroup(Tex(r"\#", font_size=28).move_to([x0 - 0.7, 0.25, 0]),
                  *[Tex(str(c), font_size=30, fill_color=YELLOW).move_to([x0 + dx * (n - 1), 0.25, 0])
                    for n, c in zip(ns, CAT_COUNTS)])
    formula = Tex(r"C_n=\frac{(2n)!}{n!\,(n+1)!}", font_size=36).move_to([4.45, -0.85, 0])
    back = zh("又回到卡塔蘭數！", font_size=30, color=OK_COLOR).move_to([4.45, -1.95, 0])
    assert_in_frame(title, heads, *rows, nrow, crow, formula, back)
    for k in range(len(rows) - 1):
        assert_apart(rows[k], rows[k + 1], gap=0.05)
    for row in rows:
        assert_apart(row[0], row[1], gap=0.2)
        assert_apart(row[1], row[2], gap=0.2)
        assert_apart(row, VGroup(nrow, crow, formula, back), gap=0.3)
    for a, b in [(title, heads), (heads, rows[0]), (nrow, crow), (crow, formula), (formula, back)]:
        assert_apart(a, b, gap=0.1)

    scene.say("彩蛋：字裡只有 1 和 2、各 ", "$n$", " 個，有幾個反格字？")
    scene.play(FadeIn(title), run_time=0.7)
    scene.play(FadeIn(heads[0]), LaggedStart(*[FadeIn(r[0], shift=0.1 * RIGHT) for r in rows], lag_ratio=0.15),
               run_time=1.2)
    scene.say("$n=" + str(CAT_N) + "$", f" 時有 {len(CAT_WORDS)} 個；從右往左讀，1 是上坡、2 是下坡")
    scene.play(FadeIn(heads[1]), LaggedStart(*[ShowCreation(r[1]) for r in rows], lag_ratio=0.15), run_time=1.8)
    scene.say("反格字＝永遠不跌破地面的山路")
    scene.wait(1.2)
    scene.say("換成 ", "$U(w)$", "：正好是 ", "$(" + str(CAT_N) + "," + str(CAT_N) + ")$", " 形的全部標準表")
    scene.play(FadeIn(heads[2]), LaggedStart(*[FadeIn(r[2]) for r in rows], lag_ratio=0.12), run_time=1.0)
    scene.wait(1.2)
    scene.say("數一數 ", "$n=1,2,\\dots,6$", "：", ", ".join(str(c) for c in CAT_COUNTS))
    scene.play(FadeIn(nrow), LaggedStart(*[FadeIn(t, scale=1.4) for t in crow], lag_ratio=0.12), run_time=1.4)
    scene.wait(0.6)
    scene.say("正是卡塔蘭數 ", "$C_n$", "：LR 的故事又接回了卡塔蘭系列")
    scene.play(FadeIn(formula, shift=0.1 * UP), run_time=0.7)
    scene.play(FadeIn(back, scale=1.2), run_time=0.7)
    scene.wait(2.0)


class SceneF24LROther(ChuScene):
    def construct(self):
        self.show_header("LR 數的其他算法")
        check_math()
        part_hook(self)
        self.clear_stage()
        part_uw(self)
        self.clear_stage()
        part_rw(self)
        self.clear_stage()
        part_count(self)
        self.clear_stage()
        part_catalan(self)
        self.wait(1.0)
