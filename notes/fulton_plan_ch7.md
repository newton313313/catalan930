# Fulton《Young Tableaux》第 7 章 → Manim：定稿大綱（省 token 版，2026-10-12）

**路徑的寫法：** 本檔的相對路徑相對於 `C:\mypython\manim\projects\catalan930`。
**權威順序：** 本檔 ＞ `C:\mypython\manim\projects\ref\fulton78_manim_大綱_合併版.md`（詳細分鏡，只在本檔沒寫清楚時用 `rg "### F7xx"` 查那一張卡）＞ 原文。

## 0. 調整說明（為什麼這樣省）
| 調整 | 原大綱 | 定稿 | 省在哪裡 |
|---|---|---|---|
| 篇幅 | 31 幕、主線 82 分＋延伸 19 分 | 14 幕、約 40 分 | 程式碼量與渲染次數約減半；數學內容一項不刪 |
| 與舊影片重複 | F713 對稱函數、X701 鉤長、X704 LR、F709 平方和 | 各縮成一句回顧（字幕註明「見 F25–F27／M13、F19／F20–F24／F16」） | 不重做已有動畫 |
| 工作包 | `projects/fulton7_agent_pack/fulton7_agent_pack/`（已存在，`tools/selfcheck.py` 通過） | **只取兩樣**：`MATH_DATA.json`（已驗證的固定算例）與 `scene_cards/F7xx.md`（每張約 1.6 KB）；不照它的資料夾結構、不用 STATE／context.py | 第 9 節不必從頭寫；代理人只讀自己的 2–3 張小卡 |
| 代理人讀什麼 | 完整版大綱與範本場景 | 本檔第 2–5 節＋自己場景對應的 `scene_cards/*.md` | 每個代理人少讀約 15–20k tokens |
| 檢查圖 | 4×3、每格 640px | `render_check.py --tile 480`（4×3） | 每張總覽圖少約三分之一 |
| 第 8 章 | F800–F803 | 第 7 章完成後再決定 | 不做可能用不到的東西 |

不變的原則：數學正確優先；每個畫面上的數字都由程式算出並 assert；Fulton 記號；獨立的一組（`FultonDemo4`），不覆寫舊影片。
用詞：字幕用「列（row）／行（column）」，與 F01–F27 一致（原大綱的「橫行／直欄」同義）。

## 1. 步驟
| 步驟 | 內容 | 誰 |
|---|---|---|
| 1 | 把工作包的 `MATH_DATA.json` 複製成 `codes/data/fulton7_math.json`；寫 `codes/utils/rep_data.py`：`load(key)` 讀資料，`check()` 用 `tableaux.py` 獨立重算交叉核對（`character_table`、`kostka`、`standard_tableaux`、`lr_coefficient`、`hook_product`），並補資料沒有的小函式（置換合成、tabloid 作用）。場景一律從 `rep_data` 取數 | 主對話 |
| 2 | `codes/utils/rep_draw.py`：tabloid 卡、帶號的線性組合列、「像 → 矩陣欄」、置換箭頭；先做一個試渲染 | 主對話 |
| 3 | 4 個代理人平行：A＝F28–F31、B＝F32–F35、C＝F36–F38、D＝F39–F41 | 代理人 |
| 4 | 看總覽圖、整合（`main.py` 的 `FULTON4_SCENES`／`FultonDemo4`、`render_all.py --fulton4`、`--fulton4-demo`）、1080p、文件、combkit 1.3.0 | 主對話 |

