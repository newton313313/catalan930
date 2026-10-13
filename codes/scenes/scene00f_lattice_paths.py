"""
Scene 00f —— 格子路徑（來源論文 2.4 節）

    (0,0) 到 (n,n)、每步往右 R 或往上 U：共 binom(2n,n) 條
    不走到對角線 y = x 上方的：C_n 條
    binom(2n,n) - binom(2n,n-1) = C_n
最後的「反射原理」是補充說明（來源論文只給公式，沒有證明）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00f_lattice_paths.py Scene00fLatticePaths
"""
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    lattice_diagonal,
    lattice_grid,
    lattice_path_mob,
    lattice_thumbnail,
)
from utils.counting import catalan, first_bad_step, lattice_ok, lattice_points, lattice_words, reflect_tail
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, ROOT_COLOR, YELLOW, mixed, zh

N = 3
EXAMPLE = "RURRUU"          # 示範路徑（合法）
BAD = "RUURRU"              # 反射原理示範用的不合法路徑
UNIT = 0.95
ORIGIN_PT = np.array([-6.1, -1.55, 0.0])


def grid_point(origin, unit, x, y):
    return origin + unit * np.array([x, y, 0.0])


class Scene00fLatticePaths(ChuScene):
    def construct(self):
        self.show_header("格子路徑")
        words = lattice_words(N)
        assert len(words) == comb(2 * N, N) == 20
        assert sum(lattice_ok(w) for w in words) == catalan(N) == 5
        assert lattice_ok(EXAMPLE) and not lattice_ok(BAD) and reflect_tail(BAD) == "RUUUUR"

        # ------------------------------------------------------------ 格子與一條路徑
        grid = lattice_grid(N, N, UNIT, ORIGIN_PT, color=GREY_C, stroke_width=2)
        start_lab = Tex("(0,0)", font_size=28, fill_color=MUTED_COLOR).next_to(ORIGIN_PT, DL, buff=0.08)
        end_lab = Tex("(3,3)", font_size=28, fill_color=MUTED_COLOR).next_to(
            grid_point(ORIGIN_PT, UNIT, N, N), RIGHT, buff=0.12)
        legend = VGroup(mixed("$R$", "：往右一格", font_size=28),
                        mixed("$U$", "：往上一格", font_size=28)).arrange(RIGHT, buff=0.6)
        legend.move_to(np.array([-4.65, 2.45, 0.0]))
        self.say("在格子上從 (0,0) 走到 (3,3)，每一步只能往右（R）或往上（U）")
        self.play(ShowCreation(grid), FadeIn(start_lab), FadeIn(end_lab), FadeIn(legend), run_time=1.2)

        path = lattice_path_mob(EXAMPLE, UNIT, ORIGIN_PT, color=CATALAN_COLOR, stroke_width=6,
                                dot_radius=0.06)
        letters = VGroup(*[Tex(c, font_size=46) for c in EXAMPLE]).arrange(RIGHT, buff=0.22)
        letters.move_to(np.array([-4.65, -2.5, 0.0]))
        self.play(FadeIn(path.dots[0]), run_time=0.3)
        for j, c in enumerate(EXAMPLE):
            self.play(ShowCreation(path.steps[j]), FadeIn(path.dots[j + 1]),
                      FadeIn(letters[j], shift=0.2 * UP), run_time=0.45)
        self.say("一條路徑就是一個由 R 和 U 組成的字，例如 RURRUU")
        self.wait(1.2)

        # ------------------------------------------------------------ 全部 20 條
        cols = 5
        thumbs = VGroup()
        for idx, w in enumerate(words):
            r, c = divmod(idx, cols)
            center = np.array([-0.15 + 1.6 * c, 1.75 - 1.18 * r, 0.0])
            unit = 0.27
            thumbs.add(lattice_thumbnail(w, N, unit=unit, origin=center - 1.5 * unit * np.array([1, 1, 0])))
        self.say("每條路徑恰有 3 個 R、3 個 U：從 6 個位置選 3 個放 R，共 ", "$\\binom{6}{3}=20$", " 條")
        self.play(LaggedStart(*[FadeIn(t, scale=0.7) for t in thumbs], lag_ratio=0.06), run_time=2.6)
        self.say("一般來說，", "$(0,0)$", " 到 ", "$(n,n)$", " 共有 ", "$\\binom{2n}{n}$", " 條路徑")
        self.wait(1.0)

        # ------------------------------------------------------------ 不可以走到對角線上方
        diag = lattice_diagonal(N, UNIT, ORIGIN_PT, color=GREY_A, stroke_width=3)
        diag_lab = Tex("y=x", font_size=30, fill_color=GREY_A).next_to(diag.get_end(), UL, buff=0.08)
        self.say("加一個限制：不可以走到對角線 ", "$y=x$", " 的上方（碰到對角線可以）")
        self.play(ShowCreation(diag), FadeIn(diag_lab), run_time=0.9)
        self.wait(0.6)
        bad_ids = [i for i, w in enumerate(words) if not lattice_ok(w)]
        good_ids = [i for i, w in enumerate(words) if lattice_ok(w)]
        self.say("走到對角線上方的路徑標成紅色")
        self.play(*[thumbs[i].path.steps.animate.set_stroke(CROSSING_COLOR) for i in bad_ids], run_time=1.2)
        self.play(*[Indicate(thumbs[i], scale_factor=1.15, color=CATALAN_COLOR) for i in good_ids],
                  run_time=1.0)
        self.say("20 條裡只有 5 條從不越過對角線")
        self.wait(1.2)

        # 只留下合法的 5 條
        good_row_targets = VGroup(*[thumbs[i].copy() for i in good_ids])
        good_row_targets.arrange(RIGHT, buff=0.55).move_to(np.array([3.05, 1.6, 0.0]))
        self.play(*[FadeOut(thumbs[i]) for i in bad_ids], run_time=0.7)
        self.play(*[Transform(thumbs[i], t) for i, t in zip(good_ids, good_row_targets)], run_time=1.0)
        c3 = Tex(R"C_3=5", font_size=44, fill_color=YELLOW).next_to(good_row_targets, DOWN, buff=0.3)
        self.play(FadeIn(c3, scale=1.3), run_time=0.6)

        # ------------------------------------------------------------ 公式：全部減掉不合法的
        formula = Tex(R"\binom{2n}{n}-\binom{2n}{n-1}=\frac{1}{n+1}\binom{2n}{n}=C_n", font_size=44)
        formula.move_to(np.array([3.05, -0.45, 0.0]))
        box = SurroundingRectangle(formula, buff=0.22, color=YELLOW, stroke_width=3)
        check = Tex(R"n=3:\ \ \binom{6}{3}-\binom{6}{2}=20-15=5", font_size=36, fill_color=MUTED_COLOR)
        check.next_to(box, DOWN, buff=0.3)
        self.say("來源論文的公式：全部的路徑，減掉不合法的路徑")
        self.play(Write(formula), run_time=1.6)
        self.play(ShowCreation(box), run_time=0.6)
        self.play(FadeIn(check, shift=0.2 * UP), run_time=0.8)
        self.say("不合法的路徑為什麼剛好有 ", "$\\binom{2n}{n-1}$", " 條？")
        self.wait(2.0)

        # ------------------------------------------------------------ 補充說明：反射原理
        self.clear_stage()
        tag = zh("補充說明：反射原理（來源論文只給公式，沒有證明）", font_size=26, color=YELLOW)
        tag.move_to(np.array([0.0, 2.95, 0.0]))
        unit = 0.85
        origin = np.array([-5.6, -2.3, 0.0])
        grid2 = lattice_grid(N, N + 1, unit, origin, color=GREY_C, stroke_width=2)
        diag2 = lattice_diagonal(N, unit, origin, color=GREY_A, stroke_width=3)
        line_x1 = DashedLine(grid_point(origin, unit, 0, 1), grid_point(origin, unit, N, N + 1),
                             dash_length=0.08, stroke_color=CROSSING_COLOR, stroke_width=3)
        line_lab = Tex("y=x+1", font_size=30, fill_color=CROSSING_COLOR).next_to(line_x1.get_end(), RIGHT, buff=0.1)
        end_lab = Tex("(3,3)", font_size=26, fill_color=MUTED_COLOR).next_to(grid_point(origin, unit, N, N), RIGHT, buff=0.1)
        self.play(FadeIn(tag), ShowCreation(grid2), ShowCreation(diag2), FadeIn(end_lab), run_time=1.0)
        bad_path = lattice_path_mob(BAD, unit, origin, color=CROSSING_COLOR, stroke_width=6, dot_radius=0.06)
        self.say("一條不合法的路徑，一定會碰到 ", "$y=x+1$", " 這條線")
        self.play(ShowCreation(bad_path.steps), FadeIn(bad_path.dots), run_time=1.6)
        self.play(ShowCreation(line_x1), FadeIn(line_lab), run_time=0.8)
        j = first_bad_step(BAD)
        hit = Dot(bad_path.vertex(j), radius=0.12, fill_color=ROOT_COLOR).set_z_index(3)
        self.say("找到第一次碰到這條線的點")
        self.play(FadeIn(hit, scale=2), Flash(bad_path.vertex(j), color=ROOT_COLOR, flash_radius=0.35),
                  run_time=0.9)
        self.wait(0.6)

        # 之後的部分沿著 y = x + 1 翻過去（3D 翻轉 180 度 = 平面上的鏡射）
        tail = VGroup(*bad_path.steps[j:], *bad_path.dots[j + 1:])
        axis = normalize(np.array([1.0, 1.0, 0.0]))
        self.say("把這一點之後的部分，沿著 ", "$y=x+1$", " 翻過去")
        self.play(Rotate(tail, PI, axis=axis, about_point=bad_path.vertex(j)), run_time=1.6)
        new_end = Tex("(2,4)", font_size=30, fill_color=YELLOW).next_to(grid_point(origin, unit, N - 1, N + 1), UP, buff=0.12)
        self.play(FadeIn(new_end, scale=1.3), run_time=0.6)
        before = Tex("RUU|RRU", font_size=36)
        after = Tex("RUU|UUR", font_size=36)
        for word_tex, color in ((before, CROSSING_COLOR), (after, YELLOW)):
            glyphs = sorted(word_tex.submobjects, key=lambda g: g.get_center()[0])
            VGroup(*glyphs[4:]).set_fill(color)          # 翻轉的那一段
        swap = VGroup(before, Tex(R"\longrightarrow", font_size=36), after).arrange(RIGHT, buff=0.3)
        explain = VGroup(
            mixed("翻過去之後 ", "$R$", " 和 ", "$U$", " 互換：", font_size=26),
            swap,
            mixed("終點變成 ", "$(n-1,\\,n+1)=(2,4)$", font_size=26),
            mixed("這種路徑有 ", "$n-1$", " 個 ", "$R$", "、", "$n+1$", " 個 ", "$U$", "：共 ",
                  "$\\binom{2n}{n-1}$", " 條", font_size=26),
            mixed("反過來，走到 (2,4) 的路徑都會碰到 ", "$y=x+1$", font_size=26),
            mixed("把它翻回來，就是一條不合法的路徑", font_size=26),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        explain.move_to(np.array([2.1, 0.75, 0.0]))
        assert explain.get_right()[0] < FRAME_WIDTH / 2 - 0.3
        for row in explain:
            self.play(FadeIn(row, shift=0.2 * LEFT), run_time=0.7)
            self.wait(0.7)
        self.say("所以不合法的路徑和終點 (2,4) 的路徑一一對應：", "$\\binom{6}{2}=15$", " 條")
        self.wait(1.5)
        result = mixed("合法的路徑 ", "$=\\binom{2n}{n}-\\binom{2n}{n-1}=C_n$", font_size=28)
        result_box = SurroundingRectangle(result, buff=0.2, color=YELLOW, stroke_width=3)
        VGroup(result, result_box).next_to(explain, DOWN, buff=0.3)
        assert result_box.get_bottom()[1] > -3.0
        self.play(FadeIn(result), ShowCreation(result_box), run_time=0.9)
        self.say("全部減掉不合法的，就是卡塔蘭數")
        self.wait(2.5)
