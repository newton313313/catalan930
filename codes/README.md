# 卡塔蘭數與 Chu (1987) 廣義卡塔蘭數：Manim 演示

用動畫講解兩件事：

1. **卡塔蘭基礎模組（場景 00a–00m）**：什麼是卡塔蘭數、為什麼同一個 $C_n$ 會在三角剖分、括號、二元樹、格子路徑、Dyck 路徑、投票、圓上配對裡反覆出現，最後接到 Chu 的推廣。
   內容來源：Aybeyan Selimi、Muzafer Saračević, *Catalan Numbers and Applications*,
   Vision International Scientific Journal 4(1) (2019) 99–114（`../ref/aybeyan-pdf.pdf`）。
   製作依據的指令：`../notes/note1012.txt`。
2. **Chu 的論文（場景 01–09）**：
   Wenchang Chu, *A new combinatorial interpretation for generalized Catalan number*,
   Discrete Mathematics 65 (1987) 91–94。
3. **MIT 18.212 Lecture 1–4 補充（場景 M01–M14）**：卡塔蘭模組沒有涵蓋的部分——Cauchy 乘積、閉式、醉漢走路、循環移位、
   平面樹、弧圖、對偶樹、DFS、堆疊／佇列排序、模式迴避、整數分割與 Young 表、鉤長公式與鉤上漫步證明。
   依據：`../notes/MIT18212_L1-4_精簡.md`（理論）與 `../notes/mit_plan.md`（盤點與規格）。
4. **Fulton《Young Tableaux》第 1 章（場景 F01–F08，獨立的一組）**：Young 圖、Young 表、Schur 多項式、列插入（bumping）、
   Row Bumping Lemma、表的乘積、jeu de taquin 與 rectification。來源：W. Fulton, *Young Tableaux*（`../ref/9781107108738_A23693136.pdf` 的節錄，
   純文字版 `../ref/fulton_ch1_text.md`）；計畫表 `../notes/fulton_plan.md`。
