"""
Scene N16 —— Chu 的推廣也是「走路的部分和」（Raney 導讀第 2.4 小節的說明框、附錄 A）
執行（在 codes/ 內）：manimgl scenes/sceneN16_walk_sums.py SceneN16WalkSums

1. 每個符號換成一步：0 走 +1，v 點群組走 1 − v（弦 −1、三角形 −2）。
   字 203000 倒過來讀：+1,+1,+1,−2,+1,−1，高度 1,2,3,1,2,1 —— 部分和都 > 0，總和 t = 1。
2. 循環引理：4 個 +1、1 個 −1、1 個 −2 的排法 30 種；同一圈的 6 種讀法恰有 1 種部分和全正 ⇒ 30/6 = 5。
3. t = 2：多一個 +1，總和 2；7 種讀法恰有 2 種 ⇒ 42·2/7 = 12。
4. 為什麼恰好 t 種：把路重複畫，從右邊照來水平光線，每一圈恰好照到 t 個點（每步 ≤ 1、每圈升高 t）。
5. 總結：同一個東西的四種樣子（圓周群組、字、樹、路徑），以及公式 A_t = (t/(N+t))·（全部排法）。
"""
import sys
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.polygon_groups import make_configuration
from utils.raney import chu_heights, good_starts, heights, partition_to_word
from utils.raney_draw import IntPathMob, WordTreeMob, chu_walk, level_line, readings_row, step_tiles, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

EX = [(0, 1), (2, 3, 4)]
EX_WORD = (2, 0, 3, 0, 0, 0)
S1 = (1, -2, 1, -1, 1, 1)                  # t = 1：4 個 +1、1 個 −1、1 個 −2
S2 = (1, -2, 1, 1, -1, 1, 1)               # t = 2：多一個 +1


def check_math():
    assert partition_to_word(EX, 5) == EX_WORD
    steps = [1 - x for x in reversed(EX_WORD)]
    assert steps == [1, 1, 1, -2, 1, -1] and chu_heights(EX_WORD)[1:] == [1, 2, 3, 1, 2, 1]
    assert sum(S1) == 1 and sorted(S1) == [-2, -1, 1, 1, 1, 1] and len(good_starts(S1)) == 1
    assert sum(S2) == 2 and sorted(S2) == [-2, -1, 1, 1, 1, 1, 1] and len(good_starts(S2)) == 2
    assert factorial(6) // factorial(4) == 30 and 30 // 6 == 5
    assert factorial(7) // factorial(5) == 42 and 42 * 2 // 7 == 12
    hs = heights(S2 * 3)
    for p in range(3):                      # 每一圈照到的點恰好是 good_starts，且比後面每一點都低
        for i in good_starts(S2):
            assert all(hs[p * 7 + i] < h for h in hs[p * 7 + i + 1:])


