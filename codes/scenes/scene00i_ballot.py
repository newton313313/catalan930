"""
Scene 00i —— 投票問題（來源論文 2.6 節）

清楚區分兩件事：
    一般的 Bertrand 投票問題：A 得 a 票、B 得 b 票（a > b），
        開票過程中 A 始終「嚴格領先」的機率 = (a - b)/(a + b)
        （來源論文寫的是 k 倍的推廣 (a - kb)/(a + b)，k = 1 就是這個）
    卡塔蘭的特例：兩人各 n 票，每開一張後 A 的票數 >= B 的票數
        -> 合法的開票順序有 C_n 種，和 Dyck 路徑一一對應
兩個公式都在 counting.py 用暴力列舉檢查過。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00i_ballot.py Scene00iBallot
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import CATALAN_COLOR, dyck_item, dyck_path_mob
from utils.counting import ballot_ok, binary_trees, catalan, dyck_to_ballot, tree_to_dyck
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, YELLOW, mixed, zh

VOTES = "AABABB"
A_COLOR = BLUE_B
B_COLOR = GREY_B


def vote_tile(c: str, size: float = 0.5) -> VGroup:
    color = A_COLOR if c == "A" else B_COLOR
    sq = RoundedRectangle(width=size, height=size, corner_radius=0.08, stroke_color=color, stroke_width=2.5)
    sq.set_fill(color, opacity=0.2)
    return VGroup(sq, Tex(c, font_size=64 * size, fill_color=color).move_to(sq))


class Scene00iBallot(ChuScene):
    def construct(self):
        self.show_header("投票問題")
        assert ballot_ok(VOTES) and dyck_to_ballot("UUDUDD") == VOTES

        # ------------------------------------------------------------ 兩個不同的問題
        general_title = zh("一般的 Bertrand 投票問題（1887）", font_size=28, color=YELLOW)
        general_body = VGroup(
            mixed("A 得 ", "$a$", " 票、B 得 ", "$b$", " 票（", "$a>b$", "），票一張一張開，每種順序機率相同",
                  font_size=24),
            mixed("開票過程中 A 始終「嚴格領先」的機率是 ", "$\\dfrac{a-b}{a+b}$", font_size=24),
            mixed("（來源論文寫的是「始終多於 B 的 ", "$k$", " 倍」的推廣：", "$\\dfrac{a-kb}{a+b}$",
                  "；", "$k=1$", " 就是上式）", font_size=20, color=MUTED_COLOR),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        general = VGroup(general_title, general_body).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        general_box = SurroundingRectangle(general, buff=0.2, color=GREY_B, stroke_width=2)
        VGroup(general, general_box).move_to(1.75 * UP)
        self.say("投票問題有一般的版本，也有卡塔蘭的特例，兩者要分清楚")
        self.play(FadeIn(general_title), ShowCreation(general_box), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in general_body], lag_ratio=0.4),
                  run_time=1.8)
        self.wait(2.5)

        special_title = zh("卡塔蘭的特例（本段要看的）", font_size=28, color=CATALAN_COLOR)
        special_body = VGroup(
            mixed("兩人各得 ", "$n$", " 票；要求每開一張票之後，A 的票數 ", "$\\ge$", " B 的票數", font_size=24),
            mixed("這樣的開票順序有 ", "$C_n$", " 種", font_size=24, t2c={"C_n": CATALAN_COLOR}),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        special = VGroup(special_title, special_body).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        special_box = SurroundingRectangle(special, buff=0.2, color=CATALAN_COLOR, stroke_width=2.5)
        VGroup(special, special_box).next_to(general_box, DOWN, buff=0.35).align_to(general_box, LEFT)
        self.say("卡塔蘭的特例：同票、而且 A 從不落後（可以平手）")
        self.play(FadeIn(special_title), ShowCreation(special_box), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=0.15 * UP) for r in special_body], lag_ratio=0.4),
                  run_time=1.4)
        self.say("注意：一般的問題要「嚴格領先」、票數不同；不是每個投票問題的答案都是 ", "$C_n$")
        self.wait(3.0)

        # ------------------------------------------------------------ 例子：A A B A B B
        self.clear_stage()
        tiles = VGroup(*[vote_tile(c) for c in VOTES]).arrange(RIGHT, buff=0.15)
        tiles.move_to(np.array([-3.2, 2.45, 0.0]))
        rule = mixed("A：", "$+1$", "　　B：", "$-1$", font_size=28)
        rule.next_to(tiles, RIGHT, buff=0.8)
        self.say("例子：開票順序 A A B A B B；記分：A 加 1、B 減 1")
        self.play(LaggedStart(*[FadeIn(t, shift=0.2 * DOWN) for t in tiles], lag_ratio=0.15),
                  FadeIn(rule), run_time=1.3)

        # 計分板：x = 已開的票數，y = A 的票數 − B 的票數
        unit = 0.62
        origin = np.array([-4.6, -1.15, 0.0])
        x_axis = Arrow(origin + 0.2 * LEFT, origin + (len(VOTES) * unit + 0.6) * RIGHT, buff=0,
                       thickness=2, fill_color=GREY_B)
        y_axis = Arrow(origin + 0.2 * DOWN, origin + 2.9 * unit * UP, buff=0, thickness=2, fill_color=GREY_B)
        x_lab = zh("已開的票數", font_size=22, color=MUTED_COLOR).next_to(x_axis, DOWN, buff=0.12)
        y_lab = zh("A 領先幾票", font_size=22, color=MUTED_COLOR).next_to(y_axis, UP, buff=0.1)
        self.play(GrowArrow(x_axis), GrowArrow(y_axis), FadeIn(x_lab), FadeIn(y_lab), run_time=0.8)

        score = 0
        points = [origin.copy()]
        dots = VGroup(Dot(origin, radius=0.07, fill_color=WHITE))
        score_tex = Tex("0", font_size=44, fill_color=YELLOW)
        score_tex.move_to(np.array([3.6, 0.3, 0.0]))
        score_title = zh("目前比分（A − B）", font_size=24, color=MUTED_COLOR).next_to(score_tex, UP, buff=0.25)
        seq_tex = Tex("0", font_size=40).move_to(np.array([3.6, -0.9, 0.0]))
        self.play(FadeIn(dots[0]), FadeIn(score_tex), FadeIn(score_title), FadeIn(seq_tex), run_time=0.6)
        seq = ["0"]
        for j, c in enumerate(VOTES):
            score += 1 if c == "A" else -1
            p = origin + unit * np.array([j + 1, score, 0.0])
            points.append(p)
            dot = Dot(p, radius=0.07, fill_color=WHITE)
            new_score = Tex(str(score), font_size=44, fill_color=YELLOW).move_to(score_tex)
            seq.append(str(score))
            new_seq = Tex(R"\to".join(seq), font_size=40).move_to(seq_tex)
            self.play(Indicate(tiles[j], scale_factor=1.2, color=YELLOW), FadeIn(dot, scale=1.5),
                      Transform(score_tex, new_score), Transform(seq_tex, new_seq), run_time=0.55)
            dots.add(dot)
        self.wait(0.6)

        # 把點連起來：就是一條 Dyck 路徑
        path = dyck_path_mob("UUDUDD", unit=unit, origin=origin, color=CATALAN_COLOR, stroke_width=6,
                             dot_radius=0.07)
        self.say("把這些點連起來：A 是上坡、B 是下坡；「A 從不落後」就是「不掉到地面以下」")
        self.play(ShowCreation(path.steps), run_time=1.4)
        self.play(FadeOut(dots), FadeIn(path.dots), run_time=0.4)
        ground = Line(origin, origin + len(VOTES) * unit * RIGHT, stroke_color=GREY_A, stroke_width=3)
        self.play(ShowCreation(ground), Indicate(path, scale_factor=1.05, color=CATALAN_COLOR), run_time=0.9)
        self.wait(1.2)

        # ------------------------------------------------------------ n = 3 的五種合法順序
        self.clear_stage()
        trees = binary_trees(3)
        xs = np.linspace(-5.0, 5.0, 5)
        items = VGroup()
        for x, t in zip(xs, trees):
            word = dyck_to_ballot(tree_to_dyck(t))
            row = VGroup(*[vote_tile(c, size=0.25) for c in word]).arrange(RIGHT, buff=0.04)
            mini = dyck_item(t, scale=1.5, stroke_width=4)
            group = VGroup(mini, row).arrange(DOWN, buff=0.3)
            group.move_to(np.array([x, 0.9, 0.0]))
            items.add(group)
        self.say("兩人各 3 票：合法的開票順序剛好 5 種，對應 5 條 Dyck 路徑")
        self.play(LaggedStart(*[FadeIn(i, shift=0.2 * UP) for i in items], lag_ratio=0.2), run_time=1.8)
        statement = mixed("合法的開票順序", "$\\longleftrightarrow$", "Dyck 路徑", font_size=30, buff=0.25)
        count = mixed("兩人各 ", "$n$", " 票：", "$C_n$", " 種（", "$C_3=5$", "）", font_size=28,
                      t2c={"C_n": CATALAN_COLOR})
        block = VGroup(statement, count).arrange(DOWN, buff=0.2)
        box = SurroundingRectangle(block, buff=0.22, color=YELLOW, stroke_width=3)
        VGroup(block, box).move_to(1.25 * DOWN)
        self.play(FadeIn(block), ShowCreation(box), run_time=0.9)
        self.wait(2.5)
