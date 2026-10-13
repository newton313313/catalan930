"""
Scene M12 —— 標準 Young 表 ↔ Dyck 路徑（MIT 18.212 第 4 講）

    形狀 (n, n)：依序讀 1..2n，在第一列 -> U、在第二列 -> D
    行遞增 => 第 j 個 D 之前一定已經有第 j 個 U => 不會掉到地面以下 => Dyck 路徑
    所以 f^{(n,n)} = C_n
    一般形狀 λ：i 在第 r 列 -> 走 e_r；條件 = 一路上 x_1 >= x_2 >= ... >= x_k

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM12_syt_dyck.py SceneM12SYTDyck
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, dyck_path_mob
from utils.counting import (catalan, dyck_to_syt, is_dyck, is_lattice_rowword, rowword_counts,
                            rowword_to_syt, syt, syt_count, syt_to_dyck, syt_to_rowword)
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, mixed, zh

EX_T = ((1, 2, 4), (3, 5, 6))            # 第 3 節的例子
EX_WORD = "UUDUDD"
GEN_LAM = (2, 2, 1)                      # 一般 λ 的 3 列小例子
GEN_T = ((1, 3), (2, 5), (4,))
BAD_T = ((1, 5), (2, 4), (3,))           # 5 在 4 上面：不是標準 Young 表

ROW_COLORS = [TEAL_B, PURPLE_B, GOLD_B]  # 第 1／2／3 列（U／D 沿用第 1／2 列的顏色）
ACTIVE_COLOR = YELLOW

X_MIN, X_MAX, Y_MIN, Y_MAX = -6.8, 6.8, -3.0, 3.2


def check_inside(*mobs):
    for m in mobs:
        assert m.get_left()[0] >= X_MIN - 1e-6 and m.get_right()[0] <= X_MAX + 1e-6, m
        assert m.get_bottom()[1] >= Y_MIN - 1e-6 and m.get_top()[1] <= Y_MAX + 1e-6, m


def check_apart(a, b, gap=0.05):
    """兩個物件的外框不重疊。"""
    sep_x = a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
    sep_y = a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1]
    assert sep_x or sep_y, (a, b)


def fit_width(mob, width=FRAME_WIDTH - 1.0):
    if mob.get_width() > width:
        mob.set_width(width)
    return mob


def cell_of(T, x):
    for i, row in enumerate(T):
        if x in row:
            return i, row.index(x)
    raise ValueError(x)


def active_frame(dia, i, j):
    sq = Square(side_length=dia.cell_size, stroke_color=ACTIVE_COLOR, stroke_width=6)
    sq.move_to(dia.cell_center(i, j))
    sq.set_z_index(2)
    return sq


def tint_rows(dia, opacity=0.22):
    return [dia.cell(i, j).animate.set_fill(ROW_COLORS[i], opacity=opacity)
            for i, j in [(i, j) for i, r in enumerate(dia.lam) for j in range(r)]]


def row_tags(dia, texts, font_size=34, buff=0.25):
    """每一列右邊的標籤（對齊在最寬那一列的右邊）。"""
    x0 = dia.cell_center(0, dia.lam[0] - 1)[0] + dia.cell_size / 2 + buff
    tags = VGroup()
    for i, t in enumerate(texts):
        tag = Tex(t, font_size=font_size, fill_color=ROW_COLORS[i])
        tag.move_to(np.array([x0, dia.cell_center(i, 0)[1], 0.0]), aligned_edge=LEFT)
        tags.add(tag)
    return tags


# =============================================================================
# 1. (3,3) 的例子：逐步轉成 UUDUDD
# =============================================================================
def part1_convert(scene):
    word = syt_to_dyck(EX_T)
    assert word == EX_WORD and is_dyck(word) and dyck_to_syt(word) == EX_T
    assert EX_T in syt((3, 3))

    dia = YoungDiagramMob((3, 3), cell_size=0.75, top_left=np.array([-6.3, 2.45, 0.0]), entries=EX_T)
    tags = row_tags(dia, [r"\rightarrow \mathrm{U}", r"\rightarrow \mathrm{D}"])
    scene.say("形狀 ", "$(3,3)$", " 的標準 Young 表：依序讀 1, 2, …, 6")
    scene.play(FadeIn(dia, shift=0.2 * RIGHT), run_time=0.8)
    scene.play(*tint_rows(dia), FadeIn(tags, shift=0.15 * RIGHT), run_time=0.7)

    unit = 0.6
    origin = np.array([1.0, 1.05, 0.0])
    colors = [ROW_COLORS[0] if c == "U" else ROW_COLORS[1] for c in word]
    path = dyck_path_mob(word, unit=unit, origin=origin, colors=colors, stroke_width=7, dot_radius=0.06)
    ground = Line(origin + 0.3 * LEFT, origin + (len(word) * unit + 0.3) * RIGHT,
                  stroke_color=GREY_A, stroke_width=2.5)
    nums, letters = VGroup(), VGroup()
    for k, c in enumerate(word):
        x = origin[0] + (k + 0.5) * unit
        nums.add(Tex(str(k + 1), font_size=30, fill_color=GREY_A).move_to(np.array([x, origin[1] - 0.42, 0.0])))
        letters.add(Tex(r"\mathrm{" + c + "}", font_size=40, fill_color=colors[k])
                    .move_to(np.array([x, origin[1] - 0.92, 0.0])))
    check_inside(dia, tags, path, ground, letters)
    check_apart(tags, ground)

    scene.say("數字 ", "$i$", " 在第 1 列 ", "$\\Rightarrow$", " 第 ", "$i$", " 步往上（U）；在第 2 列 ", "$\\Rightarrow$",
              " 往下（D）")
    scene.play(ShowCreation(ground), FadeIn(path.dots[0]), run_time=0.5)
    frame = None
    for k in range(len(word)):
        i, j = cell_of(EX_T, k + 1)
        assert (i == 0) == (word[k] == "U")
        new_frame = active_frame(dia, i, j)
        anims = [FadeIn(new_frame)] if frame is None else [ReplacementTransform(frame, new_frame)]
        scene.play(*anims, TransformFromCopy(dia.entry(i, j), nums[k]), run_time=0.45)
        scene.play(FadeIn(letters[k], shift=0.1 * DOWN), ShowCreation(path.steps[k]),
                   FadeIn(path.dots[k + 1]), run_time=0.4)
        frame = new_frame
    scene.play(FadeOut(frame), run_time=0.3)
    scene.wait(0.4)

    # ------------------------------------------------ 為什麼不會掉到地面以下
    scene.say("每一行都是上面小、下面大：第 ", "$j$", " 個 D 之前，一定已經有第 ", "$j$", " 個 U")
    ineqs = VGroup()
    for j in range(3):
        a, b = EX_T[0][j], EX_T[1][j]
        assert a < b
        col = SurroundingRectangle(dia.cell_group([(0, j), (1, j)]), buff=0.04, color=ACTIVE_COLOR,
                                   stroke_width=5)
        ineq = mixed(f"第 {j + 1} 行：", f"${a}<{b}$", font_size=24, color=ACTIVE_COLOR)
        ineq.move_to(np.array([dia.get_left()[0], dia.get_bottom()[1] - 0.4 - 0.48 * j, 0.0]),
                     aligned_edge=LEFT)
        ineqs.add(ineq)
        hi = VGroup(*[path.steps[s - 1].copy().set_stroke(ACTIVE_COLOR, width=11) for s in (a, b)])
        hi_nums = VGroup(*[nums[s - 1] for s in (a, b)])
        scene.play(ShowCreation(col), FadeIn(ineq, shift=0.1 * DOWN), FadeIn(hi),
                   hi_nums.animate.set_fill(ACTIVE_COLOR), run_time=0.6)
        scene.wait(0.5)
        scene.play(FadeOut(col), FadeOut(hi), hi_nums.animate.set_fill(GREY_A), run_time=0.35)
    check_inside(ineqs)
    for a, b in zip(ineqs, ineqs[1:]):
        check_apart(a, b)

    rule = VGroup(
        mixed("任何時候 U 的個數 ", "$\\ge$", " D 的個數", font_size=28),
        mixed("$\\Rightarrow$", " 路徑不會掉到地面以下 ", "$\\Rightarrow$", " Dyck 路徑", font_size=28),
    ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    rule.move_to(np.array([0.3, -1.65, 0.0]))
    box = SurroundingRectangle(rule, buff=0.22, color=YELLOW, stroke_width=3)
    check_inside(box)
    check_apart(box, ineqs)
    check_apart(box, letters)
    scene.play(FadeIn(rule), ShowCreation(box), run_time=0.8)
    scene.wait(1.2)
    scene.say("反過來：第 ", "$i$", " 步是 U 就把 ", "$i$", " 填進第 1 列，是 D 就填進第 2 列，表就還原了")
    scene.wait(1.8)
    scene.clear_stage()


# =============================================================================
# 2. 全部 5 對，f^{(n,n)} = C_n
# =============================================================================
def part2_all_pairs(scene):
    tabs = syt((3, 3))
    words = [syt_to_dyck(T) for T in tabs]
    assert len(tabs) == syt_count((3, 3)) == catalan(3) == 5
    assert sorted(words) == sorted(set(words)) and all(is_dyck(w) for w in words)
    ex_idx = tabs.index(EX_T)

    xs = np.linspace(-5.3, 5.3, 5)
    items = VGroup()
    for x, T, w in zip(xs, tabs, words):
        dia = YoungDiagramMob((3, 3), cell_size=0.42, center=np.array([x, 1.85, 0.0]), entries=T)
        for i, r in enumerate(dia.lam):
            dia.fill_cells([(i, j) for j in range(r)], ROW_COLORS[i], opacity=0.22)
        arrow = Arrow(np.array([x, 1.38, 0.0]), np.array([x, 0.98, 0.0]), buff=0, thickness=2.5,
                      fill_color=GREY_B)
        unit = 0.2
        colors = [ROW_COLORS[0] if c == "U" else ROW_COLORS[1] for c in w]
        path = dyck_path_mob(w, unit=unit, origin=np.array([x - 3 * unit, 0.2, 0.0]), colors=colors,
                             stroke_width=4, dot_radius=0.03)
        base = Line(path.vertex(0), path.vertex(6), stroke_color=GREY_C, stroke_width=1.5)
        text = Tex(r"\mathrm{" + w + "}", font_size=30).move_to(np.array([x, -0.2, 0.0]))
        items.add(VGroup(dia, arrow, base, path, text))
    check_inside(items)
    for a, b in zip(items, items[1:]):
        check_apart(a, b)

    scene.say("形狀 ", "$(3,3)$", " 的標準 Young 表共 5 個，正好對應 5 條 Dyck 路徑")
    scene.play(LaggedStart(*[FadeIn(it, shift=0.2 * UP) for it in items], lag_ratio=0.2), run_time=2.0)
    ex_box = SurroundingRectangle(items[ex_idx], buff=0.15, color=YELLOW, stroke_width=3)
    ex_lab = zh("剛才的例子", font_size=22, color=YELLOW).next_to(ex_box, DOWN, buff=0.12)
    scene.play(ShowCreation(ex_box), FadeIn(ex_lab), run_time=0.6)
    scene.wait(0.8)

    ns = list(range(1, 7))
    vals = [syt_count((n, n)) for n in ns]
    assert vals == [catalan(n) for n in ns] == [1, 2, 5, 14, 42, 132]
    claim = mixed("形狀 ", "$(n,n)$", " 的標準 Young 表個數 ", "$f^{(n,n)}=C_n$", font_size=30,
                  t2c={"C_n": CATALAN_COLOR})
    table = mixed("$n=1,\\dots,6$", "：", "$f^{(n,n)}=" + ",\\ ".join(map(str, vals)) + "$", font_size=26)
    block = VGroup(claim, table).arrange(DOWN, buff=0.25)
    block.move_to(np.array([0.0, -1.9, 0.0]))
    box = SurroundingRectangle(block, buff=0.22, color=YELLOW, stroke_width=3)
    check_inside(box)
    check_apart(box, ex_lab)
    scene.say("所以 ", "$f^{(n,n)}=C_n$", "（程式算到 ", "$n=6$", " 都相符）")
    scene.play(FadeIn(block), ShowCreation(box), run_time=0.9)
    scene.wait(2.2)
    scene.clear_stage()


# =============================================================================
# 3. 一般 λ：k 維格子路徑，一路保持 x_1 >= x_2 >= x_3
# =============================================================================
def part3_general(scene):
    word = syt_to_rowword(GEN_T)
    counts = rowword_counts(word, k=3)
    assert GEN_T in syt(GEN_LAM) and is_lattice_rowword(word)
    assert word == (0, 1, 0, 2, 1) and counts[-1] == GEN_LAM
    assert all(x[0] >= x[1] >= x[2] for x in counts)

    dia = YoungDiagramMob(GEN_LAM, cell_size=0.7, top_left=np.array([-6.4, 2.45, 0.0]), entries=GEN_T)
    tags = row_tags(dia, [r"\rightarrow e_1", r"\rightarrow e_2", r"\rightarrow e_3"], font_size=32, buff=0.2)
    scene.say("一般形狀 ", "$\\lambda=(\\lambda_1,\\dots,\\lambda_k)$", "：數字 ", "$i$", " 在第 ", "$r$",
              " 列，第 ", "$i$", " 步就走 ", "$e_r$", "（第 ", "$r$", " 個座標加 1）")
    scene.play(FadeIn(dia, shift=0.2 * RIGHT), run_time=0.7)
    scene.play(*tint_rows(dia), FadeIn(tags, shift=0.15 * RIGHT), run_time=0.7)

    # ------------------------------------------------ 累計次數表
    col_x = [-1.7 + 0.82 * t for t in range(len(counts))]
    row_y = [2.25, 1.7, 1.12, 0.6, 0.08]
    lab_x = -2.95
    labels = VGroup(
        zh("讀完", font_size=22, color=MUTED_COLOR),
        zh("這一步", font_size=22, color=MUTED_COLOR),
        Tex("x_1", font_size=32, fill_color=ROW_COLORS[0]),
        Tex("x_2", font_size=32, fill_color=ROW_COLORS[1]),
        Tex("x_3", font_size=32, fill_color=ROW_COLORS[2]),
    )
    for lab, y in zip(labels, row_y):
        lab.move_to(np.array([lab_x, y, 0.0]))
    rule = Line(np.array([lab_x - 0.55, 1.98, 0.0]), np.array([col_x[-1] + 0.4, 1.98, 0.0]),
                stroke_color=GREY_C, stroke_width=1.5)
    cols = []
    for t, x in enumerate(counts):
        head = Tex(str(t), font_size=30, fill_color=MUTED_COLOR)
        step = (Tex(f"e_{word[t - 1] + 1}", font_size=30, fill_color=ROW_COLORS[word[t - 1]])
                if t > 0 else VectorizedPoint())
        vals = [Tex(str(v), font_size=32) for v in x]
        col = VGroup(head, step, *vals)
        for m, y in zip(col, row_y):
            m.move_to(np.array([col_x[t], y, 0.0]))
        if t > 0:
            vals[word[t - 1]].set_fill(YELLOW)
        cols.append(col)
    table = VGroup(labels, rule, *cols)
    check_inside(dia, tags, table)
    check_apart(tags, table)

    scene.play(FadeIn(labels), ShowCreation(rule), FadeIn(cols[0]), run_time=0.7)
    frame = None
    for t in range(1, len(counts)):
        i, j = cell_of(GEN_T, t)
        assert i == word[t - 1]
        new_frame = active_frame(dia, i, j)
        anims = [FadeIn(new_frame)] if frame is None else [ReplacementTransform(frame, new_frame)]
        prev_vals = cols[t - 1][2:]
        scene.play(*anims, TransformFromCopy(dia.entry(i, j), cols[t][0]), FadeIn(cols[t][1]),
                   TransformFromCopy(prev_vals, cols[t][2:]), run_time=0.65)
        frame = new_frame
    scene.play(FadeOut(frame), run_time=0.3)

    end_box = SurroundingRectangle(VGroup(*cols[-1][2:]), buff=0.1, color=YELLOW, stroke_width=3)
    end_lab = mixed("終點 ", "$=(2,2,1)=\\lambda$", font_size=24)
    end_lab.next_to(end_box, RIGHT, buff=0.2)
    checks = VGroup(*[Tex(r"\checkmark", font_size=30, fill_color=OK_COLOR).move_to(np.array([x, -0.42, 0.0]))
                      for x in col_x])
    check_lab = Tex(r"x_1\ge x_2\ge x_3", font_size=26).move_to(np.array([lab_x, -0.42, 0.0]))
    check_inside(end_lab, checks, check_lab)
    scene.say("每一欄都有 ", "$x_1\\ge x_2\\ge x_3$", "：行遞增保證上面那格早就填好了")
    scene.play(ShowCreation(end_box), FadeIn(end_lab), run_time=0.6)
    scene.play(FadeIn(check_lab), LaggedStart(*[FadeIn(c, scale=1.5) for c in checks], lag_ratio=0.12),
               run_time=1.0)
    scene.wait(1.0)

    # ------------------------------------------------ 反例：5 在 4 上面
    bad_word = syt_to_rowword(BAD_T)
    bad_counts = rowword_counts(bad_word, k=3)
    assert BAD_T not in syt(GEN_LAM) and rowword_to_syt(bad_word) == BAD_T
    assert not is_lattice_rowword(bad_word)
    first_bad = next(t for t, x in enumerate(bad_counts) if not (x[0] >= x[1] >= x[2]))
    assert first_bad == 4 and bad_counts[4] == (1, 2, 1) and BAD_T[0][1] == 5 and BAD_T[1][1] == 4

    bad = YoungDiagramMob(GEN_LAM, cell_size=0.5, top_left=np.array([-6.4, -0.95, 0.0]), entries=BAD_T)
    for x in (4, 5):
        bad.entry(*cell_of(BAD_T, x)).set_fill(CROSSING_COLOR)
    bad_cols = SurroundingRectangle(bad.cell_group([(0, 1), (1, 1)]), buff=0.03, color=CROSSING_COLOR,
                                    stroke_width=4)
    tuples = VGroup(*[Tex("(" + ",".join(map(str, x)) + ")", font_size=30) for x in bad_counts[1:]])
    tuples.arrange(RIGHT, buff=0.32)
    tuples.move_to(np.array([-4.9, -1.25, 0.0]), aligned_edge=LEFT)
    tuples[first_bad - 1].set_fill(CROSSING_COLOR)
    why = mixed("讀到 4：", "$x_2=2>x_1=1$", "，因為 4 上面那格（5）還空著", font_size=24, color=CROSSING_COLOR)
    why.next_to(tuples, DOWN, buff=0.3).align_to(tuples, LEFT)
    not_syt = zh("不是標準 Young 表（5 在 4 上面）", font_size=22, color=CROSSING_COLOR)
    not_syt.next_to(why, DOWN, buff=0.25).align_to(tuples, LEFT)
    lower = VGroup(bad, bad_cols, tuples, why, not_syt)
    check_inside(lower)
    check_apart(lower, VGroup(checks, check_lab))
    check_apart(bad, tuples)
    scene.say("反例：把 5 放在 4 上面，讀到 4 時 ", "$x_2>x_1$", "，路徑跑出區域")
    scene.play(FadeIn(bad), FadeIn(tuples), run_time=0.8)
    scene.play(ShowCreation(bad_cols), FadeIn(why), FadeIn(not_syt),
               Flash(tuples[first_bad - 1].get_center(), color=CROSSING_COLOR, flash_radius=0.5), run_time=0.9)
    scene.wait(1.8)
    scene.play(FadeOut(lower), run_time=0.5)

    # ------------------------------------------------ 結論
    concl = VGroup(
        mixed("形狀 ", "$\\lambda$", " 的標準 Young 表 ", "$\\longleftrightarrow$", " 從原點走到 ", "$\\lambda$",
              "、一路保持 ", "$x_1\\ge x_2\\ge\\cdots\\ge x_k$", " 的格子路徑", font_size=26),
        mixed("$\\lambda=(n,n)$", "：", "$x_1\\ge x_2$", " 就是「U 不比 D 少」，回到 Dyck 路徑與 ", "$C_n$", font_size=26,
              t2c={"C_n": CATALAN_COLOR}),
    ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    fit_width(concl, FRAME_WIDTH - 1.2)
    concl.move_to(np.array([0.0, -1.75, 0.0]))
    cbox = SurroundingRectangle(concl, buff=0.2, color=YELLOW, stroke_width=3)
    check_inside(cbox)
    check_apart(cbox, VGroup(checks, check_lab))
    scene.say("標準 Young 表就是「不跑出區域」的格子路徑")
    scene.play(FadeIn(concl), ShowCreation(cbox), run_time=0.9)
    scene.wait(2.5)


class SceneM12SYTDyck(ChuScene):
    def construct(self):
        self.show_header("標準 Young 表與 Dyck 路徑")
        part1_convert(self)
        part2_all_pairs(self)
        part3_general(self)
        self.wait(1.0)