class SceneN16WalkSums(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N16　Chu 的推廣也是走路的部分和")

        # 1. 符號 → 步
        legend = VGroup(
            mixed("0（樹葉）", "$\\to$", " 走 ", "$+1$", font_size=28),
            mixed("弦（2 點群組）", "$\\to$", " 走 ", "$1-2=-1$", font_size=28),
            mixed("三角形（3 點群組）", "$\\to$", " 走 ", "$1-3=-2$", font_size=28),
            mixed("一般：", "$v$", " 點群組 ", "$\\to$", " 走 ", "$1-v$", font_size=28),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(np.array([3.4, 1.6, 0]))
        cfg = make_configuration(5, EX, radius=1.1, center=np.array([-4.6, 1.7, 0]), root=0)
        tiles = word_tiles(EX_WORD, size=0.5, font_size=30).move_to(np.array([-1.3, 1.7, 0]))
        assert_in_frame(legend, cfg, tiles)
        assert_apart(VGroup(cfg, tiles), legend)
        self.say("把每個符號換成走一步：樹葉往上，群組往下")
        self.play(FadeIn(cfg), FadeIn(tiles))
        self.play(LaggedStartMap(FadeIn, legend, lag_ratio=0.3), run_time=2)
        self.wait(2)
        rev = tiles.copy()
        self.say("把 N14 的字 ", "$203000$", " 倒過來讀（倒過來，條件才會變成「一直在上面」，見 N03）")
        self.play(*[m.animate.move_to(tiles[5 - k].get_center() + 1.0 * DOWN) for k, m in enumerate(rev)],
                  tiles.animate.set_opacity(0.3), run_time=1.5)
        steps = step_tiles([1 - x for x in EX_WORD], size=0.5, font_size=26)
        for s, m in zip(steps, rev):
            s.move_to(m.get_center() + 0.8 * DOWN)
        self.play(FadeIn(steps, lag_ratio=0.1))
        walk = chu_walk(EX_WORD, unit=0.42, origin=np.array([1.2, -2.4, 0]))
        base = level_line(walk, 0, 0, 6, color=MAROON_B)
        hl = Tex(r"1,\ 2,\ 3,\ 1,\ 2,\ 1", font_size=30).next_to(VGroup(walk, base), LEFT, buff=0.6)
        hlab = zh("部分和（高度）：", font_size=26).next_to(hl, UP, buff=0.15)
        assert_in_frame(rev, steps, walk, base, hl, hlab)
        assert_apart(steps, walk)
        self.play(FadeIn(VGroup(base, walk.dots[0])))
        self.play(ShowCreation(walk.steps, lag_ratio=1), FadeIn(walk.dots), run_time=2.2)
        self.play(FadeIn(hlab), FadeIn(hl))
        self.say("部分和一直 ", "$>0$", "，最後停在 ", "$t=1$", "：一個分法 ", "$=$", " 一條「好路徑」")
        self.wait(3)
        rule = boxed(mixed("$A_t(\\vec n)$", " ＝ ", "$\\ell$", " 個 ", "$+1$", "、", "$n_i$", " 個 ", "$1-v_i$",
                           " 排成一列，部分和都 ", "$>0$", "、總和 ", "$t$", " 的排法數", font_size=28))
        rule.move_to(0.1 * UP)
        self.play(FadeOut(VGroup(legend, rev, steps, walk, base, hl, hlab)))
        assert_in_frame(rule)
        self.say("所以 Chu 數的東西可以整個換成走路")
        self.play(FadeIn(rule))
        self.wait(4)
        self.play(FadeOut(VGroup(rule, cfg, tiles)))

        # 2. 循環引理 t = 1
        self.say("數這種路：4 個 ", "$+1$", "、1 個 ", "$-1$", "、1 個 ", "$-2$", " 隨便排，有 ",
                 "$\\frac{6!}{4!\\,1!\\,1!}=30$", " 種")
        row1 = readings_row(S1, list(range(6)), center=np.array([0, 1.2, 0]), spacing=2.05, unit=0.24, font_size=24)
        top1 = step_tiles(S1, size=0.42, font_size=22).move_to(2.85 * UP)
        assert_in_frame(row1, top1)
        self.play(FadeIn(top1))
        self.say("取其中一種，繞成一圈，從 6 個不同的地方開始走")
        for cell in row1:
            self.play(FadeIn(VGroup(cell[0], cell[1], cell[2])), run_time=0.55)
        self.wait(1)
        self.say("只看哪幾條一直在虛線上面")
        self.play(LaggedStartMap(FadeIn, row1.tags, lag_ratio=0.2), run_time=1.5)
        self.wait(1.5)
        c1 = mixed("總和是 1：6 種走法中恰好 1 種 ", "$\\Rightarrow$", " ", "$30/6=5$", "（就是 N14 的 5 種分法）", font_size=30)
        c1.move_to(1.6 * DOWN)
        assert_in_frame(c1)
        self.play(FadeIn(c1))
        self.wait(3.5)
        self.play(FadeOut(VGroup(row1, top1, c1)))

        # 3. t = 2
        self.say("再多一個 ", "$+1$", "：總和變成 2（", "$t=2$", "），排法 ", "$\\frac{7!}{5!\\,1!\\,1!}=42$", " 種")
        row2 = readings_row(S2, list(range(7)), center=np.array([0, 1.2, 0]), spacing=1.8, unit=0.21, font_size=22)
        top2 = step_tiles(S2, size=0.42, font_size=22).move_to(2.85 * UP)
        assert_in_frame(row2, top2)
        self.play(FadeIn(top2))
        self.play(LaggedStartMap(FadeIn, VGroup(*[VGroup(c[0], c[1], c[2]) for c in row2]), lag_ratio=0.15), run_time=2.5)
        self.play(LaggedStartMap(FadeIn, row2.tags, lag_ratio=0.2), run_time=1.5)
        c2 = mixed("總和是 2：7 種走法中恰好 2 種 ", "$\\Rightarrow$", " ", "$42\\times\\frac{2}{7}=12$", "（N15 的 12 種）", font_size=30)
        c2.move_to(1.6 * DOWN)
        assert_in_frame(c2)
        self.play(FadeIn(c2))
        self.say("規律：總和是 ", "$t$", "，就恰好有 ", "$t$", " 種走法一直在上面")
        self.wait(3.5)
        self.play(FadeOut(VGroup(row2, c2)))

        # 4. 為什麼恰好 t 種：光線
        self.say("為什麼？把這條路一圈接一圈重複畫下去")
        path = IntPathMob(S2 * 3, unit=0.36, origin=np.array([-5.6, -2.0, 0]), stroke_width=4, dot_radius=0.04)
        seps = VGroup(*[DashedLine(path.vertex(7 * p) + 0.4 * DOWN, path.vertex(7 * p) + 4.2 * UP, stroke_color=GREY_D,
                                   stroke_width=1.5) for p in (1, 2)])
        assert_in_frame(path)
        self.play(ShowCreation(path.steps, lag_ratio=1), FadeIn(path.dots), run_time=3)
        self.play(FadeIn(seps))
        self.say("每走一圈升高 ", "$t=2$", "；而往上每次最多走 1 格，所以一個高度都不會跳過")
        self.wait(3)
        x_right = path.vertex(21)[0] + 1.6
        rays, marks = VGroup(), VGroup()
        for p in range(3):
            for i in good_starts(S2):
                v = path.vertex(7 * p + i)
                rays.add(Arrow(np.array([x_right, v[1], 0]), v + 0.08 * RIGHT, buff=0, thickness=2.5, fill_color=TEAL_B))
                marks.add(Dot(v, radius=0.09, fill_color=ORANGE).set_z_index(3))
        assert_in_frame(rays)
        self.say("從右邊遠處照來水平的光：照得到的點（比後面每一點都低）就是好的起點")
        self.play(LaggedStartMap(GrowArrow, rays, lag_ratio=0.15), run_time=2.5)
        self.play(FadeIn(marks))
        self.wait(2)
        self.say("每一圈升高 ", "$t$", "、每格都有一個「最後一次到達」的點：每圈恰好照到 ", "$t$", " 個")
        self.wait(4)
        self.play(FadeOut(VGroup(path, seps, rays, marks, top2)))

        # 5. 總結：四種樣子
        self.say("最後把同一個東西的四種樣子放在一起")
        cfg2 = make_configuration(5, EX, radius=0.9, root=0)
        w2 = word_tiles(EX_WORD, size=0.4, font_size=24)
        tr2 = WordTreeMob(EX_WORD, x_gap=0.45, y_gap=0.55)
        wk2 = chu_walk(EX_WORD, unit=0.32)
        bs2 = level_line(wk2, 0, 0, 6, color=MAROON_B)
        pics = [cfg2, w2, tr2, VGroup(wk2, bs2)]
        names = ["Chu：圓周上的群組", "Raney：字", "平面樹", "走路：部分和"]
        cols = VGroup()
        for pic, name in zip(pics, names):
            col = VGroup(pic, zh(name, font_size=24)).arrange(DOWN, buff=0.35)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to(1.3 * UP)
        arr = VGroup(*[Tex(r"\leftrightarrow", font_size=40).move_to((cols[k][0].get_right() + cols[k + 1][0].get_left()) / 2)
                       for k in range(3)])
        fin = VGroup(
            boxed(mixed("$A_t(\\vec n)=\\dfrac{t}{N+t}\\times$", "（全部排法）", "$=\\dfrac{t}{N+t}\\dbinom{N+t}{\\vec n}$", font_size=30)),
            mixed("卡塔蘭：只有 ", "$\\pm1$", " 兩種步 ", "$\\Rightarrow$", " Dyck 路徑", font_size=28),
        ).arrange(DOWN, buff=0.25).move_to(1.85 * DOWN)
        assert_in_frame(cols, fin)
        for k, c in enumerate(cols):
            self.play(FadeIn(c), *([FadeIn(arr[k - 1])] if k else []), run_time=0.9)
            self.wait(0.6)
        self.wait(2)
        self.say("Chu 的好路徑、Raney 的字列、部分和全正的讀法：同一件事的三種說法")
        self.play(FadeIn(fin))
        self.wait(5)
        self.play(FadeOut(VGroup(cols, arr, fin)))
        self.clear_caption()
