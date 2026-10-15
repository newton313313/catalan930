"""
Scene R05 —— 例題二：摸牌（洛谷 P6672）＝ Raney 的字（notes/ran_note015_改寫.pdf 第 6 節）
執行（在 codes/ 內）：manimgl scenes/sceneR05_card_game.py SceneR05CardGame

規則：m+1 張有標號的牌；n 張特殊牌（摸到第 i 張再摸 w_i 張，w_i ≥ 1，Σw_i = m）、m−n 張無用牌、最底下一張勝利牌；一開始摸 1 張。
例 w = (1,2)、m = 3：S1(+1)、S2(+2)、U1、★。
1. 合格的牌序 S2 U1 S1：還能摸 1→2→1→1，摸到 ★；不合格的 U1 開頭：還能摸 0。
2. 「還能摸幾張」= Raney 的「還欠幾個引數」= 開頭的秩 + 1：合格的牌序（加上 ★）就是以 ★ 結尾的字；三種是 1200、2100、2010。
3. 數：(m+1)! 種排成一圈，每圈恰有一種讀法是字 → m! 個字；字的最後一張是 m−n+1 張「0 牌」之一，對稱 → m!/(m−n+1)。
4. 原筆記「加一個 −1、取負號、倒過來」= Raney 導讀第 4.5 節的換算；公式的 n 只算 w_i ≥ 1 的牌。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import card_game_brute, card_game_formula, draws_left, is_word
from utils.raney_draw import CardMob, draws_badge
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

W = (1, 2)
M = 3
VAL = {"S1": 1, "S2": 2, "U1": 0}
GOOD = ("S2", "U1", "S1")
BAD = ("U1", "S1", "S2")
TABLE = [((3,), 3), ((1, 2), 3), ((2, 2), 4), ((1, 1, 2), 4), ((2, 3), 5)]


def check_math():
    decks = card_game_brute(W, M)
    assert len(decks) == 3 == card_game_formula(W, M) and GOOD in decks and BAD not in decks
    assert draws_left([VAL[c] for c in GOOD]) == [1, 2, 1, 1]
    assert draws_left([VAL[c] for c in BAD])[1] == 0
    words = sorted("".join(str(VAL[c]) for c in d) + "0" for d in decks)
    assert words == ["1200", "2010", "2100"] and all(is_word(tuple(map(int, w))) for w in words)
    for w, m in TABLE:
        assert len(card_game_brute(w, m)) == card_game_formula(w, m)
    assert card_game_formula((0, 3), 3) == 2


def deck_row(order, y: float, x0: float = -2.4, gap: float = 1.25, with_win: bool = True) -> VGroup:
    cards = [CardMob(VAL[c], c) for c in order] + ([CardMob(None, "")] if with_win else [])
    row = VGroup(*cards)
    for k, c in enumerate(row):
        c.move_to(np.array([x0 + gap * k, y, 0]))
    return row


class SceneR05CardGame(ChuScene):
    def construct(self):
        check_math()
        self.show_header("R05　例題二：摸牌遊戲就是 Raney 的字")

        # 0. 規則
        legend = VGroup(
            VGroup(CardMob(2, "S"), mixed("特殊牌：摸到再摸 ", "$w_i$", " 張（", "$w_i\\ge 1$", "）", font_size=26)).arrange(RIGHT, buff=0.3),
            VGroup(CardMob(0, "U"), zh("無用牌", font_size=26)).arrange(RIGHT, buff=0.3),
            VGroup(CardMob(None, ""), zh("勝利牌（在最底下）", font_size=26)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([-3.0, 0.6, 0]))
        rule = VGroup(mixed("$\\sum w_i=m$", "，共 ", "$m+1$", " 張", font_size=28),
                      zh("一開始可以摸 1 張", font_size=28),
                      zh("問：前 m 張怎麼排才摸得到勝利牌？", font_size=28)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rule.move_to(np.array([3.75, 0.6, 0]))
        assert_in_frame(legend, rule)
        assert_apart(legend, rule)
        self.say("洛谷 P6672：牌都有標號")
        self.play(LaggedStartMap(FadeIn, legend, lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(rule), run_time=1.2)
        self.wait(3)
        self.play(FadeOut(VGroup(legend, rule)))

        # 1. 模擬
        title = mixed("例：", "$w=(1,2)$", "、", "$m=3$", font_size=30).move_to(np.array([-4.6, 2.5, 0]))
        row = deck_row(GOOD, 0.6)
        badge_lab = zh("還能摸", font_size=24, color=GREY_A)
        badges = [draws_badge(k) for k in draws_left([VAL[c] for c in GOOD])]
        for k, b in enumerate(badges):
            b.move_to(row[k].get_center() + 1.15 * UP + (0.62 * LEFT if k == 0 else 0.62 * RIGHT - 1.25 * RIGHT))
        positions = [row[0].get_center() + 1.15 * UP + 0.62 * LEFT] + [row[k - 1].get_center() + 1.15 * UP + 0.62 * RIGHT
                                                                      for k in range(1, len(badges))]
        for b, p in zip(badges, positions):
            b.move_to(p)
        badge_lab.next_to(badges[0], LEFT, buff=0.2)
        assert_in_frame(title, row, badge_lab, *badges)
        self.say("照 S2、U1、S1 的順序摸：圓圈裡是「還能摸幾張」")
        self.play(FadeIn(title), LaggedStartMap(FadeIn, row, lag_ratio=0.15), run_time=1.5)
        self.play(FadeIn(badge_lab), FadeIn(badges[0]))
        for k in range(1, len(badges)):
            self.play(Indicate(row[k - 1], color=YELLOW, scale_factor=1.08), FadeIn(badges[k]), run_time=0.9)
        win = zh("摸到勝利牌！", font_size=28, color=GOLD_C).next_to(row[-1], DOWN, buff=0.35)
        self.play(Indicate(row[-1], color=GOLD_C), FadeIn(win))
        self.wait(1.5)
        bad = deck_row(BAD, -1.9)
        bb = [draws_badge(k) for k in draws_left([VAL[c] for c in BAD])[:2]]
        bb[0].move_to(bad[0].get_center() + 0.62 * LEFT + 0.75 * UP)
        bb[1].move_to(bad[0].get_center() + 0.62 * RIGHT + 0.75 * UP)
        lose = zh("沒得摸了", font_size=26, color=RED_C).next_to(bad, RIGHT, buff=0.3)
        assert_in_frame(bad, lose, *bb)
        self.say("若第一張是無用牌：還能摸 ", "$0$", " 張，輸了")
        self.play(FadeIn(bad), FadeIn(bb[0]))
        self.play(Indicate(bad[0], color=RED), FadeIn(bb[1]), FadeIn(lose))
        self.wait(2)
        self.play(FadeOut(VGroup(bad, lose, *bb, win)))

        # 2. Raney 的字
        syms = VGroup(*[Tex(str(c.w if c.w is not None else 0), font_size=40, fill_color=YELLOW).next_to(c, DOWN, buff=0.3)
                        for c in row])
        rank_note = VGroup(
            mixed("還能摸幾張 ", "$=$", " 還欠幾個引數 ", "$=$", " 開頭的秩 ", "$+1$", font_size=28),
            mixed("合格 ", "$\\Leftrightarrow$", " 牌序（加上勝利牌）是 Raney 的字，而且最後一個是勝利牌", font_size=28),
        ).arrange(DOWN, buff=0.3).move_to(1.85 * DOWN)
        assert_in_frame(syms, rank_note)
        self.say("把每張牌換成 Raney 的符號：特殊牌 ", "$\\to w_i$", "、無用牌與勝利牌 ", "$\\to 0$")
        self.play(LaggedStartMap(FadeIn, syms, lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(rank_note[0]))
        self.wait(1.5)
        self.play(FadeIn(rank_note[1]))
        self.wait(2.5)
        self.play(FadeOut(VGroup(row, syms, rank_note, *badges, badge_lab, title)))

        decks = card_game_brute(W, M)
        rows = VGroup()
        for d in decks:
            r = VGroup(*[CardMob(VAL[c], c, width=0.62, height=0.85, font_size=24) for c in d] +
                       [CardMob(None, "", width=0.62, height=0.85, font_size=24)]).arrange(RIGHT, buff=0.15)
            word = Tex("".join(str(VAL[c]) for c in d) + "0", font_size=34, fill_color=YELLOW).next_to(r, DOWN, buff=0.2)
            rows.add(VGroup(r, word))
        rows.arrange(RIGHT, buff=0.9).move_to(1.1 * UP)
        assert_in_frame(rows)
        self.say("合格的牌序恰有 3 種，對應三個字 ", "$1200$", "、", "$2100$", "、", "$2010$")
        self.play(LaggedStartMap(FadeIn, rows, lag_ratio=0.3), run_time=2)
        self.wait(2)

        # 3. 數
        self.play(rows.animate.scale(0.75).move_to(2.3 * UP), run_time=0.8)
        count = VGroup(
            mixed("$m+1$", " 張有標號的牌排成一圈：", "$(m+1)!$", " 種", font_size=28),
            mixed("Raney 引理：每圈恰有一種讀法是字 ", "$\\Rightarrow$", " 字有 ", "$m!$", " 個", font_size=28),
            mixed("字的最後一張是 ", "$m-n+1$", " 張「0 牌」之一，交換標號可知一樣多", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(rows, DOWN, buff=0.55)
        ans = Tex(r"\frac{m!}{m-n+1}\qquad\text{e.g. }\frac{3!}{3-2+1}=3", font_size=40)
        box = boxed(ans, color=YELLOW).next_to(count, DOWN, buff=0.35)
        assert_in_frame(count, box)
        self.say("一般的情形：循環引理＋對稱性")
        self.play(LaggedStartMap(FadeIn, count, lag_ratio=0.5), run_time=3)
        self.play(FadeIn(box))
        self.wait(3)

        # 4. 原筆記的做法、條件
        self.play(FadeOut(VGroup(rows, count, box)))
        notes = VGroup(
            mixed("原筆記：末尾加一個 ", "$-1$", "、取負號、倒過來", font_size=28),
            mixed("$=$", " Raney 的字倒過來讀、符號 ", "$j\\to 1-j$", "：Chu 講義的好路徑", font_size=28),
            mixed("公式的 ", "$n$", " 只能算 ", "$w_i\\ge 1$", " 的牌（", "$w_i=0$", " 的牌是無用牌）", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(1.4 * UP)
        tab = VGroup(*[Tex(r"w=(%s),\ m=%d:\ %d=\frac{%d!}{%d}" % (",".join(map(str, w)), m, card_game_formula(w, m), m,
                                                                     m - len(w) + 1), font_size=30)
                       for w, m in TABLE]).arrange_in_grid(n_cols=2, h_buff=0.9, v_buff=0.22, aligned_edge=LEFT)
        tab.next_to(notes, DOWN, buff=0.5)
        assert_in_frame(notes, tab)
        self.say("小例子都和窮舉一致（牌有標號）")
        self.play(LaggedStartMap(FadeIn, notes, lag_ratio=0.5), run_time=3)
        self.play(FadeIn(tab), run_time=1.2)
        self.wait(3)
