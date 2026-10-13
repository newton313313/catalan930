"""
Scene M04 —— 循環移位（古典循環引理）證明 C_n = binom(2n+1, n) / (2n+1)（MIT 18.212 第 2 講）

    n+1 個 +1、n 個 -1 排成一圈（總和 +1，長度 2n+1）：
    2n+1 種讀法中恰有 1 種「出發後前綴和都 > 0」。
    n = 3：binom(7,3) = 35 種排法，每 7 種一組、每組恰 1 種好 -> 35 / 7 = 5 = C_3。
    好的序列 = 一個 +1 接一條 Dyck 路徑。

路徑用 utils/lattice_paths.py 的 PathMob／path_thumbnail，v = (2,)：字母 0 = +1、字母 1 = -1。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM04_cyclic_shift.py SceneM04CyclicShift
"""
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR
from utils.counting import (
    LEAF, MIT_EXAMPLE_TREE, catalan, cycle_classes, cycle_good_to_dyck, cycle_words, dyck_words,
    good_rotations, is_good_path, path_heights, rotate, step_weight, tree_to_dyck,
)
from utils.lattice_paths import level_line, path_thumbnail, word_tiles
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, OK_COLOR, YELLOW, mixed, zh

V = (2,)                                  # 字母 0 = +1、字母 1 = -1
N = 3
M = 2 * N + 1                             # 7 步
GOOD = (LEAF, LEAF, LEAF, 1, LEAF, 1, 1)  # +1 接 UUDUDD（貫穿例子的 Dyck 路徑）
SHIFT = 3
BAD = rotate(GOOD, SHIFT)                 # (1,0,1,1,0,0,0)：不好的序列


def check(color=OK_COLOR, scale=0.5):
    return Checkmark().set_fill(color).scale(scale)


def cross(color=CROSSING_COLOR, scale=0.5):
    return Exmark().set_fill(color).scale(scale)


def verify_math():
    """畫面上所有數字都在這裡檢查。"""
    words = cycle_words(N)
    classes = cycle_classes(N)
    assert len(words) == comb(M, N) == 35
    assert len(classes) == catalan(N) == 5
    assert comb(M, N) % M == 0 and comb(M, N) // M == 5
    seen = set()
    for g, rots in classes:
        assert len(rots) == M and len(set(rots)) == M
        assert [is_good_path(r, V) for r in rots] == [True] + [False] * (M - 1)
        assert g[0] == LEAF
        seen |= set(rots)
    assert seen == set(words)
    assert len(words) - len(classes) == 30          # 不好的有 30 種
    assert sorted(cycle_good_to_dyck(g) for g, _ in classes) == sorted(dyck_words(N))
    for n in range(1, 10):
        assert comb(2 * n + 1, n) % (2 * n + 1) == 0
        assert comb(2 * n + 1, n) // (2 * n + 1) == comb(2 * n, n) // (n + 1) == catalan(n)
    # 例子
    assert cycle_good_to_dyck(GOOD) == tree_to_dyck(MIT_EXAMPLE_TREE) == "UUDUDD"
    assert BAD == (1, LEAF, 1, 1, LEAF, LEAF, LEAF)
    assert BAD.count(LEAF) == N + 1 and BAD.count(1) == N
    assert sum(step_weight(x, V) for x in BAD) == 1
    assert good_rotations(BAD, V) == [M - SHIFT] == [4]
    assert rotate(BAD, 4) == GOOD
    hs = path_heights(BAD, V)
    low = min(hs)
    assert low == -2 and max(j for j, h in enumerate(hs) if h == low) == 4
    return classes


def rotation_row(word, unit, xs, base_y):
    """第 j 種讀法的小圖，置中在 xs[j]。"""
    thumbs = VGroup()
    for j, x in enumerate(xs):
        origin = np.array([x - len(word) * unit / 2, base_y, 0.0])
        thumbs.add(path_thumbnail(rotate(word, j), V, unit=unit, origin=origin))
    return thumbs


def class_grid(classes, unit, x0, dx, y0, dy):
    """5 列 × 7 行：第 r 列是第 r 組的 7 種讀法（第 0 行是好的）。"""
    rows = VGroup()
    for r, (_, rots) in enumerate(classes):
        row = VGroup()
        for c, w in enumerate(rots):
            origin = np.array([x0 + c * dx, y0 - r * dy, 0.0])
            row.add(path_thumbnail(w, V, unit=unit, origin=origin, stroke_width=2.6, dot_radius=0.025))
        rows.add(row)
    return rows