5. **Fulton《Young Tableaux》第 2–4 章（場景 F09–F19，獨立的一組）**：字與 Knuth 等價、plactic monoid、Pieri 公式、Kostka 數、
   行字、遞增子序列與 Greene 定理、唯一性的證明、R-S-K 對應、矩陣球構造與應用。來源：`C:\mypython\manim\projects\ref\fulton\`
   （各章 PDF 與機械轉出的 Markdown）；計畫表 `../notes/fulton_plan_ch2-4.md`。
6. **Fulton《Young Tableaux》第 5–6 章（場景 F20–F27，獨立的一組）**：表的因數分解與 Littlewood–Richardson 數、反格字、
   LR 規則、Remmel–Whitney；對稱多項式的五組基底、Newton 恆等式、Jacobi–Trudi、對稱函數環、內積與 ω。計畫表 `../notes/fulton_plan_ch5-6.md`。
7. **Fulton《Young Tableaux》第 7 章（場景 F28–F41，獨立的一組）**：對稱群的表示——tabloid、Specht 模、標準基底、表示矩陣與特徵標、
   Young's rule、表示環 $R\cong\Lambda$、Frobenius 公式、分支律、straightening、Young 對稱化子、模 3。計畫表 `../notes/fulton_plan_ch7.md`。
8. **Fulton《Young Tableaux》第 8 章（場景 F42–F45，獨立的一組）**：Schur 模 $E^\lambda$、權重與特徵標 $s_\lambda$、Schur–Weyl 對偶、
   Plücker 二次關係。計畫表 `../notes/fulton_plan_ch8.md`。
9. **Raney 引理筆記（場景 R01–R06，獨立的一組）**：整數序列的 Raney 引理、最後一個最低點的證明、加強版、出棧序列與 $C_n$、摸牌遊戲（洛谷 P6672）＝ Raney 的字、原筆記的勘誤。依 `../notes/ran_note015_改寫.pdf`。
10. **Raney (1960) 論文導讀（場景 N01–N12，獨立的一組）**：前序記法與字、秩、三種讀法、Raney 的循環引理證明、雙重計數、用循環引理製造隨機例子、切開與第一個符號、L*、Lagrange 反演、三項式與 Problem 4983、卷積、總結。依 `../notes/raney1960_導讀.pdf`，分鏡 `../notes/raney/manim_plan.md`。
11. **Fulton《Young Tableaux》第 9–10 章（場景 F46–F55，獨立的一組）**：Plücker 座標、旗流形的座標環、Grassmannian 與旗流形的 Schubert 胞腔、四條線問題（Schubert 計算）、差商、Schubert 多項式、pipe dream、Bruhat 序、Grassmann 置換＝Schur 多項式。計畫表 `../notes/fulton_plan_ch9-10.md`。

共 109 個可以單獨執行的場景，外加十三種連續播放的版本。配套的中文講義在 `../notes/chu1987_導讀.pdf`（40 頁；第 1 節的 13 個小節依序對應卡塔蘭模組 00a–00m，附錄 A.1–A.14 依序對應 MIT 補充 M01–M14）；Fulton 的部分另有 `../notes/young_tableaux_導讀.pdf`（25 頁，第 1–8 節對應 F01–F45）。Chu 引用的 Raney 公式的出處另有 `../notes/raney1960_導讀.pdf`（33 頁，Raney (1960) 論文導讀，動畫 N01–N12）。

## 注意：這是 ManimGL，不是 Manim Community

規劃文件（`../ref/overview.txt`、`../notes/note1012.txt`）裡偶爾出現 Manim Community 的寫法。
這台電腦裝的是 3Blue1Brown 的 **ManimGL**，所以程式一律用 ManimGL 的寫法：

| Community 的寫法 | 本專案實際使用 |
|---|---|
| `manim -pql file.py Scene` | `manimgl file.py Scene` |
| `from manim import *` | `from manimlib import *` |
| `Create(...)` | `ShowCreation(...)` |

## 環境與依賴（2026-10-13 實測）

完整的安裝步驟、重建方法與踩過的坑見 `C:\mypython\manim\環境與交接_ENVIRONMENT.md`；這裡只列執行本專案需要的東西。

| 項目 | 版本／位置 | 用途 |
|---|---|---|
| Windows 11 Home（繁體中文，系統編碼 cp950） | — | `custom_config.yml` 只能寫英文；終端機輸出中文前設 `PYTHONIOENCODING=utf-8` |
| Python | 3.10.9（Anaconda base，`C:\Users\User\anaconda3\python.exe`） | |
| **ManimGL** | 1.7.2，3b1b/manim commit **fafa083**，原始碼 `C:\mypython\manim`，`pip install -e .` | 所有場景。**不要升級、重裝或 `git pull`** |
| 繪圖後端 | `wgpu` 0.31.0、`rendercanvas` 2.7.2、`glfw` 2.10.2 | ManimGL 自帶 |
| Python 套件 | numpy 1.23.5、Pillow 9.4.0、`av` 17.1.0、diskcache 5.6.3、ManimPango 0.6.1；PyMuPDF 1.28.2 | `av` 要另由 manim 的 `requirements.txt` 安裝；PyMuPDF 只給 `../ref/*/convert_to_md.py` 與講義預覽用 |
| ffmpeg／ffprobe | 4.3.1（conda-forge） | 輸出影片、量長度 |
| LaTeX | MiKTeX 25.12：`latex` + `dvisvgm` 3.4.3 + **`cm-super`** | 場景裡的公式（沒有 cm-super 會出現 "SVG has no content"） |
| 講義 | MiKTeX 的 `xelatex` + `xeCJK`、`tcolorbox`、`tikz`、`ytableau`、`booktabs`、`hyperref` | `../notes/*.tex`（第一次編譯時 MiKTeX 會自動裝套件） |
| 字型 | 微軟正黑體 `Microsoft JhengHei` | 字幕與講義 |
| 工具包 | `C:\mypython\manim\projects\combkit`（1.8.0） | `tools/render_check.py`（低畫質試渲染＋總覽圖）、`tools/strict_render.py`；`utils/` 改過後用 `tools/sync_from_catalan930.py` 同步 |

檢查環境：在 `codes/` 裡執行 `python check_env.py --render`。

**`utils/` 模組的相依關係**（箭頭左邊 import 右邊；[M] 表示需要 ManimGL，其餘是純 Python）：

```text
counting                      （無相依；卡塔蘭、Raney、MIT 補充的計數）
tableaux      ← counting      （Young 表、Knuth、R-S-K、LR、對稱函數；第 8 章也用它）
schubert      ← tableaux      （Fulton 第 9–10 章：Plücker、胞腔、Bruhat 序、差商、Schubert 多項式、pipe dream）
rep_data      ← counting, tableaux；讀 data/fulton7_math.json   （Fulton 第 7 章）
styles [M]                    （顏色、字型、zh()、mixed()）
scene_base [M]   ← styles
circle_points [M] ← styles；polygon_groups [M] ← circle_points, counting, styles；root_figure [M] ← polygon_groups, styles
lattice_paths [M] ← counting, styles；formulas [M] ← counting, styles
catalan_draw [M] ← counting, polygon_groups, styles；mit_draw [M] ← catalan_draw, counting, styles
fulton_draw [M]  ← mit_draw, styles, tableaux；rep_draw [M] ← rep_data；schubert_draw [M] ← schubert
```

場景檔只 import `utils.*` 與 `manimlib`；`main.py` import 所有場景檔；`render_all.py` 以子程序呼叫 `manimgl`。

## 怎麼執行

**所有指令都要在 `codes/` 資料夾裡執行。** ManimGL 會讀取這個資料夾裡的 `custom_config.yml`。

```bash
cd C:\mypython\manim\projects\catalan930\codes
```

### 1. 開視窗預覽（最常用）

```bash
manimgl main.py
```

會列出所有場景，輸入編號或名稱後按 Enter。也可以直接指定場景：

```bash
manimgl main.py Scene00cTriangulationRecurrence
```

或是從場景自己的檔案執行：

```bash
manimgl scenes/scene00c_triangulation_recurrence.py Scene00cTriangulationRecurrence
```

動畫播完後視窗會停在最後一格，等你關閉。預覽視窗的操作（依本機這一版 ManimGL 的原始碼）：

| 操作 | 功能 |
|---|---|
| `Ctrl` + `Q`，或直接按視窗的 ✕ | 關閉視窗 |
| 滑鼠滾輪 | 縮放 |
| 按住 `f` 再移動滑鼠 | 平移 |
| 按住 `d` 再移動滑鼠 | 旋轉 3D 視角 |
| `r` | 畫面回到原位 |

### 2. 連續播放

| 指令 | 內容 |
|---|---|
| `manimgl main.py CatalanIntroDemo` | 卡塔蘭基礎模組 00a–00m |
| `manimgl main.py FullDemo` | Chu 的部分 01–09 |
| `manimgl main.py CompleteDemo` | **完整版**：卡塔蘭基礎模組 00a–00m，接著 Chu 的 03–09 |
| `manimgl main.py MITDemo` | MIT 18.212 L1–4 補充 M01–M14 |
| `manimgl main.py MITCompleteDemo` | **MIT 完整版**：00a–00k → M01–M14 → 00l、00m → Chu 的 03–09 |
| `manimgl main.py FultonDemo` | Fulton《Young Tableaux》第 1 章 F01–F08（獨立，不接其他影片） |
| `manimgl main.py FultonDemo2` | Fulton 第 2–4 章 F09–F19（獨立） |
| `manimgl main.py FultonDemo3` | Fulton 第 5–6 章 F20–F27（獨立） |
| `manimgl main.py FultonDemo4` | Fulton 第 7 章 F28–F41（獨立） |
| `manimgl main.py FultonDemo5` | Fulton 第 8 章 F42–F45（獨立） |
| `manimgl main.py FultonDemo6` | Fulton 第 9–10 章 F46–F55（獨立） |
| `manimgl main.py RaneyLemmaDemo` | Raney 引理筆記 R01–R06（獨立） |
| `manimgl main.py RaneyPaperDemo` | Raney (1960) 導讀 N01–N12（獨立） |

完整版跳過 Scene01 與 Scene02：Scene01（經典卡塔蘭與圓上配對）已由 00a、00j 取代，Scene02（從弦到多邊形、兩個向量）已由 00m 取代。
這兩個場景仍保留，單獨播放或 `FullDemo` 都會用到。

### 3. 輸出成影片

```bash
manimgl main.py Scene00cTriangulationRecurrence -w --hd
```

影片會存到 `renders/Scene00cTriangulationRecurrence.mp4`。畫質選項：

| 參數 | 解析度 | 用途 |
|---|---|---|
| `-l` | 480p | 最快，檢查內容用 |
| `-m` | 720p | |
| `--hd` | 1080p | 正式輸出 |
| `--uhd` | 4K | |

其他常用參數：`-o` 輸出後自動打開；`-n 5` 從第 5 個動畫開始；`-n 3,6` 只做第 3 到 6 個。

### 4. 一次輸出很多支

| 指令 | 輸出 |
|---|---|
| 對 `render_all.bat` 按兩下 | **一鍵輸出**：選單 1 全部場景＋13 個連續播放（1080p）、2 只輸出連續播放、3 只輸出單一場景、4 全部用 480p；也可帶參數，例如 `render_all.bat --fulton5 -l`。找不到 `manimgl` 時會自己啟用 Anaconda |
| `python render_all.py` | 全部單一場景（00a–00m、01–09、08r、M01–M14、F01–F55、R01–R06、N01–N12），1080p |
| `python render_all.py --intro` | 只有卡塔蘭模組 00a–00m |
| `python render_all.py --chu` | 只有 Chu 的部分 01–09 與 08r |
| `python render_all.py --mit` | 只有 MIT 補充 M01–M14 |
| `python render_all.py --fulton` | 只有 Fulton 第 1 章 F01–F08 |
| `python render_all.py --fulton2` | 只有 Fulton 第 2–4 章 F09–F19 |
| `python render_all.py --fulton3` | 只有 Fulton 第 5–6 章 F20–F27 |
| `python render_all.py --fulton4` | 只有 Fulton 第 7 章 F28–F41 |
| `python render_all.py --fulton5` | 只有 Fulton 第 8 章 F42–F45 |
| `python render_all.py --fulton6` | 只有 Fulton 第 9–10 章 F46–F55 |
| `python render_all.py --raney` | 只有 Raney 引理筆記 R01–R06 |
| `python render_all.py --raney-paper` | 只有 Raney (1960) 導讀 N01–N12 |
| `python render_all.py 00c 05` | 指定的場景（代號見下面的表） |
| `python render_all.py --complete --demos-only` | 只輸出完整版 `CompleteDemo.mp4` |

連續播放的影片用 `--intro-demo`、`--full`、`--complete`、`--mit-demo`、`--mit-complete`、`--fulton-demo`、`--fulton2-demo`、`--fulton3-demo`、`--fulton4-demo`、`--fulton5-demo`、`--fulton6-demo`、`--raney-demo`、`--raney-paper-demo` 加上去。加 `-l` 改成低畫質。

## 卡塔蘭基礎模組（00a–00m）

依照 `../notes/note1012.txt` 的敘事順序：數列 → 三角剖分 → 遞迴 → 括號 → 二元樹 → 格子路徑 → Dyck 路徑 → 平衡括號 → 投票 → 圓上配對 → 同一個 5 → $C=1+xC^2$ → Chu 的推廣。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| 00a | `Scene00aCatalanDefinition` | 數列 1, 1, 2, 5, 14, …；「為什麼到處出現？」；公式 $C_n=\frac{1}{n+1}\binom{2n}{n}$ 與 $C_0$–$C_4$ 驗算；一點歷史；路線圖 | 36 秒 |
| 00b | `Scene00bTriangulation` | 凸多邊形的三角剖分：$T_3=1$、$T_4=2$、$T_5=5$（逐一畫出）、$T_6=14$（圖庫）；**凸 $(n+2)$ 邊形有 $C_n$ 種** | 39 秒 |
| 00c | `Scene00cTriangulationRecurrence` | 固定底邊，第三個頂點走過所有位置；左右兩塊獨立 → 相乘、位置不同 → 相加；$C_4=1\cdot5+1\cdot2+2\cdot1+5\cdot1=14$；回頭把 14 種分成 5+2+2+5；Segner 遞迴 | 47 秒 |
| 00d | `Scene00dParenthesization` | 2、3、4 個因子；括號由內而外長出來；依最後一次乘法分組 2+1+2；**$n+1$ 個因子有 $C_n$ 種完全括號化** | 36 秒 |
| 00e | `Scene00eBinaryTrees` | 括號 → 滿二元樹的一一對應（乘號 → 內部節點、因子 → 葉子、最後一次乘法 → 樹根）；五種括法對五棵樹；拿掉葉子 → $n$ 個節點的二元樹 | 36 秒 |
| 00f | `Scene00fLatticePaths` | $(0,0)\to(3,3)$ 的路徑與 R/U 字；20 條中只有 5 條不越過 $y=x$；$\binom{2n}{n}-\binom{2n}{n-1}=C_n$；**補充說明**：反射原理 | 51 秒 |
| 00g | `Scene00gDyckPaths` | 格子路徑轉 45° 再上下翻轉變成 Dyck 路徑（R → ↗、U → ↘）；$n=0,1,2,3$ 有 1、1、2、5 條（來源 Fig. 2.4）；第一個上坡的分解 | 32 秒 |
| 00h | `Scene00hBalancedParentheses` | 上坡「(」、下坡「)」；高度 = 還沒關上的左括號數；反例 $())(()$；兩種括號別搞混 | 26 秒 |
| 00i | `Scene00iBallot` | 一般的 Bertrand 投票問題與卡塔蘭特例分開講；A A B A B B 的比分 0→1→2→1→2→1→0 連成 Dyck 路徑；兩人各 3 票有 5 種 | 32 秒 |
| 00j | `Scene00jNoncrossingMatchings` | 圓周 6 點的不交叉完美配對（$C_3=5$）；**固定一點，它的弦把其餘的點分成 2 個獨立區域**：$C_0C_2+C_1C_1+C_2C_0$ | 36 秒 |
| 00k | `Scene00kOneNumberManyObjects` | 中間一個 5，周圍六種物件各 5 個，同一位置彼此一一對應；用顏色顯示「根＋左＋右」 | 26 秒 |
| 00l | `Scene00lCatalanGeneratingFunction` | $C(x)=\sum C_nx^n$；根 → $x$、內側 → $C$、外側 → $C$，得 $C=1+xC^2$；其他結構也是 $x\cdot C\cdot C$；展開驗算 | 38 秒 |
| 00m | `Scene00mBridgeToChu` | 配對 = 3 組 2 點群組；一條弦換成三角形 → $\vec n=(2,1),\vec v=(2,3)$；兩個向量與 $N$；切成 2 塊 → $v_i$ 塊；$C=1+xC^2\Rightarrow D=1+\sum x_iD^{v_i}$ | 45 秒 |
| | `CatalanIntroDemo` | 以上十三個連續播放 | 8 分 15 秒 |

### 正名與指標（全模組統一）

| 物件 | 精確說法 | 數目 |
|---|---|---|
| 三角剖分 | 凸 $(n+2)$ 邊形的三角剖分（凸 $m$ 邊形是 $C_{m-2}$） | $C_n$ |
| 括號 | $n+1$ 個因子 $a_0a_1\cdots a_n$ 的完全括號化（$n$ 次乘法） | $C_n$ |
| 二元樹 | $n$ 個內部節點的滿二元樹（$n+1$ 片葉子）；等價：$n$ 個節點、左右小孩可有可無的二元樹 | $C_n$ |
| 格子路徑 | $(0,0)\to(n,n)$、只走 R、U、不走到 $y=x$ 上方 | $C_n$ |
| Dyck 路徑 | 半長 $n$：$n$ 個上坡、$n$ 個下坡、不低於起點 | $C_n$ |
| 平衡括號字串 | $n$ 對括號 | $C_n$ |
| 投票（卡塔蘭特例） | 兩人各 $n$ 票，每開一張後 A 的票數 $\ge$ B | $C_n$ |
| 圓上配對 | 圓周 $2n$ 點的不交叉完美配對 | $C_n$ |

### 和指令或來源論文不同的地方（都已在畫面上處理）

- **格子路徑 → Dyck 路徑的方向。** 指令要求格子路徑「不走到 $y=x$ 上方」，又寫 U → ↗、R → ↘。這兩者矛盾：照那樣對應會掉到地面以下。正確是 **R → ↗、U → ↘**，動畫照這個做（轉 45° 之後再上下翻轉）。
- **二元樹的說法。** 來源論文寫「$n$ 個頂點的二元樹」。動畫統一說「$n$ 個內部節點的滿二元樹」，並在 00e 示範拿掉葉子後就是論文說的那一種。
- **括號化的指標。** 來源論文的 $M_n$ 以「$n$ 個數」計數，照它寫的遞迴算出來是 $C_{n-1}$，它卻寫成 $M_n=C_n$（第 104–105 頁）。動畫與講義一律說「$n+1$ 個因子有 $C_n$ 種」。
- **投票問題。** 來源論文給的是 $k$ 倍的推廣公式 $\frac{a-kb}{a+b}$，而且把機率說成「數目」。動畫把「一般的 Bertrand 問題（嚴格領先的機率 $\frac{a-b}{a+b}$）」和「卡塔蘭特例（同票、不落後，$C_n$ 種）」分開講。兩個公式都用暴力列舉驗證過。
- **反射原理** 是補充說明：來源論文只給 $\binom{2n}{n}-\binom{2n}{n-1}$，沒有證明。畫面上有標示。

### 上色規則

| 東西 | 顏色 |
|---|---|
| 一般的卡塔蘭物件（對角線、路徑、樹的節點） | 藍（＝ 2 點群組的顏色，之後的 $x_1$） |
| 根（固定的那一個：根三角形、最後一次乘法、樹根、第一個上坡、含固定點的弦） | 橘 |
| 左邊的子問題 / 右邊的子問題（$C_k$ / $C_{n-1-k}$） | 青 / 粉紅（＝ Chu 部分的區域 $R_1$ / $R_2$） |
| 不合法（越過對角線、交叉、掉到地面以下） | 紅 |

所有物件都由同一種「樹」產生（`utils/counting.py` 第 5 節），所以 00k 裡同一位置的六個物件真的彼此一一對應。

## MIT 18.212 Lecture 1–4 補充（M01–M14）

依 `../notes/mit_plan.md`：MIT 四堂課的每個主題先和既有場景比對，已經做過的（Dyck 定義、三角剖分與遞迴、反射原理、圓上配對、pairs → blocks）沿用，不再重做；只新增下面 14 幕。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| M01 | `SceneM01CauchyProduct` | 4×4 乘法表亮反對角線：$[x^n]C^2=\sum C_kC_{n-k}$（1, 2, 5, 14）；對照遞迴得 $C_{n+1}=[x^n]C^2$ → $C=1+xC^2$ | 51 秒 |
| M02 | `SceneM02ClosedForm` | $xC^2-C+1=0$ 的兩個根，取減號的理由（兩條曲線）；$\binom{1/2}{m}(-4)^m$ 表；代回得 $C_n=\frac1{n+1}\binom{2n}{n}$ | 46 秒 |
| M03 | `SceneM03DrunkardsWalk` | 醉漢走到 −1 就掉下懸崖；第 $2n+1$ 步第一次掉 ⇔ Dyck 路徑＋一步往下；$\sum C_n/2^{2n+1}=\tfrac12C(\tfrac14)=1$ | 56 秒 |
| M04 | `SceneM04CyclicShift` | 古典循環引理：7 種循環讀法恰 1 種好；35 = 5 × 7；$C_n=\binom{2n+1}{n}/(2n+1)$；預告第 8 場景的 Raney | 43 秒 |
| M05 | `SceneM05PlaneTrees` | 平面樹（小孩有順序，交換就不同）；$n+1$ 個頂點有 $C_n$ 棵；和 00k 的二元樹上下對齊 | 39 秒 |
| M06 | `SceneM06ArcDiagrams` | 圓上配對剪開攤平成弧圖；交叉／巢狀的定義；6 點 15 種配對中不交叉 5 種、不巢狀 5 種 | 46 秒 |
| M07 | `SceneM07TriangulationDualTree` | 五邊形三角剖分的對偶圖 → 完全二元樹；二元樹 → 平面樹（左小孩＝第一個小孩、右小孩＝下一個兄弟） | 48 秒 |
| M08 | `SceneM08TreeDyckMatching` | 沿平面樹輪廓走（DFS）讀出 UUDUDD；U、D 配對成弧 (1,6),(2,3),(4,5)；一條一一對應的鏈 | 48 秒 |
| M09 | `SceneM09StackQueueSorting` | 堆疊排序（4213 成功、231 失敗）；佇列＋插隊線（231 成功、321 失敗）；可排序 ⇔ 避開 231／321 | 1 分 2 秒 |
| M10 | `SceneM10PatternAvoidance` | 模式包含（41532 含 231）、52143 避開 231；$n=3,4$ 的排列表 5、14 個；六個長度 3 模式都是 $C_n$ | 45 秒 |
| M11 | `SceneM11PartitionsYoung` | 整數分割與合成；**整數分割 ≠ Chu 的集合分割**；Young 圖 (5,3,3,2,1)；(3,2) 的 5 個標準 Young 表 | 53 秒 |
| M12 | `SceneM12SYTDyck` | SYT ((1,2,4),(3,5,6)) → UUDUDD；(3,3) 的 5 對；$f^{(n,n)}=C_n$；一般 λ 的 $k$ 維格子路徑 | 47 秒 |
| M13 | `SceneM13HookLength` | 鉤與鉤長、(4,3,1) 的 $8!/576=70$；鉤長公式三組驗算；角落遞迴；化約成 $\sum_c\frac1n\frac{H(\lambda)}{H(\lambda-c)}=1$ | 1 分 1 秒 |
| M14 | `SceneM14HookWalk` | 鉤上漫步證明，分五段：漫步 → 主張 → 路徑權重與投影 → 關鍵恆等式與引理 → 加總得 $P(c)$（λ=(4,3,1)：3/10＋1/2＋1/5＝1） | 2 分 34 秒 |
| | `MITDemo` | 以上十四個連續播放 | 13 分 33 秒 |

和 `note103how.txt` 不同的決定（細節見 `mit_plan.md` 第 1 節）：
- 該指令依 10/1 的 101 版撰寫，不知道後來的 00a–00m；已經做過的主題改為沿用。
- **不修改任何既有場景**（使用者要求舊影片不刪）：弧圖改成新的 M06；$C=1+xC^2\to D$ 的連結已由 00m 做到；循環移位 → Raney 的預告放在 M04 結尾。
- 貫穿的例子用本專案的對應：五邊形對角線 {1,4},{2,4} → 二元樹 → 平面樹（根 → A → 兩片葉子）→ UUDUDD → 配對 (1,6),(2,3),(4,5) → SYT ((1,2,4),(3,5,6))。
- 佇列排序採「佇列＋插隊線」模型：可排序 ⇔ 避開 321（程式暴力驗證，畫面上有註明）。

共用工具：`utils/mit_draw.py`（弧圖、Young 圖、平面樹、數字方塊）；數學資料在 `utils/counting.py` 第 6 節。

## Fulton《Young Tableaux》第 1 章（F01–F08，獨立）

依 `../notes/fulton_plan.md`；例子都用書上的資料（書頁碼見計畫表）。這一組不接前面的影片，用 `FultonDemo` 連續播放。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| F01 | `SceneF01YoungDiagrams` | Young 圖與分割 λ=(6,4,4,2)⊢16、次方記號；沿對角線翻轉得共軛 (4,4,3,3,1,1)；填數與編號 | 53 秒 |
| F02 | `SceneF02Tableaux` | 書上的表逐列、逐行檢查兩個條件；標準表；轉置；斜形狀 (5,5,4,3,2)/(4,4,1) 與斜表 | 53 秒 |
| F03 | `SceneF03Schur` | $x^T$；$s_\lambda=\sum x^T$；$s_{(2,1)}(x_1,x_2,x_3)$ 的 8 個表；交換變數看對稱；$s_{(n)}=h_n$、$s_{(1^n)}=e_n$ | 57 秒 |
| F04 | `SceneF04RowInsertion` | 列插入 $T\leftarrow 2$ 逐步擠出 3→5→6；為什麼結果仍是表；從新格子反向擠出還原 | 1 分 3 秒 |
| F05 | `SceneF05BumpingLemma` | 擠壓路徑與新格子；Row Bumping Lemma 兩種情況；依序插入遞增／遞減的數 → 水平條／垂直條 | 1 分 13 秒 |
| F06 | `SceneF06Product` | 表的字（由最下列讀到最上列）；乘積 $T\cdot U$；結合律與單位元的小例子 | 56 秒 |
| F07 | `SceneF07JeuDeTaquin` | 內角、外角、滑動規則（相等取下面）、反向滑動；兩種挑內角的順序得到同一個 Rect | 1 分 17 秒 |
| F08 | `SceneF08RectifyProduct` | $T*U$ 滑 8 次 → 等於列插入算出的 $T\cdot U$；書中的三個 Claim（第 2–3 章才證明） | 1 分 14 秒 |
| | `FultonDemo` | 以上八個連續播放 | 8 分 34 秒 |

數學資料：`utils/tableaux.py`（純 Python；格子 0 起算；列插入、反向擠出、乘積、jeu de taquin、rectification、Schur 多項式），
`python utils/tableaux.py` 用暴力列舉驗證書中的三個 Claim 與 Row Bumping Lemma 等性質。

## Fulton《Young Tableaux》第 2–4 章（F09–F19，獨立）

依 `../notes/fulton_plan_ch2-4.md`；例子都用書上的資料。原文的各章 PDF 與機械轉出的 Markdown 在 `C:\mypython\manim\projects\ref\fulton\`。
這一組也不接前面的影片，用 `FultonDemo2` 連續播放（第 1 章的 `FultonDemo` 不受影響）。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| F09 | `SceneF09WordsKnuth` | 表 ↔ 字（在變小處切開）；字的語言寫列插入；Knuth 的基本變換 K′、K″；命題 1：$T\leftarrow 2$ 拆成 8 步基本變換 | 1 分 21 秒 |
| F10 | `SceneF10SlidesTheorem` | 滑動保持 Knuth 等價（23514 ≡ 25134 四步）；主定理與 $P(w)$；推論 1 $\mathrm{Rect}(S)=P(w(S))$；推論 2 三種乘積相同；plactic monoid 與 tableau ring | 1 分 17 秒 |
| F11 | `SceneF11Pieri` | $S_\lambda$ 是表的和；Pieri 公式（水平帶／垂直帶，λ=(2,1)、p=2）；化成 $s_\lambda h_p$、$s_\lambda e_p$ 並驗算係數 | 58 秒 |
| F12 | `SceneF12Kostka` | 內容與 Kostka 數（水平帶鏈）；$h_\mu=\sum K_{\lambda\mu}s_\lambda$；字典序與支配序；Kostka 矩陣下三角；練習 2 | 1 分 9 秒 |
| F13 | `SceneF13ColumnWords` | 行字 ≡ 列字；Lemma 1：切成兩塊、搬到左下再滑回去；逐行剝下 | 54 秒 |
| F14 | `SceneF14Increasing` | $L(w,k)$ = 6、9、12；$w'=w(P(w))$；Lemma 1（前 k 列）；Lemma 2（基本變換不改變 L 的交換論證） | 1 分 15 秒 |
| F15 | `SceneF15Uniqueness` | Lemma 3；由 $L(w,k)$ 一格一格重建 $P(w)$（唯一性）；主定理與三個 Claim 證完；Erdős–Szekeres | 1 分 6 秒 |
| F16 | `SceneF16RS` | 記錄表 $Q$（$w$ = 5 4 8 2 3 4 1 7 5 3 1）；反向擠出還原；排列 ↔ 兩個標準表，$n!=\sum (f^\lambda)^2$；練習 17 | 1 分 12 秒 |
| F17 | `SceneF17RSKArrays` | 字典序雙列陣列 → $(P,Q)$（練習 1）；R-S-K 定理；矩陣的列和與行和；對稱定理；$P(w^{-1})=Q(w)$；對合 ↔ 標準表 | 1 分 20 秒 |
| F18 | `SceneF18MatrixBall` | 矩陣球：編號、讀出第一列、導出矩陣 $A^\flat$、第二列；轉置看出對稱定理；練習 4；Viennot 影子線 | 1 分 18 秒 |
| F19 | `SceneF19RSKApplications` | Kostka 數與 μ 的順序無關 → Schur 多項式對稱；Cauchy–Littlewood；$n!$、$m^n$、對合數；鉤長公式回顧、Stanley 鉤–內容公式 3,360；練習 12 | 1 分 16 秒 |
| | `FultonDemo2` | 以上十一個連續播放 | 13 分 18 秒 |

共用工具：`utils/fulton_draw.py`（字母方塊與 Knuth 變換動畫、斜表與有洞的表、雙列陣列、矩陣球、版面檢查）；
數學資料在 `utils/tableaux.py` 第 7 節（字、Knuth 等價、L(w,k)、R-S-K、矩陣球、Pieri、Kostka 矩陣、鉤–內容公式）。

## Fulton《Young Tableaux》第 5–6 章（F20–F27，獨立）

依 `../notes/fulton_plan_ch5-6.md`；每幕開頭一個「鉤子」（問題、比喻或小遊戲）。用 `FultonDemo3` 連續播放。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| F20 | `SceneF20FactorTableaux` | 表的因數分解：$V=T\cdot U$ 有幾種寫法只看形狀；滑成 $U_0$ 的斜表一樣多 → LR 數 $c^\nu_{\lambda\mu}$ | 1 分 13 秒 |
| F21 | `SceneF21LRSymmetry` | LR 數的三張臉（交換、轉置）；穿出 $\lambda*\mu$ 的框 → 0；表環裡的乘法 $S_\lambda S_\mu=\sum c\,S_\nu$ | 1 分 7 秒 |
| F22 | `SceneF22Yamanouchi` | 反格字＝倒著開票；LR 斜表滑成 $U(\mu)$（Lemma 1）；Knuth 變換保持反格字（Lemma 2）；命題 3 | 1 分 15 秒 |
| F23 | `SceneF23LRRule` | LR 計數機：(5,4,3,2)/(3,3,1) 的 15 個 LR 斜表分堆 → $s_{\nu/\lambda}$ 的展開；$s_{(2,1)}^2$；練習 2 | 1 分 18 秒 |
| F24 | `SceneF24LROther` | 反格字 ↔ 標準表 $U(w)$；Remmel–Whitney（189 個標準表裡恰 15 個過關）；彩蛋：卡塔蘭數 | 1 分 13 秒 |
| F25 | `SceneF25Bases` | 五組基底 $m,s,e,h,p$；$E(-t)H(t)=1$；Newton 恆等式；$z(\lambda)$ 與 $h_n=\sum p_\lambda/z(\lambda)$ | 1 分 18 秒 |
| F26 | `SceneF26JacobiTrudi` | 三條路到 $s_\lambda$：Jacobi–Trudi、對偶、雙交錯式；$s_{(2,1)}(1,q,q^2)$ 與 $q=1$ 的表數 | 1 分 13 秒 |
| F27 | `SceneF27SymFunctions` | 對稱函數環 $\Lambda$；Cauchy 核的三種展開；內積與 $\omega$；預告第 7 章的特徵標表 | 1 分 14 秒 |
| | `FultonDemo3` | 以上八個連續播放 | 10 分 0 秒 |

數學資料在 `utils/tableaux.py` 第 8 節（LR 規則、反格字、Remmel–Whitney、對稱多項式的五組基底、Jacobi–Trudi、內積、ω、特徵標表）。

## Fulton《Young Tableaux》第 7 章（F28–F41，獨立）

依 `../notes/fulton_plan_ch7.md`（由使用者的 F700–F725、X701–X705 分鏡合併成 14 幕）；固定算例在 `data/fulton7_math.json`（來自
`C:\mypython\manim\projects\fulton7_agent_pack`，`python -m utils.rep_data` 用 `tableaux.py` 獨立重算核對）。用 `FultonDemo4` 連續播放。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| F28 | `SceneF28SixShuffles` | 三張卡片六種排列：置換＝換座標；平均方向與零和平面；穩定子空間、Maschke、Schur；$3=1+2$、$6=1+2\cdot2+1$ | 2 分 30 秒 |
| F29 | `SceneF29RowsColumns` | 座位表：$(3,2)$ 與共軛、標準表；列群 $R(T)$、行群 $C(T)$；$a_T,b_T,c_T=b_Ta_T$；$R(\sigma T)=\sigma R(T)\sigma^{-1}$ | 2 分 30 秒 |
| F30 | `SceneF30Collision` | 同列又同行的一對數讓 $b_T\{T'\}=0$；無碰撞 ⇒ 支配；Fulton 的二分引理 | 1 分 59 秒 |
| F31 | `SceneF31TabloidsPlane` | tabloid、$M^{(2,1)}$；零和平面與等邊三角形；$v_T=b_T\{T\}$、$S^{(2,1)}=W$；$\sigma v_T=v_{\sigma T}$ | 2 分 58 秒 |
| F32 | `SceneF32IrreducibleBasis` | 零和平面沒有共同的特徵線；$b_TM^\lambda=\mathbb Cv_T$ ⇒ 不可約；標準 $v_T$ 是基底，$\dim S^\lambda=f^\lambda$ | 2 分 25 秒 |
| F33 | `SceneF33MatricesCharacters` | 逐欄算 $\rho(12)$、$\rho(23)$；兩個反射與 120° 旋轉；特徵標 $2,0,-1$ 與內積 | 2 分 55 秒 |
| F34 | `SceneF34YoungRule` | 置換模組的特徵標 $\xi=2$；Young's rule：$\mu=(2,2,1)$ 的 7 個半標準表、$30=1+8+10+6+5$；$\theta_T$ | 2 分 56 秒 |
| F35 | `SceneF35InductionDictionary` | 誘導積 $V\circ W$；$\varphi:\Lambda\to R$、$\psi$、等距；LR：$S^{21}\circ S^{21}\supset2S^{321}$；Hopf 一句 | 2 分 54 秒 |
| F36 | `SceneF36Frobenius` | Frobenius 特徵標公式：$\ell=(3,1)$ 的收集槽算出 $2,0,-1$；$s_{21}=(p_1^3-p_3)/3$ | 2 分 29 秒 |
| F37 | `SceneF37BranchingSign` | 分支律（限制與誘導、Young 格、$8=3+2+3$）；$S^\lambda\otimes\mathbb U_n\cong S^{\tilde\lambda}$ | 2 分 31 秒 |
| F38 | `SceneF38ColumnTabloids` | 帶方向的行 tabloid、$\alpha$、$\beta$；交換關係 $[21/3]=[12/3]-[13/2]$ | 2 分 22 秒 |
| F39 | `SceneF39Straightening` | 兩輪 straightening $[125/43]=[125/34]-[135/24]$、停止的理由；$\ker\alpha=Q^\lambda$ | 2 分 58 秒 |
| F40 | `SceneF40SymmetrizerMod3` | $c_T^2=3c_T$、冪等元 $c_T/3$、$n_\lambda$＝鉤長乘積；多項式模型 $F_T$；模 3 時兩種構造不同構 | 2 分 32 秒 |
| F41 | `SceneF41FourViews` | 四個視角拼成同一件事；$3、2、3$；$6=1+2\cdot2+1$；預告第 8 章（$E^{(2,1)}$ 8 維） | 2 分 2 秒 |
| | `FultonDemo4` | 以上十四個連續播放 | 36 分 15 秒 |

共用工具：`utils/rep_data.py`（資料與置換、tabloid、polytabloid、表示矩陣、群環）、`utils/rep_draw.py`（tabloid、帶號線性組合、矩陣）。

## Fulton《Young Tableaux》第 8 章（F42–F45，獨立）

依 `../notes/fulton_plan_ch8.md`（使用者大綱的 F800–F803）；數字由 `utils/tableaux.py`（`ssyt`、`content`、`hook_content_count`、`schur_poly`）現算並在各場景的 `check_math()` assert。用 `FultonDemo5` 連續播放。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| F42 | `SceneF42SchurModule` | 把數字換成向量：一列 → $\operatorname{Sym}^nE$、一行 → $\bigwedge^nE$；$E^{(2,1)}$＝$\bigwedge^2E\otimes E$ 模掉同一條交換關係；基底＝半標準表（$m=2$：2 個、$m=3$：8 個）；$f^\lambda$ 對 $d_\lambda(m)$ | 2 分 35 秒 |
| F43 | `SceneF43Weights` | 對角矩陣 $e_T\mapsto x^Te_T$；8 個表按權重排成六角形（中間 $2x_1x_2x_3$）；最高權重 11/2；$\operatorname{Char}E^{(2,1)}=s_{(2,1)}$；至多 $m$ 列 | 2 分 17 秒 |
| F44 | `SceneF44SchurWeyl` | $GL(E)$ 與 $S_3$ 在 $E^{\otimes3}$ 上可交換（交換圖）；$E^{\otimes n}\cong\bigoplus E^\lambda\otimes S^\lambda$；$8=4\cdot1+2\cdot2+0\cdot1$、$27=10\cdot1+8\cdot2+1\cdot1$；$E^\lambda\cong E^{\otimes n}\otimes_{\mathbb C[S_n]}S^\lambda$ | 2 分 6 秒 |
| F45 | `SceneF45QuadraticRelations` | 同一條交換關係的三個身分：Specht、Schur 模、$2\times4$ 矩陣的子式；Plücker $p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=-3-9+12=0$；預告第 9 章 Grassmannian；總結第 7–8 章 | 2 分 15 秒 |
| | `FultonDemo5` | 以上四個連續播放 | 9 分 17 秒 |

## Fulton《Young Tableaux》第 9–10 章（F46–F55，獨立）

依 `../notes/fulton_plan_ch9-10.md`（草稿 → 生動度與例子檢討 → 程式大綱 → 省 token 定稿）；數學在 `utils/schubert.py`（自我測試：pipe dream 總和＝Schubert 多項式、Grassmann 置換＝Schur 多項式、秩矩陣＝前綴判準＝下降鏈、$\mathbb F_2$ 點數＝$q$-二項式），畫圖在 `utils/schubert_draw.py`；各場景的 `check_math()` 用它們 assert 畫面上的每個數字。用 `FultonDemo6` 連續播放。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| F46 | `SceneF46Plucker` | 六個數認出一個平面：$2\times4$ 矩陣的 6 個子式、換基底全部 ×$\det g$；$p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=0$；練習 2 由 $1,2,1,1,2,3$ 還原矩陣 | 2 分 12 秒 |
| F47 | `SceneF47FlagRing` | 點在線上 $x_1y_{23}-x_2y_{13}+x_3y_{12}=0$；$Fl(\mathbb C^3)\subset\mathbb P^2\times\mathbb P^2$；座標環的維數 $=\dim E^{(a+b,b)}$（$9-1=8$）；不變量、Borel–Weil 各一句 | 2 分 12 秒 |
| F48 | `SceneF48GrassCells` | 數星星：$Gr(2,4)$ 的 6 個胞腔（列梯形矩陣、方框裡的 Young 圖）；$\binom42_q$，$\mathbb F_2$ 上 35 個平面；$\Omega_\lambda$ 與閉包；書上 $\lambda=(5,3,2,2,1)$ | 2 分 9 秒 |
| F49 | `SceneF49FourLines` | 四條線問題：$\sigma_1^4=2\sigma_{22}$（方框裡的兩條路徑＝兩個標準表）；對偶；$Gr(2,5)$：5、$Gr(3,6)$：42；$\sigma_{21}^2=\sigma_{33}+2\sigma_{321}+\sigma_{222}$ | 2 分 29 秒 |
| F50 | `SceneF50FlagCells` | $Fl(3)$ 的 6 個不動點（座標三角形）與胞腔（星號＝$\ell(w)$）；書上 $w=426135$；$[3]_q!$，Fano 平面上 21 個旗、$S_4$：315；$\sigma_w$ 的對偶基底 | 2 分 36 秒 |
| F51 | `SceneF51DividedDifferences` | $H^*(Fl(3))=\mathbb Z[x]/(e_1,e_2,e_3)$ 的 6 個基底；吃多項式的機器 $\partial_i$；$\partial_i^2=0$、辮關係、Leibniz；$\partial_i\sigma_w=\sigma_{ws_i}$ | 2 分 39 秒 |
| F52 | `SceneF52SchubertPolys` | 從 $\mathfrak S_{w_0}=x_1^2x_2$ 沿 $S_3$ 的 Hasse 圖流下來；書上 $54321\to\cdots\to41352=x_1^3(x_2x_3+x_2x_4+x_3x_4)$；穩定性、基底 | 2 分 13 秒 |
| F53 | `SceneF53PipeDreams` | 練習 5：$\mathfrak S_{21543}$ 的 13 項、係數 2 ＝兩張 pipe dream；水管規則、非縮減的反例；全部 14 張（書外延伸：Billey–Jockusch–Stanley） | 2 分 15 秒 |
| F54 | `SceneF54Bruhat` | 秩矩陣 $r_w(p,q)$；前綴排序遊戲（$2143\le4231$、$1423$ 與 $3124$ 不可比）；$S_3$、$S_4$ 的 Hasse 圖；書上 9 位數的下降鏈與卡住的例子；$u\le v\iff X_u\subset X_v$ | 2 分 17 秒 |
| F55 | `SceneF55GrassmannianSchur` | Grassmann 置換：$\mathfrak S_{2413}=s_{21}(x_1,x_2)$、$\mathfrak S_{1342}=e_2$；$p^*\sigma_\lambda=\sigma_w$；四條線在 $Fl(4)$ 重算 $(x_1+x_2)^4\equiv2\mathfrak S_{3412}$；三個「2」；第 9–10 章總結 | 2 分 11 秒 |
| | `FultonDemo6` | 以上十個連續播放 | 23 分 24 秒 |

## Raney 引理筆記（R01–R06，獨立）

依 `../notes/ran_note015_改寫.pdf`（他人所寫的 `ran_note015.txt` 的勘誤與改寫）；數學在 `utils/raney.py` 第 9 節，畫圖在 `utils/raney_draw.py`；各場景開頭的 `check_math()` assert 畫面上的數字。用 `RaneyLemmaDemo` 連續播放。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| R01 | `SceneR01RaneyLemma` | 和為 1 的整數序列 $x=(2,-1,-3,1,2)$ 畫成路徑；5 種循環讀法只有從第 3 點開始的是好讀法；定理（$t=1$ 的循環引理） | 30 秒 |
| R02 | `SceneR02LastMinimum` | 無限重複、$S_{i+M}=S_i+1$；最後一個最低點給出好讀法；換起點 $y$ 的兩種情形（整數：$S_y\ge S_x+1$）；好幾個最低點；$(\frac12,\frac12)$ 與 $(2,0)$ 的反例 | 51 秒 |
| R03 | `SceneR03PositiveCounts` | 加強版：正點數 $3,1,2,5,4$；依 $(S_k,-k)$ 排序得 $3,4,5,2,1$ 與正點數 $5,4,3,2,1$；$P(x)$ 的公式 | 34 秒 |
| R04 | `SceneR04StackCatalan` | 棧的動畫（進進出進出出 → $(2,3,1)$）；5 條 Dyck 路徑；前面加一個 ↑ 變成好路徑；$\binom73=35=7\times5$；$\frac1{2n+1}\binom{2n+1}{n}=C_n=A_1((n),(2))$ | 38 秒 |
| R05 | `SceneR05CardGame` | 洛谷 P6672：$w=(1,2)$、$m=3$ 的模擬（還能摸 1→2→1→1）；還能摸幾張 ＝ 還欠幾個引數；3 種牌序 ↔ 字 1200、2100、2010；$\frac{m!}{m-n+1}$（循環引理＋對稱性）；原筆記的做法與 $w_i\ge1$ 條件 | 53 秒 |
| R06 | `SceneR06Summary` | 三種用法的回顧；原筆記的五個勘誤重點 | 23 秒 |
| | `RaneyLemmaDemo` | 以上六個連續播放 | 3 分 56 秒 |

## Raney (1960) 論文導讀（N01–N12，獨立）

依 `../notes/raney1960_導讀.pdf`，分鏡 `../notes/raney/manim_plan.md`；數學在 `utils/raney.py`，隨機例子由 `utils/raney_examples.py` 產生（固定 seed，每次渲染相同），畫圖在 `utils/raney_draw.py`；各場景開頭的 `check_math()` assert 畫面上的數字。用 `RaneyPaperDemo` 連續播放。
例題集：`python utils/raney_examples.py --md --seed 7 --count 3 --out ../notes/raney/raney_examples_seed7.md`。

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| N01 | `SceneN01PrefixWords` | Cayley：abcd 的 5 種乘積 ↔ 5 棵樹 ↔ 5 個字；前序記法與「型」；$F(G(x,H(y,z),t),K(u))\to230200010$；$a_0=1+\sum(i-1)a_i$ | 46 秒 |
| N02 | `SceneN02RankCounter` | 讀 230200010 的「還欠幾個引數」計數器 ＝ 秩＋1，同步畫秩路徑；Rosenbloom 判別法；020 不是字；字列 3000200 ＝ 3000 | 200 | 40 秒 |
| N03 | `SceneN03ThreeReadings` | 同一個 2 字列的三種畫法：Raney 的秩路徑、倒過來讀的 Chu 路徑、森林；高度 ＝ −後綴的秩；Gessel 的後序碼 00201（鏡射） | 40 秒 |
| N04 | `SceneN04RaneyProof` | σ = 0020030 的 7 個循環變形（k = 2、5）；Raney 證明四步：圓周上最大的弧 α、從 α 讀、切成字並輪換、從字中間讀不行；200200 的重複 | 47 秒 |
| N05 | `SceneN05DoubleCounting` | 30 個字串排成 5 × 6，每列恰一個字 ⇒ 30 = 6 × 5；定理 2.2；Chu 原文 Fig. 1 的 5 種分法 ↔ 5 個字（203000 的分解）；Cayley $L(1;0,k)=C_k$ | 45 秒 |
| N06 | `SceneN06RandomExamples` | 循環引理 ＝ 均勻隨機樹產生器：打亂 → 轉到好起點 → 樹與運算式；2100 次抽樣的直方圖；隨機不交叉分法；例題集指令（`utils/raney_examples.py`） | 40 秒 |
| N07 | `SceneN07SplitFirst` | 定理 2.3：2003000 的唯一 1 字列開頭；12 = 5+1+1+5；定理 2.4：12 = 5+3+4、5 = 2+3（Chu 的收尾）；$F_n=F_1^n$、$F_1=1+\sum x_iF_1^i$ | 45 秒 |
| N08 | `SceneN08LStar` | 大代數的變數 $E_i$；$L^*$ 的前幾項；定理 4.1 與 $E_1E_2$ 的係數 3 = 1 + 2；三種代換（依邊數 → $C_e$、依節點數不行、Chu 的 (6)(8)(9)(10)） | 37 秒 |
| N09 | `SceneN09Lagrange` | $[x^n]w=\frac1n[x^{n-1}]\phi^n$ ＝ 樹的權重和；Motzkin 4 棵樹；$\phi=2+3x+x^3$ 的 18；同態 $E_j\mapsto a_0^{j-1}a_jx^j$；四個 $\phi$ 的係數表；冪次版本 | 45 秒 |
| N10 | `SceneN10Trinomial` | 三項式 $w=1+xw^n$ 的 Fuss–Catalan 表；Problem 4983（$P_5(2)=3$、Kelly 的方程）；六邊形切成四邊形 3 種；$C_n$ 奇 ⇔ $n=2^j-1$ | 40 秒 |
| N11 | `SceneN11Convolution` | 定理 7.1（森林切兩片）；投票數表、$b(2,3)=14=5+2+2+5$；Gould 的 $G$：$\gamma=1$ ＝ Chu 的 $A_t$（$\alpha=\frac12$ 也成立）、$\gamma=0$ ＝ Abel（50 = 16+9+9+16） | 46 秒 |
| N12 | `SceneN12Summary` | 邏輯流程圖；Chu 講義第 4–8 節 ↔ Raney 的定理對照 | 23 秒 |
| | `RaneyPaperDemo` | 以上十二個連續播放 | 8 分 26 秒 |

## Chu 的部分（01–09）

| 代號 | 類別名稱 | 內容 | 長度 |
|---|---|---|---|
| 01 | `Scene01ClassicalCatalan` | 卡塔蘭數公式；6 個點的不交叉配對與交叉配對；$C_3=5$ 的五種配對 | 34 秒 |
| 02 | `Scene02FromPairsToBlocks` | 弦 → 三角形 → 四邊形 → 五邊形；引入 $\vec v$ 與 $\vec n$ | 30 秒 |
| 03 | `Scene03GeneralizedSetup` | 例子 $\vec n=(2,1)$、$\vec v=(2,3)$；總點數 $N=7$；Chu 的定理；交叉的反例；共 21 種 | 41 秒 |
| 04 | `Scene04PaperExample` | 論文 Fig. 1：旋轉得到 5 種分法；為什麼只有 5 種；公式也算出 5 | 41 秒 |
| 05 | `Scene05RootDecomposition` | **核心**：固定一點 → 根群組 → 切成 $v_i$ 段 → 各段獨立 → $x_iD^{v_i}$ | 55 秒 |
| 06 | `Scene06Recurrence` | $\vec r_1+\cdots+\vec r_{v_i}=\vec n-\vec e_i$；論文式 (5)；用 Fig. 1 驗算 $2+3=5$ | 55 秒 |
| 07 | `Scene07GeneratingFunction` | 生成函數 $D$；各項飛入組成論文式 (6)；退化成 $D=1+xD^2$ 檢查 | 51 秒 |
| 08 | `Scene08FormulaVerification` | **Raney 公式的完整證明**（見下一節），再推出論文式 (10) 與 $D=C$ | 4 分 2 秒 |
| 09 | `Scene09Summary` | 整篇論文的流程圖與結論 | 22 秒 |
| 08r | `Scene08RaneyProof` | 第 8 場景裡只有 Raney 證明的部分 | 3 分 2 秒 |
| | `FullDemo` | 01–09 連續播放 | 約 9 分 40 秒 |
| | `CompleteDemo` | 00a–00m ＋ 03–09 | 16 分 50 秒 |
| | `MITCompleteDemo` | 00a–00k ＋ M01–M14 ＋ 00l、00m ＋ 03–09 | 30 分 24 秒 |

### 第 8 場景：Raney 公式的證明

論文第 93 頁直接引用 Raney 公式（式 (9)）。第 8 場景把它從頭證明，分成八段（第 0 段是路線圖）：

| 段 | 內容 |
|---|---|
| 0 | 路線圖：要證明 $C=1+\sum_i x_iC^{v_i}$ |
| 1 | 定義 $A_t(\vec n)=\frac{t}{N+t}\binom{N+t}{\vec n}$，寫出 Raney 公式 $A_{s+t}(\vec n)=\sum_{\vec r}A_s(\vec r)A_t(\vec n-\vec r)$ |
| 2 | **路徑**：↑ 步高度 $+1$，第 $i$ 型步高度 $1-v_i$。用 $n_i$ 個第 $i$ 型步與 $t+\sum n_i(v_i-1)$ 個 ↑ 步，終點高度 $t$。**好路徑**：出發後高度一直 $>0$ |
| 3 | **循環引理**：每條路徑的 $N+t$ 種循環讀法中恰有 $t$ 種是好路徑。證明用「把路徑無限重複，從右邊照水平光」 |
| 4 | 雙重計數：$(N+t)\cdot G_t(\vec n)=t\binom{N+t}{\vec n}$，所以好路徑數 $G_t(\vec n)=A_t(\vec n)$ |
| 5 | 終點 $s+t$ 的好路徑，在「最後一次落在高度 $s$」的點切開，一一對應，這就是 Raney 公式；用 12 條路徑驗算 |
| 6 | Raney 公式 $\Rightarrow F_{s+t}=F_sF_t \Rightarrow [x^{\vec n}]C^t=A_t(\vec n)$；取 $t=v_i$ 加總得到論文式 (10) |
| 7 | $D$ 與 $C$ 滿足同一條方程，所以 $D=C$ |

「路徑」與「循環引理」是證明 Raney 公式的標準方法（Dvoretzky–Motzkin 循環引理），不是論文原文的內容。

## 資料夾結構

下面的路徑以 `C:\mypython\manim\projects\catalan930\` 為基準。

```text
catalan930/
├── 交接說明_HANDOFF.md       ★ 最權威的說明：內容、全部指令、場景與影片清單、踩過的坑
├── codes/                    動畫程式（manimgl 一律在這裡執行）
│   ├── README.md             本檔
│   ├── main.py               每個場景的同名子類別＋十種連續播放：CatalanIntroDemo、FullDemo、CompleteDemo、MITDemo、MITCompleteDemo、
│   │                         FultonDemo（F01–F08）、FultonDemo2（F09–F19）、FultonDemo3（F20–F27）、FultonDemo4（F28–F41）、FultonDemo5（F42–F45）、FultonDemo6（F46–F55）
│   ├── render_all.py         一次輸出很多支影片（--intro、--chu、--mit、--fulton…--fulton6、各 -demo、場景代號）
│   ├── render_all.bat        一鍵輸出（按兩下出現選單；包裝 render_all.py；必須純 ASCII、CRLF）
│   ├── check_env.py          環境檢查（python check_env.py --render）
│   ├── custom_config.yml     ManimGL 設定（輸出資料夾、背景色、字型）—— 只能寫英文
│   ├── scenes/               一個檔案一個場景：scene00a…00m（卡塔蘭模組）、scene01…09＋08r（Chu）、sceneM01…M14（MIT 補充）、sceneF01…F55（Fulton）
│   ├── data/
│   │   └── fulton7_math.json 第 7 章的固定算例（複製自 ../../fulton7_agent_pack 的 MATH_DATA.json，已驗證）
│   ├── utils/
│   │   ├── styles.py           顏色、字型、zh()、mixed() 等文字工具
│   │   ├── scene_base.py       ChuScene：左上標題、底部字幕、clear_stage()
│   │   ├── circle_points.py    圓、圓周上的點、弦、點的標籤、弦的交點
│   │   ├── polygon_groups.py   群組的畫法、Configuration（圓+群組+點）、弓形區域
│   │   ├── root_figure.py      「根分解」示意圖、群組小圖示
│   │   ├── lattice_paths.py    Raney 證明用的路徑圖形、步驟方塊
│   │   ├── catalan_draw.py     卡塔蘭模組的圖形：三角剖分、滿二元樹、括號、格子／Dyck 路徑、配對、上色
│   │   ├── mit_draw.py         MIT 補充的圖形：弧圖、Young 圖（含鉤）、平面樹、數字方塊
│   │   ├── fulton_draw.py      Fulton 的圖形：Young 表、字母方塊與 Knuth 變換、斜表、雙列陣列、矩陣球、assert_in_frame／assert_apart
│   │   ├── rep_data.py         Fulton 第 7 章的固定算例（讀 data/fulton7_math.json）與置換、tabloid、polytabloid、表示矩陣、群環
│   │   ├── rep_draw.py         Fulton 第 7 章的圖形：tabloid、帶方向的行 tabloid、帶號線性組合、矩陣
│   │   ├── formulas.py         常用公式的 Tex 物件
│   │   ├── counting.py         純 Python 的計數與驗證（公式、暴力列舉、遞迴、Raney、卡塔蘭物件、MIT 補充）
│   │   ├── raney.py            純 Python：Raney (1960) 的字、循環引理、L(n;a)、L*、Lagrange 反演、卷積；第 9 節整數序列的 Raney 引理（N、R 場景與兩份講義用）
│   │   ├── raney_examples.py   純 Python：用循環引理製造例子（均勻隨機的字／樹／不交叉分法、Markdown 例題集）
│   │   ├── raney_draw.py       N、R 場景的圖形：字的方塊、平面樹、秩路徑、整數步路徑、牌
│   │   ├── schubert.py         純 Python：Fulton 第 9–10 章（Plücker、Schubert 胞腔與計算、Bruhat 序、差商、Schubert 多項式、pipe dream）
│   │   ├── schubert_draw.py    F46–F55 的圖形：列梯形矩陣、方框裡的 Young 圖、Hasse 圖、pipe dream
│   │   └── tableaux.py         純 Python 的 Young 表運算與驗證（插入、乘積、jeu de taquin、Schur 多項式、Knuth、R-S-K、LR、對稱函數、半標準表與權重）
│   ├── latex_cache/          LaTeX 編譯的中間檔（ManimGL 自動產生，可以刪）
│   └── renders/              輸出的 1080p 影片（123 支；不要刪除或覆寫）
├── notes/                    講義與計畫表（xelatex，在 notes/ 裡編譯兩次）
│   ├── chu1987_導讀.tex/.pdf      Chu 1987＋卡塔蘭模組＋附錄 A（MIT 補充），40 頁；圖：make_catalan_figs.py、make_mit_figs.py（→ mit/）
│   ├── young_tableaux_導讀.tex/.pdf Fulton 第 1–8 章的講義；內文 fulton/part1..6.tex，圖與數字檢查 fulton/make_figs.py（→ fulton/figs.tex）
│   ├── raney1960_導讀.tex/.pdf    Raney (1960) 論文導讀；內文 raney/part1..6.tex，圖與數字檢查 raney/make_figs.py（→ raney/figs.tex）
│   ├── fulton_plan*.md            各章的計畫表（ch2-4、ch5-6、ch7、ch8、ch9-10；ch7-8 已被取代）
│   └── mit_plan.md、note1012.txt…  其他計畫與原始筆記
└── ref/                      參考文獻 PDF 與抄錄（僅供個人研讀，不可散布）
```

相關的外部資料夾（以 `C:\mypython\manim\projects\` 為基準）：`ref/fulton/`（Fulton 各章 PDF 與 `md/` 轉檔）、`ref/sagan/`、
`ref/Fulton78_整合參考.md`、`ref/fulton78_manim_大綱_合併版.md`（第 7–8 章分鏡）、`fulton7_agent_pack/`（第 7 章固定算例與場景卡）、`combkit/`（可攜工具包）。

## 數值驗證

```bash
python utils/counting.py
```

- 第 1–3 節：用三種獨立的方法（論文的公式、暴力列舉、論文式 (5) 的遞迴）計算同一批例子並互相比對。
- 第 4 節：逐步檢查 Raney 公式的證明。
- 第 5 節：卡塔蘭模組的每一種物件都用兩種方法列舉（由樹產生 vs. 暴力列舉），檢查 $n=0$ 到 $6$ 的數目都是 $C_n$，並檢查彼此的一一對應、反射原理、一般投票定理與 $k$ 倍推廣、$C=1+xC^2$。

- 第 6 節：MIT 補充用到的每一種計數都用兩種方法算（平面樹、弧圖、堆疊／佇列排序 ⇔ 模式迴避、整數分割、標準 Young 表 ⇔ 鉤長公式、角落遞迴、鉤上漫步的精確機率、醉漢走路、循環引理），並檢查貫穿例子的每個值。

最後應印出「全部一致」、「Raney 公式證明的每一步都通過」、「卡塔蘭基礎模組：所有物件的數目與一一對應都通過」、「MIT 補充模組：所有計數與一一對應都通過」。
另外 `python utils/tableaux.py` 應印出「Fulton 第 1 章：插入、乘積、jeu de taquin 全部驗證通過」，接著是「Fulton 第 2–4 章：Knuth 等價、L(w,k)、R-S-K、矩陣球全部驗證通過」，最後一行是「Fulton 第 5–6 章：Littlewood–Richardson 規則、對稱函數全部驗證通過」（`check_env.py` 兩者都檢查）。`python utils/raney.py` 應印出「Raney (1960)：字、循環引理、L(n;a)、L*、Lagrange 反演、第 6–7 節全部驗證通過」。
第 7 章另有 `python -m utils.rep_data`（應印出「rep_data：固定算例與 tableaux.py 的獨立重算全部一致」）；第 8 章的數字在各場景的 `check_math()` 裡由 `tableaux.py` 現算。
講義的數字由 `python ../notes/fulton/make_figs.py`（在 `notes/` 裡執行 `python fulton/make_figs.py`）在產生圖之前全部檢查。
每個場景開頭也有 `assert`，數字不對時渲染會直接失敗。

## 想修改時

- **改文字**：每個場景裡的 `self.say(...)` 是底部字幕。以 `$` 開頭的字串是 LaTeX 數學式，其餘是中文。
- **改例子**：每個場景檔案最上方的常數就是點的編號（從正上方順時針、由 0 起算）或路徑的字（R/U、U/D、A/B）。
- **改顏色或字型**：改 `utils/styles.py`；卡塔蘭模組的根／左／右顏色在 `utils/catalan_draw.py` 開頭。
- **改節奏**：調整 `self.wait(秒數)` 與 `run_time=`。
- **新增場景**：繼承 `utils.scene_base.ChuScene`；輔助函式寫成模組層級的函式（不要寫成場景的方法，否則連續播放時會找不到）；再到 `main.py`、`render_all.py` 登記（新的連續播放也要加進 `render_all.bat` 的 `DEMOS` 變數）。

## 已知限制

- `custom_config.yml` 只能寫英文。ManimGL 在繁體中文 Windows 上用 cp950 讀這個檔，寫中文會出錯。
- 公式著色時要整個因子一起上色，例如 `x_1^{n_1}`。只給 `x_1` 上色會讓指數的位置偏掉。
- 多段字串的 `Tex("a", "b")` 用 `[1]` 取到的是單一字形，不是第二段；要上色請用 `t2c` 或依字形位置（例如 `catalan_product_tex`）。
- **Tex 字串的開頭、結尾不要放 `\;`、`\,` 之類的間距指令。** ManimGL 編譯「帶顏色標記」的版本時會失敗，卻不報錯，而是沿用上一個公式的 DVI，把錯的圖形存進快取（例如箭頭變成上一句的公式）。遇到公式顯示成別的東西，先改字串，再執行 `manimgl --clear-cache`。
- LaTeX 出錯時先執行 `manimgl --clear-cache`。
- 輸出影片時偶爾會在最後一步出現 `PermissionError: [WinError 32]`（檔案正由另一個程序使用）。這發生在 ManimGL 把 `renders/X_temp.mp4` 改名成 `X.mp4` 的時候，可能是防毒軟體正在掃描剛寫好的檔案。重新輸出那一個場景（例如 `python render_all.py 00a`），再刪掉留下的 `X_temp.mp4`。
- **不要同時跑兩個 `manimgl`**：它們會共用 `%TEMP%` 裡 `Text` 的暫存 .svg 與 `latex_cache/working.tex`，互相覆蓋而失敗。要平行試渲染就用 combkit 的 `render_check.py`（各自的資料夾與快取），正式輸出一次一個。
- 影片沒有配音與背景音樂。