## 2. 固定算例（資料鍵在 `MATH_DATA.json`：`shape21`、`shape32`、`collision`、`plane21`、`matrices21`、`character_S3`、`permutation_char32`、`young221`、`symmetric_functions`、`frobenius21`、`branching`、`straightening21`、`straightening32`、`young_symmetrizer21`、`hooks`、`specht_polynomial21`、`mod3`、`LR_example`；下列數字已與工作包核對一致）
- **主例** $\lambda=(2,1)$：$T_a=12/3$、$T_b=13/2$；$t_i$ = 第二列是 $i$ 的 tabloid；$v_a=t_3-t_1$、$v_b=t_2-t_1$；
  $\rho(12)=\begin{psmallmatrix}1&0\\-1&-1\end{psmallmatrix}$、$\rho(23)=\begin{psmallmatrix}0&1\\1&0\end{psmallmatrix}$（第 $j$ 欄＝第 $j$ 個基底的像）；$\chi^{(2,1)}=2,0,-1$（類 $(1^3),(2,1),(3)$，大小 1、3、2）；
  $M^{(2,1)}$ 的特徵標 $3,1,0$；$c_{T_a}=(1-(13))(1+(12))$，$c^2=3c$。
- **較大形狀** $\lambda=(3,2)$：$\tilde\lambda=(2,2,1)$、$f=5$、$\#R=12$、$\#C=4$、$\dim M=10$、$n_\lambda=24$；兩輪 straightening $[125/43]=[125/34]-[135/24]$。
- **重數** $\mu=(2,2,1)$：$\dim M^\mu=30=1+2\cdot4+2\cdot5+6+5$（$K=1,2,2,1,1$ 對 $(5),(4,1),(3,2),(3,1,1),(2,2,1)$）。
- 其他：$[x_1^3x_2^2](x_1^2+x_2^2)^2(x_1+x_2)=2$；$\operatorname{Ind}_{S_3}^{S_4}S^{(2,1)}=S^{(3,1)}\oplus S^{(2,2)}\oplus S^{(2,1,1)}$（$8=3+2+3$）；
  mod 3：$\alpha=\begin{psmallmatrix}2&-1\\-1&2\end{psmallmatrix}$、$\beta=\begin{psmallmatrix}2&1\\1&2\end{psmallmatrix}$、$\alpha\beta=3I$；$F_{21/3}=F_{12/3}-F_{13/2}$。

