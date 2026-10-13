# Fulton《Young Tableaux》第 1 章 → Manim 演示：計畫表（2026-10-04）

## 0. 範圍
- 來源：`ref/9781107108738_A23693136.pdf` = W. Fulton, *Young Tableaux*（LMS Student Texts 35, Cambridge）的節錄，28 頁。
- 內容只有：Notation（書 p.1–4）、Part I 第 1 章 Bumping and sliding 的 §1.1 Row-insertion 與 §1.2 Sliding; jeu de taquin 前半（到 p.16）。
  （PDF 第 13–28 頁；第 3–12 頁是版權頁、目錄、序。）
- 影片**獨立**，不接先前的卡塔蘭／Chu／MIT 影片；只沿用程式基礎（`ChuScene`、`mit_draw.YoungDiagramMob`、渲染工具）。
- 版權：書是使用者的個人參考資料。純文字版只存在本機供研讀；畫面上的說明用自己的話，不逐字抄書。

## 1. 步驟與省 token 原則
| 步驟 | 做法 | 產出 |
|---|---|---|
| 1 計畫 | 只看 PDF 中繼資料與目錄頁 | 本檔（第一版） |
| 2 純文字 | `pdftotext` 先機械轉出；有 Young 表的頁面由 2 個代理人對照頁面影像重新謄寫（圖改成等寬文字表格），同時各交一份內容摘要 | `ref/fulton_ch1_text.md` |
| 3a 補計畫 | 只讀摘要（不讀全文），把場景規格補進本檔第 3 節 | 本檔（第二版） |
| 3b 數學資料 | 1 個代理人寫 `codes/utils/tableaux.py`（純 Python：插入、bumping 路徑、字、乘積、jeu de taquin、rectification、Schur 多項式），附暴力驗證 | `tableaux.py` |
| 3c 場景 | 每幕 1 個代理人平行製作，數字都 assert 自 `tableaux.py`；用暫存區的嚴格渲染工具檢查總覽圖 | `scenes/sceneF0x_*.py` |
| 3d 審查 | 1 個代理人看全部場景的總覽圖、抽查數學並修正 | — |
| 3e 整合 | `main.py` 加 `FultonDemo`、`render_all.py` 加 `--fulton`／`--fulton-demo`、輸出 1080p、更新 README／交接說明 | 影片 |
- 主對話只讀摘要、總覽圖與代理人的簡短回報；長文件只給代理人讀。

## 2. 場景草案（步驟 3a 會依摘要修訂）
| 代號 | 主題（書中位置） |
|---|---|
| F01 | Young 圖、分割、共軛分割（Notation） |
| F02 | 填數：半標準 Young 表 vs 標準 Young 表；斜形狀 λ/μ 與斜表（Notation） |
| F03 | Schur 多項式 s_λ = Σ_T x^T：例子、對稱性、s_(n)=h_n、s_(1^n)=e_n（Notation） |
| F04 | 列插入（bumping）演算法：逐步示範（§1.1） |
| F05 | Row Bumping Lemma：兩次插入的 bumping 路徑與新格子的位置；推論（插入遞增／遞減序列 → 水平／垂直條）（§1.1） |
| F06 | 表的字（word）與乘積 T·U（§1.1） |
| F07 | jeu de taquin：內角、滑動、rectification；用斜表 T*U 得到 T·U（§1.2，書在後面章節才證明）（§1.2） |
（第二版：F07 拆成 F07 滑動、F08 T∗U 的 rectification，共 8 幕。）

## 3. 場景規格（第二版，依謄寫代理人的摘要；書頁碼 p.N；格子 (列,行) 1 起算）
純文字版：`ref/fulton_ch1_text.md`（需要原文細節時再查，可用 〔p. N〕 搜尋）。

