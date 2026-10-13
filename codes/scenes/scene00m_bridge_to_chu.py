"""
Scene 00m —— 從卡塔蘭數到 Chu 的推廣（卡塔蘭基礎模組的最後一幕）

    卡塔蘭：圓上的點分成「2 點群組」、互不交叉（n_1 = 3, v_1 = 2）
    如果一組可以有 3 個點？-> 一條弦換成三角形：n = (2,1), v = (2,3), N = 7（正好是 Chu 第 3 段的例子）
    不同大小同時出現 -> 向量 n、v，總點數 N = sum n_i v_i
    生成函數：根切出 2 塊 -> x C^2；根切出 v_i 塊 -> x_i D^{v_i}
        C = 1 + x C^2   ==>   D = 1 + x_1 D^{v_1} + ... + x_k D^{v_k}

接下來接 Chu 的部分（Scene03GeneralizedSetup）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00m_bridge_to_chu.py Scene00mBridgeToChu
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, LEFT_COLOR, RIGHT_COLOR
from utils.circle_points import circle_coords, make_circle_points
from utils.counting import closed_form, is_noncrossing
from utils.formulas import GF_T2C
from utils.polygon_groups import circular_segment, make_block, make_configuration
from utils.root_figure import RootFigure
from utils.scene_base import ChuScene
from utils.styles import (
    D_COLOR,
    MUTED_COLOR,
    REGION_COLORS,
    ROOT_COLOR,
    TYPE1_COLOR,
    TYPE2_COLOR,
    TYPE3_COLOR,
    YELLOW,
    mixed,
    zh,
)

CENTER = np.array([-4.0, 0.4, 0.0])
RADIUS = 1.75
SIX = [(0, 5), (1, 2), (3, 4)]                 # 6 點的一種不交叉配對
OLD_TO_NEW = [0, 1, 2, 3, 5, 6]                # 在第 3、4 點之間插入新的一點（新的第 4 點）
SEVEN = [(0, 6), (1, 2), (3, 4, 5)]            # 2 條弦 + 1 個三角形：n = (2,1), v = (2,3)
NINE = [(0, 1), (2, 3, 4), (5, 6, 7, 8)]       # 弦 + 三角形 + 四邊形：n = (1,1,1), v = (2,3,4)


def block_dots_colors(dots, blocks, colors):
    anims = []
    for b, c in zip(blocks, colors):
        for i in b:
            anims.append(dots[i].animate.set_fill(c))
    return anims


class Scene00mBridgeToChu(ChuScene):
    def construct(self):
        self.show_header("從卡塔蘭數到 Chu 的推廣")
        assert is_noncrossing(SIX) and is_noncrossing(SEVEN) and is_noncrossing(NINE)
        assert closed_form((2, 1), (2, 3)) == 21 and closed_form((1, 1, 1), (2, 3, 4)) == 72

        # ------------------------------------------------------------ 每一組都是 2 個點
        circle, dots, coords = make_circle_points(6, radius=RADIUS, center=CENTER)
        chords = VGroup(*[make_block(b, coords, color=TYPE1_COLOR) for b in SIX])
        self.play(ShowCreation(circle), FadeIn(dots), run_time=0.8)
        self.play(LaggedStart(*[ShowCreation(c) for c in chords], lag_ratio=0.3),
                  *block_dots_colors(dots, SIX, [TYPE1_COLOR] * 3), run_time=1.2)
        self.say("回到 6 個點的不交叉配對（", "$C_3=5$", " 種中的一種）")
        self.wait(0.8)

        one = chords[1]
        tag = zh("一組 ＝ 2 個點", font_size=26, color=TYPE1_COLOR).next_to(circle, RIGHT, buff=0.5).shift(0.9 * UP)
        self.say("每一條弦把 2 個點綁成一組：群組的大小是 2")
        self.play(Indicate(one, scale_factor=1.15, color=YELLOW), FadeIn(tag, shift=0.2 * LEFT), run_time=1.0)
        self.wait(0.6)
        count = mixed("3 組，每組 2 個點：", "$n_1=3,\\ v_1=2$", font_size=28, t2c={"n_1": TYPE1_COLOR, "v_1": TYPE1_COLOR})
        count.next_to(tag, DOWN, buff=0.4).align_to(tag, LEFT)
        self.play(LaggedStart(*[Indicate(c, scale_factor=1.1, color=TYPE1_COLOR) for c in chords], lag_ratio=0.25),
                  FadeIn(count, shift=0.2 * UP), run_time=1.4)
        self.say("卡塔蘭數數的，就是「全部都是 2 點群組」的不交叉分組")
        self.wait(1.5)

        # ------------------------------------------------------------ 一組可以有 3 個點嗎？
        question = zh("如果一組可以有 3 個點？", font_size=34, color=YELLOW).move_to(np.array([2.6, 2.4, 0.0]))
        self.play(FadeIn(question, shift=0.2 * DOWN), FadeOut(tag), FadeOut(count), run_time=0.8)
        new_coords = circle_coords(7, RADIUS, CENTER)
        new_dot = Dot(new_coords[4], radius=dots[0].get_width() / 2, fill_color=TYPE2_COLOR).set_z_index(2)
        targets = [make_block(b, new_coords, color=TYPE1_COLOR) for b in SEVEN[:2]]
        triangle = make_block(SEVEN[2], new_coords, color=TYPE2_COLOR)
        self.say("在兩個點之間多放一個點，把這條弦換成三角形")
        self.play(
            *[dots[i].animate.move_to(new_coords[OLD_TO_NEW[i]]) for i in range(6)],
            Transform(chords[0], targets[0]), Transform(chords[1], targets[1]),
            chords[2].animate.put_start_and_end_on(new_coords[3], new_coords[5]),
            run_time=1.2,
        )
        self.play(GrowFromCenter(new_dot), run_time=0.5)
        self.play(ReplacementTransform(chords[2], triangle),
                  dots[3].animate.set_fill(TYPE2_COLOR), dots[4].animate.set_fill(TYPE2_COLOR), run_time=1.0)
        seven_text = VGroup(
            mixed("2 條弦（2 點群組）＋ 1 個三角形（3 點群組）", font_size=24),
            Tex(R"\vec v=(2,3),\qquad \vec n=(2,1)", font_size=40, t2c={"2,3": WHITE}),
            Tex(R"N=2\times 2+1\times 3=7", font_size=40),
        ).arrange(DOWN, buff=0.28)
        seven_text.move_to(np.array([2.6, 0.6, 0.0]))
        self.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in seven_text], lag_ratio=0.4), run_time=1.6)
        self.say("一樣要求不交叉：這樣的分法有幾種？（Chu 的公式給出 21 種）")
        self.wait(2.0)

        # ------------------------------------------------------------ 不同大小同時出現
        nine = make_configuration(9, NINE, radius=1.15, center=np.array([5.2, -1.55, 0.0]))
        nine_text = VGroup(
            Tex(R"\vec v=(2,3,4)", font_size=32),
            Tex(R"\vec n=(1,1,1)", font_size=32),
            Tex(R"N=9", font_size=32),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        nine_text.next_to(nine, LEFT, buff=0.35)
        self.say("還可以讓好幾種大小同時出現：弦、三角形、四邊形……")
        self.play(seven_text.animate.scale(0.85).move_to(np.array([2.6, 1.25, 0.0])), run_time=0.6)
        self.play(FadeIn(nine, scale=0.8), FadeIn(nine_text), run_time=1.0)
        self.wait(1.2)

        general = VGroup(
            mixed("$\\vec v=(v_1,\\ldots,v_k)$", "：各型群組的點數", font_size=22),
            mixed("$\\vec n=(n_1,\\ldots,n_k)$", "：各型群組的個數", font_size=22),
            mixed("$N=n_1v_1+\\cdots+n_kv_k$", "：圓周上的總點數", font_size=22),
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        general_box = SurroundingRectangle(general, buff=0.16, color=YELLOW, stroke_width=2.5)
        VGroup(general, general_box).move_to(np.array([-3.9, -2.4, 0.0]))
        assert general_box.get_top()[1] < CENTER[1] - RADIUS - 0.2
        self.say("一般的情形用兩個向量描述：每一型群組有幾個點、要幾個")
        self.play(FadeIn(general), ShowCreation(general_box), run_time=1.0)
        self.wait(2.2)

        # ------------------------------------------------------------ 生成函數：2 塊 -> v_i 塊
        self.clear_stage()
        # 左：普通卡塔蘭（根是一條弦，切成 2 塊）
        lc = np.array([-3.7, 1.15, 0.0])
        lr = 1.15
        ref = circle_coords(12, lr, lc)
        l_circle = Circle(radius=lr, stroke_color=GREY_C, stroke_width=2.5).move_to(lc)
        l_regions = VGroup(circular_segment(0, 6, 12, lr, lc, color=LEFT_COLOR, opacity=0.32),
                           circular_segment(6, 0, 12, lr, lc, color=RIGHT_COLOR, opacity=0.32))
        l_chord = Line(ref[0], ref[6], stroke_color=ROOT_COLOR, stroke_width=6)
        l_fixed = Dot(ref[0], radius=0.1, fill_color=ROOT_COLOR).set_z_index(3)
        l_c = VGroup(Tex("C", font_size=40, fill_color=LEFT_COLOR).move_to(lc + 0.6 * RIGHT),
                     Tex("C", font_size=40, fill_color=RIGHT_COLOR).move_to(lc + 0.6 * LEFT))
        left_pic = VGroup(l_regions, l_circle, l_chord, l_fixed, l_c)
        left_cap = mixed("根是 2 點群組 ", "$\\Rightarrow$", " 切成 2 塊 ", "$\\Rightarrow$", " ",
                         "$xC^2$", font_size=24, t2c={"x": ROOT_COLOR, "C": D_COLOR})
        left_cap.next_to(l_circle, DOWN, buff=0.3)

        # 右：Chu（根是三角形，切成 3 塊）
        rc = np.array([2.4, 1.15, 0.0])
        fig = RootFigure(center=rc, radius=1.15, label_font_size=30, with_subs=False, label_buff=0.3)
        d_labels = VGroup(*[Tex("D", font_size=40, fill_color=REGION_COLORS[j]).move_to(lab)
                            for j, lab in enumerate(fig.region_labels)])
        right_pic = VGroup(fig.regions, fig.config, d_labels)
        right_cap = mixed("根是 3 點群組 ", "$\\Rightarrow$", " 切成 3 塊 ", "$\\Rightarrow$", " ",
                          "$x_2D^3$", font_size=24, t2c={"x_2": TYPE2_COLOR, "D": D_COLOR})
        right_cap.next_to(fig.config.circle, DOWN, buff=0.45)

        self.say("普通卡塔蘭：根是一組 2 個點，把其餘的點切成 2 塊，所以是 ", "$xC^2$")
        self.play(FadeIn(left_pic), run_time=1.0)
        self.play(FadeIn(left_cap, shift=0.2 * UP), run_time=0.7)
        self.wait(1.0)
        self.say("如果根是一組 3 個點，就切成 3 塊：", "$x_2D^3$", "（", "$x_2$", " 記一個三角形）")
        self.play(FadeIn(right_pic), run_time=1.0)
        self.play(FadeIn(right_cap, shift=0.2 * UP), run_time=0.7)
        self.wait(1.4)

        c_eq = Tex("C=1+xC^2", font_size=46, t2c={"x": ROOT_COLOR, "C": D_COLOR})
        arrow = Tex(R"\Longrightarrow", font_size=46)
        d_eq = Tex(R"D=1+x_1D^{v_1}+x_2D^{v_2}+\cdots+x_kD^{v_k}", font_size=46, t2c={"D": D_COLOR, **GF_T2C})
        eqs = VGroup(c_eq, arrow, d_eq).arrange(RIGHT, buff=0.45).move_to(1.45 * DOWN)
        c_lab = zh("普通卡塔蘭（只有 2 點群組）", font_size=22, color=MUTED_COLOR).next_to(c_eq, DOWN, buff=0.22)
        d_lab = zh("Chu 的推廣（第 5–7 段會推導）", font_size=22, color=MUTED_COLOR).next_to(d_eq, DOWN, buff=0.22)
        self.say("每一型群組各記一個變數 ", "$x_i$", "：普通卡塔蘭的方程，自然推廣成 Chu 的方程")
        self.play(Write(c_eq), FadeIn(c_lab), run_time=1.0)
        self.play(GrowFromCenter(arrow), run_time=0.5)
        self.play(Write(d_eq), FadeIn(d_lab), run_time=1.6)
        self.wait(2.2)

        # ------------------------------------------------------------ 結論
        self.clear_stage()
        top = VGroup(zh("卡塔蘭數", font_size=32, color=CATALAN_COLOR),
                     zh("＝ 不交叉的「2 點群組」分法", font_size=32)).arrange(RIGHT, buff=0.2)
        bottom = VGroup(zh("Chu 的廣義卡塔蘭數", font_size=32, color=YELLOW),
                        zh("＝ 指定大小的不交叉群組分法", font_size=32)).arrange(RIGHT, buff=0.2)
        down = Tex(R"\Downarrow", font_size=56)
        stack = VGroup(top, down, bottom).arrange(DOWN, buff=0.4).move_to(0.4 * UP)
        box = SurroundingRectangle(bottom, buff=0.2, color=YELLOW, stroke_width=3)
        self.play(FadeIn(top, shift=0.2 * DOWN), run_time=0.8)
        self.play(FadeIn(down), run_time=0.4)
        self.play(FadeIn(bottom, shift=0.2 * UP), ShowCreation(box), run_time=1.0)
        self.say("接下來：Chu（1987）的定理與證明")
        self.wait(3.0)
