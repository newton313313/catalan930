"""
Scene F13 —— 行字（Fulton《Young Tableaux》§2.3，書 p.27–29）

    行字 w_col(T)：每一行由下往上讀，行由左到右
        T = [[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]] → w_col = 5 4 2 1 | 6 4 3 2 | 6 5 2 | 5 3
        把 w_col 依序列插入空表，長回同一個 T → (10) w_col(T) ≡ w_row(T) = w(T)
    Lemma 1：用水平或垂直線把斜表 T 切成 T′、T″，則 w(T) ≡ w(T′)·w(T″)
        水平切：字本來就是先讀下半塊；垂直切（例：切在第 2 行之後）：T′ 移到 T″ 的左下得 T′∗T″
        （它的字 = w(T′)w(T″)），從 T′ 正上方的內角由右到左滑 6 次（每次挑最右邊的內角）回到 T；
        滑動保持 Knuth 等價（Proposition 2）
    逐行剝下：w(T) ≡ w(C1)·w(C2)·w(C3)·w(C4) = w_col(T)；Lemma 2：其實只用 K′ 就夠（一句）

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算；字幕裡的「第 k 行」1 起算）。
滑動的板子沿用 F07 的工具（make_board、anims_open_hole、anims_move、anims_drop_cell）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF13_column_words.py SceneF13ColumnWords
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from scenes.sceneF07_jeu_de_taquin import (
    anims_drop_cell,
    anims_move,
    anims_open_hole,
    board_as_skew,
    make_board,
    new_cell,
)
from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob, word_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    FULTON_INSERT_T,
    column_word,
    insert_word,
    insert_word_steps,
    jdt_steps,
    star,
    tableau_word,
)

T0 = FULTON_INSERT_T
W_COL = (5, 4, 2, 1, 6, 4, 3, 2, 6, 5, 2, 5, 3)
W_ROW = (5, 6, 4, 4, 6, 2, 3, 5, 5, 1, 2, 2, 3)
COL_LENS = (4, 4, 3, 2)                      # 各行長度＝行字的分段
CUT = 2                                      # 切在第 2 行之後
T_LEFT = ((1, 2), (2, 3), (4, 4), (5, 6))
T_RIGHT = ((2, 3), (5, 5), (6,))
DROP = 3                                     # T″ 有 3 列：T′ 往下移 3 格
CORNERS = ((2, 1), (1, 1), (0, 1), (2, 0), (1, 0), (0, 0))
H_CUT = 2                                    # 水平切的例子：切在第 2 列之下
COL_COLORS = (TEAL, GOLD, PINK, BLUE_B)
LEFT_COLOR, RIGHT_COLOR = TEAL, GOLD


def pick_right(corners):
    """T′ 正上方的內角由右到左：每次挑最右邊（清單最前面）的那個。"""
    return corners[0]


def columns(T):
    """各行由下往上讀的字。"""
    return [tuple(T[i][j] for i in reversed(range(len(T))) if j < len(T[i])) for j in range(len(T[0]))]


def check_math():
    assert column_word(T0) == W_COL and tableau_word(T0) == W_ROW
    assert insert_word(W_COL) == T0 == insert_word(W_ROW)
    assert tuple(len(c) for c in columns(T0)) == COL_LENS and sum(columns(T0), ()) == W_COL
    steps = insert_word_steps(W_COL)
    assert max(len(s[1]) for s in steps) == 4 and max(len(s[1][0]) for s in steps) == 4     # 版面：最大 4×4
    assert tableau_word(T0) == tableau_word(T0[H_CUT:]) + tableau_word(T0[:H_CUT])            # 水平切
    assert T_LEFT == tuple(r[:CUT] for r in T0) and T_RIGHT == tuple(r[CUT:] for r in T0 if len(r) > CUT)
    S = star(T_LEFT, T_RIGHT)
    assert len(T_RIGHT) == DROP and len(T_LEFT[0]) == CUT
    assert S[:DROP] == tuple((None,) * CUT + r for r in T_RIGHT) and S[DROP:] == T_LEFT
    assert tableau_word(S) == tableau_word(T_LEFT) + tableau_word(T_RIGHT)
    slides = jdt_steps(S, pick_right)
    assert tuple(c for c, _, _ in slides) == CORNERS and slides[-1][2] == T0
    assert all(c[1] < CUT and c[0] < DROP for c in CORNERS)                                   # 都在 T′ 正上方
    for c, path, _ in slides:                     # 每次都是 T′ 的一行整段往上移一格
        assert [p[1] for p in path] == [c[1]] * len(path)
        assert [p[0] for p in path] == list(range(c[0], c[0] + len(path)))
    return S, slides


def digits_line(label, groups, colors, font_size=38, buff_in=0.16, buff_out=0.42, baseline=True):
    """VGroup(標籤, 數字群組們)；群組 k 的數字顏色 colors[k]。baseline：數字底線對齊標籤第一個字（否則置中）。"""
    gs = VGroup(*[VGroup(*[Tex(str(v), font_size=font_size, fill_color=col) for v in g]).arrange(RIGHT, buff=buff_in)
                  for g, col in zip(groups, colors)]).arrange(RIGHT, buff=buff_out)
    lab = Tex(label, font_size=font_size)
    gs.next_to(lab, RIGHT, buff=0.25)
    if baseline:
        gs.align_to(lab[0], DOWN)
    return VGroup(lab, gs)


# =============================================================================
# 第 1 段：行字，插入後回到 T
# =============================================================================
def part_column_word(scene):
    cs = 0.62
    tm = tableau_mob(T0, cs, top_left=(-6.3, 2.2, 0))
    name = Tex("T", font_size=40).next_to(tm, DOWN, buff=0.25)
    wcol = digits_line(r"w_{\mathrm{col}}(T)=", columns(T0), COL_COLORS)
    wcol.move_to([-3.0, 1.75, 0], aligned_edge=LEFT)
    wrow = digits_line(r"w_{\mathrm{row}}(T)=", [tuple(r) for r in reversed(T0)], [GREY_A] * len(T0))
    wrow.move_to([-3.0, 0.95, 0], aligned_edge=LEFT)
    wrow.shift((wcol[0].get_right()[0] - wrow[0].get_right()[0]) * RIGHT)     # 兩個等號對齊
    ins_lab = mixed("把行字依序列插入：", font_size=24).move_to([-3.0, -0.25, 0], aligned_edge=LEFT)
    p_top_left = np.array([0.6, 0.15, 0.0])
    p_cs = 0.48
    ghost = Rectangle(width=4 * p_cs, height=4 * p_cs).move_to(p_top_left, aligned_edge=UL)
    eq_t = mixed("$=T$", font_size=34, color=OK_COLOR).next_to(ghost, RIGHT, buff=0.35)
    f10 = mixed("(10)  ", "$w_{\\mathrm{col}}(T)\\equiv w_{\\mathrm{row}}(T)=w(T)$", font_size=30)
    f10.move_to(2.45 * DOWN)
    box10 = SurroundingRectangle(f10, buff=0.15, color=OK_COLOR, stroke_width=3)
    assert_in_frame(tm, name, wcol, wrow, ins_lab, ghost, eq_t, box10)
    assert_apart(VGroup(tm, name), VGroup(wcol, wrow, ins_lab, ghost), gap=0.3)
    assert_apart(wcol, wrow, gap=0.15)
    assert_apart(wrow, VGroup(ins_lab, ghost), gap=0.15)
    assert_apart(ins_lab, ghost, gap=0.2)
    assert_apart(VGroup(ghost, eq_t, name), box10, gap=0.15)

    scene.say("行字：每一行由下往上讀，再由左到右一行接一行")
    scene.play(FadeIn(tm), FadeIn(name), FadeIn(wcol[0]), run_time=0.8)
    for j, g in enumerate(wcol[1]):
        cells = VGroup(*[tm.cell(i, j) for i in range(len(T0)) if j < len(T0[i])])
        src = VGroup(*[tm.entry(i, j) for i in reversed(range(len(T0))) if j < len(T0[i])])
        assert tuple(e.tab_value for e in src) == columns(T0)[j]
        scene.play(cells.animate.set_fill(COL_COLORS[j], opacity=0.3), TransformFromCopy(src, g), run_time=0.75)
    scene.wait(0.6)
    scene.say("原來的字是一列一列讀：", "$w_{\\mathrm{row}}(T)$", "，兩個字長得不一樣")
    scene.play(FadeIn(wrow, shift=0.15 * DOWN), run_time=0.7)
    scene.wait(1.4)

    scene.say("把行字的字母依序列插入空表……")
    digits = [d for g in wcol[1] for d in g]
    marker = SurroundingRectangle(digits[0], buff=0.06, color=YELLOW, stroke_width=3)
    scene.play(FadeIn(ins_lab), ShowCreation(marker), run_time=0.5)
    cur = None
    for k, (x, P, _, _) in enumerate(insert_word_steps(W_COL)):
        assert x == W_COL[k]
        new = tableau_mob(P, p_cs, top_left=p_top_left)
        anims = [FadeIn(new), marker.animate.move_to(digits[k])]
        if cur is not None:
            anims.append(FadeOut(cur))
        scene.play(*anims, run_time=0.28)
        cur = new
    assert P == T0
    scene.say("……長出來的正是 ", "$T$", " 本身：所以行字與列字 Knuth 等價")
    scene.play(FadeOut(marker), FadeIn(eq_t, scale=1.3), Indicate(tm, color=OK_COLOR), run_time=0.8)
    scene.play(FadeIn(f10), ShowCreation(box10), run_time=0.8)
    scene.wait(1.8)


# =============================================================================
# 第 2 段：Lemma 1（垂直切 → T′∗T″ → 滑回 T）
# =============================================================================
def part_lemma(scene, S, slides):
    cs, fs = 0.56, 30
    origin = np.array([-6.3, 2.2, 0.0])
    board = make_board(T0, cs, origin, fs)
    for (i, j), t in board["nums"].items():
        t.set_fill(LEFT_COLOR if j < CUT else RIGHT_COLOR)
    grid = VGroup(*board["cells"].values(), *board["nums"].values())
    stmt = mixed("Lemma 1：斜表被一條水平或垂直線切成 ", "$T'$", "、", "$T''$", "，則 ",
                 "$w(T)\\equiv w(T')\\cdot w(T'')$", font_size=26).move_to([-6.3, 2.75, 0], aligned_edge=LEFT)
    x_cut = origin[0] + CUT * cs
    v_line = DashedLine([x_cut, origin[1] + 0.15, 0], [x_cut, origin[1] - len(T0) * cs - 0.15, 0],
                        dash_length=0.08).set_stroke(YELLOW, width=3)
    y_cut = origin[1] - H_CUT * cs
    h_line = DashedLine([origin[0] - 0.15, y_cut, 0], [origin[0] + len(T0[0]) * cs + 0.15, y_cut, 0],
                        dash_length=0.08).set_stroke(YELLOW, width=3)
    lab_l = Tex("T'", font_size=34, fill_color=LEFT_COLOR).move_to([origin[0] + cs, origin[1] - len(T0) * cs - 0.35, 0])
    lab_r = Tex("T''", font_size=34, fill_color=RIGHT_COLOR)
    lab_r.move_to([origin[0] + len(T0[0]) * cs + 0.45, origin[1] - cs, 0])
    # 右邊的文字
    wl, wr = tableau_word(T_LEFT), tableau_word(T_RIGHT)
    w_lab = Tex(r"w(T'\ast T'')=w(T')\cdot w(T'')", font_size=34).move_to([-2.4, 1.75, 0], aligned_edge=LEFT)
    w_digits = VGroup(word_tex(wl, font_size=36), Tex(r"\cdot", font_size=36), word_tex(wr, font_size=36))
    w_digits[0].set_fill(LEFT_COLOR)
    w_digits[2].set_fill(RIGHT_COLOR)
    w_digits.arrange(RIGHT, buff=0.2).next_to(w_lab, DOWN, buff=0.3, aligned_edge=LEFT)
    rule = mixed("內角挑在 ", "$T'$", " 正上方，由右到左（滑動保持 ", "$\\equiv$", "）", font_size=24,
                 color=MUTED_COLOR).move_to([-2.4, 0.15, 0], aligned_edge=LEFT)

    def counter(k):
        return mixed("滑動 ", f"${k}/{len(slides)}$", font_size=26).move_to([-2.4, -0.5, 0], aligned_edge=LEFT)

    result = mixed("滑回 ", "$T$", "：", "$w(T)\\equiv w(T'\\ast T'')=w(T')\\cdot w(T'')$", font_size=28)
    result.move_to([1.9, -1.75, 0])
    box = SurroundingRectangle(result, buff=0.15, color=OK_COLOR, stroke_width=3)
    star_frame = Rectangle(width=len(T0[0]) * cs, height=len(S) * cs).move_to(origin, aligned_edge=UL)
    assert_in_frame(stmt, star_frame, lab_l.copy().shift(DROP * cs * DOWN), lab_r, w_lab, w_digits, rule,
                    counter(0), box)
    assert_apart(stmt, VGroup(star_frame, lab_r, w_lab), gap=0.15)
    assert_apart(VGroup(star_frame, lab_l.copy().shift(DROP * cs * DOWN), lab_r), VGroup(w_lab, w_digits, rule, box),
                 gap=0.3)
    for a, b in [(w_lab, w_digits), (w_digits, rule), (rule, counter(0)), (counter(0), box)]:
        assert_apart(a, b, gap=0.15)

    scene.say("Lemma 1：把斜表切成兩塊，字的等價可以分開算")
    scene.play(FadeIn(stmt), FadeIn(grid), run_time=0.9)
    scene.wait(1.0)
    scene.say("水平切很明顯：字本來就是先讀下面幾列，再讀上面幾列")
    scene.play(ShowCreation(h_line), run_time=0.6)
    scene.wait(1.6)
    scene.say("垂直切：例如切在第 ", f"${CUT}$", " 行之後，左塊 ", "$T'$", "、右塊 ", "$T''$")
    scene.play(FadeOut(h_line), ShowCreation(v_line), FadeIn(lab_l), FadeIn(lab_r), run_time=0.8)
    scene.wait(1.0)

    # T′ 往下移到 T″ 的左下：變成 T′∗T″
    left_keys = [b for b in board["cells"] if b[1] < CUT]
    moving = VGroup(*[board["cells"][b] for b in left_keys], *[board["nums"][b] for b in left_keys], lab_l)
    cells, nums, vals = {}, {}, {}
    for (i, j) in list(board["cells"]):
        key = (i + DROP, j) if j < CUT else (i, j)
        cells[key] = board["cells"][(i, j)]
        nums[key] = board["nums"][(i, j)]
        vals[key] = board["vals"][(i, j)]
    board["cells"], board["nums"], board["vals"] = cells, nums, vals
    board["mu"] = {(i, j) for i in range(DROP) for j in range(CUT)}
    mu_cells = VGroup()
    for b in sorted(board["mu"]):
        board["cells"][b] = new_cell(board, *b, in_mu=True)
        mu_cells.add(board["cells"][b])
    scene.say("把 ", "$T'$", " 搬到 ", "$T''$", " 的左下方：得到 ", "$T'\\ast T''$", "，它的字就是 ",
              "$w(T')\\cdot w(T'')$")
    scene.play(moving.animate.shift(DROP * cs * DOWN), FadeOut(v_line), run_time=1.0)
    scene.play(FadeIn(mu_cells), FadeIn(w_lab), FadeIn(w_digits), run_time=0.8)
    assert board_as_skew(board) == S
    scene.wait(1.4)

    scene.say("從 ", "$T'$", " 正上方的內角滑動，由右到左；滑動不改變 Knuth 等價類")
    cnt = counter(0)
    scene.play(FadeIn(rule), FadeIn(cnt), FadeOut(lab_l), run_time=0.6)
    for k, (corner, path, S_next) in enumerate(slides):
        new_cnt = counter(k + 1)
        scene.play(*anims_open_hole(board, corner), FadeOut(cnt), FadeIn(new_cnt), run_time=0.3)
        cnt = new_cnt
        for src in path[1:]:
            scene.play(*anims_move(board, src), run_time=0.16)
        scene.play(*anims_drop_cell(board), run_time=0.25)
        assert board_as_skew(board) == S_next
    assert board_as_skew(board) == T0
    scene.say("六次滑動後回到 ", "$T$", "：所以 ", "$w(T)\\equiv w(T')\\cdot w(T'')$")
    scene.play(FadeIn(result), ShowCreation(box), run_time=0.9)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：逐行剝下得 (10)；Lemma 2
# =============================================================================
def part_peel(scene):
    cs = 0.62
    tm = tableau_mob(T0, cs, top_left=(-6.3, 2.2, 0))
    tags = VGroup()
    for j in range(len(T0[0])):
        tm.fill_cells([(i, j) for i in range(len(T0)) if j < len(T0[i])], COL_COLORS[j], opacity=0.3)
        tags.add(Tex(f"C_{j + 1}", font_size=30, fill_color=COL_COLORS[j]).next_to(tm.cell(0, j), UP, buff=0.15))
    l1 = Tex(r"w(T)\equiv " + r"\cdot ".join(f"w(C_{j + 1})" for j in range(len(T0[0]))), font_size=38)
    l1.move_to([-2.6, 1.6, 0], aligned_edge=LEFT)
    l2 = digits_line("=", columns(T0), COL_COLORS, font_size=38, baseline=False)
    l2.next_to(l1, DOWN, buff=0.4, aligned_edge=LEFT)
    l2_end = Tex(r"=w_{\mathrm{col}}(T)", font_size=38).next_to(l2, RIGHT, buff=0.3)
    l2_end.shift((l2[0].get_center()[1] - l2_end[0].get_center()[1]) * UP)     # 等號同高
    lem2 = VGroup(
        mixed("更強（Lemma 2）：只用 ", "$K'$", " 一種基本變換，", font_size=26),
        mixed("就能把 ", "$w_{\\mathrm{col}}(T)$", " 變成 ", "$w(T)$", "（", "$K'$", "-等價）", font_size=26),
    ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-2.6, -1.45, 0], aligned_edge=LEFT)
    assert_in_frame(tm, tags, l1, l2, l2_end, lem2)
    assert_apart(VGroup(tm, tags), VGroup(l1, l2, l2_end, lem2), gap=0.3)
    assert_apart(l1, VGroup(l2, l2_end), gap=0.15)
    assert_apart(VGroup(l2, l2_end), lem2, gap=0.3)

    scene.say("一次切下最左邊的一行（垂直切），剩下的再切……")
    scene.play(FadeIn(tm), LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.2), run_time=1.0)
    scene.play(Write(l1), run_time=1.2)
    scene.wait(1.0)
    scene.say("單獨一行的字就是由下往上讀：串起來正是行字，這就證明了 (10)")
    scene.play(FadeIn(l2, shift=0.15 * DOWN), run_time=0.8)
    scene.play(FadeIn(l2_end), run_time=0.6)
    scene.wait(1.6)
    scene.say("其實更強：只用 ", "$K'$", " 那種基本變換就夠了（Lemma 2）")
    scene.play(FadeIn(lem2, shift=0.15 * UP), run_time=0.8)
    scene.wait(2.2)


class SceneF13ColumnWords(ChuScene):
    def construct(self):
        self.show_header("行字與 Lemma 1")
        S, slides = check_math()
        part_column_word(self)
        self.clear_stage()
        part_lemma(self, S, slides)
        self.clear_stage()
        part_peel(self)
        self.wait(1.0)
