"""
Scene M03 —— 醉漢走路（MIT 18.212 第 1–2 講）

    醉漢從 0 出發，每步 +1 或 -1（機率各 1/2），走到 -1（懸崖）就掉下去。
    第 2n+1 步第一次掉下去  <=>  前 2n 步是 Dyck 路徑，再往下一步  ->  C_n 條，機率 C_n / 2^(2n+1)
    總和 sum C_n / 2^(2n+1) = (1/2) C(1/4) = (1/2)·2 = 1（M02 的閉式，x = 1/4 時根號為 0）
    部分和 1/2, 5/8, 11/16, ... 慢慢趨近 1；還沒掉下去的機率 = binom(2K,K) / 4^K

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneM03_drunkards_walk.py SceneM03DrunkardsWalk
"""
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, dyck_path_mob
from utils.counting import (binary_trees, catalan, drunkard_fall_prob, drunkard_fall_words,
                            drunkard_partial_sums, dyck_words, is_dyck, tree_to_dyck)
from utils.scene_base import ChuScene
from utils.styles import CROSSING_COLOR, MUTED_COLOR, ROOT_COLOR, mixed, zh

WALK = "UUDUDDD"          # 第 3 節的 Dyck 路徑 UUDUDD，再往下一步
FALL_COLOR = CROSSING_COLOR

# 橫的數線（開場）
HX0, HU, HY = -1.0, 1.5, 0.0
# 時間–位置圖：縱軸是位置（直立的數線），橫軸是時間
VX0, VY0, VU = -5.6, -0.7, 0.62

FRAME_X, FRAME_YLO, FRAME_YHI = 6.8, -3.0, 3.2


def heights(word):
    h, out = 0, [0]
    for c in word:
        h += 1 if c == "U" else -1
        out.append(h)
    return out


def h_pos(p):
    return np.array([HX0 + HU * p, HY, 0.0])


def v_pos(p):
    return np.array([VX0, VY0 + VU * p, 0.0])


def assert_in_frame(mob, name=""):
    l, r = mob.get_left()[0], mob.get_right()[0]
    b, t = mob.get_bottom()[1], mob.get_top()[1]
    assert -FRAME_X <= l and r <= FRAME_X and FRAME_YLO <= b and t <= FRAME_YHI, (name, l, r, b, t)


def number_line(vertical):
    """VGroup(線, 刻度, 數字, 「懸崖」)；橫的與直的結構相同，可以直接 Transform。"""
    pos = v_pos if vertical else h_pos
    along, perp = (UP, RIGHT) if vertical else (RIGHT, UP)
    ext = 0.4 if vertical else 0.75
    line = Line(pos(-1) - ext * along, pos(3) + ext * along, stroke_color=GREY_A, stroke_width=3)
    ticks, labels = VGroup(), VGroup()
    for p in range(-1, 4):
        col = FALL_COLOR if p == -1 else GREY_A
        ticks.add(Line(pos(p) - 0.1 * perp, pos(p) + 0.1 * perp, stroke_color=col, stroke_width=3))
        lab = Tex(str(p), font_size=30, fill_color=FALL_COLOR if p == -1 else WHITE)
        lab.next_to(pos(p), LEFT if vertical else DOWN, buff=0.22)
        labels.add(lab)
    cliff = zh("懸崖", font_size=26, color=FALL_COLOR)
    if vertical:
        cliff.next_to(np.array([VX0 + 7.6 * VU, v_pos(-1)[1], 0.0]), RIGHT, buff=0.15)
    else:
        cliff.next_to(labels[0], DOWN, buff=0.15)
    return VGroup(line, ticks, labels, cliff)


def fall_colors(word):
    return [CATALAN_COLOR] * (len(word) - 1) + [FALL_COLOR]


def fall_thumb(word, unit=0.2):
    """小圖：藍色 Dyck 部分＋紅色最後一步；灰線＝地面 0，紅虛線＝懸崖 -1。"""
    path = dyck_path_mob(word, unit=unit, origin=ORIGIN, colors=fall_colors(word), stroke_width=3.5,
                         dot_radius=0.025, show_dots=False)
    w = len(word) * unit
    ground = Line(ORIGIN, w * RIGHT, stroke_color=GREY_C, stroke_width=1.2)
    cliff = DashedLine(unit * DOWN, unit * DOWN + w * RIGHT, stroke_color=FALL_COLOR, stroke_width=1.5,
                       dash_length=0.05)
    return VGroup(ground, cliff, path)


