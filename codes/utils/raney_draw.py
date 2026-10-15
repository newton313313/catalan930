"""
raney_draw.py —— 整數序列的 Raney 引理（動畫 R01–R06）用到的圖形

    IntPathMob(steps, unit, origin)   一條路徑：每步改變高度 x_j（任意整數）；.vertex(j)、.y_of(h)、.heights
    level_line(path, h, j0, j1)       在高度 h、第 j0 到 j1 點之間畫虛線
    step_tiles(seq)                   一排數字方塊（依步的值上色）
    CardMob(w)                        摸牌遊戲的牌：w ≥ 1 是特殊牌、0 是無用牌、None 是勝利牌
    draws_badge(k)                    「還能摸幾張」的小圓牌

顏色規則與 Chu 講義、lattice_paths.py 一致：步 x = 1 − v 對應 v 點群組，
所以 x = +1（↑ 步）灰、x = −1 藍（弦）、x = −2 橘（三角形）、x = −3 綠；x = 0 淺灰；x ≥ 2 黃（Chu 的路徑沒有這種步）。
"""
from manimlib import *

from utils.styles import block_color, zh

UP_COLOR = GREY_B
BIG_UP_COLOR = YELLOW_C
WIN_COLOR = GOLD_C
USELESS_COLOR = GREY_C


def step_color(x: int):
    if x == 1:
        return UP_COLOR
    if x >= 2:
        return BIG_UP_COLOR
    return block_color(1 - x)


class IntPathMob(VGroup):
    """
    一條路徑。origin 是第 0 點的位置（高度 start_height）。
    屬性：.steps（每步一條線段）、.dots、.heights（各點高度）
    方法：.vertex(j)（第 j 點目前的座標）、.y_of(h)（高度 h 目前在畫面上的 y）
    """

    def __init__(self, steps, unit: float = 0.4, origin=ORIGIN, start_height: int = 0,
                 stroke_width: float = 5, show_dots: bool = True, dot_radius: float = 0.05, colors=None):
        origin = np.array(origin, dtype=float)
        hs = [start_height]
        for x in steps:
            hs.append(hs[-1] + x)
        pts = [origin + unit * (j * RIGHT + (h - start_height) * UP) for j, h in enumerate(hs)]
        segs = VGroup(*[
            Line(pts[j], pts[j + 1], stroke_color=(colors[j] if colors else step_color(x)), stroke_width=stroke_width)
            for j, x in enumerate(steps)
        ])
        dots = VGroup()
        if show_dots:
            dots = VGroup(*[Dot(p, radius=dot_radius, fill_color=WHITE) for p in pts])
            dots.set_z_index(2)
        super().__init__(segs, dots)
        self.steps = segs
        self.dots = dots
        self.heights = hs
        self.unit = unit
        self.start_height = start_height
        self._anchor = Dot(origin, radius=0.001, fill_opacity=0, stroke_width=0)
        self.add(self._anchor)

    def vertex(self, j: int):
        """第 j 點目前的座標（整條路徑移動或縮放後也正確）。"""
        o = self._anchor.get_center()
        u = self.get_unit()
        return o + u * (j * RIGHT + (self.heights[j] - self.start_height) * UP)

    def get_unit(self) -> float:
        if len(self.steps) == 0:
            return self.unit
        seg = self.steps[0]
        return abs(seg.get_end()[0] - seg.get_start()[0])

    def y_of(self, h: float) -> float:
        return self._anchor.get_center()[1] + self.get_unit() * (h - self.start_height)


def level_line(path: IntPathMob, h: float, j0: float, j1: float, color=GREY_C, stroke_width: float = 2,
               dashed: bool = True) -> VMobject:
    x0 = path._anchor.get_center()[0] + path.get_unit() * j0
    x1 = path._anchor.get_center()[0] + path.get_unit() * j1
    y = path.y_of(h)
    cls = DashedLine if dashed else Line
    return cls(np.array([x0, y, 0]), np.array([x1, y, 0]), stroke_color=color, stroke_width=stroke_width)