| 代號 | 檔名 / 類別 | 內容（例子都用書上的資料） | 長度 |
|---|---|---|---|
| F01 | `sceneF01_young_diagrams.py` / `SceneF01YoungDiagrams` | Young 圖 = 分割（p.1）：λ=(6,4,4,2)、n=16、λ⊢n、\|λ\|、記號 (d^a)；共軛 λ̃：沿對角線翻轉 → (4,4,3,3,1,1)（p.2）；numbering 與 filling 的差別 | ~45s |
| F02 | `sceneF02_tableaux.py` / `SceneF02Tableaux` | 表（p.2）：[[1,2,2,3,3,5],[2,3,5,5],[4,4,6,6],[5,6]]，逐列檢查「列弱增、行嚴格增」；標準表 [[1,3,7,12,13,15],[2,5,10,14],[4,8,11,16],[6,9]]；轉置：標準表仍標準、一般表不一定；斜形狀 (5,5,4,3,2)/(4,4,1) 與斜表 [[·,·,·,·,2],[·,·,·,·,6],[·,2,4,4],[2,3,6],[5,6]]（p.4） | ~55s |
| F03 | `sceneF03_schur.py` / `SceneF03Schur` | x^T（p.3）：上面的表 → x1 x2³ x3³ x4² x5⁴ x6³；s_λ(x1..xm)=Σx^T；例 s_(2,1)(x1,x2,x3) 列出全部 8 個表並合併（x1x2x3 的係數 2 = (2,1) 的標準表數）；交換變數看出對稱；s_(n)=h_n、s_(1^n)=e_n（p.3–4） | ~60s |
| F04 | `sceneF04_row_insertion.py` / `SceneF04RowInsertion` | 列插入（p.7–8）：T=[[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]] ← 2：2 擠出 (1,4) 的 3、3 擠出 (2,3) 的 5、5 擠出 (3,3) 的 6、6 接在第 4 列 → [[1,2,2,2],[2,3,3,5],[4,4,5],[5,6,6]]，新格子 (4,3)；為何仍是表（被擠出的數在同一行或往左）；反向擠出（p.8–9）從 (4,3) 還原 T 與 x=2 | ~60s |
| F05 | `sceneF05_bumping_lemma.py` / `SceneF05BumpingLemma` | bumping 路徑 R、新格子 B（p.9）；Row Bumping Lemma 兩種情況（x≤x′：R 嚴格在 R′ 左邊、B 嚴格在 B′ 左邊且不高於；x>x′：R′ 不在 R 右邊、B′ 嚴格在 B 下面且不在右邊），各用一個小例子連續插入兩次、上色路徑（例子由 `tableaux.py` 選並 assert）；命題（p.11）：插入弱遞增的數 → 新格子落在不同行（水平條）、由左到右；嚴格遞減 → 不同列（垂直條）、由上到下 | ~60s |
| F06 | `sceneF06_product.py` / `SceneF06Product` | 表的字 w(U)：由最下列讀到最上列；乘積 T·U = 把 w(U) 逐個插入 T（p.11–12）：T 同 F04、U=[[1,3],[2]]、w(U)=2 1 3 → [[1,2,2,2],[2,3,3,5],[4,4,5],[5,6,6]] → [[1,1,2,2],[2,2,3,5],[3,4,5],[4,6,6],[5]] → [[1,1,2,2,3],[2,2,3,5],[3,4,5],[4,6,6],[5]]；Claim 1：結合律、空表是單位元（小例子兩種括法驗算） | ~55s |
| F07 | `sceneF07_jeu_de_taquin.py` / `SceneF07JeuDeTaquin` | 斜表（p.12）[[·,·,·,·,2],[·,·,·,·,6],[·,2,4,4],[2,3,6],[5,5]]：內角 (2,4)、(3,1)，外角；滑動規則（洞取右邊／下面較小者，相等取下面）（p.13）；從 (3,1) 滑：2 上移 → 3 左移 → 5 上移 → 洞在 (5,2) 刪掉 → [[·,·,·,·,2],[·,·,·,·,6],[2,2,4,4],[3,5,6],[5]]；局部規則圖（p.14）；反向滑動；rectification；Claim 2：與內角的選法無關（p.15） | ~65s |
| F08 | `sceneF08_rectify_product.py` / `SceneF08RectifyProduct` | T∗U（p.15）：空矩形 + 左下 T、右上 U；Exercise 1（p.16）的斜表 [[·,·,·,·,1,3],[·,·,·,·,2],[1,2,2,3],[2,3,5,5],[4,4,6],[5,6]]，8 次滑動（洞的路徑 (2,4)→(2,5)、(1,4)→(1,6)、(2,3)→(4,4)、(1,3)→(3,4)、(2,2)→(6,2)、(1,2)→(5,3)、(2,1)→(6,1)、(1,1)→(5,2)，以 `tableaux.py` 重算為準）→ 結果等於 F06 的 T·U（Claim 3）；結尾列出三個 Claim，註明書在第 2–3 章證明 | ~70s |

