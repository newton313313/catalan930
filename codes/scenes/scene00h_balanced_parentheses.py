"""
Scene 00h —— Dyck 路徑與平衡括號字串（來源論文 2.5 節）

    上坡 -> 「(」、下坡 -> 「)」
    高度 = 目前還沒關上的左括號數
    不掉到地面以下 <=> 任何前綴裡「)」都不比「(」多

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00h_balanced_parentheses.py Scene00hBalancedParentheses
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, dyck_item, dyck_path_mob
from utils.counting import binary_trees, dyck_to_brackets, is_dyck, tree_to_dyck
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, YELLOW, mixed, zh

WORD = "UUDUDD"          # ↑↑↓↑↓↓  ->  (()())
BAD = "UDDUUD"           # ())(()：第 3 步掉到 -1


def heights(word):
    h, out = 0, [0]
    for c in word:
        h += 1 if c == "U" else -1
        out.append(h)
    return out


class Scene00hBalancedParentheses(ChuScene):
    def construct(self):
        self.show_header("Dyck 路徑與括號")
        assert dyck_to_brackets(WORD) == "(()())" and is_dyck(WORD) and not is_dyck(BAD)

        # ------------------------------------------------------------ 一步一步寫括號
        unit = 0.6
        origin = np.array([-5.9, 0.35, 0.0])
        path = dyck_path_mob(WORD, unit=unit, origin=origin, color=CATALAN_COLOR, stroke_width=6,
                             dot_radius=0.06)
        ground = Line(origin + 0.3 * LEFT, origin + (len(WORD) * unit + 0.3) * RIGHT,
                      stroke_color=GREY_A, stroke_width=2.5)
        self.play(ShowCreation(ground), FadeIn(path.dots[0]), run_time=0.6)
        self.say("沿著 Dyck 路徑走：上坡寫「(」，下坡寫「)」")
        hs = heights(WORD)
        parens, h_labels = VGroup(), VGroup()
        for j, c in enumerate(WORD):
            mid_x = origin[0] + (j + 0.5) * unit
            p = Tex("(" if c == "U" else ")", font_size=46).move_to(np.array([mid_x, origin[1] - 0.45, 0.0]))
            lab = Tex(str(hs[j + 1]), font_size=26, fill_color=YELLOW).next_to(path.vertex(j + 1), UP, buff=0.12)
            self.play(ShowCreation(path.steps[j]), FadeIn(path.dots[j + 1]), FadeIn(p, shift=0.15 * DOWN),
                      FadeIn(lab), run_time=0.55)
            parens.add(p)
            h_labels.add(lab)
        result = Tex("(()())", font_size=70).move_to(np.array([2.6, 1.5, 0.0]))
        self.play(TransformFromCopy(parens, result), run_time=1.0)
        self.wait(0.6)

        rules = VGroup(
            mixed("高度（黃色數字）＝ 還沒關上的左括號個數", font_size=26),
            mixed("不掉到地面以下 ", "$\\Longleftrightarrow$", " 讀到任何地方，「)」都不比「(」多", font_size=26),
            mixed("最後回到地面 ", "$\\Longleftrightarrow$", " 左右括號一樣多", font_size=26),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        rules.next_to(result, DOWN, buff=0.5)
        if rules.get_right()[0] > FRAME_WIDTH / 2 - 0.2:
            rules.shift((FRAME_WIDTH / 2 - 0.2 - rules.get_right()[0]) * RIGHT)
        self.say("高度就是「還沒關上的左括號」有幾個")
        for r in rules:
            self.play(FadeIn(r, shift=0.2 * UP), run_time=0.7)
            self.wait(0.8)
        self.wait(0.8)

        # ------------------------------------------------------------ 反例：())(()
        self.play(FadeOut(rules), FadeOut(result), run_time=0.5)
        bad_origin = np.array([0.9, 0.35, 0.0])
        bad = dyck_path_mob(BAD, unit=unit, origin=bad_origin, color=CROSSING_COLOR, stroke_width=6,
                            dot_radius=0.06)
        bad_ground = Line(bad_origin + 0.3 * LEFT, bad_origin + (len(BAD) * unit + 0.3) * RIGHT,
                          stroke_color=GREY_A, stroke_width=2.5)
        dip = Dot(bad.vertex(3), radius=0.11, fill_color=CROSSING_COLOR).set_z_index(3)
        dip_lab = zh("掉到地面以下：這時「)」比「(」多", font_size=24, color=CROSSING_COLOR)
        dip_lab.next_to(dip, DOWN, buff=0.2)
        bad_text = Tex(dyck_to_brackets(BAD), font_size=56, fill_color=CROSSING_COLOR)
        bad_text.move_to(np.array([bad_ground.get_center()[0], -1.75, 0.0]))
        self.say("反例：", "$())(()$", " 第 3 個符號就多了一個「)」，路徑掉到地面以下")
        self.play(ShowCreation(bad_ground), ShowCreation(bad.steps), FadeIn(bad.dots), run_time=1.2)
        self.play(FadeIn(dip, scale=2), Flash(bad.vertex(3), color=CROSSING_COLOR, flash_radius=0.3),
                  FadeIn(dip_lab), FadeIn(bad_text), run_time=0.9)
        self.wait(2.0)

        # ------------------------------------------------------------ n = 3：五個平衡括號字串
        self.clear_stage()
        trees = binary_trees(3)
        xs = np.linspace(-5.0, 5.0, 5)
        items = VGroup()
        for x, t in zip(xs, trees):
            mini = dyck_item(t, scale=1.6, stroke_width=4)
            mini.move_to(np.array([x, 1.35, 0.0]))
            text = Tex(dyck_to_brackets(tree_to_dyck(t)), font_size=44).move_to(np.array([x, 0.45, 0.0]))
            items.add(VGroup(mini, text))
        self.say("3 對括號的平衡字串剛好有 5 個，和 5 條 Dyck 路徑一一對應")
        self.play(LaggedStart(*[FadeIn(i, shift=0.2 * UP) for i in items], lag_ratio=0.2), run_time=1.8)
        self.wait(0.8)

        statement = mixed("Dyck 路徑", "$\\longleftrightarrow$", "平衡括號字串（balanced parentheses）",
                          font_size=30, buff=0.25)
        count = mixed("數目都是 ", "$C_n$", "（", "$n$", " 對括號）", font_size=28, t2c={"C_n": CATALAN_COLOR})
        block = VGroup(statement, count).arrange(DOWN, buff=0.2)
        box = SurroundingRectangle(block, buff=0.22, color=YELLOW, stroke_width=3)
        VGroup(block, box).move_to(1.0 * DOWN)
        self.play(FadeIn(block), ShowCreation(box), run_time=0.9)
        note = mixed("注意：這裡的括號字串和上一段「乘法的括號」是不同的東西，只是數目都是 ", "$C_n$",
                     font_size=24, color=MUTED_COLOR)
        note.next_to(box, DOWN, buff=0.35)
        self.say("兩種括號別搞混：一種是乘法順序，一種是配對的括號字串")
        self.play(FadeIn(note), run_time=0.6)
        self.wait(2.5)
