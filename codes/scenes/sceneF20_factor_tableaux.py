"""
Scene F20 —— 表的因數分解與 Littlewood–Richardson 數（Fulton《Young Tableaux》§5.1，書 p.60–62）

    鉤子：12 = 3×4 = 2×6；表也有乘法 T·U，反過來能拆幾種？
    V = 123/45/6、λ = μ = (2,1)：恰好 2 種 [T,U] = [14/6, 23/5]、[16/4, 23/5]；把 w(U) = 5 2 3 逐一插入 T 驗算
    V = 112/23/3 也是 2 種；形狀 (3,2,1) 的 16 個標準表，每個都是 2 種 → 個數只看形狀
    另一面：ν/λ = (3,2,1)/(2,1)、內容 (2,1) 的斜表 3 個，一起滑動：恰好 2 個 rectify 成 U0 = 11/2
    命題 2：(U, U0) 經 RSK 給出陣列 (1 1 2 / 2 5 3)；把下列插入 T、新格子填上列 → 斜表；一一對應 → c^ν_{λμ} = 2

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算）。
滑動動畫借用 sceneF07_jeu_de_taquin 的 board 工具（make_board、anims_open_hole、anims_move、anims_drop_cell）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF20_factor_tableaux.py SceneF20FactorTableaux
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
    board_group,
    make_board,
)
from utils.fulton_draw import SkewMob, TwoRowArray, assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    factorizations,
    insert_word_steps,
    inverse_rsk,
    jdt_steps,
    lr_coefficient,
    product,
    rectify,
    rectifying_skews,
    row_insert,
    rsk,
    skew_cells,
    skew_tableaux,
    standard_tableaux,
    tableau_word,
    young_boxes,
)

N_ = None
LAM, MU, NU = (2, 1), (2, 1), (3, 2, 1)
V1 = ((1, 2, 3), (4, 5), (6,))
V2 = ((1, 1, 2), (2, 3), (3,))
FACT1 = ((((1, 4), (6,)), ((2, 3), (5,))), (((1, 6), (4,)), ((2, 3), (5,))))
FACT2 = ((((1, 2), (3,)), ((1, 2), (3,))), (((1, 3), (3,)), ((1, 2), (2,))))
U0 = ((1, 1), (2,))
CANDS = (((N_, N_, 1), (N_, 1), (2,)), ((N_, N_, 1), (N_, 2), (1,)), ((N_, N_, 2), (N_, 1), (1,)))
GOOD = CANDS[:2]
ARRAY = ((1, 1, 2), (2, 5, 3))          # (U, U0) 經 RSK 對應的雙列陣列（上列, 下列）
MATCH = (1, 0)                          # 第 k 種 [T,U] ↔ GOOD[MATCH[k]]
N_STD = 16
C_VALUE = 2

T_COLOR, U_COLOR = BLUE_C, GREEN_C


def content_of(S):
    vals = [v for r in S for v in r if v is not None]
    return tuple(vals.count(k) for k in range(1, max(vals) + 1))


def grow(T, letters, labels):
    """把 letters 依序列插入 T，第 k 個新長出的格子填 labels[k]：回傳 (結果, {新格子: 標籤}, 新格子順序)。"""
    cells, order = {}, []
    for x, u in zip(letters, labels):
        T, _, new = row_insert(T, x)
        cells[new] = u
        order.append(new)
    return T, cells, order


def check_math():
    assert tuple(factorizations(V1, LAM, MU)) == FACT1
    assert tuple(factorizations(V2, LAM, MU)) == FACT2
    for V, fs in ((V1, FACT1), (V2, FACT2)):
        for T, U in fs:
            assert product(T, U) == V and insert_word_steps(tableau_word(U), T)[-1][1] == V
    stds = standard_tableaux(NU)
    assert len(stds) == N_STD and all(len(factorizations(V, LAM, MU)) == C_VALUE for V in stds)
    assert tuple(S for S in skew_tableaux(NU, LAM, 2) if content_of(S) == (2, 1)) == CANDS
    assert tuple(rectifying_skews(NU, LAM, U0)) == GOOD
    assert [rectify(S) == U0 for S in CANDS] == [True, True, False]
    assert len({tuple(st[0] for st in jdt_steps(S)) for S in CANDS}) == 1     # 內角順序相同，可同步滑
    for k, (T, U) in enumerate(FACT1):
        top, bottom = inverse_rsk(U, U0)
        assert (tuple(top), tuple(bottom)) == ARRAY and rsk(top, bottom) == (U, U0)
        V, cells, _ = grow(T, bottom, top)
        assert V == V1 and skew_cells(GOOD[MATCH[k]]) == cells
    assert lr_coefficient(LAM, MU, NU) == C_VALUE == len(FACT1) == len(FACT2) == len(GOOD)


def colored_tab(T, cs, color, opacity=0.28):
    m = tableau_mob(T, cs)
    m.fill_cells(young_boxes(tuple(len(r) for r in T)), color, opacity=opacity)
    return m


def pair_mob(T, U, cs):
    return VGroup(colored_tab(T, cs, T_COLOR), Tex(r"\cdot", font_size=40), colored_tab(U, cs, U_COLOR)
                  ).arrange(RIGHT, buff=0.14)


def check_mark(color=OK_COLOR, fs=40):
    return Tex(r"\checkmark", font_size=fs, fill_color=color)


# =============================================================================
# 第 1 段：鉤子——整數的因數分解 vs. 表的因數分解
# =============================================================================
def part_hook(scene):
    c = np.array([-3.7, 1.0, 0])
    dots = VGroup(*[Dot(radius=0.1, fill_color=TEAL) for _ in range(12)]).arrange(RIGHT, buff=0.22).move_to(c)
    grids = [dots.copy().arrange_in_grid(n_rows=r, n_cols=k, buff=0.34).move_to(c) for r, k in ((3, 4), (2, 6))]
    eq = VGroup(Tex("12", font_size=44), Tex(r"=3\times 4", font_size=44), Tex(r"=2\times 6", font_size=44))
    eq.arrange(RIGHT, buff=0.12).move_to([-3.7, -0.9, 0])
    cs = 0.55
    vm = tableau_mob(V1, cs)
    tq = YoungDiagramMob(LAM, cell_size=cs, entries=(("?", "?"), ("?",)), fill_color=T_COLOR, fill_opacity=0.28)
    uq = YoungDiagramMob(MU, cell_size=cs, entries=(("?", "?"), ("?",)), fill_color=U_COLOR, fill_opacity=0.28)
    row = VGroup(Tex("V=", font_size=44), vm, Tex("=", font_size=44), tq, Tex(r"\cdot", font_size=44), uq)
    row.arrange(RIGHT, buff=0.2).move_to([3.0, 1.0, 0])
    lt = Tex(r"T:\ \lambda", font_size=30, fill_color=T_COLOR).next_to(tq, DOWN, buff=0.25)
    lu = Tex(r"U:\ \mu", font_size=30, fill_color=U_COLOR).next_to(uq, DOWN, buff=0.25)
    lu.match_y(lt)
    q = mixed("有幾種拆法？", font_size=34, color=YELLOW).move_to([3.0, -0.9, 0])
    assert_in_frame(dots, *grids, eq, row, lt, lu, q)
    for g in [dots] + grids:
        assert_apart(g, row, gap=0.4)
        assert_apart(g, eq, gap=0.2)
    assert_apart(VGroup(row, lt, lu), q, gap=0.2)

    scene.say("先熱身：12 可以拆成好幾種乘積")
    scene.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.06), FadeIn(eq[0]), run_time=1.0)
    scene.play(Transform(dots, grids[0]), FadeIn(eq[1], shift=0.1 * RIGHT), run_time=0.9)
    scene.wait(0.4)
    scene.play(Transform(dots, grids[1]), FadeIn(eq[2], shift=0.1 * RIGHT), run_time=0.9)
    scene.wait(0.6)
    scene.say("表也有乘法 ", "$T\\cdot U$", "：那表也能「因數分解」嗎？")
    scene.play(FadeIn(row, shift=0.15 * LEFT), run_time=0.9)
    scene.play(FadeIn(lt), FadeIn(lu), run_time=0.5)
    scene.wait(1.0)
    scene.say("給定 ", "$V$", "，要 ", "$T$", " 的形狀是 ", "$\\lambda$", "、", "$U$", " 的形狀是 ", "$\\mu$",
              "：有幾種寫法？")
    scene.play(FadeIn(q, scale=1.2), run_time=0.6)
    scene.wait(2.0)


# =============================================================================
# 第 2 段：V = 123/45/6 的兩種拆法，逐一插入驗算
# =============================================================================
def insertion_row(T, U, cs, y_top, x0=-6.4, x_chain=-3.75):
    """[T · U] 與插入鏈 T ← 5 ← 2 ← 3；U 的數字所在格塗綠。回傳 (pair, steps)，steps = [(字母, 箭頭組, 表)]。"""
    pair = pair_mob(T, U, cs)
    pair.move_to([x0, y_top, 0], aligned_edge=UL)
    uvals = {v for r in U for v in r}
    steps, x = [], x_chain
    for letter, T2, _, _ in insert_word_steps(tableau_word(U), T):
        arr = Arrow(ORIGIN, 0.62 * RIGHT, buff=0, stroke_width=4, fill_color=GREY_B)
        arr.move_to([x + 0.31, y_top - cs, 0])
        lab = Tex(str(letter), font_size=30, fill_color=U_COLOR).next_to(arr, UP, buff=0.06)
        x += 0.62 + 0.14
        tm = tableau_mob(T2, cs, top_left=(x, y_top, 0))
        tm.fill_cells([(i, j) for i, r in enumerate(T2) for j, v in enumerate(r) if v in uvals], U_COLOR, 0.35)
        x = tm.get_right()[0] + 0.14
        steps.append((letter, VGroup(arr, lab), tm))
    return pair, steps


def part_two_ways(scene):
    cs = 0.46
    head = mixed("$\\lambda=\\mu=(2,1)$", "：", "$T$", " 填藍格、", "$U$", " 填綠格", font_size=26)
    head.move_to([-6.4, 2.6, 0], aligned_edge=LEFT)
    rows = [insertion_row(T, U, cs, y) for (T, U), y in zip(FACT1, (1.75, -0.3))]
    vbox = tableau_mob(V1, 0.55, center=[5.3, 0.15, 0])
    vlab = Tex("V", font_size=40, fill_color=YELLOW).next_to(vbox, UP, buff=0.2)
    vfr = SurroundingRectangle(vbox, buff=0.12, color=YELLOW, stroke_width=3)
    checks = [check_mark().next_to(steps[-1][2], RIGHT, buff=0.25) for _, steps in rows]
    names = [Tex(n, font_size=30, fill_color=MUTED_COLOR).next_to(rows[0][0][k], UP, buff=0.12)
             for k, n in ((0, "T"), (2, "U"))]
    total = mixed("試遍所有的 ", "$T$", "、", "$U$", f"：恰好 {len(FACT1)} 種", font_size=28, color=YELLOW)
    total.move_to([0.0, -2.55, 0])
    all_rows = [VGroup(pair, *[VGroup(a, t) for _, a, t in steps], ck) for (pair, steps), ck in zip(rows, checks)]
    assert_in_frame(head, *all_rows, vbox, vlab, vfr, total, *names)
    assert_apart(all_rows[0], all_rows[1], gap=0.25)
    assert_apart(VGroup(head), VGroup(all_rows[0], *names), gap=0.1)
    for r in all_rows:
        assert_apart(r, VGroup(vfr, vlab), gap=0.2)
    assert_apart(all_rows[1], total, gap=0.15)
    for (_, steps), V in zip(rows, (V1, V1)):
        assert steps[-1][2].entry(0, 0).tab_value == V[0][0]

    scene.say("目標：", "$V$", "，", "$\\lambda=\\mu=(2,1)$")
    scene.play(FadeIn(vbox), ShowCreation(vfr), FadeIn(vlab), FadeIn(head), run_time=0.8)
    scene.wait(0.5)
    for k, ((pair, steps), ck) in enumerate(zip(rows, checks)):
        T, U = FACT1[k]
        um = pair[2]
        if k == 0:
            scene.say("第一種：", "$T\\cdot U$", " 就是把 U 的字（由下往上讀）5、2、3 依序插入 T")
            scene.play(FadeIn(pair, shift=0.1 * RIGHT), FadeIn(VGroup(*names)), run_time=0.7)
            scene.wait(0.6)
        else:
            scene.say("第二種：換一個 ", "$T$", "，", "$U$", " 不變")
            scene.play(FadeIn(pair, shift=0.1 * RIGHT), run_time=0.6)
        prev = pair[0]
        for letter, arr, tm in steps:
            cell = next((i, j) for i, r in enumerate(U) for j, v in enumerate(r) if v == letter)
            scene.play(Indicate(um.entry(*cell), color=YELLOW, scale_factor=1.4), GrowArrow(arr[0]), FadeIn(arr[1]),
                       TransformFromCopy(prev, tm), run_time=0.75 if k == 0 else 0.55)
            prev = tm
        scene.say("插完正好是 ", "$V$", "，驗算成功")
        scene.play(FadeIn(ck, scale=1.5), Indicate(vfr, color=YELLOW), run_time=0.6)
        scene.wait(1.0)
    scene.say("其他的 ", "$T$", "、", "$U$", " 全部試過：", "$V$", f" 恰好有 {len(FACT1)} 種拆法")
    scene.play(FadeIn(total, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：換一個 V 也是 2 種；16 個標準表全部都是 2 種
# =============================================================================
def part_shape_only(scene):
    vm = tableau_mob(V2, 0.46)
    top = VGroup(Tex("V=", font_size=40), vm).arrange(RIGHT, buff=0.15).move_to([-4.6, 1.75, 0])
    pairs = VGroup()
    for T, U in FACT2:
        pairs.add(VGroup(pair_mob(T, U, 0.42), check_mark(fs=34)).arrange(RIGHT, buff=0.3))
    pairs.arrange(DOWN, buff=0.45).next_to(top, DOWN, buff=0.5)
    stds = standard_tableaux(NU)
    grid = VGroup()
    for V in stds:
        assert len(factorizations(V, LAM, MU)) == C_VALUE
        grid.add(VGroup(tableau_mob(V, 0.22, fs=15), Tex(str(C_VALUE), font_size=28, fill_color=YELLOW)
                        ).arrange(RIGHT, buff=0.14))
    grid.arrange_in_grid(n_rows=4, n_cols=4, h_buff=0.5, v_buff=0.3).move_to([2.9, -0.25, 0])
    gtitle = mixed("$\\nu=(3,2,1)$", f" 的 {len(stds)} 個標準表：拆法數", font_size=24).next_to(grid, UP, buff=0.3)
    moral = mixed("拆法數只看形狀 ", "$\\lambda,\\mu,\\nu$", "，不看數字", font_size=28, color=YELLOW)
    moral.move_to([0.0, -2.6, 0])
    mfr = SurroundingRectangle(moral, buff=0.12, color=YELLOW, stroke_width=2.5)
    assert_in_frame(top, pairs, grid, gtitle, mfr)
    assert_apart(VGroup(top, pairs), VGroup(grid, gtitle), gap=0.5)
    assert_apart(top, pairs, gap=0.2)
    assert_apart(VGroup(top, pairs, grid), mfr, gap=0.1)

    scene.say("換一個有重複數字的 ", "$V$", "，形狀還是 ", "$(3,2,1)$")
    scene.play(FadeIn(top), run_time=0.6)
    scene.wait(0.5)
    scene.say("結果也恰好 ", f"${len(FACT2)}$", " 種拆法")
    scene.play(LaggedStart(*[FadeIn(p, shift=0.1 * DOWN) for p in pairs], lag_ratio=0.4), run_time=1.0)
    scene.wait(1.2)
    scene.say("形狀 ", "$(3,2,1)$", f" 的 {len(stds)} 個標準表逐一檢查：每一個都是 ", f"${C_VALUE}$")
    scene.play(FadeIn(gtitle), LaggedStart(*[FadeIn(g, scale=0.8) for g in grid], lag_ratio=0.08), run_time=1.8)
    scene.wait(1.4)
    scene.say("巧合嗎？不是：這個個數只由三個形狀決定")
    scene.play(FadeIn(moral), ShowCreation(mfr), run_time=0.7)
    scene.wait(2.0)


# =============================================================================
# 第 4 段：另一面——ν/λ 上的斜表一起滑動
# =============================================================================
def slide_together(scene, boards, skews, rt=0.45):
    """所有斜表用同一串內角同步做 jeu de taquin。"""
    all_steps = [jdt_steps(S) for S in skews]
    for k in range(len(all_steps[0])):
        corner = all_steps[0][k][0]
        paths = [st[k][1] for st in all_steps]
        scene.play(*[a for b in boards for a in anims_open_hole(b, corner)], run_time=rt)
        for t in range(1, max(len(p) for p in paths)):
            scene.play(*[a for b, p in zip(boards, paths) if t < len(p) for a in anims_move(b, p[t])], run_time=rt)
        scene.play(*[a for b in boards for a in anims_drop_cell(b)], run_time=rt * 0.8)


def part_skews(scene):
    cs = 0.62
    xs = (-6.3, -3.55, -0.8)
    boards = [make_board(S, cs, (x, 1.75, 0), 34) for S, x in zip(CANDS, xs)]
    groups = [board_group(b) for b in boards]
    title = mixed("$\\nu/\\lambda=(3,2,1)/(2,1)$", "，內容 ", "$(2,1)$", f"：共 {len(CANDS)} 個斜表",
                  font_size=26).move_to([-6.3, 2.55, 0], aligned_edge=LEFT)
    u0 = tableau_mob(U0, cs, center=[4.6, 0.85, 0])
    u0.fill_cells(young_boxes((2, 1)), U_COLOR, opacity=0.3)
    u0lab = Tex("U_0", font_size=40, fill_color=U_COLOR).next_to(u0, UP, buff=0.25)
    marks = []
    for S, g in zip(CANDS, groups):
        ok = rectify(S) == U0
        m = check_mark(fs=48) if ok else Tex(r"\times", font_size=52, fill_color=RED)
        marks.append(m.move_to([g.get_center()[0], -0.75, 0]))
    count = mixed("滑成 ", "$U_0$", f" 的恰好 {len(GOOD)} 個", font_size=28, color=YELLOW).move_to([4.6, -0.75, 0])
    assert_in_frame(title, *groups, u0, u0lab, *marks, count)
    for a, b in zip(groups, groups[1:]):
        assert_apart(a, b, gap=0.5)
    assert_apart(groups[-1], VGroup(u0, u0lab), gap=0.5)
    assert_apart(title, VGroup(*groups), gap=0.15)
    assert_apart(VGroup(*groups), VGroup(*marks), gap=0.2)
    assert_apart(VGroup(u0, u0lab), count, gap=0.3)

    scene.say("換個角度：在斜形 ", "$\\nu/\\lambda$", " 上填數，內容是 ", "$(2,1)$", f"：有 {len(CANDS)} 個斜表")
    scene.play(FadeIn(title), LaggedStart(*[FadeIn(g, shift=0.1 * DOWN) for g in groups], lag_ratio=0.25),
               run_time=1.1)
    scene.play(FadeIn(u0), FadeIn(u0lab), run_time=0.5)
    scene.wait(0.8)
    scene.say("三個一起滑動（jeu de taquin），看誰會變成 ", "$U_0$")
    slide_together(scene, boards, CANDS)
    for b, S in zip(boards, CANDS):
        assert board_as_skew(b) == rectify(S)
    scene.play(*[FadeIn(m, scale=1.4) for m in marks], run_time=0.6)
    scene.wait(0.6)
    scene.say("前兩個變成 ", "$U_0$", "，第三個變成一列：", "$U_0$", f" 的「來源」恰好 {len(GOOD)} 個")
    scene.play(FadeIn(count), board_group(boards[2]).animate.set_opacity(0.3), run_time=0.7)
    scene.wait(2.2)


# =============================================================================
# 第 5 段：命題 2——兩邊一一對應，定義 c^ν_{λμ}
# =============================================================================
def part_bijection(scene):
    cs = 0.44
    arr = TwoRowArray(*ARRAY, font_size=34, center=[-1.2, 2.3, 0])
    alab = mixed("$(U,U_0)$", " 的 RSK 陣列", font_size=22, color=MUTED_COLOR).next_to(arr, LEFT, buff=0.3)
    u0 = VGroup(Tex("U_0=", font_size=32), tableau_mob(U0, 0.36)).arrange(RIGHT, buff=0.12)
    u0.next_to(arr, RIGHT, buff=0.6)
    rows = []
    for k, ((T, U), y) in enumerate(zip(FACT1, (0.75, -1.35))):
        pair = pair_mob(T, U, cs).move_to([-5.3, y, 0])
        S = GOOD[MATCH[k]]
        sk = SkewMob(S, cs, center=[-0.9, y, 0])
        _, cells, order = grow(T, ARRAY[1], ARRAY[0])
        assert {b: sk.entry(*b).tab_value for b in order} == cells
        a = Arrow([-3.85, y, 0], [-2.05, y, 0], buff=0, stroke_width=4, fill_color=GREY_B)
        al = Tex(r"T\leftarrow 2,5,3", font_size=24, fill_color=MUTED_COLOR).next_to(a, UP, buff=0.08)
        rows.append((pair, sk, order, VGroup(a, al)))
    d1 = Tex(r"c^{\nu}_{\lambda\mu}", font_size=60, fill_color=YELLOW)
    d2 = mixed("＝", "$V=T\\cdot U$", " 的拆法數", font_size=22)
    d3 = mixed("＝滑成 ", "$U_0$", " 的斜表數", font_size=22)
    d4 = Tex(r"c^{(3,2,1)}_{(2,1),(2,1)}=" + str(C_VALUE), font_size=36)
    d5 = mixed("Littlewood–Richardson 數", font_size=22, color=MUTED_COLOR)
    defs = VGroup(d1, d2, d3, d4, d5).arrange(DOWN, buff=0.25).move_to([4.6, -0.35, 0])
    dfr = SurroundingRectangle(defs, buff=0.2, color=YELLOW, stroke_width=3)
    left = VGroup(*[VGroup(p, s, a) for p, s, _, a in rows])
    assert_in_frame(arr, alab, u0, left, dfr)
    assert_apart(VGroup(arr, alab, u0), left, gap=0.2)
    assert_apart(left, dfr, gap=0.3)
    assert_apart(VGroup(arr, alab, u0), dfr, gap=0.1)
    assert_apart(VGroup(*left[0]), VGroup(*left[1]), gap=0.3)
    for p, s, _, a in rows:
        assert_apart(p, a, gap=0.1)
        assert_apart(a, s, gap=0.1)

    scene.say("命題 2：兩邊一樣多，因為可以一對一配對")
    scene.play(*[FadeIn(r[0]) for r in rows], FadeIn(u0), run_time=0.7)
    scene.say("先由 ", "$U$", " 與 ", "$U_0$", " 用 RSK 反推出一個雙列陣列")
    scene.play(FadeIn(arr), FadeIn(alab), run_time=0.7)
    scene.wait(0.8)
    for k, (pair, sk, order, a) in enumerate(rows):
        if k == 0:
            scene.say("把下列 2、5、3 插入 ", "$T$", "；每長出一格，就在那格寫上列的數")
        else:
            scene.say("第二種 ", "$[T,U]$", " 照做，得到另一個斜表")
        scene.play(GrowArrow(a[0]), FadeIn(a[1]), FadeIn(sk.cells), run_time=0.6)
        for t, box in enumerate(order):
            col = arr.col(t)
            scene.play(Indicate(col[1], color=T_COLOR), TransformFromCopy(col[0], sk.entry(*box)),
                       run_time=0.6 if k == 0 else 0.45)
        scene.wait(0.6)
    scene.say("正是剛才那 2 個斜表；反過來也能還原：一一對應")
    scene.play(*[Indicate(r[1], color=U_COLOR) for r in rows], run_time=0.8)
    scene.wait(1.0)
    scene.say("這個共同的個數記作 ", "$c^{\\nu}_{\\lambda\\mu}$", "：Littlewood–Richardson 數")
    scene.play(FadeIn(defs, shift=0.15 * LEFT), ShowCreation(dfr), run_time=1.0)
    scene.wait(2.6)


class SceneF20FactorTableaux(ChuScene):
    def construct(self):
        self.show_header("表的因數分解與 LR 數")
        check_math()
        part_hook(self)
        self.clear_stage()
        part_two_ways(self)
        self.clear_stage()
        part_shape_only(self)
        self.clear_stage()
        part_skews(self)
        self.clear_stage()
        part_bijection(self)
        self.wait(1.0)
