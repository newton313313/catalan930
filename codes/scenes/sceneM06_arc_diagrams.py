"""
Scene M06 —— 直線上的弧圖：不交叉與不巢狀（MIT 18.212 L3）

    圓上 2n 點的配對，在點 2n 與點 1 之間剪開、攤平 -> 直線上 1..2n 的點，弦變成上方的弧
    兩條弧 i<j<k<l：(i,j),(k,l) 分開；(i,k),(j,l) 交叉；(i,l),(j,k) 巢狀
    6 點的完美配對共 15 種：不交叉 5 種、不巢狀 5 種（都是 C_3）；
    同一個 Dyck 字（左端記 U、右端記 D）在兩排各對應一個。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM06_arc_diagrams.py SceneM06ArcDiagrams
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.circle_points import label_points, make_circle_points
from utils.counting import (
    arcs_cross,
    arcs_nest,
    binary_trees,
    catalan,
    dyck_to_matching,
    dyck_to_nonnesting,
    matching_crossings,
    matching_is_noncrossing,
    matching_is_nonnesting,
    matching_nestings,
    matching_to_dyck,
    perfect_matchings,
    tree_to_dyck,
)
from utils.mit_draw import CATALAN_COLOR, CROSSING_COLOR, NEST_COLOR, ArcDiagramMob
from utils.polygon_groups import make_block
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, YELLOW, boxed, mixed, zh

N = 3
EX = ((0, 5), (1, 2), (3, 4))           # (1,6),(2,3),(4,5)：第 3 節的貫穿例子
SHARED = ((0, 1), (2, 3), (4, 5))       # (1,2),(3,4),(5,6)：不交叉也不巢狀
OK_COLOR = GREEN                        # 「不巢狀」那一排的框

CIRCLE_CENTER = np.array([-3.3, 0.45, 0.0])
RADIUS = 1.6
CUT_ANGLE = PI / 2 + PI / 6             # 點 1（90°）與點 6（150°）之間
LINE_CENTER = np.array([-3.3, -1.05, 0.0])


def norm(pairs):
    return tuple(sorted(tuple(sorted(p)) for p in pairs))


def thumb(pairs, gap=0.32, center=ORIGIN, stroke_width=3):
    """小弧圖（沒有點的編號）。"""
    return ArcDiagramMob(2 * N, pairs, gap=gap, center=center, labels=False, stroke_width=stroke_width,
                         dot_radius=0.04, line_margin=0.15, line_width=1.5)


def relation_panel(pairs, title, color, y):
    """右邊一列：名稱、兩條弧的寫法、i j k l 上的小弧圖。"""
    diagram = ArcDiagramMob(4, pairs, gap=0.62, center=np.array([4.7, y, 0.0]), color=color,
                            labels=["i", "j", "k", "l"], label_font=30, label_color=GREY_A)
    names = "ijkl"
    formula = ",".join(f"({names[a]},{names[b]})" for a, b in pairs)
    name = zh(title, font_size=28, color=color)
    tex = Tex(formula, font_size=34)
    text = VGroup(name, tex).arrange(RIGHT, buff=0.25)
    text.move_to(np.array([1.8, y + 0.3, 0.0]))
    return VGroup(text, diagram)


def frame(mob, color, buff):
    return SurroundingRectangle(mob, buff=buff, stroke_color=color, stroke_width=2.5)


class SceneM06ArcDiagrams(ChuScene):
    def construct(self):
        self.show_header("直線上的弧圖：不交叉與不巢狀")

        # ------------------------------------------------------------ 數學資料
        assert matching_is_noncrossing(EX) and matching_nestings(EX) == [(0, 1), (0, 2)]
        words = [tree_to_dyck(t) for t in binary_trees(N)]
        nc_row = [norm(dyck_to_matching(w)) for w in words]
        nn_row = [norm(dyck_to_nonnesting(w)) for w in words]
        assert words[3] == "UUDUDD" and nc_row[3] == EX
        all_m = [norm(m) for m in perfect_matchings(2 * N)]
        assert len(all_m) == 15 == 5 * 3 * 1
        nc_set = [m for m in all_m if matching_is_noncrossing(m)]
        nn_set = [m for m in all_m if matching_is_nonnesting(m)]
        assert sorted(nc_set) == sorted(nc_row) and sorted(nn_set) == sorted(nn_row)
        assert len(nc_set) == len(nn_set) == catalan(N) == 5
        assert [m for m in nc_set if m in nn_set] == [SHARED]
        assert all(matching_to_dyck(a) == w == matching_to_dyck(b) for a, b, w in zip(nc_row, nn_row, words))
        shared_col = nc_row.index(SHARED)
        assert nn_row[shared_col] == SHARED and words[shared_col] == "UDUDUD"
        four = [norm(m) for m in perfect_matchings(4)]
        assert four == [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
        assert not arcs_cross(*four[0]) and not arcs_nest(*four[0])
        assert arcs_cross(*four[1]) and not arcs_nest(*four[1])
        assert arcs_nest(*four[2]) and not arcs_cross(*four[2])

        # ------------------------------------------------------------ 圓上的配對
        circle, dots, coords = make_circle_points(2 * N, radius=RADIUS, center=CIRCLE_CENTER)
        ring = Arc(start_angle=CUT_ANGLE, angle=-TAU, radius=RADIUS, arc_center=CIRCLE_CENTER)
        ring.match_style(circle)                       # 從剪開處順時針一圈：攤平時 1 在左、6 在右
        labels = label_points(coords, CIRCLE_CENTER, buff=0.32)
        chords = VGroup(*[make_block(p, coords, color=CATALAN_COLOR) for p in EX])
        self.say("圓上 6 個點的不交叉配對 ", "$(1,6),(2,3),(4,5)$")
        self.play(ShowCreation(ring), FadeIn(dots), FadeIn(labels), run_time=1.0)
        self.play(LaggedStart(*[ShowCreation(c) for c in chords], lag_ratio=0.3), run_time=1.0)
        self.wait(0.6)

        cut_dir = np.array([np.cos(CUT_ANGLE), np.sin(CUT_ANGLE), 0.0])
        cut_pt = CIRCLE_CENTER + RADIUS * cut_dir
        cut = Line(cut_pt - 0.28 * cut_dir, cut_pt + 0.28 * cut_dir, stroke_color=CROSSING_COLOR,
                   stroke_width=5)
        cut_note = zh("剪開", font_size=24, color=CROSSING_COLOR).next_to(cut_pt + 0.3 * cut_dir, UL, buff=0.05)
        self.say("在點 6 和點 1 之間剪開，把圓攤平成一條直線")
        self.play(ShowCreation(cut), FadeIn(cut_note), run_time=0.7)
        self.wait(0.4)

        line_diag = ArcDiagramMob(2 * N, EX, gap=0.85, center=LINE_CENTER, labels=True, label_font=28)
        self.play(
            ReplacementTransform(VGroup(ring, chords, dots, labels), line_diag),
            FadeOut(cut), FadeOut(cut_note),
            run_time=2.2,
        )
        self.say("點變成直線上的 1 到 6，弦變成直線上方的弧")
        self.wait(1.0)

        # ------------------------------------------------------------ 兩條弧的三種關係
        ineq = Tex("i<j<k<l", font_size=40).move_to(np.array([3.4, 2.55, 0.0]))
        panels = VGroup(
            relation_panel(four[0], "分開", CATALAN_COLOR, 1.35),
            relation_panel(four[1], "交叉", CROSSING_COLOR, 0.0),
            relation_panel(four[2], "巢狀", NEST_COLOR, -1.6),
        )
        self.say("兩條弧的四個端點 ", "$i<j<k<l$", "：只有三種配法")
        self.play(FadeIn(ineq), run_time=0.5)
        for panel in panels:
            self.play(FadeIn(panel[0], shift=0.2 * RIGHT), FadeIn(panel[1].baseline), FadeIn(panel[1].dots),
                      FadeIn(panel[1].labels), run_time=0.5)
            self.play(LaggedStart(*[ShowCreation(a) for a in panel[1].arcs], lag_ratio=0.4), run_time=0.8)
            self.wait(0.4)
        self.say("$(i,k),(j,l)$", " 交叉（紅）；", "$(i,l),(j,k)$", " 巢狀：一條包住另一條（紫）")
        self.play(*[Indicate(m, color=YELLOW, scale_factor=1.15) for m in (panels[1][0], panels[2][0])],
                  run_time=1.0)
        self.wait(1.0)

        nest_idx = sorted({k for pair in matching_nestings(EX) for k in pair})
        assert nest_idx == [0, 1, 2]
        self.say("左邊的例子沒有交叉，但 ", "$(1,6)$", " 包住 ", "$(2,3)$", " 和 ", "$(4,5)$", "：有巢狀")
        self.play(*[line_diag.arcs[k].animate.set_stroke(NEST_COLOR) for k in nest_idx],
                  Indicate(panels[2][1], color=YELLOW, scale_factor=1.1), run_time=0.9)
        self.wait(1.6)

        # ------------------------------------------------------------ 15 種完美配對
        self.clear_stage()
        title = mixed("6 個點的完美配對：", "$5\\times 3\\times 1=15$", " 種", font_size=32)
        title.move_to(np.array([0.0, 2.75, 0.0]))
        grid = VGroup()
        for idx, m in enumerate(all_m):
            c, r = divmod(idx, 3)          # 第 c 欄：點 1 配點 c+2；同一欄的 3 列：剩下最左邊的點的 3 種選擇
            assert m[0] == (0, c + 1) and m[1][0] == min(set(range(2 * N)) - {0, c + 1})
            grid.add(thumb(m, center=np.array([(c - 2) * 2.55, 1.35 - 1.55 * r, 0.0])))
        assert len(grid) == 5 * 3
        self.say("點 1 有 5 個對象可選（5 欄），剩下最左邊的點有 3 個（3 列），再來 1 個")
        self.play(FadeIn(title), LaggedStart(*[FadeIn(g, scale=0.8) for g in grid], lag_ratio=0.06),
                  run_time=2.0)
        self.wait(0.8)

        # 第一遍：交叉的弧變紅
        cross_anims, nc_frames = [], VGroup()
        for m, g in zip(all_m, grid):
            bad = sorted({k for pair in matching_crossings(m) for k in pair})
            cross_anims += [g.arcs[k].animate.set_stroke(CROSSING_COLOR) for k in bad]
            if not bad:
                nc_frames.add(frame(g, CATALAN_COLOR, 0.1))
        assert len(nc_frames) == 5 and len(cross_anims) > 0
        self.say("交叉的弧畫成紅色：沒有紅弧的（藍框）是不交叉，", "$5$", " 種")
        self.play(*cross_anims, run_time=1.0)
        self.play(LaggedStart(*[ShowCreation(f) for f in nc_frames], lag_ratio=0.15), run_time=1.0)
        self.wait(1.2)

        # 第二遍：巢狀的弧變紫
        reset = [g.arcs.animate.set_stroke(CATALAN_COLOR) for g in grid]
        self.play(*reset, run_time=0.5)
        nest_anims, nn_frames = [], VGroup()
        for m, g in zip(all_m, grid):
            bad = sorted({k for pair in matching_nestings(m) for k in pair})
            nest_anims += [g.arcs[k].animate.set_stroke(NEST_COLOR) for k in bad]
            if not bad:
                nn_frames.add(frame(g, OK_COLOR, 0.19))
        assert len(nn_frames) == 5
        self.say("巢狀的弧畫成紫色：沒有紫弧的（綠框）是不巢狀，也是 ", "$5$", " 種")
        self.play(*nest_anims, run_time=1.0)
        self.play(LaggedStart(*[ShowCreation(f) for f in nn_frames], lag_ratio=0.15), run_time=1.0)
        self.wait(1.2)
        both = grid[all_m.index(SHARED)]
        self.say("$(1,2),(3,4),(5,6)$", " 有兩個框：不交叉也不巢狀")
        self.play(Indicate(both, color=YELLOW, scale_factor=1.15), run_time=1.0)
        self.wait(0.6)

        # ------------------------------------------------------------ 兩排並列
        xs = [-3.3 + 2.25 * c for c in range(5)]
        row_y = (1.35, -0.75)
        rows = [VGroup(*[thumb(m, gap=0.34, center=np.array([x, y, 0.0])) for m, x in zip(ms, xs)])
                for ms, y in zip((nc_row, nn_row), row_y)]
        row_labels = VGroup(
            zh("不交叉", font_size=30, color=CATALAN_COLOR).move_to(np.array([-5.85, row_y[0] + 0.3, 0.0])),
            zh("不巢狀", font_size=30, color=OK_COLOR).move_to(np.array([-5.85, row_y[1] + 0.3, 0.0])),
        )
        moves = []
        for row, ms in zip(rows, (nc_row, nn_row)):
            for th, m in zip(row, ms):
                moves.append(TransformFromCopy(grid[all_m.index(m)], th))
        self.say("把兩種各自排成一排")
        self.play(FadeOut(nc_frames), FadeOut(nn_frames), FadeOut(title), run_time=0.4)
        self.play(*moves, FadeOut(grid), run_time=1.4)
        self.play(FadeIn(row_labels, shift=0.2 * RIGHT), run_time=0.4)

        word_mobs = VGroup(*[Tex(rf"\mathrm{{{w}}}", font_size=30, fill_color=YELLOW).move_to(np.array([x, 0.65, 0.0]))
                             for w, x in zip(words, xs)])
        self.say("同一欄：弧的左端記 U、右端記 D，得到同一個 Dyck 字")
        self.play(LaggedStart(*[FadeIn(w, shift=0.15 * UP) for w in word_mobs], lag_ratio=0.15), run_time=1.2)
        self.wait(1.4)

        col = VGroup(rows[0][shared_col], word_mobs[shared_col], rows[1][shared_col])
        col_box = SurroundingRectangle(col, buff=0.15, stroke_color=YELLOW, stroke_width=3)
        summary = boxed(mixed("不交叉、不巢狀各有 ", "$C_3=5$", " 種", font_size=34))
        summary.move_to(np.array([0.0, -2.35, 0.0]))
        self.say("$(1,2),(3,4),(5,6)$", " 不交叉也不巢狀：兩排都有它（黃框）")
        self.play(ShowCreation(col_box), FadeIn(summary), run_time=1.0)
        self.wait(2.5)