class SceneM03DrunkardsWalk(ChuScene):
    def construct(self):
        self.show_header("醉漢走路")

        # ------------------------------------------------------------ 數學資料（全部 assert）
        ex_dyck = tree_to_dyck(binary_trees(3)[3])
        assert ex_dyck == "UUDUDD" and WALK == ex_dyck + "D"
        assert is_dyck(WALK[:-1]) and WALK in drunkard_fall_words(3)
        hs = heights(WALK)
        assert min(hs[:-1]) == 0 and hs[-1] == -1 and max(hs) <= 3
        small = {n: drunkard_fall_words(n) for n in range(4)}
        assert small[0] == ["D"] and small[1] == ["UDD"] and small[2] == ["UDUDD", "UUDDD"]
        for n, words in small.items():
            assert words == sorted(d + "D" for d in dyck_words(n)) and len(words) == catalan(n)
        assert [catalan(n) for n in range(4)] == [1, 1, 2, 5]
        probs = [Fraction(catalan(n), 2 ** (2 * n + 1)) for n in range(4)]
        assert probs == [drunkard_fall_prob(n) for n in range(4)]
        assert probs == [Fraction(1, 2), Fraction(1, 8), Fraction(2, 32), Fraction(5, 128)]
        quarter = Fraction(1, 4)
        assert 1 - 4 * quarter == 0 and (1 - 0) / (2 * quarter) == 2 and Fraction(1, 2) * 2 == 1
        NB = 10
        ps = drunkard_partial_sums(NB)
        assert ps[:4] == [Fraction(1, 2), Fraction(5, 8), Fraction(11, 16), Fraction(93, 128)]
        assert all(1 - ps[K - 1] == Fraction(comb(2 * K, K), 4 ** K) for K in range(1, NB + 1))
        rest100 = 1 - drunkard_partial_sums(100)[99]
        assert rest100 == Fraction(comb(200, 100), 4 ** 100)
        pct = f"{float(rest100) * 100:.1f}"
        assert pct == "5.6"

        # ------------------------------------------------------------ 1. 數線上的醉漢
        h_line = number_line(vertical=False)
        drunk = Dot(h_pos(0), radius=0.13, fill_color=ROOT_COLOR).set_z_index(4)
        drunk_lab = zh("醉漢", font_size=26, color=ROOT_COLOR).next_to(drunk, UP, buff=0.2)
        self.play(ShowCreation(h_line[0]), FadeIn(h_line[1]), FadeIn(h_line[2]), run_time=0.9)
        self.play(FadeIn(drunk, scale=1.5), FadeIn(drunk_lab), run_time=0.5)
        self.say("醉漢從 0 出發，每一步往右 ", "$+1$", " 或往左 ", "$-1$", "，機率各 ", "$\\tfrac12$")
        y_arr = HY + 1.05
        arr_r = Arrow(h_pos(0) + y_arr * UP + 0.15 * RIGHT, h_pos(1) + y_arr * UP, buff=0,
                      stroke_color=GREY_A, stroke_width=4)
        arr_l = Arrow(h_pos(0) + y_arr * UP + 0.15 * LEFT, h_pos(-1) + y_arr * UP, buff=0,
                      stroke_color=GREY_A, stroke_width=4)
        lab_r = Tex(r"+1:\ \tfrac12", font_size=30).next_to(arr_r, UP, buff=0.12)
        lab_l = Tex(r"-1:\ \tfrac12", font_size=30).next_to(arr_l, UP, buff=0.12)
        arrows = VGroup(arr_r, arr_l, lab_r, lab_l)
        drunk_lab.generate_target()
        drunk_lab.target.next_to(drunk, DOWN, buff=0.75)
        self.play(MoveToTarget(drunk_lab), GrowArrow(arr_r), GrowArrow(arr_l), FadeIn(lab_r), FadeIn(lab_l),
                  run_time=0.9)
        assert_in_frame(VGroup(h_line, arrows, drunk_lab), "h_line")
        self.wait(1.2)
        self.say("走到 ", "$-1$", " 就掉下懸崖。他最後一定會掉下去嗎？")
        self.play(FadeIn(h_line[3], shift=0.15 * DOWN),
                  Flash(h_pos(-1), color=FALL_COLOR, flash_radius=0.3), run_time=0.8)
        self.wait(1.2)

        # ------------------------------------------------------------ 2. 時間–位置圖
        v_line = number_line(vertical=True)
        graph_w = 7.6 * VU
        ground = Line(v_pos(0), v_pos(0) + graph_w * RIGHT, stroke_color=GREY_C, stroke_width=2)
        cliff_line = DashedLine(v_pos(-1), v_pos(-1) + graph_w * RIGHT, stroke_color=FALL_COLOR,
                                stroke_width=2.5, dash_length=0.12)
        t_axis_lab = zh("時間 →", font_size=22, color=MUTED_COLOR)
        t_axis_lab.next_to(ground.get_end(), UR, buff=0.08)
        p_axis_lab = zh("位置", font_size=22, color=MUTED_COLOR).next_to(v_line[0], UP, buff=0.12)
        self.say("把時間畫成橫軸、位置畫成縱軸：數線立起來")
        self.play(FadeOut(arrows), FadeOut(drunk_lab), run_time=0.4)
        self.play(ReplacementTransform(h_line, v_line), drunk.animate.move_to(v_pos(0)), run_time=1.3)
        self.play(ShowCreation(ground), ShowCreation(cliff_line), FadeIn(t_axis_lab), FadeIn(p_axis_lab),
                  run_time=0.7)

        path = dyck_path_mob(WALK, unit=VU, origin=v_pos(0), colors=fall_colors(WALK), stroke_width=5,
                             dot_radius=0.05)
        letters = VGroup()
        for j, c in enumerate(WALK):
            x = VX0 + (j + 0.5) * VU
            col = FALL_COLOR if j == len(WALK) - 1 else CATALAN_COLOR
            letters.add(Tex(r"\mathrm{" + c + "}", font_size=30, fill_color=col).move_to(np.array([x, -2.2, 0.0])))
        assert_in_frame(VGroup(v_line, ground, cliff_line, t_axis_lab, p_axis_lab, path, letters), "graph")
        self.say("走一次：往上記 U（", "$+1$", "），往下記 D（", "$-1$", "）")
        self.add(path.dots[0])
        for j in range(len(WALK)):
            self.play(ShowCreation(path.steps[j]), FadeIn(path.dots[j + 1], rate_func=squish_rate_func(smooth, 0.75, 1.0)), FadeIn(letters[j], shift=0.1 * UP),
                      drunk.animate.move_to(v_pos(hs[j + 1])), run_time=0.55)
        self.play(drunk.animate.set_fill(FALL_COLOR), Flash(path.vertex(len(WALK)), color=FALL_COLOR,
                                                            flash_radius=0.35), run_time=0.6)
        self.play(drunk.animate.shift(0.9 * DOWN).set_opacity(0), run_time=0.6)
        self.remove(drunk)
        self.say("第 7 步第一次走到 ", "$-1$", "：掉下去了")
        self.wait(0.6)

        # 右邊：拆成 Dyck 路徑＋一步往下
        r0 = VGroup(zh("這次的走法：", font_size=28),
                    Tex(r"\mathrm{UUDUDD}", font_size=38, fill_color=CATALAN_COLOR),
                    Tex(r"+\ \mathrm{D}", font_size=38, fill_color=FALL_COLOR)).arrange(RIGHT, buff=0.15)
        r1 = mixed("藍：一直 ", "$\\ge 0$", "，最後回到 ", "$0$", "：Dyck 路徑", font_size=26, color=CATALAN_COLOR)
        r2 = mixed("紅：最後一步往下，第一次到 ", "$-1$", font_size=26, color=FALL_COLOR)
        right_top = VGroup(r0, r1, r2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        right_top.to_edge(RIGHT, buff=0.4).set_y(2.1)
        self.say("掉下去之前一直 ", "$\\ge 0$", "，而且第 6 步一定在 0：前 6 步正是一條 Dyck 路徑")
        self.play(FadeIn(r0, shift=0.15 * UP), run_time=0.6)
        self.play(FadeIn(r1, shift=0.15 * UP), path.steps[:-1].animate.set_stroke(width=8), run_time=0.6)
        self.play(path.steps[:-1].animate.set_stroke(width=5), run_time=0.3)
        self.play(FadeIn(r2, shift=0.15 * UP), path.steps[-1].animate.set_stroke(width=8), run_time=0.6)
        self.play(path.steps[-1].animate.set_stroke(width=5), run_time=0.3)
        self.wait(0.8)

        g1 = mixed("第 ", "$2n+1$", " 步第一次掉下去", font_size=26)
        g2 = mixed("$\\Longleftrightarrow$", " 前 ", "$2n$", " 步是 Dyck 路徑，再往下一步", font_size=26)
        g3 = mixed("共 ", "$C_n$", " 條，每條機率 ", "$\\left(\\tfrac12\\right)^{2n+1}$", font_size=26,
                   t2c={"C_n": CATALAN_COLOR})
        g4 = mixed("$P$", "（第 ", "$2n+1$", " 步掉下去）", "$=\\dfrac{C_n}{2^{2n+1}}$", font_size=28,
                   t2c={"C_n": CATALAN_COLOR})
        gen = VGroup(g1, g2, g3, g4).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        gen_box = SurroundingRectangle(gen, buff=0.22, color=YELLOW, stroke_width=3)
        gen_all = VGroup(gen_box, gen)
        gen_all.next_to(right_top, DOWN, buff=0.45, aligned_edge=LEFT)
        if gen_all.get_right()[0] > FRAME_X - 0.15:
            gen_all.shift((FRAME_X - 0.15 - gen_all.get_right()[0]) * RIGHT)
        assert_in_frame(VGroup(right_top, gen_all), "right text")
        assert right_top.get_left()[0] > cliff_line.get_end()[0] + 0.9   # 不碰到「懸崖」字
        self.say("一般來說：第 ", "$2n+1$", " 步第一次掉下去的走法有 ", "$C_n$", " 條")
        self.play(LaggedStart(*[FadeIn(g, shift=0.15 * UP) for g in gen[:3]], lag_ratio=0.35), run_time=1.6)
        self.play(FadeIn(g4, shift=0.15 * UP), ShowCreation(gen_box), run_time=0.8)
        self.wait(1.8)

        # ------------------------------------------------------------ 3. 小例子 n = 0..3
        self.clear_stage()
        col_x = [-5.3, -3.55, -1.15, 3.4]
        heads, thumbs, prob_mobs = VGroup(), VGroup(), VGroup()
        for n in range(4):
            words = small[n]
            head = Tex(f"n={n}", font_size=34).move_to(np.array([col_x[n], 2.65, 0.0]))
            tg = VGroup(*[fall_thumb(w, unit=0.2) for w in words])
            if n == 3:
                tg.arrange_in_grid(2, 3, h_buff=0.3, v_buff=0.3)
            else:
                tg.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
            tg.move_to(np.array([col_x[n], 1.35, 0.0]))
            if n < 3:   # n=0,1,2 的地面線對齊
                tg.shift((1.2 - tg[0][0].get_center()[1]) * UP)
            c, d = catalan(n), 2 ** (2 * n + 1)
            pm = Tex(f"\\frac{{{c}}}{{{d}}}", font_size=40).move_to(np.array([col_x[n], -0.05, 0.0]))
            heads.add(head)
            thumbs.add(tg)
            prob_mobs.add(pm)
        y_cnt = min(t.get_bottom()[1] for t in thumbs) - 0.3
        counts = VGroup(*[mixed(f"${catalan(n)}$", " 條", font_size=24, color=MUTED_COLOR)
                          .move_to(np.array([col_x[n], y_cnt, 0.0])) for n in range(4)])
        for n in range(4):
            prob_mobs[n].set_y(y_cnt - 0.75)
        stage3 = VGroup(heads, thumbs, counts, prob_mobs)
        assert_in_frame(stage3, "stage3")
        for a in range(4):
            for b in range(a + 1, 4):
                assert VGroup(thumbs[a], counts[a]).get_right()[0] < VGroup(thumbs[b], counts[b]).get_left()[0] - 0.3
        self.say("小例子：", "$n=0,1,2,3$", " 各有 1, 1, 2, 5 條 —— 正是卡塔蘭數")
        self.play(LaggedStart(*[FadeIn(VGroup(heads[n], thumbs[n], counts[n]), shift=0.15 * UP)
                                for n in range(4)], lag_ratio=0.3), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(p) for p in prob_mobs], lag_ratio=0.2), run_time=0.9)
        self.wait(1.2)

        # 機率相加
        sum_line = mixed("$P$", "（最後掉下去）", "$=$", "$\\frac{1}{2}$", "$+$", "$\\frac{1}{8}$", "$+$",
                         "$\\frac{2}{32}$", "$+$", "$\\frac{5}{128}$", "$+\\cdots$", font_size=30)
        sum_line.move_to(np.array([0.0, 2.6, 0.0]))
        terms = [sum_line[i] for i in (3, 5, 7, 9)]
        others = VGroup(*[sum_line[i] for i in (0, 1, 2, 4, 6, 8, 10)])
        self.say("醉漢最後掉下去的機率：把所有情況加起來")
        self.play(FadeOut(VGroup(heads, thumbs, counts)), run_time=0.5)
        self.play(*[ReplacementTransform(prob_mobs[n], terms[n]) for n in range(4)], FadeIn(others),
                  run_time=1.2)
        eq_x = sum_line[2].get_left()[0]
        line2 = Tex(r"=\sum_{n\ge 0}\frac{C_n}{2^{2n+1}}=\frac12\sum_{n\ge 0}C_n\Big(\frac14\Big)^{n}"
                    r"=\frac12\,C\Big(\frac14\Big)", font_size=40, t2c={"C_n": CATALAN_COLOR})
        line2.next_to(sum_line, DOWN, buff=0.3)
        line2.shift((eq_x - line2.get_left()[0]) * RIGHT)
        VGroup(sum_line, line2).set_x(0)   # 兩行一起置中
        self.play(FadeIn(line2, shift=0.15 * DOWN), run_time=0.9)
        self.wait(1.2)
        line3 = mixed("上一幕的閉式：", "$C(x)=\\dfrac{1-\\sqrt{1-4x}}{2x}$", font_size=28)
        line4 = mixed("$x=\\tfrac14$", " 時根號是 ", "$\\sqrt{1-1}=0$", "，所以 ",
                      "$C\\big(\\tfrac14\\big)=\\dfrac{1-0}{2\\cdot\\frac14}=2$", font_size=28)
        lines34 = VGroup(line3, line4).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        lines34.next_to(line2, DOWN, buff=0.35).set_x(0)
        self.say("用上一幕的閉式：", "$x=\\tfrac14$", " 時根號正好是 ", "$0$")
        self.play(FadeIn(line3, shift=0.15 * DOWN), run_time=0.8)
        self.play(FadeIn(line4, shift=0.15 * DOWN), run_time=0.8)
        self.wait(1.2)
        final = mixed("$P$", "（最後掉下去）", "$=\\tfrac12\\cdot 2=1$", font_size=32)
        final_box = SurroundingRectangle(final, buff=0.2, color=YELLOW, stroke_width=3)
        fin = VGroup(final_box, final)
        # 註：x=1/4 在收斂半徑的邊界上（C_n/4^n ~ n^(-3/2)/sqrt(pi)，級數收斂；Abel 定理）
        abel = VGroup(mixed("註：", "$x=\\tfrac14$", " 在收斂半徑的邊界上，", font_size=20, color=MUTED_COLOR),
                      mixed("但級數 ", "$\\sum C_n/4^n$", " 仍收斂，可以直接代入（Abel 定理）",
                            font_size=20, color=MUTED_COLOR)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        VGroup(fin, abel).arrange(RIGHT, buff=0.6).next_to(lines34, DOWN, buff=0.3).set_x(0)
        assert_in_frame(VGroup(sum_line, line2, lines34, fin, abel), "sum")
        self.say("醉漢一定會掉下懸崖：機率是 ", "$1$")
        self.play(FadeIn(final), ShowCreation(final_box), run_time=0.8)
        self.play(FadeIn(abel), run_time=0.5)
        self.wait(2.0)

        # ------------------------------------------------------------ 4. 部分和慢慢趨近 1
        self.clear_stage()
        base_y, one_y = -2.3, 1.85
        scale = one_y - base_y
        bx0, bdx, bw = -5.5, 0.68, 0.44
        x_end = bx0 + (NB - 1) * bdx + 0.5
        axis = Line(np.array([bx0 - 0.5, base_y, 0]), np.array([x_end, base_y, 0]),
                    stroke_color=GREY_A, stroke_width=2.5)
        one_line = DashedLine(np.array([bx0 - 0.5, one_y, 0]), np.array([x_end, one_y, 0]),
                              stroke_color=YELLOW, stroke_width=2.5, dash_length=0.12)
        one_lab = Tex("1", font_size=32, fill_color=YELLOW).next_to(one_line, LEFT, buff=0.15)
        zero_lab = Tex("0", font_size=28).next_to(axis, LEFT, buff=0.15)
        bars, t_labs, f_labs = VGroup(), VGroup(), VGroup()
        for K, s in enumerate(ps, 1):
            h = float(s) * scale
            bar = Rectangle(width=bw, height=h, fill_color=CATALAN_COLOR, fill_opacity=0.65,
                            stroke_color=CATALAN_COLOR, stroke_width=1.5)
            bar.move_to(np.array([bx0 + (K - 1) * bdx, base_y + h / 2, 0.0]))
            bars.add(bar)
            t_labs.add(Tex(str(2 * K - 1), font_size=24, fill_color=GREY_A).next_to(bar, DOWN, buff=0.12))
            if K <= 4:
                f_labs.add(Tex(f"\\frac{{{s.numerator}}}{{{s.denominator}}}", font_size=26)
                           .next_to(bar, UP, buff=0.1))
        step_lab = mixed("步數 ", "$t$", font_size=20, color=MUTED_COLOR).next_to(t_labs[-1], RIGHT, buff=0.3)
        chart_title = mixed("前 ", "$t$", " 步之內掉下去的機率", font_size=26)
        chart_title.move_to(np.array([(bx0 + x_end) / 2 - 0.25, 2.55, 0.0]))
        chart = VGroup(axis, one_line, one_lab, zero_lab, bars, t_labs, f_labs, step_lab, chart_title)
        self.say("把前幾項加起來：", "$\\tfrac12,\\ \\tfrac58,\\ \\tfrac{11}{16},\\ \\tfrac{93}{128},\\ \\dots$")
        self.play(ShowCreation(axis), ShowCreation(one_line), FadeIn(one_lab), FadeIn(zero_lab),
                  FadeIn(chart_title), FadeIn(step_lab), run_time=0.8)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(t) for t in t_labs], lag_ratio=0.15), run_time=2.2)
        self.play(LaggedStart(*[FadeIn(f, shift=0.1 * DOWN) for f in f_labs], lag_ratio=0.2), run_time=0.9)
        self.wait(1.0)

        n0 = mixed("還沒掉下去的機率", font_size=26)
        n1 = mixed("前 ", "$2K-1$", " 步都沒掉：", "$\\binom{2K}{K}\\big/4^K$", font_size=26)
        n2 = mixed("前 ", "$199$", " 步都沒掉：約 ", f"${pct}\\%$", font_size=26)
        n3 = zh("會趨近 0，但非常慢", font_size=26, color=YELLOW)
        notes = VGroup(n0, n1, n2, n3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        notes.next_to(np.array([x_end, 0.0, 0.0]), RIGHT, buff=0.55)
        assert_in_frame(VGroup(chart, notes), "chart")
        assert notes.get_left()[0] > x_end + 0.3
        self.say("還沒掉下去的機率一直變小，只是很慢")
        self.play(FadeIn(n0, shift=0.15 * UP), FadeIn(n1, shift=0.15 * UP), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(n2, shift=0.15 * UP), run_time=0.6)
        self.play(FadeIn(n3, shift=0.15 * UP), run_time=0.6)
        self.wait(1.2)
        self.say("所以醉漢最後一定會掉下去（機率 ", "$1$", "），只是可能要走很久")
        self.wait(2.0)
