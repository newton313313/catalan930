"""
Scene 00d —— 乘法的順序（完全括號化）：n+1 個因子有 C_n 種括法（來源論文 2.2 節）

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00d_parenthesization.py Scene00dParenthesization
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    LEFT_COLOR,
    RIGHT_COLOR,
    catalan_product_tex,
    paren_build_animations,
    paren_mob,
)
from utils.counting import binary_trees, catalan, parenthesizations, tree_size
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, ROOT_COLOR, YELLOW, mixed, zh


def build(scene, plain, target, run_time=0.6):
    for step in paren_build_animations(plain, target):
        scene.play(*step, run_time=run_time)


def count_tag(count: int, n: int, color=WHITE) -> VGroup:
    """「→ 5 種 = C_3」"""
    return mixed("$\\rightarrow$", f" {count} 種 ", f"$=C_{{{n}}}$", font_size=30, color=color)


class Scene00dParenthesization(ChuScene):
    def construct(self):
        self.show_header("乘法的順序：完全括號化")
        assert parenthesizations(3) == ["a·(b·(c·d))", "a·((b·c)·d)", "(a·b)·(c·d)",
                                        "(a·(b·c))·d", "((a·b)·c)·d"]

        self.say("乘法一次只能乘兩個數：要把幾個數乘起來，得先決定乘的順序")
        self.wait(0.6)

        # ------------------------------------------------------------ 2 個、3 個因子
        label_x = -5.2
        lab2 = zh("2 個因子", font_size=28, color=MUTED_COLOR).move_to(np.array([label_x, 2.2, 0]))
        two = paren_mob(binary_trees(1)[0], "ab", font_size=44).move_to(np.array([-2.6, 2.2, 0]))
        cnt2 = count_tag(1, 1).next_to(two, RIGHT, buff=0.6)
        self.play(FadeIn(lab2), Write(two), run_time=0.9)
        self.play(FadeIn(cnt2, shift=0.2 * LEFT), run_time=0.5)
        self.say("2 個因子：只有一種乘法 ", "$a\\cdot b$")
        self.wait(0.5)

        lab3 = zh("3 個因子", font_size=28, color=MUTED_COLOR).move_to(np.array([label_x, 1.0, 0]))
        plain3 = Tex(R"a\cdot b\cdot c", font_size=44).move_to(np.array([-2.6, 1.0, 0]))
        self.play(FadeIn(lab3), Write(plain3), run_time=0.8)
        self.say("3 個因子：先乘 ", "$a\\cdot b$", "，或先乘 ", "$b\\cdot c$")
        threes = VGroup()
        xs3 = [-0.5, 1.9]
        for x, t in zip(xs3, reversed(binary_trees(2))):          # (a·b)·c 先，a·(b·c) 後
            target = paren_mob(t, "abc", font_size=44).move_to(np.array([x, 1.0, 0]))
            build(self, plain3, target)
            self.add(target)
            threes.add(target)
        cnt3 = count_tag(2, 2).next_to(threes, RIGHT, buff=0.6)
        self.play(FadeIn(cnt3, shift=0.2 * LEFT), run_time=0.5)
        self.wait(1.0)

        # ------------------------------------------------------------ 4 個因子：五種
        lab4 = zh("4 個因子", font_size=28, color=MUTED_COLOR).move_to(np.array([label_x, -0.2, 0]))
        plain4 = Tex(R"a\cdot b\cdot c\cdot d", font_size=44).move_to(np.array([-2.6, -0.2, 0]))
        self.play(FadeIn(lab4), Write(plain4), run_time=0.8)
        self.say("4 個因子：括號由內而外一層一層長出來，表示乘的先後")
        trees = binary_trees(3)
        slots = [np.array([x, -1.35, 0]) for x in (-5.2, -2.6, 0.0, 2.6, 5.2)]
        fours = VGroup()
        for slot, t in zip(slots, trees):
            target = paren_mob(t, "abcd", font_size=34).move_to(slot)
            build(self, plain4, target, run_time=0.5)
            self.add(target)
            fours.add(target)
        cnt4 = count_tag(5, 3, color=YELLOW).next_to(plain4, RIGHT, buff=0.8)
        self.play(FadeIn(cnt4, scale=1.3), run_time=0.6)
        self.say("一共 5 種")
        self.wait(1.2)

        # ------------------------------------------------------------ 依最後一次乘法分組：同樣的遞迴
        self.play(FadeOut(VGroup(lab2, two, cnt2, lab3, plain3, threes, cnt3)),
                  VGroup(lab4, plain4, cnt4).animate.move_to(2.25 * UP), run_time=0.9)
        colored = VGroup(*[paren_mob(t, "abcd", font_size=34, colored=True) for t in trees])
        for c, f in zip(colored, fours):
            c.move_to(f)
        self.say("最後一次乘法（橘色）把乘積切成左、右兩段")
        self.play(*[Transform(f, c) for f, c in zip(fours, colored)], run_time=1.2)
        self.wait(1.0)

        # 依左段的因子數分組：1 | 2 | 3 個因子
        groups = {}
        for f, t in zip(fours, trees):
            groups.setdefault(tree_size(t[0]), []).append(f)
        group_mobs = [VGroup(*groups[k]) for k in range(3)]
        for g in group_mobs:
            g.target_group = g.copy().arrange(RIGHT, buff=0.35)
        layout = VGroup(*[g.target_group for g in group_mobs]).arrange(RIGHT, buff=0.75).move_to(0.75 * UP)
        assert layout.get_width() < FRAME_WIDTH - 0.6
        self.play(*[Transform(g, g.target_group) for g in group_mobs], run_time=1.0)
        frames, labels = VGroup(), VGroup()
        for k, g in enumerate(group_mobs):
            frame = SurroundingRectangle(g, buff=0.18, color=GREY_C, stroke_width=1.5)
            lab = catalan_product_tex(k, 2 - k, f"={catalan(k) * catalan(2 - k)}", font_size=34)
            lab.next_to(frame, DOWN, buff=0.2)
            frames.add(frame)
            labels.add(lab)
        self.play(LaggedStart(*[ShowCreation(f) for f in frames], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(l, shift=0.15 * UP) for l in labels], lag_ratio=0.2), run_time=1.4)
        self.say("左段有 ", "$k+1$", " 個因子、右段有 ", "$3-k$", " 個：兩段各自括，互不影響")
        self.wait(1.8)

        # 逐項上色：左段 C_k 青色、右段 C_{2-k} 粉紅（用 glyph 位置上色，因為 C_1C_1 兩個字相同）
        recurrence = Tex(R"C_3=C_0C_2+C_1C_1+C_2C_0=2+1+2=5", font_size=46)
        glyphs = sorted(recurrence.submobjects, key=lambda g: g.get_center()[0])
        assert len(glyphs) == 25
        for start in (3, 8, 13):                 # 每一項 C_kC_{2-k} 佔 4 個 glyph
            VGroup(*glyphs[start:start + 2]).set_fill(LEFT_COLOR)
            VGroup(*glyphs[start + 2:start + 4]).set_fill(RIGHT_COLOR)
        recurrence.move_to(1.25 * DOWN)
        self.say("又是同一個遞迴：", "$C_n=\\sum C_kC_{n-1-k}$")
        self.play(Write(recurrence), run_time=1.6)
        self.wait(1.2)

        summary = mixed("$n+1$", " 個因子（做 ", "$n$", " 次乘法）", "$\\longleftrightarrow$", " ",
                        "$C_n$", " 種完全括號化", font_size=30)
        summary_box = SurroundingRectangle(summary, buff=0.2, color=YELLOW, stroke_width=3)
        VGroup(summary, summary_box).move_to(2.35 * DOWN)
        self.play(FadeIn(summary), ShowCreation(summary_box), run_time=1.0)
        self.say("所以括號的方法數也是卡塔蘭數")
        self.wait(2.5)
