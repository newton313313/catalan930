"""
Scene 00g —— Dyck 路徑（來源論文 2.5 節、Fig. 2.4）

把不越過 y = x 的格子路徑轉 45°、再上下翻轉：
    往右 R -> 上坡 ↗，往上 U -> 下坡 ↘
    「不越過對角線」 -> 「不掉到地面以下」
（注意：因為格子路徑要求「不走到對角線上方」，對應方向是 R -> ↗、U -> ↘，不是反過來。）

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00g_dyck_paths.py Scene00gDyckPaths
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    dyck_item,
    dyck_path_mob,
    lattice_diagonal,
    lattice_grid,
    lattice_path_mob,
)
from utils.counting import binary_trees, catalan, dyck_to_lattice, dyck_words, tree_to_dyck
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, YELLOW, mixed, zh

N = 3
LATTICE_WORD = "RURRUU"
DYCK_WORD = "URUURR".replace("R", "D")       # R->U(↗), U->D(↘)：RURRUU -> UDUUDD
UNIT = 0.9
O = np.array([-4.9, -0.55, 0.0])


class Scene00gDyckPaths(ChuScene):
    def construct(self):
        self.show_header("Dyck 路徑")
        assert dyck_to_lattice(DYCK_WORD) == LATTICE_WORD
        assert [len(dyck_words(n)) for n in range(4)] == [1, 1, 2, 5]

        # ------------------------------------------------------------ 從格子路徑出發
        grid = lattice_grid(N, N, UNIT, O, color=GREY_C, stroke_width=2)
        diag = lattice_diagonal(N, UNIT, O, color=GREY_A, stroke_width=3)
        path = lattice_path_mob(LATTICE_WORD, UNIT, O, color=CATALAN_COLOR, stroke_width=6, dot_radius=0.06)
        self.say("從上一段的一條合法格子路徑出發")
        self.play(ShowCreation(grid), ShowCreation(diag), run_time=0.8)
        self.play(ShowCreation(path.steps), FadeIn(path.dots), run_time=1.2)
        self.wait(0.5)

        figure = VGroup(grid, diag, path)
        self.say("把整張圖順時針轉 45°，讓對角線變成水平")
        self.play(Rotate(figure, -PI / 4, about_point=O), run_time=1.6)
        self.wait(0.4)
        self.say("再上下翻過來：路徑就在水平線的上方")
        self.play(Rotate(figure, PI, axis=RIGHT, about_point=O), run_time=1.6)
        self.wait(0.4)

        # 換成乾淨的 Dyck 路徑（每一步與原來的步一模一樣）
        dyck = dyck_path_mob(DYCK_WORD, unit=UNIT / np.sqrt(2), origin=O, color=CATALAN_COLOR,
                             stroke_width=6, dot_radius=0.06)
        ground = Line(O + 0.3 * LEFT, O + (2 * N * UNIT / np.sqrt(2) + 0.3) * RIGHT,
                      stroke_color=GREY_A, stroke_width=3)
        self.play(FadeOut(grid), ReplacementTransform(diag, ground), ReplacementTransform(path, dyck),
                  run_time=1.0)
        ground_lab = zh("地面（原來的對角線）", font_size=22, color=MUTED_COLOR).next_to(ground, DOWN, buff=0.15)
        self.play(FadeIn(ground_lab), run_time=0.5)

        # 字的對應
        lattice_row = VGroup(zh("格子路徑", font_size=26, color=MUTED_COLOR),
                             *[Tex(c, font_size=44) for c in LATTICE_WORD]).arrange(RIGHT, buff=0.3)
        arrows = {"U": R"\nearrow", "D": R"\searrow"}
        dyck_row = VGroup(zh("Dyck 路徑", font_size=26, color=MUTED_COLOR),
                          *[Tex(arrows[c], font_size=44) for c in DYCK_WORD]).arrange(RIGHT, buff=0.3)
        for a, b in zip(lattice_row[1:], dyck_row[1:]):
            b.move_to(np.array([a.get_center()[0], b.get_center()[1], 0.0]))
        rows = VGroup(lattice_row, dyck_row).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        for a, b in zip(lattice_row[1:], dyck_row[1:]):
            b.set_x(a.get_x())
        rows.move_to(np.array([2.6, 1.5, 0.0]))
        self.say("往右（R）變成上坡，往上（U）變成下坡")
        self.play(FadeIn(lattice_row), run_time=0.6)
        self.play(*[TransformFromCopy(a, b) for a, b in zip(lattice_row[1:], dyck_row[1:])],
                  FadeIn(dyck_row[0]), run_time=1.2)
        self.wait(0.8)
        rule = VGroup(
            mixed("不走到對角線上方", "$\\Longleftrightarrow$", "不掉到地面以下", font_size=28),
        )
        rule.next_to(rows, DOWN, buff=0.5)
        self.say("「不越過對角線」正好變成「不掉到地面以下」")
        self.play(FadeIn(rule, shift=0.2 * UP), run_time=0.8)
        self.wait(1.0)

        definition = VGroup(
            mixed("半長 ", "$n$", " 的 Dyck 路徑：", font_size=26, color=YELLOW),
            mixed("$n$", " 個上坡、", "$n$", " 個下坡，從不低於起點的高度", font_size=26),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        definition_box = SurroundingRectangle(definition, buff=0.2, color=YELLOW, stroke_width=3)
        VGroup(definition, definition_box).next_to(rule, DOWN, buff=0.45).align_to(rows, LEFT)
        assert definition_box.get_left()[0] > dyck.get_right()[0] + 0.2
        assert definition_box.get_right()[0] < FRAME_WIDTH / 2 - 0.3
        self.play(FadeIn(definition), ShowCreation(definition_box), run_time=0.9)
        self.say("這就是 Dyck 路徑；來源論文說它像一排「山」")
        self.wait(1.8)

        # ------------------------------------------------------------ n = 0, 1, 2, 3：1、1、2、5（Fig. 2.4）
        self.clear_stage()
        unit = 0.25
        row_y = {0: 1.85, 1: 1.05, 2: 0.15, 3: -1.0}
        table = VGroup()
        n3_items = None
        for n in range(4):
            label = Tex(f"n={n}", font_size=36).move_to(np.array([-5.9, row_y[n], 0.0]))
            if n == 0:
                items = VGroup(VGroup(Dot(radius=0.06), zh("（空路徑）", font_size=20, color=MUTED_COLOR)).arrange(RIGHT, buff=0.15))
            else:
                items = VGroup(*[dyck_item(t, scale=unit / 0.15, stroke_width=4)
                                 for t in binary_trees(n)])
                items.arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
            items.move_to(np.array([0.0, row_y[n], 0.0]))
            items.align_to(np.array([-4.8, 0, 0]), LEFT)
            count = mixed(f"{catalan(n)} 種", font_size=30, color=YELLOW).move_to(np.array([6.0, row_y[n], 0.0]))
            table.add(VGroup(label, items, count))
            if n == 3:
                n3_items = items
        assert [tree_to_dyck(t) for t in binary_trees(3)] == dyck_words(3)
        self.say("數一數：", "$n=0,1,2,3$", " 分別有 1、1、2、5 條（來源論文 Fig. 2.4）")
        for row in table:
            self.play(FadeIn(row[0]), LaggedStart(*[FadeIn(i, shift=0.15 * UP) for i in row[1]], lag_ratio=0.2),
                      FadeIn(row[2]), run_time=1.0)
        self.wait(1.0)

        # 第一個上坡與它對應的下坡：同一個遞迴結構
        colored = VGroup(*[dyck_item(t, scale=unit / 0.15, stroke_width=4, colored=True)
                           for t in binary_trees(3)])
        for c, i in zip(colored, n3_items):
            c.move_to(i)
        self.say("第一個上坡和它對應的下坡（橘）把路徑分成：裡面一段（青）＋後面一段（粉紅）")
        self.play(*[Transform(i, c) for i, c in zip(n3_items, colored)], run_time=1.2)
        self.wait(1.5)
        self.say("又是「一個根 ＋ 兩個獨立的小卡塔蘭結構」")
        self.wait(2.0)