## 3. 場景卡（14 幕；括號內是原大綱卡號，查細節用）
| 代號 | 主題（原卡） | 內容要點 | 長度 |
|---|---|---|---|
| F28 | 三張卡片、六種排列（F700、F701） | 鉤子：洗三張卡；$t_1,t_2,t_3$ 三軸，置換＝換座標；共同變化（直線）與相對變化（零和平面）；穩定子空間、直和、不可約；Maschke 一行（平均化投影）、Schur 引理一句；預告 $3=1+2$、$6=1+2\cdot2+1$（兩個計數窗分開，1、2、1 是維度） | 150s |
| F29 | 座位表與兩種洗牌（F702、F703） | $(3,2)$ 與共軛 $(2,2,1)$；$(2,1)$ 的 6 個編號挑出 2 個標準表；$(3,2)$ 的 5 個；$R(T)$（藍）、$C(T)$（橙）；$a_T=1+(12)$、$b_T=1-(13)$、$c_T=b_Ta_T$ 展開四項；$R(\sigma T)=\sigma R(T)\sigma^{-1}$；$(3,2)$ 只報 $\#R=12$、$\#C=4$ | 150s |
| F30 | 碰撞相消與支配序（F704） | $T=12/3$、$T'=123$ 共用 $\{1,3\}$：$b_T\tau=-b_T$、$\tau\{T'\}=\{T'\}$ ⇒ $b_T\{T'\}=0$（正負項配對消失）；$(3,2)$ 對 $(4,1)$ 的碰撞；無碰撞 ⇒ 支配（前綴容量圖）；$(3,3)$ 與 $(4,1,1)$ 不可比（同 F12，一句帶過） | 120s |
| F31 | tabloid、零和平面、polytabloid（F705、F706、F707） | 6 個編號壓成 3 張 tabloid；$(12)$、$(23)$ 怎麼搬卡；$\dim M^\lambda=n!/\prod\lambda_i!$（3、10）；$x=$ 平均$\cdot z$ ＋零和部分；正交座標畫等邊三角形；$v_a=t_3-t_1$、$v_b=t_2-t_1$ 是兩條邊差；其餘 4 個 $v_T$ 都在平面上 ⇒ $S^{(2,1)}=W$，$M^{(2,1)}=\mathbb Cz\oplus W$；$\sigma v_T=v_{\sigma T}$ | 180s |
| F32 | 不可約與標準基底（F708、F709） | 零和平面沒有共同的特徵直線（兩個反射的特徵線不同）；一般證明：$b_TM^\lambda=\mathbb Cv_T$ ⇒ 不可分解；Sagan 的二分（含 $S^\lambda$ 或在 $(S^\lambda)^\perp$）一句；三種形狀↔三個類；標準 $v_T$ 獨立（首項三角形）＋ $\sum(f^\lambda)^2=n!$（見 F16）⇒ 基底，$\dim S^\lambda=f^\lambda$ | 150s |
| F33 | 矩陣與特徵標（F710、F711） | 逐欄算 $\rho(12)$：$(12)T_b=23/1$ 排行帶負號 → $-v_b$；$(12)T_a$ 用 tabloid 差 → $v_a-v_b$；$\rho(23)$ 交換兩欄；$A^2=B^2=I$、$ABA=BAB$；切到正交座標看兩個反射、$AB$ 是 120° 旋轉（標明換座標）；按類取跡 $2,0,-1$；平凡、sign 兩列；內積 $(4+0+2)/6=1$；$M^{(2,1)}$ 的 $3,1,0$ 減平凡列 | 180s |
| F34 | 置換模組的特徵標與 Young's rule（F712、F714、X705 精簡） | $\sigma=(12)(34)(5)$ 在 $(3,2)$：循環整隊放進一列 → 固定的 tabloid 只有 $125/34$、$345/12$ → $\xi=[x^\lambda]p_\mu=2$；回 $S_3$：$\xi^{(2,1)}_{(2,1)}=1$ 但 $\chi=0$；Young's rule：$M^{(2,1)}=S^{(3)}\oplus S^{(2,1)}$（表 112、11/2）；$\mu=(2,2,1)$ 的 7 個半標準表 → $M=S^5\oplus2S^{41}\oplus2S^{32}\oplus S^{311}\oplus S^{221}$、$30$ 的驗算；半標準表＝$\operatorname{Hom}(S^\lambda,M^\mu)$ 的基底（$\theta_T$ 一例：$T=112$ 給 $t_1+t_2+t_3$） | 180s |
| F35 | 誘導積與 Fulton 的字典（F715、F716、F713 回顧、X704 精簡） | 兩桌標號 → 合併洗牌 → $V\circ W=\operatorname{Ind}(V\otimes W)$；$\mathbb I_1\circ\mathbb I_1=S^{(2)}\oplus S^{(1,1)}$ 對 $h_1^2=s_2+s_{11}$；與同一 $S_n$ 的張量積區分（一句）；$h,e,p,s$ 回顧一句（見 F25–F27）；$\varphi(h_\lambda)=[M^\lambda]$、$\varphi(s_\lambda)=[S^\lambda]$、$\psi$；三角形展開＋等距 ⇒ 非對角係數為 0；LR：$S^{21}\circ S^{21}\supset2S^{321}$（兩個 LR 斜表，見 F23）；Hopf 一句 | 180s |
| F36 | Frobenius 特徵標公式（F717） | $\ell=(3,1)$、收集槽 $x_1^3x_2$；三個類各算一次得 $2,0,-1$（與 F33 對上）；$s_{21}=(p_1^3-p_3)/3$ 由 $\chi$ 與 $z=6,2,3$ 組回；負號的意義 | 150s |
| F37 | 分支律與轉置（F718、F719） | 最大標號在角格；$\operatorname{Res}S^{(2,1)}=S^{(2)}\oplus S^{(1,1)}$ 用特徵向量 $2v_a-v_b$、$v_b$（$+1$、$-1$）看；Young 格 0–4 格；$\operatorname{Ind}$ 到 $S_4$：$8=3+2+3$；$S^\lambda\otimes\mathbb U_n\cong S^{\tilde\lambda}$：$S_3$ 特徵標乘 sign、$\omega(s_\lambda)=s_{\tilde\lambda}$、$(3,2)\leftrightarrow(2,2,1)$ | 150s |
| F38 | 帶方向的行 tabloid 與交換關係（F720、F721） | 列 tabloid 無號、行 tabloid $[qT]=\operatorname{sgn}(q)[T]$；$\tilde v_T=a_T[T]$、$\alpha([T])=v_T$、$\beta(\{T\})=\tilde v_T$；「以下等式在商空間中」；$[21/3]=[12/3]-[13/2]$（第二項排行出現明確的 $-1$）；作用 $\alpha$ 回到 F33 的 $v_a-v_b$；Garnir 一句 | 150s |
| F39 | 兩輪 straightening 與 kernel（F722、F723） | $[125/43]$：第一輪修好下列卻弄壞上列，第二輪得 $[125/34]-[135/24]$、座標 $(0,0,1,0,-1)$；Fulton 的序保證停止（不是「下降數減少」）；$Q\subseteq\ker\alpha$（碰撞相消、包含排除係數 $-1,0,+1$）＋ $\dim\le f$ ＋滿射 ⇒ $\ker\alpha=Q^\lambda$ | 180s |
| F40 | Young 對稱化子、多項式模型、模 3（F724、X703、X702） | $c^2=3c$（合併計數表，不播 16 個乘法）；$c/3$ 才是冪等；$n_\lambda=n!/f^\lambda$＝鉤長乘積（$(3,2)$：24，見 M13）；$F_T$：$F_{12/3}=x_1-x_3$、$F_{13/2}=x_1-x_2$、$F_{21/3}=F_{12/3}-F_{13/2}$；模 3：$c\ne0$ 但 $c^2=0$，$v_a+v_b$ 是平凡線、對偶版本沒有 ⇒ 不同構；$\alpha\beta=3I$ | 150s |
| F41 | 四個視角拼成一件事（F725） | $\lambda=(2,1)$ 居中，四角：tabloid 子模、$Ac_T$、行 tabloid 商、標準基底；三個快問 $\dim M=3$、$\dim S=2$、尺度 3；整個 $S_3$：$6=1+2\cdot2+1$；操作鏈；第 8 章預告：$E^{(2,1)}$ 在 $m=3$ 是 8 維、$S^{(2,1)}$ 仍是 2 維 | 120s |