def step_tiles(seq, size: float = 0.55, buff: float = 0.08, font_size: float = 30) -> VGroup:
    """一排方塊，每格寫一個步的值（Tex），邊框依值上色。"""
    tiles = VGroup()
    for x in seq:
        sq = Square(side_length=size, stroke_color=step_color(x), stroke_width=3,
                    fill_color=step_color(x), fill_opacity=0.18)
        lab = Tex(str(x), font_size=font_size).move_to(sq)
        tiles.add(VGroup(sq, lab))
    tiles.arrange(RIGHT, buff=buff)
    return tiles


class CardMob(VGroup):
    """
    摸牌遊戲的牌。w ≥ 1：特殊牌（寫 +w，顏色同 w 點群組）；w = 0：無用牌；w = None：勝利牌（星號）。
    label：牌的名字（例如 "S1"、"U1"），寫在牌的上緣。
    """

    def __init__(self, w, label: str = "", width: float = 0.8, height: float = 1.1, font_size: float = 30):
        if w is None:
            color, text = WIN_COLOR, r"\bigstar"
        elif w == 0:
            color, text = USELESS_COLOR, "0"
        else:
            color, text = block_color(w), "+%d" % w
        body = RoundedRectangle(width=width, height=height, corner_radius=0.1,
                                stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18)
        mark = Tex(text, font_size=font_size, fill_color=color if w is None else WHITE).move_to(body)
        parts = [body, mark]
        if label:
            lab = Tex(r"\mathrm{%s}" % label, font_size=font_size * 0.6, fill_color=GREY_A)
            lab.next_to(body.get_top(), DOWN, buff=0.06)
            mark.shift(0.08 * DOWN)
            parts.append(lab)
        super().__init__(*parts)
        self.w = w
        self.body = body


def draws_badge(k: int, radius: float = 0.24, font_size: float = 26) -> VGroup:
    """「還能摸 k 張」的小圓牌：k ≥ 1 綠、k = 0 紅。"""
    color = GREEN_C if k >= 1 else RED_C
    c = Circle(radius=radius, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.2)
    return VGroup(c, Tex(str(k), font_size=font_size).move_to(c))


def caption_zh(text: str, font_size: float = 26, color=GREY_A) -> Text:
    return zh(text, font_size=font_size, color=color)


def readings_row(seq, starts, center=ORIGIN, spacing: float = 2.5, unit: float = 0.22,
                 label_gap: float = 0.25, mark: str = "good", font_size: float = 26) -> VGroup:
    """
    把「從第 i 點開始讀」的路徑排成一列（i 取自 starts），各條路徑的第 0 點在同一高度，基線（高度 0）畫虛線。
    每格下方寫 i 與標記：mark = "good" 畫 ✓/✗（好讀法與否），"count" 寫正的點數，None 不畫。
    回傳 VGroup(cells)，每格是 VGroup(path, base, label, tag)，另有屬性 .paths、.tags。
    """
    from utils.raney import positive_count, reading
    center = np.array(center, dtype=float)
    n = len(starts)
    M = len(seq)
    x0 = center[0] - spacing * (n - 1) / 2 - unit * M / 2
    paths = [IntPathMob(reading(seq, i), unit=unit, origin=np.array([x0 + spacing * k, center[1], 0]),
                        stroke_width=4, dot_radius=0.035) for k, i in enumerate(starts)]
    low = min(p.get_bottom()[1] for p in paths)
    cells, tags = VGroup(), VGroup()
    for p, i in zip(paths, starts):
        base = level_line(p, 0, 0, M)
        lab = Tex("i=%d" % i, font_size=font_size)
        lab.move_to(np.array([p.vertex(0)[0] + unit * M / 2, low - label_gap, 0]))
        r = reading(seq, i)
        if mark == "good":
            ok = positive_count(r) == M
            tag = Tex(r"\checkmark" if ok else r"\times", font_size=font_size * 1.2,
                      fill_color=GREEN if ok else RED)
        elif mark == "count":
            tag = Tex(str(positive_count(r)), font_size=font_size * 1.2, fill_color=YELLOW)
        else:
            tag = VGroup()
        tag.next_to(lab, DOWN, buff=0.12)
        cells.add(VGroup(p, base, lab, tag))
        tags.add(tag)
    cells.paths = paths
    cells.tags = tags
    return cells
