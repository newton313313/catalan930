"""
Scene N12 —— 總結：Raney (1960) 的邏輯與 Chu 講義的對照（Raney 導讀第 15 節）
執行（在 codes/ 內）：manimgl scenes/sceneN12_summary.py SceneN12Summary

1. 流程圖：前序記法與字 → 循環引理 → L = (n/m)M → 切開／第一個符號 → L* 的方程 → 三種代換（Lagrange、Chu／三項式、卷積）。
2. 對照表：Chu 講義第 4–8 節 ↔ Raney 的定理。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import raney_A
from utils.fulton_draw import assert_in_frame
from utils.raney import L_formula
from utils.scene_base import ChuScene
from utils.styles import mixed, zh


def check_math():
    assert L_formula(2, (0, 1, 1)) == raney_A(2, (1, 1), (2, 3)) == 12


def node(*parts, color=BLUE_B, width=4.6, font_size=24):
    t = mixed(*parts, font_size=font_size)
    box = RoundedRectangle(width=max(width, t.get_width() + 0.4), height=t.get_height() + 0.3, corner_radius=0.12,
                           stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.08)
    return VGroup(box, t.move_to(box))


class SceneN12Summary(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N12　總結")

        chain = VGroup(
            node("前序記法 ", "$\\to$", " 字；秩、Rosenbloom 判別法"),
            node("定理 2.1：循環引理"),
            node("定理 2.2：", "$L(n;a)=\\frac{n}{m}M$"),
            node("定理 2.3（切開）、2.4（第一個符號）"),
            node("定理 4.1：", "$L^*=\\sum_iE_i(L^*)^i$"),
        ).arrange(DOWN, buff=0.2).move_to(np.array([0, 0.95, 0]))
        arrows = VGroup(*[Arrow(chain[k].get_bottom(), chain[k + 1].get_top(), buff=0.04, stroke_width=3,
                                max_tip_length_to_length_ratio=0.35) for k in range(4)])
        apps = VGroup(
            node("§5 Lagrange 反演", color=ORANGE, width=3.6),
            node("§6 三項式、Chu 的 (6)", color=ORANGE, width=3.6),
            node("§7 卷積：Abel、Hagen–Rothe", color=ORANGE, width=3.6),
        ).arrange(RIGHT, buff=0.35).next_to(chain, DOWN, buff=0.45)
        arr2 = VGroup(*[Arrow(chain[-1].get_bottom(), a.get_top(), buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.2)
                        for a in apps])
        assert_in_frame(chain, apps)
        self.say("Raney (1960) 的邏輯：藍框是組合，橘框是用代換 ", "$H$", " 得到的應用")
        for k, b in enumerate(chain):
            self.play(FadeIn(b, shift=0.1 * DOWN), *( [GrowArrow(arrows[k - 1])] if k else []), run_time=0.8)
        self.play(*[GrowArrow(a) for a in arr2], LaggedStartMap(FadeIn, apps, lag_ratio=0.3), run_time=1.8)
        self.wait(3)
        self.play(FadeOut(VGroup(chain, arrows, apps, arr2)))

        left_parts = [["第 4 節：固定一個點、遞迴"], ["第 5 節：", "$D=1+\\sum x_iD^{v_i}$"],
                      ["第 6 節：", "$[x^{\\vec n}]C^t=A_t(\\vec n)$", "、收尾"], ["第 7.1 節：路徑與好路徑"],
                      ["第 7.2 節：循環引理"], ["第 7.3 節：雙重計數"], ["第 7.4 節：切成兩段"], ["第 8.3 節：Lagrange 反演"]]
        right_parts = [["定理 2.4（組合版本）；分法 ↔ 字（N05）"], ["定理 4.1 在代換 ", "$E_{v_i}\\mapsto x_i$", " 下的影像"],
                       ["定理 4.1＋2.2；定理 2.4（", "$k=0$", "）"], ["字列倒過來讀（N03）"], ["定理 2.1（證明方法不同，N04）"],
                       ["定理 2.2 的證明（N05）"], ["定理 2.3（N07）"], ["§5（單變數，N09）"]]
        assert len(left_parts) == len(right_parts)
        head = VGroup(zh("Chu 講義", font_size=26, color=YELLOW), zh("Raney (1960)", font_size=26, color=YELLOW))
        table = VGroup()
        y0 = 2.35
        head[0].move_to(np.array([-3.2, y0, 0]))
        head[1].move_to(np.array([2.8, y0, 0]))
        for k, (lp, rp) in enumerate(zip(left_parts, right_parts)):
            l = mixed(*lp, font_size=22)
            r = mixed(*rp, font_size=22)
            y = y0 - 0.6 * (k + 1)
            l.move_to(np.array([0, y, 0])).align_to(np.array([-6.3, 0, 0]), LEFT)
            r.move_to(np.array([0, y, 0])).align_to(np.array([0.2, 0, 0]), LEFT)
            table.add(VGroup(l, r))
        line = Line(np.array([-6.4, y0 - 0.3, 0]), np.array([6.4, y0 - 0.3, 0]), stroke_color=GREY_C, stroke_width=1.5)
        assert_in_frame(head, table)
        self.say("和 Chu 講義的對照：Chu 的每一步都能在 Raney 的論文裡找到")
        self.play(FadeIn(head), ShowCreation(line))
        self.play(LaggedStartMap(FadeIn, table, lag_ratio=0.25), run_time=4)
        self.wait(3)
        self.say("講義：", "notes/raney1960_導讀.pdf", "；例題產生器：", "utils/raney_examples.py")
        self.wait(3)
