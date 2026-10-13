"""
Scene F02 —— 表、標準表、轉置、斜表（Fulton《Young Tableaux》Notation，p.2、p.4）

    表（tableau）：Young 圖每格填正整數，每列 → 弱遞增（≤）、每行 ↓ 嚴格遞增（<）
        例：[[1,2,2,3,3,5],[2,3,5,5],[4,4,6,6],[5,6]]，形狀 (6,4,4,2) ⊢ 16
    標準表：1..n 各用一次，例：[[1,3,7,12,13,15],[2,5,10,14],[4,8,11,16],[6,9]]
    轉置 T^τ：沿主對角線翻轉；標準表轉置後仍是標準表，一般的表不一定（列裡相等的數變成同一行）
    斜形狀 λ/μ = (5,5,4,3,2)/(4,4,1)，斜表 [[·,·,·,·,2],[·,·,·,·,6],[·,2,4,4],[2,3,6],[5,6]]（p.4）

數學資料全部由 utils/tableaux.py 檢查。格子 (i, j) 0 起算。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF02_tableaux.py SceneF02Tableaux
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.mit_draw import CATALAN_COLOR, YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh
from utils.tableaux import (
    FULTON_SKEW,
    FULTON_STANDARD,
    FULTON_TABLEAU,
    conjugate,
    contains,
    is_skew_tableau,
    is_standard,
    is_tableau,
    num_boxes,
    shape,
    skew_boxes,
    skew_shape,
    transpose,
)

T = FULTON_TABLEAU                       # p.2 左圖
S = FULTON_STANDARD                      # p.2 右圖
LAM = (6, 4, 4, 2)
SKEW_LAM = (5, 5, 4, 3, 2)
SKEW_MU = (4, 4, 1)
SKEW_P4 = ((None, None, None, None, 2),  # p.4 的斜表（最後一列是 5 6；p.12 的 FULTON_SKEW 是 5 5）
           (None, None, None, None, 6),
           (None, 2, 4, 4),
           (2, 3, 6),
           (5, 6))
SKEW_ROW = 2                             # 示範的列：2 ≤ 4 ≤ 4
SKEW_COL = 1                             # 示範的行：2 < 3 < 6

ROW_COLOR = YELLOW
COL_COLOR = TEAL
MU_COLOR = GREY_D
X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


# =============================================================================
# 小工具（模組層級，連續播放時才找得到）
# =============================================================================
def assert_in_frame(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def assert_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊（至少一個方向分開 gap）。"""
    apart_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    apart_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert apart_x or apart_y, (a, b)


def tuple_str(parts):
    return "(" + ",".join(str(p) for p in parts) + ")"


def chain_tex(values, rel, font_size=30, color=WHITE):
    """1\\le 2\\le 2 ... 這種比較鏈。"""
    return Tex(rel.join(str(v) for v in values), font_size=font_size, fill_color=color)


def columns_of(T_):
    """各行由上到下的數（T_ 可以是斜表，None 略過）。"""
    width = max(len(r) for r in T_)
    return [[r[j] for r in T_ if j < len(r) and r[j] is not None] for j in range(width)]


def row_rect(diag, i, cols, color, buff=0.03):
    return SurroundingRectangle(diag.cell_group([(i, j) for j in cols]), buff=buff, color=color,
                                stroke_width=4)


def col_rect(diag, j, rows, color, buff=0.03):
    return SurroundingRectangle(diag.cell_group([(i, j) for i in rows]), buff=buff, color=color,
                                stroke_width=4)


def equal_row_pairs(T_):
    """表裡同一列相鄰且相等的格子對 ((i, j), (i, j+1))。"""
    return [((i, j), (i, j + 1)) for i, r in enumerate(T_) for j in range(len(r) - 1) if r[j] == r[j + 1]]


def column_violations(T_):
    """同一行相鄰、上面 >= 下面（違反行嚴格遞增）的格子對。"""
    return [((i, j), (i + 1, j)) for i in range(len(T_) - 1) for j in range(len(T_[i + 1]))
            if T_[i][j] >= T_[i + 1][j]]


