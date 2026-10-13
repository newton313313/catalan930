"""
Scene 06 —— 從幾何到遞迴：r_1 + ... + r_{v_i} = n - e_i 與論文式 (5)

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene06_recurrence.py Scene06Recurrence
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import recurrence
from utils.formulas import recurrence_formula
from utils.polygon_groups import make_block, make_configuration
from utils.root_figure import (
    ROOT_ALT_R2,
    ROOT_N_VEC,
    ROOT_R_VECTORS,
    ROOT_V_VEC,
    RootFigure,
)
from utils.scene_base import ChuScene
from utils.styles import REGION_COLORS, TYPE1_COLOR, TYPE2_COLOR, zh

# Fig. 1 的五種分法，依「固定點 0 屬於哪一型群組」分類（手動指定）
ROOT_IN_CHORD = [
    [(0, 4), (1, 2, 3)],
    [(0, 1), (2, 3, 4)],
]
ROOT_IN_TRIANGLE = [
    [(0, 1, 2), (3, 4)],
    [(0, 1, 4), (2, 3)],
    [(0, 3, 4), (1, 2)],
]


def vec_tex(name: str, a: int, b: int, font_size: float = 44) -> Tex:
    """name = (a, b)，第一個分量塗弦的顏色、第二個分量塗三角形的顏色。"""
    tex = Tex(fR"{name}=({a},\,{b})", font_size=font_size)
    tex[-4].set_fill(TYPE1_COLOR)
    tex[-2].set_fill(TYPE2_COLOR)
    return tex


def describe(a: int, b: int) -> str:
    parts = []
    if a:
        parts.append(f"{a} 條弦")
    if b:
        parts.append(f"{b} 個三角形")
    return "、".join(parts) if parts else "空"


class Scene06Recurrence(ChuScene):
    def construct(self):
        self.show_header("從幾何到遞迴")
        assert recurrence((1, 1), ROOT_V_VEC) == 5

        # ------------------------------------------------------------ 左邊：根分解的圖
        fig = RootFigure(center=4.25 * LEFT + 0.45 * UP, radius=1.95)
        self.play(FadeIn(fig), run_time=1.0)
        self.say("延續上一幕：根群組（三角形）把其餘的點切成 3 段")
        self.wait(1.2)

        left_x = -1.2   # 右側公式的左邊界

        def put(mob, y):
            mob.move_to(y * UP)
            mob.align_to(left_x * RIGHT, LEFT)
            return mob

        # ------------------------------------------------------------ Step 1：n 與 n - e_i
        n_line = VGroup(vec_tex(R"\vec n", *ROOT_N_VEC),
                        zh("全部：3 條弦、2 個三角形", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        put(n_line, 2.55)
        self.say("用向量 ", "$\\vec n$", " 記下全部的群組")
        self.play(FadeIn(n_line, shift=0.2 * RIGHT), run_time=0.8)
        self.wait(1.0)

        m_line = VGroup(vec_tex(R"\vec n-\vec e_2", 3, 1),
                        zh("拿掉根群組（1 個三角形）", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        put(m_line, 1.75)
        self.say("根群組用掉一個三角形：剩下 ", "$\\vec n-\\vec e_2$")
        self.play(Indicate(fig.root, scale_factor=1.06, color=TYPE2_COLOR), run_time=0.9)
        self.play(TransformFromCopy(n_line[0], m_line[0]), FadeIn(m_line[1]), run_time=1.0)
        self.wait(1.0)

        # ------------------------------------------------------------ Step 2：分配到各段
        self.say("剩下的群組分配到 3 段裡：第 ", "$j$", " 段分到的記作 ", "$\\vec r_j$")
        rows = VGroup()
        for j, (a, b) in enumerate(ROOT_R_VECTORS):
            row = VGroup(
                Tex(f"R_{j + 1}:", font_size=40, fill_color=REGION_COLORS[j]),
                vec_tex(fR"\vec r_{j + 1}", a, b, font_size=40),
                zh(describe(a, b), font_size=26, color=GREY_A),
            ).arrange(RIGHT, buff=0.3)
            put(row, 0.75 - 0.72 * j)
            rows.add(row)
            self.play(
                Indicate(fig.region_labels[j], scale_factor=1.4, color=REGION_COLORS[j]),
                *[Indicate(b_mob, scale_factor=1.12, color=b_mob.get_stroke_color()) for b_mob in fig.subs[j]],
                FadeIn(row, shift=0.2 * RIGHT),
                run_time=1.0,
            )
            self.wait(0.3)

        sum_line = Tex(R"\vec r_1+\vec r_2+\vec r_3=(3,\,1)=\vec n-\vec e_2", font_size=44)
        put(sum_line, -1.65)
        self.play(Write(sum_line), run_time=1.3)
        self.say("三段加起來，剛好是剩下的全部群組")
        self.wait(1.5)

        general = Tex(R"\vec r_1+\vec r_2+\cdots+\vec r_{v_i}=\vec n-\vec e_i", font_size=48)
        put(general, -1.65)
        general_box = SurroundingRectangle(general, buff=0.2, color=YELLOW, stroke_width=3)
        self.say("一般情形：根群組是第 ", "$i$", " 型，有 ", "$v_i$", " 段")
        self.play(FadeTransform(sum_line, general), run_time=1.0)
        self.play(ShowCreation(general_box), run_time=0.6)
        self.wait(1.5)

        # ------------------------------------------------------------ Step 3：各段相乘
        constraint = VGroup(general_box, general)
        self.play(
            FadeOut(n_line), FadeOut(m_line), FadeOut(rows),
            constraint.animate.move_to(2.2 * UP).align_to(left_x * RIGHT, LEFT),
            run_time=1.0,
        )
        product = Tex(R"d(\vec r_1)\,d(\vec r_2)\cdots d(\vec r_{v_i})", font_size=52)
        put(product, 0.9)
        self.say("第 ", "$j$", " 段內部有 ", "$d(\\vec r_j)$", " 種分法；各段獨立，所以相乘")
        self.play(Write(product), run_time=1.3)
        self.wait(0.8)

        example = Tex(R"d(0,1)\cdot d(2,0)\cdot d(1,0)=1\cdot 2\cdot 1=2", font_size=42)
        example_tag = zh("本例：", font_size=28, color=GREY_A)
        example_row = VGroup(example_tag, example).arrange(RIGHT, buff=0.25)
        put(example_row, -0.35)
        self.play(FadeIn(example_row, shift=0.2 * UP), run_time=0.8)
        # 本例的「2」：R_2 有兩種分法
        coords = fig.coords
        r2_backup = fig.subs[1].copy()
        r2_alt = VGroup(*[make_block(b, coords, stroke_width=fig.subs[1][0].get_stroke_width())
                          for b in ROOT_ALT_R2])
        self.say("本例的 2 來自 ", "$R_2$", "：4 個點連兩條弦有 2 種方法")
        self.play(Transform(fig.subs[1], r2_alt), run_time=0.8)
        self.wait(0.7)
        self.play(Transform(fig.subs[1], r2_backup), run_time=0.8)
        self.wait(0.8)

        # ------------------------------------------------------------ Step 4：全部加起來
        self.play(FadeOut(fig), FadeOut(example_row), run_time=0.7)
        ingredients = VGroup(constraint, product)
        self.play(
            constraint.animate.move_to(2.35 * UP),
            product.animate.move_to(1.15 * UP),
            run_time=0.9,
        )
        rec = recurrence_formula(font_size=46)
        if rec.get_width() > 12.5:
            rec.set_width(12.5)
        rec.move_to(0.75 * DOWN)
        rec_box = SurroundingRectangle(rec, buff=0.3, color=TYPE1_COLOR, stroke_width=3)
        rec_tag = zh("論文式 (5)", font_size=26, color=GREY_A).next_to(rec_box, DOWN, buff=0.2)
        self.say("對所有分配方式求和，再對所有群組型別 ", "$i$", " 求和")
        self.play(Write(rec), run_time=2.2)
        self.play(ShowCreation(rec_box), FadeIn(rec_tag), run_time=0.8)
        self.wait(1.0)
        self.say("這就是 ", "$d(\\vec n)$", " 的遞迴關係（約定 ", "$d(\\vec 0)=1$", "）")
        self.wait(3.0)

        # ------------------------------------------------------------ Step 5：用 Fig. 1 驗算
        self.play(FadeOut(ingredients), FadeOut(rec), FadeOut(rec_box), FadeOut(rec_tag), run_time=0.8)
        task = VGroup(
            zh("驗算：", font_size=34),
            Tex(R"\vec v=(2,\,3)", font_size=44, t2c={"2": TYPE1_COLOR, "3": TYPE2_COLOR}),
            zh("，求", font_size=34),
            Tex(R"d(1,1)", font_size=44),
        ).arrange(RIGHT, buff=0.2).move_to(2.75 * UP)
        self.say("用論文的例子驗算：把 5 種分法依固定點所在的群組分類")
        self.play(FadeIn(task, shift=0.2 * DOWN), run_time=0.8)

        thumb_r = 0.85
        group_a = VGroup(*[make_configuration(5, b, radius=thumb_r, root=0) for b in ROOT_IN_CHORD])
        group_a.arrange(RIGHT, buff=0.4).move_to(3.95 * LEFT + 0.55 * UP)
        group_b = VGroup(*[make_configuration(5, b, radius=thumb_r, root=0) for b in ROOT_IN_TRIANGLE])
        group_b.arrange(RIGHT, buff=0.4).move_to(2.85 * RIGHT + 0.55 * UP)

        label_a = zh("固定點在弦上", font_size=28, color=TYPE1_COLOR).next_to(group_a, UP, buff=0.3)
        label_b = zh("固定點在三角形上", font_size=28, color=TYPE2_COLOR).next_to(group_b, UP, buff=0.3)
        eq_a = Tex(R"\vec r_1+\vec r_2=(0,1)", font_size=34).next_to(group_a, DOWN, buff=0.3)
        eq_b = Tex(R"\vec r_1+\vec r_2+\vec r_3=(1,0)", font_size=34).next_to(group_b, DOWN, buff=0.3)
        num_a = Tex("2", font_size=72, fill_color=TYPE1_COLOR).next_to(eq_a, DOWN, buff=0.3)
        num_b = Tex("3", font_size=72, fill_color=TYPE2_COLOR).next_to(eq_b, DOWN, buff=0.3)
        plus = Tex("+", font_size=72).move_to(
            np.array([(num_a.get_center()[0] + num_b.get_center()[0]) / 2, num_a.get_center()[1], 0]))

        self.play(FadeIn(label_a), LaggedStart(*[FadeIn(t, scale=0.8) for t in group_a], lag_ratio=0.3),
                  run_time=1.2)
        self.play(FadeIn(eq_a), FadeIn(num_a, scale=1.3), run_time=0.8)
        self.say("固定點在弦上：三角形放在 2 段之一，有 2 種")
        self.wait(1.2)
        self.play(FadeIn(label_b), LaggedStart(*[FadeIn(t, scale=0.8) for t in group_b], lag_ratio=0.3),
                  run_time=1.4)
        self.play(FadeIn(eq_b), FadeIn(num_b, scale=1.3), run_time=0.8)
        self.say("固定點在三角形上：弦放在 3 段之一，有 3 種")
        self.wait(1.2)

        total = Tex(R"d(1,1)=2+3=5", font_size=56)
        total.move_to(np.array([-0.4, -2.55, 0]))
        total_box = SurroundingRectangle(total, buff=0.18, color=YELLOW, stroke_width=3)
        self.play(FadeIn(plus), run_time=0.4)
        self.play(Write(total), run_time=1.0)
        self.play(ShowCreation(total_box), run_time=0.6)
        self.say("遞迴算出 5，和 Fig. 1 畫出來的 5 種分法一致")
        self.wait(3.0)
