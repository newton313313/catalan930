"""
Scene 08 —— 為什麼公式是對的：完整證明 Raney 公式（論文式 (9)），再推出 D = C

論文第 93 頁「反覆使用 Raney 公式」證明 C 也滿足式 (6)。這一幕把 Raney 公式本身也證完：

    第 0 段  路線圖
    第 1 段  定義 A_t(n)，寫出 Raney 公式
    第 2 段  路徑與「好路徑」
    第 3 段  循環引理：每條路徑恰有 t 種讀法是好路徑（附證明）
    第 4 段  數一數：好路徑的數目 = A_t(n)
    第 5 段  好路徑切成兩段 => Raney 公式
    第 6 段  由 Raney 公式得到 [x^n] C^t，再推出論文式 (10)
    第 7 段  D = C，定理得證

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene08_formula_verification.py Scene08FormulaVerification
只看 Raney 公式的證明（第 1–5 段）：
    manimgl scenes/scene08_formula_verification.py Scene08RaneyProof
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import (
    LEAF,
    closed_form,
    cut_index,
    good_paths,
    good_rotations,
    multinomial_vec,
    path_heights,
    path_words,
    raney_A,
    rotate,
    step_weight,
    sub_vectors,
)
from utils.formulas import general_formula
from utils.lattice_paths import (
    UP_STEP_COLOR,
    PathMob,
    letter_color,
    level_line,
    path_thumbnail,
    word_tiles,
)
from utils.scene_base import ChuScene
from utils.styles import (
    CROSSING_COLOR,
    D_COLOR,
    HIGHLIGHT_COLOR,
    OK_COLOR,
    TYPE1_COLOR,
    TYPE2_COLOR,
    mixed,
    zh,
)

C_COLOR = PINK          # 公式那一邊的生成函數 C
LIGHT_COLOR = HIGHLIGHT_COLOR
CUT_COLOR = HIGHLIGHT_COLOR

N_EX = (1, 1)
V_EX = (2, 3)
CH, TR = 1, 2           # 弦型步、三角形型步（第 1、2 型）
L = LEAF                # ↑ 步

GOOD_EX = (L, L, L, TR, L, CH)          # t=1 的好路徑：高度 1,2,3,1,2,1
BAD_EX = (L, CH, L, L, TR, L)           # t=1 的壞路徑：第 2 點高度 0
ROT_WORD = (L, TR, L, L, CH, L, L)      # t=2：從第 2、5 點讀起才是好路徑
ROT_GOOD = (2, 5)
CUT_WORD = (L, L, CH, L, L, L, TR)      # 終點高度 2 的好路徑，在第 3 點切開
CUT_S = 1


def check(color=OK_COLOR, scale=0.8):
    return Checkmark().set_fill(color).scale(scale)


def cross(color=CROSSING_COLOR, scale=0.8):
    return Exmark().set_fill(color).scale(scale)


class Scene08FormulaVerification(ChuScene):
    def construct(self):
        self.show_header("為什麼公式是對的")
        self.part0_roadmap()
        self.part1_statement()
        self.part2_paths()
        self.part3_cycle_lemma()
        self.part4_counting()
        self.part5_cut()
        self.part6_finish()
        self.part7_conclusion()

    # ================================================================== 共用
    def clear_stage(self, run_time: float = 0.7):
        """淡出標題以外的所有東西。"""
        mobs = [m for m in self.mobjects if m is not self.frame and m is not self.header_mob]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
        self.caption_mob = None

    def sanity_checks(self):
        assert raney_A(1, N_EX, V_EX) == closed_form(N_EX, V_EX) == 5
        assert path_heights(GOOD_EX, V_EX) == [0, 1, 2, 3, 1, 2, 1]
        assert path_heights(BAD_EX, V_EX)[2] == 0
        assert tuple(good_rotations(ROT_WORD, V_EX)) == ROT_GOOD
        assert cut_index(CUT_WORD, CUT_S, V_EX) == 3
        assert len(path_words(1, N_EX, V_EX)) == 30
        assert len(path_words(2, N_EX, V_EX)) == 42
        assert len(good_paths(1, N_EX, V_EX)) == 5
        assert len(good_paths(2, N_EX, V_EX)) == raney_A(2, N_EX, V_EX) == 12

    # ================================================================== 第 0 段：路線圖
    def part0_roadmap(self):
        self.sanity_checks()
        c_def = Tex(R"C(\vec X)=\sum_{\vec n} C_{\vec v}(\vec n)\,x_1^{n_1}x_2^{n_2}\cdots x_k^{n_k}",
                    font_size=50)
        c_def[0].set_fill(C_COLOR)
        c_def.move_to(2.45 * UP)
        self.play(Write(c_def), run_time=1.6)
        self.say("把公式給的數 ", "$C_{\\vec v}(\\vec n)$", " 收進一個生成函數 ", "$C$",
                 t2c={"C": C_COLOR})
        self.wait(1.0)

        goal_tag = zh("目標：", font_size=34, color=YELLOW)
        goal = Tex(R"C=1+\sum_{i=1}^{k} x_i\,C^{v_i}", font_size=56, t2c={"C": C_COLOR})
        goal_row = VGroup(goal_tag, goal).arrange(RIGHT, buff=0.3).move_to(1.25 * UP)
        self.play(FadeIn(goal_row, shift=0.2 * UP), run_time=0.8)
        self.say("只要證明 ", "$C$", " 也滿足上一幕那條方程就夠了", t2c={"C": C_COLOR})
        self.wait(1.5)

        rows = VGroup(
            mixed("1.  把公式裡的數，解釋成「好路徑」的個數（循環引理）", font_size=28),
            mixed("2.  好路徑可以切成兩段 ", "$\\Rightarrow$", " Raney 公式（論文式 (9)）", font_size=28),
            mixed("3.  由 Raney 公式算出 ", "$C^t$", " 的係數", font_size=28, t2c={"C": C_COLOR}),
            mixed("4.  取 ", "$t=v_i$", " 加總（論文式 (10)）", "$\\Rightarrow$", " ", "$C$",
                  " 滿足方程 ", "$\\Rightarrow$", " ", "$D=C$", font_size=28,
                  t2c={"C": C_COLOR, "D": D_COLOR}),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        rows.move_to(1.1 * DOWN)
        self.say("證明的路線：前兩步就是 Raney 公式的完整證明")
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in rows], lag_ratio=0.35),
                  run_time=2.4)
        brace = Brace(rows[:2], LEFT, buff=0.15)
        brace_tag = zh("Raney 公式", font_size=24, color=YELLOW).next_to(brace, LEFT, buff=0.1)
        self.play(GrowFromCenter(brace), FadeIn(brace_tag), run_time=0.8)
        self.wait(3.0)
        self.clear_stage()

    # ================================================================== 第 1 段：A_t 與 Raney 公式
    def part1_statement(self):
        a_def = Tex(R"A_t(\vec n)=\frac{t}{N+t}\binom{N+t}{\vec n},\qquad N=\langle\vec n,\vec v\rangle",
                    font_size=54)
        a_def.move_to(2.45 * UP)
        binom_note = Tex(R"\binom{M}{\vec n}=\frac{M!}{n_1!\cdots n_k!\,(M-n_1-\cdots-n_k)!}",
                         font_size=36, fill_color=GREY_A)
        binom_note.next_to(a_def, DOWN, buff=0.3)
        self.say("對每個正整數 ", "$t$", "，定義一個數 ", "$A_t(\\vec n)$")
        self.play(Write(a_def), run_time=1.6)
        self.play(FadeIn(binom_note, shift=0.2 * UP), run_time=0.7)
        self.wait(1.2)

        a_one = Tex(R"A_1(\vec n)=\frac{1}{N+1}\binom{N+1}{\vec n}=C_{\vec v}(\vec n)", font_size=46)
        a_one.next_to(binom_note, DOWN, buff=0.35)
        self.say("$t=1$", " 時，", "$A_1$", " 就是廣義卡塔蘭數")
        self.play(FadeIn(a_one, shift=0.2 * UP), run_time=0.9)
        self.wait(1.5)

        raney = Tex(R"A_{s+t}(\vec n)=\sum_{\vec r}A_s(\vec r)\,A_t(\vec n-\vec r)", font_size=58)
        self.play(FadeOut(binom_note), a_one.animate.move_to(binom_note.get_center() + 0.15 * DOWN),
                  run_time=0.7)
        raney.move_to(1.3 * DOWN)
        box = SurroundingRectangle(raney, buff=0.25, color=YELLOW, stroke_width=3)
        tag = zh("Raney 公式（論文式 (9)）", font_size=26, color=YELLOW).next_to(box, DOWN, buff=0.12)
        tag.align_to(box, RIGHT)
        self.say("Raney 公式：對任意正整數 ", "$s$", "、", "$t$", " 都成立")
        self.play(Write(raney), run_time=1.6)
        self.play(ShowCreation(box), FadeIn(tag), run_time=0.7)
        self.wait(1.5)
        self.say("要證明它，先替 ", "$A_t(\\vec n)$", " 找一個「數得出來」的意義")
        self.wait(2.0)
        self.clear_stage()

    # ================================================================== 第 2 段：路徑
    def part2_paths(self):
        u = 0.5
        title = zh("路徑：一串往上或往下的步", font_size=32).move_to(3.05 * UP)
        self.play(FadeIn(title), run_time=0.5)

        # --- 三種步
        legend = VGroup()
        specs = [
            (L, "↑ 步", "高度 +1", UP_STEP_COLOR),
            (CH, "弦型步（第 1 型）", "高度 −1", TYPE1_COLOR),
            (TR, "三角形型步（第 2 型）", "高度 −2", TYPE2_COLOR),
        ]
        for letter, name, change, color in specs:
            w = step_weight(letter, V_EX)
            p0 = ORIGIN
            p1 = u * (RIGHT + w * UP)
            seg = Line(p0, p1, stroke_color=color, stroke_width=6)
            ends = VGroup(Dot(p0, radius=0.06), Dot(p1, radius=0.06))
            picture = VGroup(seg, ends)
            tile = word_tiles((letter,), V_EX, size=0.5)
            label = VGroup(zh(name, font_size=26, color=color), zh(change, font_size=24, color=GREY_A))
            label.arrange(DOWN, buff=0.12)
            item = VGroup(picture, tile, label).arrange(RIGHT, buff=0.35)
            legend.add(item)
        legend.arrange(RIGHT, buff=0.75).move_to(1.95 * UP)
        self.say("每一步往右走一格，同時改變高度")
        self.play(LaggedStart(*[FadeIn(item, shift=0.2 * DOWN) for item in legend], lag_ratio=0.4),
                  run_time=1.8)
        general = mixed("一般：第 ", "$i$", " 型步讓高度改變 ", "$1-v_i$", "（", "$v_i$",
                        " 點群組 ", "$\\to$", " 往下 ", "$v_i-1$", " 格）", font_size=28)
        general.next_to(legend, DOWN, buff=0.45)
        self.play(FadeIn(general, shift=0.2 * UP), run_time=0.8)
        self.wait(1.5)

        # --- 用哪些步
        recipe = VGroup(
            mixed("用 ", "$n_i$", " 個第 ", "$i$", " 型步，再加上 ",
                  "$\\ell=t+\\sum_i n_i(v_i-1)$", " 個 ↑ 步", font_size=30),
            mixed("總步數 ", "$n_1+\\cdots+n_k+\\ell=N+t$", "，終點高度剛好是 ", "$t$", font_size=30),
            mixed("排列方式共有 ", "$\\binom{N+t}{\\vec n}$", " 種", font_size=30),
        ).arrange(DOWN, buff=0.4)
        recipe.move_to(0.95 * DOWN)
        self.say("路徑由 ", "$\\vec n$", " 和 ", "$t$", " 決定要用哪些步")
        for row in recipe:
            self.play(FadeIn(row, shift=0.2 * UP), run_time=0.8)
            self.wait(0.8)
        self.wait(1.2)
        self.play(FadeOut(recipe), FadeOut(general), run_time=0.6)

        # --- 例子
        example = VGroup(
            Tex(R"t=1,\ \ \vec n=(1,1),\ \ \vec v=(2,3)", font_size=40),
            mixed("1 個弦型步、1 個三角形型步、", "$\\ell=1+1+2=4$", " 個 ↑ 步，排法 ",
                  "$\\frac{6!}{1!\\,1!\\,4!}=30$", " 種", font_size=26),
        ).arrange(DOWN, buff=0.25).move_to(0.75 * UP)
        self.play(FadeOut(legend), FadeIn(example, shift=0.2 * UP), run_time=0.9)
        self.say("例子：用 6 步，終點高度 1")
        self.wait(1.5)

        good = PathMob(GOOD_EX, V_EX, unit=u, origin=np.array([-5.6, -2.3, 0]))
        bad = PathMob(BAD_EX, V_EX, unit=u, origin=np.array([1.4, -2.3, 0]))
        good_tiles = word_tiles(GOOD_EX, V_EX, size=0.42, font_size=22)
        bad_tiles = word_tiles(BAD_EX, V_EX, size=0.42, font_size=22)
        good_tiles.move_to(np.array([good.x_of(3), -0.45, 0]))
        bad_tiles.move_to(np.array([bad.x_of(3), -0.45, 0]))
        good_base = level_line(good, 0, -0.3, 6.3)
        bad_base = level_line(bad, 0, -0.3, 6.3)
        zero_tag = Tex("0", font_size=26, fill_color=GREY_B).next_to(good_base, LEFT, buff=0.1)
        zero_tag2 = Tex("0", font_size=26, fill_color=GREY_B).next_to(bad_base, LEFT, buff=0.1)

        self.play(FadeOut(example[1]), example[0].animate.move_to(1.3 * UP), run_time=0.6)
        self.play(FadeIn(good_tiles), ShowCreation(good_base), FadeIn(zero_tag), FadeIn(good.dots[0]),
                  run_time=0.6)
        for j in range(len(GOOD_EX)):
            self.play(Indicate(good_tiles[j], scale_factor=1.25, color=letter_color(GOOD_EX[j], V_EX)),
                      ShowCreation(good.steps[j]), FadeIn(good.dots[j + 1]), run_time=0.45)
        self.wait(0.4)

        good_def = mixed("好路徑：出發之後，每一點的高度都 ", "$>0$", font_size=30, color=YELLOW)
        good_def.move_to(2.25 * UP)
        self.say("好路徑：出發之後，路徑一直留在高度 0 的線上方")
        self.play(FadeIn(good_def, shift=0.2 * DOWN), run_time=0.8)
        ok = check().next_to(good, RIGHT, buff=0.4)
        self.play(LaggedStart(*[Indicate(d, scale_factor=2.0, color=OK_COLOR) for d in good.dots[1:]],
                              lag_ratio=0.15),
                  FadeIn(ok, scale=1.5), run_time=1.6)
        self.wait(0.8)

        self.say("換一種排法：第 2 步就回到了高度 0，不是好路徑")
        self.play(FadeIn(bad_tiles), ShowCreation(bad_base), FadeIn(zero_tag2), run_time=0.6)
        self.play(ShowCreation(bad.steps), FadeIn(bad.dots), run_time=1.5)
        bad_dot = Dot(bad.vertex(2), radius=0.11, fill_color=CROSSING_COLOR).set_z_index(3)
        no = cross().next_to(bad, RIGHT, buff=0.4)
        self.play(FadeIn(bad_dot, scale=2), Flash(bad.vertex(2), color=CROSSING_COLOR, flash_radius=0.3),
                  FadeIn(no, scale=1.5), run_time=0.9)
        self.wait(1.2)

        g_def = mixed("記 ", "$G_t(\\vec n)$", " ＝ 好路徑的數目。要證明：", "$G_t(\\vec n)=A_t(\\vec n)$",
                      font_size=30)
        g_box = SurroundingRectangle(g_def, buff=0.18, color=YELLOW, stroke_width=2.5)
        VGroup(g_def, g_box).move_to(2.25 * UP)
        self.say("關鍵：好路徑的數目，正好就是 ", "$A_t(\\vec n)$")
        self.play(FadeOut(good_def), FadeOut(example[0]), run_time=0.4)
        self.play(FadeIn(g_def), ShowCreation(g_box), run_time=0.9)
        self.wait(2.5)
        self.clear_stage()

    # ================================================================== 第 3 段：循環引理
    def part3_cycle_lemma(self):
        M = len(ROT_WORD)
        t = path_heights(ROT_WORD, V_EX)[-1]
        assert t == 2

        # ---------------- (a) 七種讀法
        info = mixed("例子：", "$t=2,\\ \\vec n=(1,1)$", "，5 個 ↑ 步、1 個弦型步、1 個三角形型步",
                     font_size=28)
        info.move_to(3.05 * UP)
        tiles = word_tiles(ROT_WORD, V_EX, size=0.55, font_size=26)
        tiles.move_to(2.15 * UP)
        slots = [tile.get_center() for tile in tiles]
        self.play(FadeIn(info), FadeIn(tiles), run_time=0.8)
        start_arrow = Arrow(slots[0] + 0.75 * LEFT, slots[0] + 0.38 * LEFT, buff=0, thickness=3,
                            fill_color=YELLOW)
        start_tag = zh("從這裡讀", font_size=22, color=YELLOW).next_to(start_arrow, LEFT, buff=0.1)
        self.play(GrowArrow(start_arrow), FadeIn(start_tag), run_time=0.6)
        self.say("把這串步驟排成一圈，從不同的位置開始讀，共有 7 種讀法")

        u = 0.17
        slot_xs = np.linspace(-5.7, 5.7, M)
        base_y = -0.25
        thumbs = VGroup()
        marks = VGroup()
        order = list(tiles)
        for j in range(M):
            word_j = rotate(ROT_WORD, j)
            origin = np.array([slot_xs[j] - M * u / 2, base_y, 0.0])
            thumb = path_thumbnail(word_j, V_EX, unit=u, origin=origin)
            mark = (check(scale=0.6) if thumb.good else cross(scale=0.6))
            mark.move_to(np.array([slot_xs[j], -1.45, 0]))
            self.play(FadeIn(thumb, shift=0.3 * DOWN), run_time=0.55)
            self.play(FadeIn(mark, scale=1.4), run_time=0.3)
            thumbs.add(thumb)
            marks.add(mark)
            if j < M - 1:
                first = order.pop(0)
                order.append(first)
                arc = ArcBetweenPoints(first.get_center(), slots[-1], angle=-PI / 2)
                self.play(
                    MoveAlongPath(first, arc),
                    *[m.animate.move_to(slots[k]) for k, m in enumerate(order[:-1])],
                    run_time=0.5,
                )
        self.say("7 種讀法裡恰好 2 種是好路徑。2 正好是終點高度 ", "$t$")
        self.play(*[Indicate(marks[j], scale_factor=1.5, color=OK_COLOR) for j in ROT_GOOD], run_time=1.0)
        self.wait(1.0)

        lemma = VGroup(
            zh("循環引理", font_size=30, color=YELLOW),
            mixed("終點高度為 ", "$t$", " 的路徑，", "$N+t$", " 種讀法中恰有 ", "$t$", " 種是好路徑",
                  font_size=30),
        ).arrange(DOWN, buff=0.2)
        lemma.move_to(2.3 * DOWN)
        lemma_box = SurroundingRectangle(lemma, buff=0.2, color=YELLOW, stroke_width=3)
        self.say("這對每一條路徑都成立。下面證明它")
        self.play(FadeIn(lemma), ShowCreation(lemma_box), run_time=1.0)
        self.wait(2.5)
        self.clear_stage()

        # ---------------- (b) 證明：無限重複
        u = 0.42
        cy = 0.2

        def X(g):
            return u * (g - 3.5)

        def Y(h):
            return cy + u * (h - 0.5)

        ext = PathMob(ROT_WORD * 3, V_EX, unit=u, origin=np.array([X(-7), Y(-t), 0]),
                      start_height=-t, stroke_width=4.5, dot_radius=0.045)

        def V(g):
            return ext.vertex(g + M)

        grid = VGroup(*[
            Line(np.array([X(-7.4), Y(h), 0]), np.array([X(15.2), Y(h), 0]),
                 stroke_color=GREY_D, stroke_width=1.2)
            for h in range(-3, 5)
        ])
        h_labels = VGroup(*[
            Tex(str(h), font_size=20, fill_color=GREY_B).move_to(np.array([X(-8.0), Y(h), 0]))
            for h in range(-3, 5)
        ])
        title = zh("證明：把同一串步驟一直重複下去", font_size=30).move_to(3.05 * UP)
        self.play(FadeIn(title), FadeIn(grid), FadeIn(h_labels), run_time=0.7)
        middle = VGroup(*ext.steps[M:2 * M], *ext.dots[M:2 * M + 1])
        self.play(ShowCreation(VGroup(*ext.steps[M:2 * M])), FadeIn(VGroup(*ext.dots[M:2 * M + 1])),
                  run_time=1.6)
        self.say("一個週期有 7 步，走完一個週期高度上升 ", "$t=2$")
        rise = Arrow(np.array([X(7) + 0.35, Y(0), 0]), np.array([X(7) + 0.35, Y(t), 0]),
                     buff=0, thickness=2.5, fill_color=YELLOW)
        rise_tag = Tex("+t", font_size=30, fill_color=YELLOW).next_to(rise, RIGHT, buff=0.08)
        self.play(GrowFromCenter(rise), FadeIn(rise_tag), run_time=0.7)
        self.wait(0.8)
        outer = VGroup(*ext.steps[:M], *ext.dots[:M], *ext.steps[2 * M:], *ext.dots[2 * M + 1:])
        self.say("前後接上同樣的步驟：路徑一直往右延伸，整體越走越高")
        self.play(FadeOut(rise), FadeOut(rise_tag), run_time=0.3)
        self.play(ShowCreation(VGroup(*ext.steps[:M])), ShowCreation(VGroup(*ext.steps[2 * M:])),
                  FadeIn(VGroup(*ext.dots[:M])), FadeIn(VGroup(*ext.dots[2 * M + 1:])), run_time=1.6)
        self.wait(0.6)

        # 好的起點 <=> 之後都比它高
        self.say("從某一點讀 7 步是好路徑 ", "$\\Longleftrightarrow$", " 這一點之後的點都比它高")
        g_good, g_bad = 5, 0
        line_good = DashedLine(V(g_good), np.array([X(g_good + 7), V(g_good)[1], 0]),
                               dash_length=0.08, stroke_color=OK_COLOR, stroke_width=3)
        win_good = VGroup(*ext.steps[g_good + M:g_good + 2 * M]).copy().set_stroke(OK_COLOR, width=7)
        self.play(ShowCreation(line_good), run_time=0.7)
        self.play(ShowCreation(win_good), run_time=1.2)
        ok = check(scale=0.6).next_to(line_good, DOWN, buff=0.15)
        self.play(FadeIn(ok, scale=1.4), run_time=0.4)
        self.wait(0.8)
        line_bad = DashedLine(V(g_bad), np.array([X(g_bad + 7), V(g_bad)[1], 0]),
                              dash_length=0.08, stroke_color=CROSSING_COLOR, stroke_width=3)
        hit = Dot(V(2), radius=0.1, fill_color=CROSSING_COLOR).set_z_index(3)
        no = cross(scale=0.6).next_to(V(2), DOWN, buff=0.15)
        self.play(FadeOut(win_good), FadeOut(ok), ShowCreation(line_bad), run_time=0.7)
        self.play(FadeIn(hit, scale=2), Flash(V(2), color=CROSSING_COLOR, flash_radius=0.3),
                  FadeIn(no), run_time=0.8)
        self.say("從第 0 點讀：第 2 點掉到它下面，不是好路徑")
        self.wait(1.2)
        self.play(FadeOut(line_good), FadeOut(line_bad), FadeOut(hit), FadeOut(no), run_time=0.5)

        # 光線
        long_hs = path_heights(ROT_WORD * 7, V_EX, start=-3 * t)    # 全域點 -21 .. 28

        def last_visit(h):
            g = max(i for i, x in enumerate(long_hs) if x <= h) - 3 * M
            assert -7 <= g <= 13
            return g

        levels = list(range(-3, 3))
        lit = {h: last_visit(h) for h in levels}
        assert sorted(g for g in lit.values() if 0 <= g < M) == list(ROT_GOOD)

        self.say("從右邊照來水平的光：每個高度的光，停在路徑最後一次到達那個高度的點")
        rays = VGroup()
        lit_dots = VGroup()
        for h in levels:
            end = V(lit[h])
            ray = Line(np.array([X(15.2), Y(h), 0]), end, stroke_color=LIGHT_COLOR, stroke_width=2.5)
            ray.set_opacity(0.8)
            rays.add(ray)
            lit_dots.add(Dot(end, radius=0.1, fill_color=LIGHT_COLOR).set_z_index(3))
        self.play(LaggedStart(*[ShowCreation(r) for r in rays], lag_ratio=0.25), run_time=2.4)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in lit_dots], lag_ratio=0.15), run_time=1.0)
        self.wait(0.8)
        self.say("被照到的點，之後的路徑全都在它上方：正是好的起點")
        self.wait(2.0)
        self.say("↑ 步一次只上一格、其他步都往下，所以每個高度都恰好照到一個點")
        self.wait(2.5)

        # 一個週期裡有幾個
        window = Rectangle(width=M * u, height=Y(4.6) - Y(-3.6), stroke_color=YELLOW, stroke_width=2.5,
                           fill_color=YELLOW, fill_opacity=0.07)
        window.move_to(np.array([(X(0) + X(M)) / 2, (Y(4.6) + Y(-3.6)) / 2, 0]))
        window_tag = zh("一個週期（7 步）", font_size=24, color=YELLOW).next_to(window, UP, buff=0.08)
        self.say("一個週期裡有幾個被照到的點？")
        self.play(FadeIn(window), FadeIn(window_tag), run_time=0.8)
        self.wait(0.6)
        jumps = VGroup()
        for h in (-1, 0):
            a, b = V(lit[h]), V(lit[h + t])
            jumps.add(CurvedArrow(a + 0.12 * UP, b + 0.12 * UP, angle=-TAU / 6, stroke_color=YELLOW))
        jump_tag = mixed("高 ", "$t$", " 層 ", "$=$", " 右移一個週期", font_size=24, color=YELLOW)
        jump_tag.move_to(np.array([X(11.8), Y(5.3), 0]))
        self.say("高度 ", "$h+t$", " 的被照點，正好是高度 ", "$h$", " 的被照點往右一個週期")
        self.play(*[ShowCreation(j) for j in jumps], FadeIn(jump_tag), run_time=1.2)
        self.wait(1.5)
        inside = VGroup(*[lit_dots[levels.index(h)] for h in levels if 0 <= lit[h] < M])
        count = Tex("2=t", font_size=40, fill_color=YELLOW).next_to(window, DOWN, buff=0.15)
        self.say("所以每個週期恰好有 ", "$t$", " 個被照點，也就是恰好 ", "$t$", " 種好讀法")
        self.play(*[Indicate(d, scale_factor=2.2, color=YELLOW) for d in inside], FadeIn(count), run_time=1.2)
        self.wait(1.5)

        done = VGroup(
            mixed("循環引理得證：每條路徑恰有 ", "$t$", " 種讀法是好路徑", font_size=30, color=YELLOW),
            check(scale=0.6),
        ).arrange(RIGHT, buff=0.25)
        done.move_to(2.45 * DOWN)
        self.say("這個論證和例子無關，對任何路徑都成立")
        self.play(FadeIn(done, shift=0.2 * UP), run_time=0.9)
        self.wait(2.5)
        self.clear_stage()

    # ================================================================== 第 4 段：數一數
    def part4_counting(self):
        title = zh("數一數好路徑", font_size=32).move_to(3.05 * UP)
        self.play(FadeIn(title), run_time=0.5)
        rows = VGroup(
            mixed("「路徑 ＋ 起點」的組合共有 ", "$(N+t)\\cdot\\binom{N+t}{\\vec n}$", " 種", font_size=28),
            mixed("循環引理：其中讀出好路徑的有 ", "$t\\cdot\\binom{N+t}{\\vec n}$", " 種", font_size=28),
            mixed("另一方面，每條好路徑恰好被 ", "$N+t$", " 種組合讀出來（每個起點一種）", font_size=28),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        rows.move_to(1.4 * UP)
        captions = [
            ("每條路徑有 ", "$N+t$", " 個可能的起點"),
            ("每條路徑恰有 ", "$t$", " 個起點讀出好路徑"),
            ("每條好路徑，配上任何一個起點，都對應一個組合",),
        ]
        for row, cap in zip(rows, captions):
            self.say(*cap)
            self.play(FadeIn(row, shift=0.2 * UP), run_time=0.8)
            self.wait(1.4)

        eq1 = Tex(R"(N+t)\cdot G_t(\vec n)=t\cdot\binom{N+t}{\vec n}", font_size=44)
        eq2 = Tex(R"G_t(\vec n)=\frac{t}{N+t}\binom{N+t}{\vec n}=A_t(\vec n)", font_size=50)
        eq1.move_to(0.6 * DOWN)
        eq2.move_to(2.1 * DOWN)
        box = SurroundingRectangle(eq2, buff=0.2, color=YELLOW, stroke_width=3)
        self.say("同一個數用兩種方法數，結果相等")
        self.play(Write(eq1), run_time=1.3)
        self.wait(1.0)
        self.play(TransformFromCopy(eq1, eq2), run_time=1.2)
        self.play(ShowCreation(box), run_time=0.6)
        self.say("好路徑的數目，正好是 ", "$A_t(\\vec n)$")
        self.wait(2.2)

        # 驗算
        self.play(FadeOut(rows), FadeOut(eq1), VGroup(eq2, box).animate.scale(0.7).move_to(2.2 * UP),
                  run_time=0.9)
        check1 = Tex(R"t=1:\ \ G_1(1,1)=\frac{1}{6}\cdot 30=5", font_size=40)
        check2 = Tex(R"t=2:\ \ G_2(1,1)=\frac{2}{7}\cdot 42=12", font_size=40)
        check1.move_to(1.0 * UP)
        self.say("驗算：", "$t=1$", " 時 30 種排法中有 5 條好路徑")
        self.play(FadeIn(check1, shift=0.2 * UP), run_time=0.8)
        u = 0.22
        goods = good_paths(1, N_EX, V_EX)
        xs = np.linspace(-4.8, 4.8, len(goods))
        thumbs = VGroup(*[
            path_thumbnail(w, V_EX, unit=u, origin=np.array([x - 3 * u, -0.85, 0]))
            for w, x in zip(goods, xs)
        ])
        self.play(LaggedStart(*[FadeIn(th, shift=0.2 * UP) for th in thumbs], lag_ratio=0.2), run_time=1.6)
        note = mixed("$A_1=C_{\\vec v}(\\vec n)=5$", "：和論文 Fig. 1 的 5 種分法同樣是 5", font_size=26,
                     color=GREY_A)
        note.move_to(1.35 * DOWN)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.5)
        check2.move_to(2.3 * DOWN)
        self.say("$t=2$", " 時 42 種排法中有 12 條好路徑（下一段會用到）")
        self.play(FadeIn(check2, shift=0.2 * UP), run_time=0.8)
        self.wait(2.2)
        self.clear_stage()

    # ================================================================== 第 5 段：切開 => Raney 公式
    def part5_cut(self):
        title = zh("好路徑可以切成兩段", font_size=32).move_to(3.05 * UP)
        self.play(FadeIn(title), run_time=0.5)
        u = 0.55
        s = CUT_S
        t = path_heights(CUT_WORD, V_EX)[-1] - s
        j_cut = cut_index(CUT_WORD, s, V_EX)
        assert (t, j_cut) == (1, 3)

        path = PathMob(CUT_WORD, V_EX, unit=u, origin=np.array([-6.3, -1.75, 0]))
        base = level_line(path, 0, -0.3, 7.4)
        s_line = level_line(path, s, -0.3, 7.4, color=CUT_COLOR, stroke_width=2.5)
        base_tag = Tex("0", font_size=26, fill_color=GREY_B).next_to(base, LEFT, buff=0.1)
        s_tag = Tex("s", font_size=30, fill_color=CUT_COLOR).next_to(s_line, LEFT, buff=0.1)
        end_tag = Tex("s+t", font_size=28, fill_color=GREY_A).next_to(path.vertex(7), RIGHT, buff=0.12)

        self.say("取一條終點高度 ", "$s+t$", " 的好路徑（這裡 ", "$s=1,\\ t=1$", "）")
        self.play(ShowCreation(base), FadeIn(base_tag), run_time=0.5)
        self.play(ShowCreation(path.steps), FadeIn(path.dots), run_time=1.6)
        self.play(FadeIn(end_tag), run_time=0.4)
        self.wait(0.6)
        self.say("在高度 ", "$s$", " 畫一條線")
        self.play(ShowCreation(s_line), FadeIn(s_tag), run_time=0.7)
        self.wait(0.5)

        self.say("找出路徑最後一次落在這條線上（或線下）的點")
        cut_dot = Dot(path.vertex(j_cut), radius=0.11, fill_color=CUT_COLOR).set_z_index(3)
        self.play(FadeIn(cut_dot, scale=2), Flash(path.vertex(j_cut), color=CUT_COLOR, flash_radius=0.35),
                  run_time=0.9)
        after = VGroup(*path.dots[j_cut + 1:])
        self.play(LaggedStart(*[Indicate(d, scale_factor=1.8, color=OK_COLOR) for d in after], lag_ratio=0.15),
                  run_time=1.2)
        self.say("↑ 步一次只上一格，所以這點剛好在高度 ", "$s$", "；之後的點都在線的上方")
        self.wait(2.5)

        # 切開
        left = VGroup(*path.steps[:j_cut], *path.dots[:j_cut + 1])
        right = VGroup(*path.steps[j_cut:], *path.dots[j_cut + 1:])
        right_start = path.dots[j_cut].copy()
        right.add(right_start)
        shift = 1.4 * RIGHT + s * u * DOWN
        self.say("從這一點切開，右段往下移 ", "$s$")
        self.play(FadeOut(end_tag), run_time=0.3)
        self.play(right.animate.shift(shift), cut_dot.animate.shift(shift), run_time=1.4)
        right_base = DashedLine(right_start.get_center() + 0.15 * LEFT,
                                right_start.get_center() + (4 * u + 0.15) * RIGHT,
                                dash_length=0.08, stroke_color=GREY_B, stroke_width=2)
        self.play(ShowCreation(right_base), run_time=0.5)
        left_tag = VGroup(
            mixed("左段：終點 ", "$s$", " 的好路徑", font_size=24),
            mixed("用掉 ", "$\\vec r=(1,0)$", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.1)
        left_tag.next_to(left, UP, buff=0.35)
        right_tag = VGroup(
            mixed("右段：終點 ", "$t$", " 的好路徑", font_size=24),
            mixed("用掉 ", "$\\vec n-\\vec r=(0,1)$", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.1)
        right_tag.next_to(right, UP, buff=0.3)
        self.play(FadeIn(left_tag), FadeIn(right_tag), run_time=0.8)
        self.wait(2.0)

        self.say("反過來，任兩段好路徑接起來，就是終點 ", "$s+t$", " 的好路徑，切點也找得回來")
        self.play(right.animate.shift(-shift), cut_dot.animate.shift(-shift), FadeOut(right_base),
                  FadeOut(right_tag), FadeOut(left_tag), run_time=1.3)
        self.wait(0.6)
        self.play(right.animate.shift(shift), cut_dot.animate.shift(shift), FadeIn(right_base),
                  FadeIn(right_tag), FadeIn(left_tag), run_time=1.3)
        self.wait(1.0)

        # 一般結論
        x_text = 3.6
        g_eq = Tex(R"G_{s+t}(\vec n)=\sum_{\vec r}G_s(\vec r)\,G_t(\vec n-\vec r)", font_size=44)
        g_eq.move_to(np.array([x_text, 1.65, 0]))
        self.say("所以終點 ", "$s+t$", " 的好路徑 ＝（左段）接（右段），一一對應")
        self.play(Write(g_eq), run_time=1.5)
        self.wait(1.0)
        sub_tag = mixed("代入 ", "$G=A$", "（第 4 段）：", font_size=26).move_to(np.array([x_text, 0.65, 0]))
        a_eq = Tex(R"A_{s+t}(\vec n)=\sum_{\vec r}A_s(\vec r)\,A_t(\vec n-\vec r)", font_size=44)
        a_eq.move_to(np.array([x_text, -0.25, 0]))
        a_box = SurroundingRectangle(a_eq, buff=0.2, color=YELLOW, stroke_width=3)
        done = VGroup(zh("Raney 公式得證", font_size=28, color=YELLOW), check(scale=0.55)).arrange(RIGHT, buff=0.2)
        done.next_to(a_box, DOWN, buff=0.2)
        self.play(FadeIn(sub_tag), run_time=0.5)
        self.play(TransformFromCopy(g_eq, a_eq), run_time=1.2)
        self.play(ShowCreation(a_box), FadeIn(done), run_time=0.8)
        self.say("Raney 公式（論文式 (9)）證完了")
        self.wait(2.5)
        self.clear_stage()

        # ---------------- 驗算：12 條好路徑依切法分組
        title = mixed("驗算：", "$A_2(1,1)=12$", " 條好路徑，依左段用掉的 ", "$\\vec r$", " 分組", font_size=30)
        title.move_to(3.05 * UP)
        self.play(FadeIn(title), run_time=0.6)
        u = 0.15
        groups = {}
        for r in sub_vectors(N_EX):
            rest = tuple(a - b for a, b in zip(N_EX, r))
            groups[r] = [(a, b) for a in good_paths(1, r, V_EX) for b in good_paths(1, rest, V_EX)]
        layout = [((0, 0), (1, 0)), ((0, 1), (1, 1))]
        row_ys = [1.0, -1.25]
        group_mobs = VGroup()
        for row, y in zip(layout, row_ys):
            row_group = VGroup()
            for r in row:
                pairs = groups[r]
                rest = tuple(a - b for a, b in zip(N_EX, r))
                thumbs = VGroup()
                for a, b in pairs:
                    th = path_thumbnail(a + b, V_EX, unit=u)
                    cut = Dot(th.path.vertex(len(a)), radius=0.06, fill_color=CUT_COLOR).set_z_index(3)
                    th.add(cut)
                    thumbs.add(th)
                thumbs.arrange(RIGHT, buff=0.32, aligned_edge=DOWN)
                r_str = f"({r[0]},{r[1]})"
                rest_str = f"({rest[0]},{rest[1]})"
                label = Tex(
                    fR"\vec r={r_str}:\ \ A_1{r_str}\cdot A_1{rest_str}"
                    fR"={raney_A(1, r, V_EX)}\cdot{raney_A(1, rest, V_EX)}",
                    font_size=26,
                )
                label.next_to(thumbs, UP, buff=0.22)
                frame = SurroundingRectangle(VGroup(label, thumbs), buff=0.18, color=GREY_C, stroke_width=1.5)
                row_group.add(VGroup(frame, label, thumbs))
            row_group.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
            row_group.move_to(y * UP)
            group_mobs.add(*row_group)
        self.say("每條好路徑在高度 1 切開（橘點），依左段用掉多少分成四組")
        self.play(LaggedStart(*[FadeIn(g, shift=0.2 * UP) for g in group_mobs], lag_ratio=0.3), run_time=2.4)
        self.wait(1.5)
        total = Tex(R"5+1+1+5=12=A_2(1,1)", font_size=44, fill_color=YELLOW).move_to(2.65 * DOWN)
        self.play(Write(total), run_time=1.0)
        self.say("四組加起來是 12，和第 4 段算的一樣")
        self.wait(2.0)
        self.clear_stage()

        # ---------------- 論文原本的寫法
        paper = Tex(
            R"\frac{s+t}{\langle\vec n,\vec v\rangle+s+t}\binom{\langle\vec n,\vec v\rangle+s+t}{\vec n}"
            R"=\sum_{\vec r}\frac{s}{\langle\vec r,\vec v\rangle+s}\binom{\langle\vec r,\vec v\rangle+s}{\vec r}"
            R"\cdot\frac{t}{\langle\vec n-\vec r,\vec v\rangle+t}\binom{\langle\vec n-\vec r,\vec v\rangle+t}{\vec n-\vec r}",
            font_size=40,
        )
        if paper.get_width() > 13.2:
            paper.set_width(13.2)
        paper.move_to(0.4 * UP)
        tag = zh("論文第 93 頁的式 (9)，寫開來就是這樣", font_size=26, color=GREY_A)
        tag.next_to(paper, DOWN, buff=0.45)
        self.say("把 ", "$A$", " 的定義代進去，就是論文寫的式 (9)")
        self.play(Write(paper), run_time=2.2)
        self.play(FadeIn(tag), run_time=0.5)
        self.wait(3.0)
        self.clear_stage()

    # ================================================================== 第 6 段：C^t 的係數與式 (10)
    def part6_finish(self):
        f_def = Tex(R"F_t(\vec X)=\sum_{\vec n}A_t(\vec n)\,x_1^{n_1}\cdots x_k^{n_k}", font_size=48)
        f_def.move_to(2.45 * UP)
        self.say("把 ", "$A_t(\\vec n)$", " 收進生成函數 ", "$F_t$")
        self.play(Write(f_def), run_time=1.4)
        self.wait(0.8)

        mult = Tex(R"F_{s+t}=F_s\cdot F_t", font_size=54).move_to(1.3 * UP)
        self.say("Raney 公式的右邊，正是兩個冪級數相乘時的係數")
        self.play(FadeIn(mult, shift=0.2 * UP), run_time=0.9)
        self.wait(1.2)

        chain = Tex(R"F_1=C,\quad F_2=F_1F_1=C^2,\quad F_3=F_2F_1=C^3,\quad\ldots", font_size=46,
                    t2c={"C": C_COLOR})
        chain.move_to(0.15 * UP)
        self.say("$F_1$", " 就是 ", "$C$", "（因為 ", "$A_1=C_{\\vec v}$", "），一路乘下去", t2c={"C": C_COLOR})
        self.play(Write(chain), run_time=1.8)
        self.wait(1.0)
        ct = Tex(R"[x^{\vec n}]\,C^{t}=\frac{t}{N+t}\binom{N+t}{\vec n}", font_size=56, t2c={"C": C_COLOR})
        ct.move_to(1.35 * DOWN)
        ct_box = SurroundingRectangle(ct, buff=0.22, color=YELLOW, stroke_width=3)
        self.say("所以 ", "$C^t$", " 的係數就是 ", "$A_t(\\vec n)$", "：這是論文由式 (8)、(9) 得到的結果",
                 t2c={"C": C_COLOR})
        self.play(TransformFromCopy(chain, ct), run_time=1.3)
        self.play(ShowCreation(ct_box), run_time=0.6)
        self.wait(2.2)

        # 式 (10)
        self.play(FadeOut(f_def), FadeOut(mult), FadeOut(chain), VGroup(ct, ct_box).animate.scale(0.75).move_to(2.5 * UP),
                  run_time=0.9)
        step1 = Tex(
            R"[x^{\vec n-\vec e_i}]\,C^{v_i}=\frac{v_i}{N}\binom{N}{\vec n-\vec e_i}"
            R"=\frac{n_i\,v_i}{N}\cdot\frac{N!}{n_1!\cdots n_k!\,(N+1-b)!}",
            font_size=44, t2c={"C": C_COLOR},
        )
        if step1.get_width() > 13.0:
            step1.set_width(13.0)
        step1.move_to(1.05 * UP)
        b_note = Tex(R"b=n_1+\cdots+n_k,\qquad \langle\vec n-\vec e_i,\vec v\rangle+v_i=N", font_size=32,
                     fill_color=GREY_A)
        b_note.next_to(step1, DOWN, buff=0.3)
        self.say("取 ", "$t=v_i$", "，算 ", "$x_iC^{v_i}$", " 裡 ", "$x^{\\vec n}$", " 的係數",
                 t2c={"C": C_COLOR})
        self.play(Write(step1), run_time=2.0)
        self.play(FadeIn(b_note), run_time=0.6)
        self.wait(2.0)

        step2 = Tex(
            R"\sum_{i=1}^{k}[x^{\vec n-\vec e_i}]\,C^{v_i}"
            R"=\frac{\sum_i n_iv_i}{N}\cdot\frac{N!}{n_1!\cdots n_k!\,(N+1-b)!}=C_{\vec v}(\vec n)",
            font_size=44, t2c={"C": C_COLOR},
        )
        if step2.get_width() > 13.0:
            step2.set_width(13.0)
        step2.move_to(1.0 * DOWN)
        tag10 = zh("論文式 (10)", font_size=24, color=GREY_A).next_to(step2, DOWN, buff=0.2).align_to(step2, RIGHT)
        self.say("對 ", "$i$", " 加總：", "$\\sum_i n_iv_i=N$", "，剛好得到 ", "$C_{\\vec v}(\\vec n)$",
                 t2c={"C": C_COLOR})
        self.play(Write(step2), run_time=2.0)
        self.play(FadeIn(tag10), run_time=0.4)
        self.wait(2.0)

        goal = Tex(R"C=1+\sum_{i=1}^{k} x_i\,C^{v_i}", font_size=52, t2c={"C": C_COLOR})
        goal.move_to(2.4 * DOWN)
        ok = check(scale=0.8).next_to(goal, RIGHT, buff=0.35)
        self.say("每個係數都對上了（常數項兩邊都是 1），所以 ", "$C$", " 滿足這條方程", t2c={"C": C_COLOR})
        self.play(FadeIn(goal, shift=0.2 * UP), run_time=0.8)
        self.play(FadeIn(ok, scale=1.5), run_time=0.5)
        self.wait(2.5)
        self.clear_stage()

    # ================================================================== 第 7 段：D = C
    def part7_conclusion(self):
        big_d = Tex("D", font_size=150, fill_color=D_COLOR)
        big_c = Tex("C", font_size=150, fill_color=C_COLOR)
        eq_d = Tex(R"D=1+\sum_{i} x_i\,D^{v_i}", font_size=44, t2c={"D": D_COLOR})
        eq_c = Tex(R"C=1+\sum_{i} x_i\,C^{v_i}", font_size=44, t2c={"C": C_COLOR})
        tag_d = zh("數分法（幾何）", font_size=28, color=GREY_A)
        tag_c = zh("代公式（代數）", font_size=28, color=GREY_A)
        col_d = VGroup(tag_d, big_d, eq_d).arrange(DOWN, buff=0.35).move_to(3.6 * LEFT + 0.6 * UP)
        col_c = VGroup(tag_c, big_c, eq_c).arrange(DOWN, buff=0.35).move_to(3.6 * RIGHT + 0.6 * UP)
        self.say("$D$", " 來自數分法，", "$C$", " 來自公式；兩者滿足同一條方程",
                 t2c={"D": D_COLOR, "C": C_COLOR})
        self.play(FadeIn(col_d, shift=2 * RIGHT), FadeIn(col_c, shift=2 * LEFT), run_time=1.4)
        self.wait(1.5)
        self.say("常數項都是 1，之後每個係數都被前面的係數唯一決定")
        self.wait(2.2)

        equal = Tex("=", font_size=150)
        self.play(
            FadeOut(eq_d), FadeOut(eq_c), FadeOut(tag_d), FadeOut(tag_c),
            big_d.animate.move_to(1.5 * LEFT + 0.9 * UP),
            big_c.animate.move_to(1.5 * RIGHT + 0.9 * UP),
            run_time=1.0,
        )
        equal.move_to(0.9 * UP)
        self.play(FadeIn(equal, scale=1.5), run_time=0.6)
        self.say("所以 ", "$D=C$", t2c={"D": D_COLOR, "C": C_COLOR})
        self.wait(1.5)

        conclusion = Tex(R"d(\vec n)=C_{\vec v}(\vec n)", font_size=80)
        conclusion.move_to(0.9 * UP)
        concl_box = SurroundingRectangle(conclusion, buff=0.3, color=YELLOW, stroke_width=4)
        formula = general_formula(font_size=48)
        formula_tail = Tex(R"N=\sum_i n_iv_i,\qquad L=1+\sum_i n_i(v_i-1)", font_size=34, fill_color=GREY_A)
        VGroup(formula, formula_tail).arrange(DOWN, buff=0.3).move_to(1.6 * DOWN)
        self.play(FadeTransform(VGroup(big_d, equal, big_c), conclusion), run_time=1.2)
        self.play(ShowCreation(concl_box), run_time=0.7)
        self.say("不交叉分法的數目，就是廣義卡塔蘭數。定理得證")
        self.play(FadeIn(formula, shift=0.2 * UP), FadeIn(formula_tail, shift=0.2 * UP), run_time=1.0)
        self.wait(4.0)


class Scene08RaneyProof(Scene08FormulaVerification):
    """只播 Raney 公式的證明（第 1–5 段）。"""

    def construct(self):
        self.show_header("Raney 公式的證明")
        self.sanity_checks()
        self.part1_statement()
        self.part2_paths()
        self.part3_cycle_lemma()
        self.part4_counting()
        self.part5_cut()