連續播放：`FultonDemo4` = F28–F41（約 37 分）。第 8 章（原 F800–F803）之後再議，會接成 F42–F45。

## 4. 製作規則（代理人必讀，就這些）
- ManimGL（`from manimlib import *`），不是 Manim Community；繼承 `ChuScene`；`construct` 只用 ChuScene 的方法與**模組層級函式**；開頭 `show_header`＋`check_math()`、結尾 `self.wait(1.0)`。
- 先讀自己場景對應的卡：`C:\mypython\manim\projects\fulton7_agent_pack\fulton7_agent_pack\scene_cards\F7xx.md`（第 3 節括號內的卡號；X7xx 同目錄）。卡與本檔衝突時以本檔為準（本檔已合併、刪減重複）。
- 每個數字從 `utils.rep_data`（`load("matrices21")` 等）取並 assert；版面用 `fulton_draw.assert_in_frame`／`assert_apart`；不在場景裡做全排列列舉或解方程（交給第 9 節）。
- 顏色：列與 $a_T$＝藍、行與 $b_T$＝橙、目前操作＝黃、標準基底／正號＝綠、負號＝紅紫；顏色之外再加框或文字。
- 公式一次最多 2–3 行；長線性組合最多 3 項；不用 Tex 字形索引猜語意（各段分開建 Tex）。
- 字幕繁中、自己的話；Tex 不放中文；Tex 開頭結尾不要 `\;`、`\,`；t2c 不配 `\left(…\right)`。
- 只建立自己的場景檔；共用檔不改（缺什麼寫成場景檔裡的模組層級函式，回報時說明）。
- 每幕 300–450 行；最多 2 次 `render_check`（第 2 次只修第 1 次看到的問題）。
- 自查：在 `C:\mypython\manim\projects\combkit` 執行
  `python tools/render_check.py ../catalan930/codes/scenes/<檔名> <類別> --config ../catalan930/codes/custom_config.yml --tile 480`，看 `runs/<類別>/sheet.png`。
