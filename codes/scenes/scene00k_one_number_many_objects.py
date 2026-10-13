"""
Scene 00k —— 同一個 5：六種不同的東西，同一個遞迴結構

    C_3 = 5：五邊形的三角剖分、4 個因子的括法、3 個內部節點的滿二元樹、
             不越過對角線的格子路徑、半長 3 的 Dyck 路徑、圓周 6 點的不交叉配對
同一組裡的第 j 個，全部由同一棵樹產生（counting.py 第 5 節），彼此一一對應。

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00k_one_number_many_objects.py Scene00kOneNumberManyObjects
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    FAMILIES,
    FAMILY_NAMES,
    LEFT_COLOR,
    RIGHT_COLOR,
    catalan_item,
)
from utils.counting import binary_trees, catalan
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, ROOT_COLOR, YELLOW, mixed, zh

SCALE = 0.85
COLUMN_X = {"left": -4.4, "right": 4.4}
ROW_Y = [2.0, 0.1, -1.85]
LAYOUT = {                      # 家族 -> (左/右欄, 第幾列)
    "triangulation": ("left", 0),
    "parens": ("left", 1),
    "tree": ("left", 2),
    "lattice": ("right", 0),
    "dyck": ("right", 1),
    "matching": ("right", 2),
}
HIGHLIGHT = 2                   # 先上色的那一個：(a·b)·(c·d) 這一棵樹


def arrange_items(family: str, items: VGroup) -> VGroup:
    """一般排成一列；括號太寬，排成 3 + 2 兩列。"""
    if family == "parens":
        top = VGroup(*items[:3]).arrange(RIGHT, buff=0.3)
        bottom = VGroup(*items[3:]).arrange(RIGHT, buff=0.3)
        VGroup(top, bottom).arrange(DOWN, buff=0.22)
    else:
        items.arrange(RIGHT, buff=0.16)
    return items


class Scene00kOneNumberManyObjects(ChuScene):
    def construct(self):
        self.show_header("同一個 5")
        trees = binary_trees(3)
        assert len(trees) == catalan(3) == 5

        five = Tex("5", font_size=180, fill_color=YELLOW)
        five_box = SurroundingRectangle(five, buff=0.3, color=YELLOW, stroke_width=4)
        center = VGroup(five_box, five).move_to(0.15 * UP)
        self.say("同一個數 5，出現在六種看起來完全不同的東西裡")
        self.play(Write(five), ShowCreation(five_box), run_time=1.2)

        groups = {}
        for family in FAMILIES:
            items = VGroup(*[catalan_item(family, t, scale=SCALE) for t in trees])
            arrange_items(family, items)
            side, row = LAYOUT[family]
            items.move_to(np.array([COLUMN_X[side], ROW_Y[row], 0.0]))
            label = zh(FAMILY_NAMES[family], font_size=20, color=MUTED_COLOR)
            label.next_to(items, UP, buff=0.14)
            groups[family] = (items, label)

        for family in FAMILIES:
            items, label = groups[family]
            self.play(FadeIn(label, shift=0.1 * DOWN),
                      LaggedStart(*[FadeIn(i, scale=0.7) for i in items], lag_ratio=0.12), run_time=1.0)
        self.say("每一種都恰好 5 個：", "$C_3=5$")
        self.play(Indicate(five, scale_factor=1.15, color=YELLOW), run_time=0.8)
        self.wait(1.2)

        # ------------------------------------------------------------ 一一對應：同一棵樹
        self.say("而且它們一一對應：每一組裡的這一個，都是同一個結構的不同樣子")
        frames = VGroup()
        for family in FAMILIES:
            items, _ = groups[family]
            frames.add(SurroundingRectangle(items[HIGHLIGHT], buff=0.08, color=YELLOW, stroke_width=2.5))
        self.play(LaggedStart(*[ShowCreation(f) for f in frames], lag_ratio=0.12), run_time=1.2)
        self.wait(0.6)
        recolor = []
        for family in FAMILIES:
            items, _ = groups[family]
            target = catalan_item(family, trees[HIGHLIGHT], scale=SCALE, colored=True).move_to(items[HIGHLIGHT])
            recolor.append(Transform(items[HIGHLIGHT], target))
        legend = VGroup(
            mixed("橘：根", font_size=22, color=ROOT_COLOR),
            mixed("青：左邊的小結構", font_size=22, color=LEFT_COLOR),
            mixed("粉紅：右邊的小結構", font_size=22, color=RIGHT_COLOR),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        legend.move_to(np.array([0.0, -1.85, 0.0]))
        self.say("拆開來看：每一個都是「一個根」加上「左、右兩個獨立的小卡塔蘭結構」")
        self.play(*recolor, FadeIn(legend), run_time=1.4)
        self.wait(2.5)

        # 全部上色
        self.say("其他四個也一樣，每一組都能這樣一一對上")
        anims = []
        for family in FAMILIES:
            items, _ = groups[family]
            for j, t in enumerate(trees):
                if j == HIGHLIGHT:
                    continue
                target = catalan_item(family, t, scale=SCALE, colored=True).move_to(items[j])
                anims.append(Transform(items[j], target))
        self.play(*anims, FadeOut(frames), run_time=1.6)
        self.wait(1.5)

        # ------------------------------------------------------------ 結論
        c3 = Tex("C_3=5", font_size=72, fill_color=YELLOW)
        motto = VGroup(zh("不同的物件，", font_size=30), zh("同一個遞迴結構", font_size=30)).arrange(DOWN, buff=0.12)
        new_center = VGroup(c3, motto).arrange(DOWN, buff=0.35).move_to(0.35 * UP)
        new_box = SurroundingRectangle(new_center, buff=0.25, color=YELLOW, stroke_width=4)
        self.play(FadeOut(legend), ReplacementTransform(five, c3), ReplacementTransform(five_box, new_box),
                  FadeIn(motto, shift=0.2 * UP), run_time=1.2)
        self.say("卡塔蘭數數的，是「可以遞迴拆成兩半」的不交叉或二元結構")
        self.wait(3.0)