def check_math():
    n = sum(LAM)
    assert shape(T) == LAM == shape(S) and n == 16 == num_boxes(T) == num_boxes(S)
    assert is_tableau(T) and not is_standard(T)
    assert is_tableau(S) and is_standard(S)
    assert sorted(v for r in S for v in r) == list(range(1, n + 1))
    # 列弱增、行嚴格增（畫面上的比較鏈）
    assert all(a <= b for r in T for a, b in zip(r, r[1:]))
    cols = columns_of(T)
    assert cols == [[1, 2, 4, 5], [2, 3, 4, 6], [2, 5, 6], [3, 5, 6], [3], [5]]
    assert all(a < b for c in cols for a, b in zip(c, c[1:]))
    assert [len(c) for c in cols] == list(conjugate(LAM)) == [4, 4, 3, 3, 1, 1]
    # 轉置
    TT, ST = transpose(T), transpose(S)
    assert shape(TT) == shape(ST) == conjugate(LAM) == (4, 4, 3, 3, 1, 1)
    assert all(TT[j][i] == T[i][j] and ST[j][i] == S[i][j] for i, r in enumerate(T) for j in range(len(r)))
    assert is_standard(ST) and not is_tableau(TT)
    eq = equal_row_pairs(T)
    viol = column_violations(TT)
    assert eq == [((0, 1), (0, 2)), ((0, 3), (0, 4)), ((1, 2), (1, 3)), ((2, 0), (2, 1)), ((2, 2), (2, 3))]
    assert sorted(((b, a), (d, c)) for (a, b), (c, d) in eq) == sorted(viol)
    assert equal_row_pairs(S) == [] and column_violations(ST) == []
    assert T[0][1] == T[0][2] == 2                 # 字幕裡的例子「2 和 2」
    # 斜表（p.4）
    assert is_skew_tableau(SKEW_P4) and skew_shape(SKEW_P4) == (SKEW_LAM, SKEW_MU)
    assert contains(SKEW_LAM, SKEW_MU) and all(m <= l for m, l in zip(SKEW_MU, SKEW_LAM))
    assert SKEW_P4[:4] == FULTON_SKEW[:4] and SKEW_P4[4] == (5, 6) != FULTON_SKEW[4]
    assert sum(SKEW_LAM) == 19 and sum(SKEW_MU) == 9
    assert num_boxes(SKEW_P4) == 10 == len(skew_boxes(SKEW_LAM, SKEW_MU)) == 19 - 9
    row_vals = [v for v in SKEW_P4[SKEW_ROW] if v is not None]
    col_vals = columns_of(SKEW_P4)[SKEW_COL]
    assert row_vals == [2, 4, 4] and col_vals == [2, 3, 6]
    return TT, ST, eq, viol