def good_marks(thumb, color=YELLOW):
    """好路徑：第一步塗黃，高度 1 畫虛線（之後是一條不低於這條線的 Dyck 路徑）。"""
    path = thumb.path
    first = path.steps[0].copy().set_stroke(color, width=4)
    line = level_line(path, 1, 1, len(path.word), color=color, stroke_width=1.6)
    return VGroup(line, first)


class SceneM04CyclicShift(ChuScene):
    def construct(self):
        self.show_header("循環移位：另一個證明")
        classes = verify_math()

        # ------------------------------------------------------------ 7 種讀法
        info = mixed("$n=3$", "：4 個 ", "$+1$", "、3 個 ", "$-1$", "，總和 ", "$+1$", "，共 7 步",
                     font_size=28)
        info.move_to(2.75 * UP)
        tiles = word_tiles(BAD, V, size=0.55, font_size=26)
        tiles.move_to(1.9 * UP)
        slots = [t.get_center() for t in tiles]
        self.say("把 4 個 ", "$+1$", " 和 3 個 ", "$-1$", " 排成一圈，從不同位置開始讀")
        self.play(FadeIn(info), FadeIn(tiles), run_time=0.8)
        start_arrow = Arrow(slots[0] + 0.75 * LEFT, slots[0] + 0.38 * LEFT, buff=0, thickness=3,
                            fill_color=YELLOW)
        start_tag = zh("從這裡讀", font_size=22, color=YELLOW).next_to(start_arrow, LEFT, buff=0.1)
        self.play(GrowArrow(start_arrow), FadeIn(start_tag), run_time=0.5)

        u = 0.21
        xs = np.linspace(-5.7, 5.7, M)
        base_y = -0.1
        thumbs = rotation_row(BAD, u, xs, base_y)
        marks = VGroup()
        for j in range(M):
            mark = check() if thumbs[j].good else cross()
            mark.move_to(np.array([xs[j], -1.2, 0.0]))
            marks.add(mark)
        assert [t.good for t in thumbs] == [j == 4 for j in range(M)]

        order = list(tiles)
        for j in range(M):
            self.play(FadeIn(thumbs[j], shift=0.3 * DOWN), FadeIn(marks[j], scale=1.4), run_time=0.5)
            first = order.pop(0)
            order.append(first)
            # 從方塊列下方繞到最後（往上繞會碰到上面那行說明）
            arc = ArcBetweenPoints(first.get_center(), slots[-1], angle=PI / 2)
            assert arc.get_bottom()[1] - first.get_height() / 2 > thumbs.get_top()[1] + 0.15
            self.play(MoveAlongPath(first, arc),
                      *[m.animate.move_to(slots[k]) for k, m in enumerate(order[:-1])],
                      run_time=0.4)
        assert order == list(tiles)      # 轉一圈回到原來的順序

        self.say("7 種讀法裡恰好 1 種是好的：出發之後，前綴和一直 ", "$>0$")
        good_box = SurroundingRectangle(VGroup(thumbs[4], marks[4]), buff=0.12, color=YELLOW,
                                        stroke_width=3)
        self.play(ShowCreation(good_box), Indicate(marks[4], scale_factor=1.5, color=OK_COLOR),
                  run_time=1.0)
        self.wait(0.8)

        lemma = VGroup(
            zh("循環引理", font_size=28, color=YELLOW),
            mixed("$n+1$", " 個 ", "$+1$", "、", "$n$", " 個 ", "$-1$", " 排成一圈：", "$2n+1$",
                  " 種讀法中恰有 1 種是好的", font_size=26),
        ).arrange(DOWN, buff=0.16)
        lemma.move_to(2.25 * DOWN)
        lemma_box = SurroundingRectangle(lemma, buff=0.18, color=YELLOW, stroke_width=3)
        self.play(FadeIn(lemma), ShowCreation(lemma_box), run_time=0.9)
        self.wait(1.8)

        # ------------------------------------------------------------ 為什麼恰好一種
        path0 = thumbs[0].path
        low_dot = Dot(path0.vertex(4), radius=0.08, fill_color=YELLOW).set_z_index(4)
        low_line = level_line(path0, -2, 0, M, color=YELLOW, stroke_width=1.6)
        tile_box = SurroundingRectangle(tiles[4], buff=0.06, color=YELLOW, stroke_width=3)
        self.say("好的讀法，從「最後一個最低點」出發：也就是第 5 步")
        self.play(ShowCreation(low_line), FadeIn(low_dot, scale=2), ShowCreation(tile_box), run_time=0.9)
        self.play(Indicate(thumbs[4], scale_factor=1.15, color=YELLOW), run_time=0.9)
        self.wait(0.6)
        self.say("從那裡出發，之後每一點都比它高；換別的起點，總會走回不高於起點的地方",
                 color=WHITE)
        self.wait(3.6)

        # ------------------------------------------------------------ 35 = 5 × 7
        self.clear_stage()
        gu = 0.11
        grid = class_grid(classes, gu, x0=-6.5, dx=1.05, y0=1.8, dy=1.0)
        self.say("全部 35 種排法，依「同一圈」分組：每列一組，每組 7 種讀法")
        self.play(LaggedStart(*[FadeIn(row, shift=0.15 * RIGHT) for row in grid], lag_ratio=0.25),
                  run_time=2.0)
        self.wait(0.6)
        ex_row = [r for r, (g, _) in enumerate(classes) if g == GOOD]
        assert ex_row == [1]
        ex_rect = SurroundingRectangle(grid[1], buff=0.08, color=MUTED_COLOR, stroke_width=2)
        ex_tag = zh("剛才那一圈", font_size=20, color=MUTED_COLOR)
        ex_tag.next_to(ex_rect, RIGHT, buff=0.12)
        self.play(ShowCreation(ex_rect), FadeIn(ex_tag), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(ex_rect), FadeOut(ex_tag), run_time=0.4)

        good_col = VGroup(*[row[0] for row in grid])
        col_rect = SurroundingRectangle(good_col, buff=0.1, color=YELLOW, stroke_width=3)
        col_tag = zh("好的", font_size=22, color=YELLOW).next_to(col_rect, UP, buff=0.1)
        assert col_rect.get_left()[0] > -6.8 and col_tag.get_top()[1] < 3.0
        assert col_rect.get_bottom()[1] > -3.0
        self.say("每組恰有 1 種好的（第一行），其他 30 種都會走到高度 ", "$\\le 0$", "（紅點）")
        self.play(ShowCreation(col_rect), FadeIn(col_tag), run_time=0.8)
        self.wait(0.8)

        panel = VGroup(
            mixed("排法共 ", "$\\binom{7}{3}=35$", " 種", font_size=28),
            mixed("每組 7 種讀法、恰 1 種好", font_size=26),
            Tex("\\frac{35}{7}=5=C_3", font_size=42, t2c={"C_3": CATALAN_COLOR}),
            mixed("好的 ＝ 一個 ", "$+1$", " 接一條 Dyck 路徑", font_size=26),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        panel.move_to(np.array([3.9, 0.85, 0.0]))
        assert grid.get_right()[0] < panel.get_left()[0] - 0.3
        for item in panel[:3]:
            self.play(FadeIn(item, shift=0.2 * UP), run_time=0.6)
            self.wait(0.5)

        dyck_marks = VGroup(*[good_marks(t) for t in good_col])
        self.say("好的序列：第一步是 ", "$+1$", "，之後不低於高度 1、最後回到 1，正是 Dyck 路徑")
        self.play(FadeIn(panel[3], shift=0.2 * UP), ShowCreation(dyck_marks), run_time=0.9)
        self.wait(1.2)

        formula = Tex("C_n=\\frac{1}{2n+1}\\binom{2n+1}{n}=\\frac{1}{n+1}\\binom{2n}{n}", font_size=36,
                      t2c={"C_n": CATALAN_COLOR})
        if formula.get_width() > 5.4:
            formula.set_width(5.4)
        formula.next_to(panel, DOWN, buff=0.45)
        formula.set_x(3.75)
        assert formula.get_left()[0] > 0.6 and formula.get_right()[0] < 6.6
        f_box = SurroundingRectangle(formula, buff=0.18, color=YELLOW, stroke_width=3)
        assert grid.get_right()[0] < f_box.get_left()[0] - 0.2 and f_box.get_right()[0] < 6.8
        assert f_box.get_bottom()[1] > -3.0
        self.say("一般的 ", "$n$", "：", "$\\tbinom{2n+1}{n}$", " 種排法，每 ", "$2n+1$", " 種一組、每組恰 1 種好")
        self.play(Write(formula), ShowCreation(f_box), run_time=1.2)
        self.wait(2.6)

        # ------------------------------------------------------------ 預告
        self.say("第 8 場景的 Raney 公式，把同樣的想法推廣到多種步長")
        self.wait(3.0)