連續播放：`FultonDemo` = F01–F08（獨立，不接其他影片）。

## 3.5 數學資料 `codes/utils/tableaux.py`（純 Python，`python utils/tableaux.py` 自我測試）
- **格子 (i,j) 從 0 起算**、第 0 列在最上面（上表的書頁座標是 1 起算，換算時減 1）。分割 = 非遞增 tuple；表 = 列 tuple 的 tuple；
  斜表 = 同樣的列，但第 i 列前面放 μ_i 個 `None`；多項式 = `{指數 tuple: 係數}`。滑動時相等取下面、反向滑動相等取上面。
- 分割：`partitions(n, max_parts)`、`conjugate`、`young_boxes`、`corners`、`addable_boxes`、`contains`、`skew_boxes`、`is_horizontal_strip`、`is_vertical_strip`。
- 表：`shape`、`num_boxes`、`is_tableau`、`is_standard`、`transpose`、`content(T,m)`（x^T 的指數）、`ssyt(lam,m)`、`standard_tableaux`。
- 插入：`row_insert(T,x)` → `(T', route, new_box)`（route 每列一格、由上到下）；`bump_steps(T,x)` → `[(box, placed, bumped或None)]`（逐步動畫用）；
  `reverse_bump(T, box)` → `(T0, x, route)`；`tableau_word(S)`（由最下列讀到最上列、略過 None）；`insert_word_steps(word, T)` → `[(x, T_after, route, new)]`；`product(T,U)`。
- 滑動：`inside_corners(S)`、`outside_corners(S)`、`skew_shape(S)` → (λ,μ)、`forward_slide(S, corner)` → `(S', hole_path)`（第 k 步把 path[k+1] 的數移到 path[k]）、
  `reverse_slide`、`jdt_steps(S, choose=None)` → `[(corner, path, S_after)]`（預設取最下面的內角）、`rectify(S, choose)`、`star(T,U)`（T 在左下、U 在右上）。
- Schur：`schur_poly(lam,m)`、`complete_h(n,m)`、`elementary_e(n,m)`、`kostka(lam,mu)`。
- 書上的例子常數：`FULTON_TABLEAU`、`FULTON_STANDARD`、`FULTON_INSERT_T`、`FULTON_PRODUCT_U`、`FULTON_SKEW`（用之前先確認是哪一頁的例子：p.4 與 p.12 的斜表最後一列不同，[5,6] 與 [5,5]）。
- 畫 Young 圖可用 `utils/mit_draw.py` 的 `YoungDiagramMob`（英式、`.cell(i,j)`、填數、鉤）；斜表可把 μ 的格子畫成灰色或不畫。

## 4. 實作規則（沿用 `mit_plan.md` 第 6 節）
- ManimGL；繼承 `ChuScene`；字幕繁體中文；輔助函式寫成模組層級；畫面上的數字都 assert。
- Young 圖用英式畫法（第一列在最上面），與書一致；格子內的數用 Tex。
- 只建立自己的場景檔；共用檔案不改。
- 檔名 `codes/scenes/sceneF0x_*.py`、類別 `SceneF0x…`；連續播放 `FultonDemo`（只含 F01–F0x）。