# =============================================================================
# 第 1 段：表的定義，逐列、逐行檢查
# =============================================================================
def part_definition(scene):
    cs = 0.66
    D = YoungDiagramMob(LAM, cell_size=cs, top_left=np.array([-6.4, 2.5, 0.0]), entries=T, font_size=34,
                        fill_color=CATALAN_COLOR, fill_opacity=0.12)
    lam_tex = Tex(r"\lambda=" + tuple_str(LAM) + r"\vdash " + str(sum(LAM)), font_size=38)
    lam_tex.next_to(D, DOWN, buff=0.4).align_to(D, LEFT)

    rule_title = mixed("表：每格填正整數，並且", font_size=26)
    rule1 = mixed("每一列 ", "$\\rightarrow$", " 不減：", "$\\le$", "（可以相等）", font_size=26, color=ROW_COLOR)
    rule2 = mixed("每一行 ", "$\\downarrow$", " 遞增：", "$<$", "（不能相等）", font_size=26, color=COL_COLOR)
    rules = VGroup(rule_title, rule1, rule2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    rules.shift((1.75 - rules.get_left()[0]) * RIGHT + (2.7 - rules.get_top()[1]) * UP)

    row_chains = VGroup()
    for i, r in enumerate(T):
        ch = chain_tex(r, r"\le ", font_size=32, color=ROW_COLOR)
        ch.move_to(np.array([-2.0, D.cell_center(i, 0)[1], 0.0]), aligned_edge=LEFT)
        row_chains.add(ch)

    cols = columns_of(T)
    long_cols = [j for j, c in enumerate(cols) if len(c) >= 2]
    assert long_cols == [0, 1, 2, 3]
    col_block = VGroup()
    for j in long_cols:
        lab = mixed("第 " + str(j + 1) + " 行", font_size=20, color=MUTED_COLOR)
        ch = chain_tex(cols[j], "<", font_size=32, color=COL_COLOR)
        col_block.add(VGroup(lab, ch).arrange(DOWN, buff=0.12))
    col_block.arrange_in_grid(n_rows=2, n_cols=2, h_buff=0.9, v_buff=0.3)
    col_block.next_to(rules, DOWN, buff=0.5).align_to(rules, LEFT).shift(0.35 * RIGHT)
    single_note = mixed("第 5、6 行只有一格，不必比較", font_size=22, color=MUTED_COLOR)
    single_note.next_to(col_block, DOWN, buff=0.3).align_to(col_block, LEFT)

    verdict = mixed("所以這是形狀 ", "$" + tuple_str(LAM) + "$", " 的表", font_size=28, color=OK_COLOR)
    verdict_box = SurroundingRectangle(verdict, buff=0.18, color=OK_COLOR, stroke_width=3)
    VGroup(verdict, verdict_box).move_to(np.array([0.0, -2.0, 0.0]))

    assert_in_frame(D, lam_tex, rules, row_chains, col_block, single_note, verdict_box)
    assert_apart(D, row_chains, gap=0.3)
    assert_apart(row_chains, rules, gap=0.3)
    assert_apart(row_chains, col_block, gap=0.3)
    assert_apart(rules, col_block, gap=0.15)
    assert_apart(col_block, single_note)
    assert_apart(single_note, verdict_box)
    assert_apart(D, lam_tex)
    assert_apart(lam_tex, verdict_box, gap=0.3)
    for a, b in zip(row_chains[:-1], row_chains[1:]):
        assert_apart(a, b)

    scene.say("在 Young 圖的格子裡填正整數，滿足兩個條件，就叫做一個「表」（tableau）")
    scene.play(ShowCreation(D.cells), FadeIn(lam_tex), run_time=0.9)
    scene.play(LaggedStart(*[FadeIn(m, scale=1.3) for m in D.entries], lag_ratio=0.05), run_time=1.2)
    scene.play(FadeIn(rule_title), run_time=0.5)
    scene.wait(0.6)

    # ------------------------------------------------------------- 列：弱遞增
    scene.say("條件一：每一列從左往右不能變小，但可以相等")
    scene.play(FadeIn(rule1, shift=0.15 * UP), run_time=0.6)
    for i, r in enumerate(T):
        rect = row_rect(D, i, range(len(r)), ROW_COLOR)
        scene.play(ShowCreation(rect), FadeIn(row_chains[i], shift=0.2 * RIGHT), run_time=0.5)
        scene.play(FadeOut(rect), run_time=0.25)
    scene.wait(0.5)

    # ------------------------------------------------------------- 行：嚴格遞增
    scene.say("條件二：每一行從上往下一定要變大，不能相等")
    scene.play(FadeIn(rule2, shift=0.15 * UP), run_time=0.6)
    for k, j in enumerate(long_cols):
        rect = col_rect(D, j, range(len(cols[j])), COL_COLOR)
        scene.play(ShowCreation(rect), FadeIn(col_block[k], shift=0.15 * UP), run_time=0.5)
        scene.play(FadeOut(rect), run_time=0.25)
    singles = VGroup(*[col_rect(D, j, range(len(cols[j])), COL_COLOR) for j in range(len(cols))
                       if j not in long_cols])
    scene.play(ShowCreation(singles), FadeIn(single_note), run_time=0.6)
    scene.play(FadeOut(singles), FadeIn(verdict), ShowCreation(verdict_box), run_time=0.7)
    scene.say("兩個條件都成立：這是形狀 ", "$" + tuple_str(LAM) + "$", " 的表，共 ", "$" + str(sum(LAM)) + "$", " 格")
    scene.wait(1.4)
    return D


# =============================================================================
# 第 2、3 段：標準表與轉置
# =============================================================================
def part_standard_transpose(scene, D_big, TT, ST, eq, viol):
    cs = 0.48
    top = 2.2
    D = YoungDiagramMob(LAM, cell_size=cs, top_left=np.array([-6.5, top, 0.0]), entries=T, font_size=26,
                        fill_color=CATALAN_COLOR, fill_opacity=0.12)
    DS = YoungDiagramMob(LAM, cell_size=cs, top_left=np.array([0.3, top, 0.0]), entries=S, font_size=24,
                         fill_color=CATALAN_COLOR, fill_opacity=0.12)
    lab_T = zh("表", font_size=26).next_to(D, UP, buff=0.22)
    lab_S = zh("標準表", font_size=26).next_to(DS, UP, buff=0.22)
    note_S = mixed("$1,2,\\dots," + str(sum(LAM)) + "$", " 各用一次", font_size=24, color=OK_COLOR)
    note_S.next_to(DS, DOWN, buff=0.3)

    # 轉置後的圖
    conj = conjugate(LAM)
    DT = YoungDiagramMob(conj, cell_size=cs, top_left=np.array([-2.55, top, 0.0]), entries=TT, font_size=26,
                         fill_color=CATALAN_COLOR, fill_opacity=0.12)
    DST = YoungDiagramMob(conj, cell_size=cs, top_left=np.array([4.3, top, 0.0]), entries=ST, font_size=24,
                          fill_color=CATALAN_COLOR, fill_opacity=0.12)
    mid_T = D.get_center()[1]
    arr_T = Arrow(np.array([D.get_right()[0] + 0.15, mid_T, 0.0]), np.array([DT.get_left()[0] - 0.15, mid_T, 0.0]),
                  buff=0, thickness=2.5, fill_color=GREY_B)
    arr_S = Arrow(np.array([DS.get_right()[0] + 0.15, mid_T, 0.0]), np.array([DST.get_left()[0] - 0.15, mid_T, 0.0]),
                  buff=0, thickness=2.5, fill_color=GREY_B)
    tau_T = Tex(r"\tau", font_size=34, fill_color=GREY_B).next_to(arr_T, UP, buff=0.1)
    tau_S = Tex(r"\tau", font_size=34, fill_color=GREY_B).next_to(arr_S, UP, buff=0.1)
    lab_TT = Tex(r"T^{\tau}", font_size=32).next_to(DT, UP, buff=0.15)
    lab_T_sym = Tex("T", font_size=32)
    lab_T_full = VGroup(lab_T, lab_T_sym)
    lab_T_sym.next_to(lab_T, RIGHT, buff=0.12)
    lab_T_full.next_to(D, UP, buff=0.22)
    verdict_T = mixed("不是表", font_size=26, color=CROSSING_COLOR).next_to(DT, DOWN, buff=0.3)
    verdict_S = mixed("仍是標準表", font_size=26, color=OK_COLOR).next_to(DST, DOWN, buff=0.3)

    why = VGroup(
        mixed("表的一列可以有相等的數，例如 ", "$2\\le 2$", font_size=24),
        mixed("轉置後它們落在同一行，卻要 ", "$2<2$", "：不成立", font_size=24),
    ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    why.move_to(np.array([-3.4, -2.2, 0.0]))
    why[1][1].set_fill(CROSSING_COLOR)
    why_S = VGroup(
        mixed("標準表沒有重複的數，", font_size=24),
        mixed("列、行本來都嚴格遞增，翻過來照樣成立", font_size=24),
    ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    why_S.move_to(np.array([3.4, -2.2, 0.0]))

    assert_in_frame(D, DS, DT, DST, lab_T_full, lab_S, lab_TT, note_S, verdict_T, verdict_S, why, why_S)
    assert_apart(D, arr_T)
    assert_apart(arr_T, DT)
    assert_apart(DT, DS, gap=0.4)
    assert_apart(DS, arr_S)
    assert_apart(arr_S, DST)
    assert_apart(note_S, DST, gap=0.2)
    assert_apart(note_S, verdict_S, gap=0.2)
    assert_apart(verdict_T, why, gap=0.2)
    assert_apart(verdict_S, why_S, gap=0.2)
    assert_apart(note_S, why_S, gap=0.2)
    assert_apart(why, why_S, gap=0.3)
    assert_apart(lab_TT, tau_T)
    assert lab_T_full.get_top()[1] <= Y_MAX

    # ------------------------------------------------------------- 標準表
    others = [m for m in scene.mobjects if m is not scene.frame and m is not scene.header_mob
              and m is not D_big and m is not scene.caption_mob]
    scene.play(*[FadeOut(m) for m in others], ReplacementTransform(D_big, D), run_time=0.9)
    scene.play(FadeIn(lab_T_full), run_time=0.4)
    scene.say("如果 1 到 ", "$" + str(sum(LAM)) + "$", " 每個數都剛好用一次，就叫做「標準表」")
    scene.play(ShowCreation(DS.cells), FadeIn(lab_S), run_time=0.7)
    order = sorted((v, (i, j)) for i, r in enumerate(S) for j, v in enumerate(r))
    scene.play(LaggedStart(*[FadeIn(DS.entry(i, j), scale=1.4) for _, (i, j) in order], lag_ratio=0.18),
               run_time=2.4)
    scene.play(FadeIn(note_S, shift=0.15 * UP), run_time=0.5)
    scene.wait(0.8)

    # ------------------------------------------------------------- 轉置
    scene.say("沿著左上到右下的對角線翻過去：第 ", "$i$", " 列變成第 ", "$i$", " 行，叫做轉置 ", "$T^{\\tau}$")
    scene.play(GrowArrow(arr_T), FadeIn(tau_T), GrowArrow(arr_S), FadeIn(tau_S), run_time=0.6)
    anims = []
    for i, r in enumerate(T):
        for j in range(len(r)):
            anims.append(TransformFromCopy(D.cell(i, j), DT.cell(j, i)))
            anims.append(TransformFromCopy(D.entry(i, j), DT.entry(j, i)))
            anims.append(TransformFromCopy(DS.cell(i, j), DST.cell(j, i)))
            anims.append(TransformFromCopy(DS.entry(i, j), DST.entry(j, i)))
    scene.play(*anims, FadeIn(lab_TT), run_time=1.8)
    scene.remove(*[a.mobject for a in anims])
    scene.add(DT, DST)
    scene.wait(0.6)

    # 標準表：轉置後仍標準
    scene.say("標準表轉置以後，仍然是標準表")
    scene.play(DST.cells.animate.set_fill(OK_COLOR, opacity=0.25), FadeIn(verdict_S, shift=0.15 * UP),
               FadeIn(why_S), run_time=0.9)
    scene.wait(1.6)

    # 一般的表：相等的數出問題
    scene.say("一般的表就不一定：列裡相等的數，翻過來在同一行上下相等，違反條件二")
    first = eq[0]
    rT = SurroundingRectangle(D.cell_group(first), buff=0.03, color=CROSSING_COLOR, stroke_width=5)
    first_t = [(b, a) for a, b in first]
    assert (first_t[0], first_t[1]) in viol
    rTT = SurroundingRectangle(DT.cell_group(first_t), buff=0.03, color=CROSSING_COLOR, stroke_width=5)
    scene.play(ShowCreation(rT), FadeIn(why[0]), run_time=0.7)
    scene.play(TransformFromCopy(rT, rTT), FadeIn(why[1]), run_time=0.9)
    scene.wait(0.8)
    bad_T = sorted({c for pair in eq for c in pair})
    bad_TT = sorted({c for pair in viol for c in pair})
    scene.play(*[D.cell(i, j).animate.set_fill(CROSSING_COLOR, opacity=0.4) for i, j in bad_T],
               *[DT.cell(i, j).animate.set_fill(CROSSING_COLOR, opacity=0.4) for i, j in bad_TT],
               FadeIn(verdict_T, shift=0.15 * UP), run_time=0.9)
    assert len(eq) == len(viol) == 5
    scene.say("$T$", " 的列裡有 ", "$" + str(len(eq)) + "$", " 對相鄰又相等的數，轉置後每一對都變成同一行的上下兩格")
    scene.wait(2.0)


# =============================================================================
# 第 4 段：斜形狀與斜表
# =============================================================================
def part_skew(scene):
    cs = 0.64
    top = 2.45
    big = YoungDiagramMob(SKEW_LAM, cell_size=cs, top_left=np.array([-6.4, top, 0.0]),
                          fill_color=CATALAN_COLOR, fill_opacity=0.3)
    mu_cells = [(i, j) for i, m in enumerate(SKEW_MU) for j in range(m)]
    skew = YoungDiagramMob(SKEW_LAM, cell_size=cs, top_left=np.array([-1.6, top, 0.0]),
                           fill_color=CATALAN_COLOR, fill_opacity=0.3)
    for i, j in mu_cells:
        skew.cell(i, j).set_fill(MU_COLOR, opacity=0.85).set_stroke(GREY_C, width=1.5)
    skew.set_entries(SKEW_P4, font_size=34)

    lam_s, mu_s = sum(SKEW_LAM), sum(SKEW_MU)
    lam_tex = Tex(r"\lambda=" + tuple_str(SKEW_LAM), font_size=34)
    mu_tex = Tex(r"\mu=" + tuple_str(SKEW_MU), font_size=34, fill_color=GREY_B)
    sub_tex = mixed("$\\mu\\subset\\lambda$", "：每一列 ", "$\\mu_i\\le\\lambda_i$", font_size=24)
    info = VGroup(lam_tex, mu_tex, sub_tex).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    info.next_to(big, DOWN, buff=0.35).align_to(big, LEFT)

    arrow = Arrow(np.array([big.get_right()[0] + 0.2, big.get_center()[1], 0.0]),
                  np.array([skew.get_left()[0] - 0.2, big.get_center()[1], 0.0]), buff=0, thickness=2.5,
                  fill_color=GREY_B)
    skew_lab = mixed("挖掉 ", "$\\mu$", font_size=22, color=GREY_B)
    skew_lab.next_to(arrow, UP, buff=0.1)
    count = mixed("斜形狀 ", "$\\lambda/\\mu$", "：剩下 ", "$" + f"{lam_s}-{mu_s}={lam_s - mu_s}" + "$", " 格",
                  font_size=26)
    count.next_to(skew, DOWN, buff=0.35).align_to(skew, LEFT)

    rules = VGroup(
        mixed("斜表：規則和表一樣", font_size=26),
        mixed("列 ", "$\\rightarrow$", " 不減，例如 ", "$2\\le 4\\le 4$", font_size=26, color=ROW_COLOR),
        mixed("行 ", "$\\downarrow$", " 遞增，例如 ", "$2<3<6$", font_size=26, color=COL_COLOR),
    ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
    rules.shift((2.6 - rules.get_left()[0]) * RIGHT + (2.35 - rules.get_top()[1]) * UP)
    empty_note = mixed("$\\mu=\\varnothing$", " 時就是一般的表", font_size=26, color=MUTED_COLOR)
    empty_note.next_to(rules, DOWN, buff=0.55).align_to(rules, LEFT)

    row_cells = [(SKEW_ROW, j) for j in range(SKEW_MU[SKEW_ROW], SKEW_LAM[SKEW_ROW])]
    col_cells = [(i, SKEW_COL) for i in range(len(SKEW_LAM)) if SKEW_P4[i][SKEW_COL:SKEW_COL + 1]
                 and SKEW_P4[i][SKEW_COL] is not None]
    assert row_cells == [(2, 1), (2, 2), (2, 3)] and col_cells == [(2, 1), (3, 1), (4, 1)]
    assert [SKEW_P4[i][j] for i, j in row_cells] == [2, 4, 4]
    assert [SKEW_P4[i][j] for i, j in col_cells] == [2, 3, 6]
    r_rect = SurroundingRectangle(skew.cell_group(row_cells), buff=0.03, color=ROW_COLOR, stroke_width=4)
    c_rect = SurroundingRectangle(skew.cell_group(col_cells), buff=0.03, color=COL_COLOR, stroke_width=4)

    assert_in_frame(big, skew, info, arrow, skew_lab, count, rules, empty_note)
    assert_apart(big, arrow)
    assert_apart(arrow, skew)
    assert_apart(skew_lab, big)
    assert_apart(skew_lab, skew)
    assert_apart(big, info)
    assert_apart(skew, count)
    assert_apart(skew, rules, gap=0.3)
    assert_apart(info, count, gap=0.3)
    assert_apart(count, rules, gap=0.2)
    assert_apart(rules, empty_note)
    assert_apart(count, empty_note, gap=0.2)

    scene.say("斜形狀：從一個大 Young 圖 ", "$\\lambda$", " 挖掉裝在它裡面的小圖 ", "$\\mu$")
    scene.play(ShowCreation(big.cells), FadeIn(lam_tex), run_time=0.9)
    scene.play(*[big.cell(i, j).animate.set_fill(MU_COLOR, opacity=0.85) for i, j in mu_cells],
               FadeIn(mu_tex), run_time=0.8)
    scene.say("$\\mu$", " 裝在 ", "$\\lambda$", " 裡面，意思是每一列都有 ", "$\\mu_i\\le\\lambda_i$")
    scene.play(FadeIn(sub_tex, shift=0.15 * UP), run_time=0.6)
    scene.wait(1.0)

    scene.say("剩下的格子組成斜形狀 ", "$\\lambda/\\mu$", "，這裡共 ", "$" + str(lam_s - mu_s) + "$", " 格")
    grow = TransformFromCopy(big.cells, skew.cells)
    scene.play(GrowArrow(arrow), FadeIn(skew_lab), grow, run_time=1.1)
    scene.remove(grow.mobject)
    scene.add(skew.cells)
    scene.play(FadeIn(count), run_time=0.5)
    scene.wait(0.6)

    scene.say("在斜形狀上照同樣的規則填數，就得到「斜表」")
    scene.play(LaggedStart(*[FadeIn(m, scale=1.3) for m in skew.entries], lag_ratio=0.1), FadeIn(rules[0]),
               run_time=1.2)
    scene.play(ShowCreation(r_rect), FadeIn(rules[1]), run_time=0.7)
    scene.play(ShowCreation(c_rect), FadeIn(rules[2]), run_time=0.7)
    scene.wait(1.0)
    scene.say("$\\mu$", " 是空的時候，斜表就是普通的表；後面的滑動遊戲會一直用到斜表")
    scene.play(FadeIn(empty_note, shift=0.15 * UP), FadeOut(r_rect), FadeOut(c_rect), run_time=0.7)
    scene.wait(2.0)


class SceneF02Tableaux(ChuScene):
    def construct(self):
        self.show_header("表、標準表與斜表")
        TT, ST, eq, viol = check_math()
        D = part_definition(self)
        part_standard_transpose(self, D, TT, ST, eq, viol)
        self.clear_stage()
        part_skew(self)
        self.wait(1.0)