- 回報 ≤ 8 行：檔名、長度、STATUS、偏離本檔之處。

## 5. 場景骨架（代理人照抄，不必讀其他場景檔）
```python
"""
Scene F3x —— 主題（Fulton §7.x，書 p.N；原大綱卡 F7xx）
執行（在 codes/ 內）：manimgl scenes/sceneF3x_xxx.py SceneF3xXxx
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.rep_draw import ...            # 第 1 節步驟 2 寫好的共用元件
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.rep_data import load          # 已驗證的固定算例（MATH_DATA.json）


def check_math():
    assert ...                           # 畫面上要出現的每個數字


def part_one(scene):
    scene.say("字幕", "$\\LaTeX$", "字幕")
    ...


class SceneF3xXxx(ChuScene):
    def construct(self):
        self.show_header("標題")
        check_math()
        part_one(self)
        self.clear_stage()
        ...
        self.wait(1.0)
```

## 6. 檔名與類別（`codes/scenes/`）
| 代號 | 檔名 | 類別 | 代理人 |
|---|---|---|---|
| F28 | `sceneF28_six_shuffles.py` | `SceneF28SixShuffles` | A |
| F29 | `sceneF29_rows_columns.py` | `SceneF29RowsColumns` | A |
| F30 | `sceneF30_collision.py` | `SceneF30Collision` | A |
| F31 | `sceneF31_tabloids_plane.py` | `SceneF31TabloidsPlane` | A |
| F32 | `sceneF32_irreducible_basis.py` | `SceneF32IrreducibleBasis` | B |
| F33 | `sceneF33_matrices_characters.py` | `SceneF33MatricesCharacters` | B |
| F34 | `sceneF34_young_rule.py` | `SceneF34YoungRule` | B |
| F35 | `sceneF35_induction_dictionary.py` | `SceneF35InductionDictionary` | B |
| F36 | `sceneF36_frobenius.py` | `SceneF36Frobenius` | C |
| F37 | `sceneF37_branching_sign.py` | `SceneF37BranchingSign` | C |
| F38 | `sceneF38_column_tabloids.py` | `SceneF38ColumnTabloids` | C |
| F39 | `sceneF39_straightening.py` | `SceneF39Straightening` | D |
| F40 | `sceneF40_symmetrizer_mod3.py` | `SceneF40SymmetrizerMod3` | D |
| F41 | `sceneF41_four_views.py` | `SceneF41FourViews` | D |

共用元件：`utils/rep_data.py`（`load`、`act`、`compose`、`sign`、`cycles`、`cycle_type`、`tabloid_key`、`tabloid_str`、`polytabloid`、`act_vec`、`specht21`、`rep_matrix21`、`gr_mul`、`symmetrizers`、`row_group`、`col_group`；`python -m utils.rep_data` 自我檢查）、
`utils/rep_draw.py`（顏色常數、`TabloidMob`、`ColumnTabloidMob`、`signed_sum`、`MatrixMob`、`perm_tex`、`oneline_tex`）、`utils/fulton_draw.py`（`tableau_mob`、`SkewMob`、`assert_in_frame`、`assert_apart`）、
`utils/tableaux.py`（`character_table`、`kostka`、`ssyt`、`standard_tableaux`、`lr_tableaux`、`schur_expand`、`p_lambda`、`z_lambda` 等）。各檔開頭的說明就是 API，不必讀程式本體。

> 講義第 7 節：`notes/young_tableaux_導讀.tex`（內文 `notes/fulton/part5.tex`，數字由 `fulton/make_figs.py` 的 `check_numbers_ch7()` 核對），完成（2026-10-12）。
