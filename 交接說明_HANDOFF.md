# 交接說明：卡塔蘭數與 Chu (1987) 廣義卡塔蘭數 —— 講義與 Manim 演示

寫給接手這個專案的人或 AI 助理。讀完這份就能在新電腦上把專案跑起來，知道每個檔案做什麼，並繼續修改。

**路徑的寫法：** 本文件裡的相對路徑（`notes/…`、`codes/…`、`ref/…`）都相對於**本文件所在的資料夾**——
開發機上是 `C:\mypython\manim\projects\catalan930`（例如 `notes/mit_plan.md` 就是 `C:\mypython\manim\projects\catalan930\notes\mit_plan.md`），
可攜版則是解壓縮後的資料夾。`C:\mypython\manim` 是 ManimGL 本身的資料夾，底下**沒有** `notes/`。

最後更新：2026-10-13（Raney (1960) 論文導讀 `notes/raney1960_導讀.pdf`；可攜版 `catalan_portable_104`、一鍵輸出 `codes/render_all.bat`、本資料夾改用 git 管理；之前：Fulton 第 8 章 F42–F45、第 7 章 F28–F41；Fulton《Young Tableaux》第 2–4 章 F09–F19、第 5–6 章 F20–F27 的獨立演示；Young 表講義獨立成 `notes/young_tableaux_導讀.pdf`；可攜工具包 combkit 1.5.0（2026-10-14，加入 raney）

---

## 1. 這個專案是什麼

把下面這篇 4 頁的論文做成「容易懂的中文講義」與「Manim 動畫演示」：

> Wenchang Chu, *A new combinatorial interpretation for generalized Catalan number*,
> Discrete Mathematics 65 (1987) 91–94.

2026-10-03 在動畫前面加了「卡塔蘭基礎模組」（13 個場景）：先把經典卡塔蘭數的各種物件與遞迴講清楚，再接到 Chu 的推廣。
製作依據是使用者的指令 `notes/note1012.txt`，內容來源是：

> Aybeyan Selimi、Muzafer Saračević, *Catalan Numbers and Applications*,
> Vision International Scientific Journal 4(1) (2019) 99–114.（`ref/aybeyan-pdf.pdf`）

2026-10-04 再加上「MIT 18.212 Algebraic Combinatorics Lecture 1–4」的補充（14 個場景 M01–M14）。
使用者提供的原始資料是 `notes/MIT18212_1_4.txt`（四堂課的理論整理）與 `notes/note103how.txt`（ChatGPT 給 AI 助理的指令）；
兩者都很長，已濃縮成 `notes/MIT18212_L1-4_精簡.md` 與 `notes/mit_plan.md`（盤點、決定、場景規格），**先讀精簡版**。

2026-10-05 另做一組**獨立**的演示（不接上面的影片）：W. Fulton, *Young Tableaux*（LMS Student Texts 35）的 Notation 與第 1 章（§1.1 列插入、§1.2 jeu de taquin），
8 個場景 F01–F08。來源是 `ref/9781107108738_A23693136.pdf`（28 頁節錄，掃描檔）；已謄寫成純文字 `ref/fulton_ch1_text.md`（圖改成文字表格），
計畫表 `notes/fulton_plan.md`。
2026-10-10 接著做第 2–4 章（字與 Knuth 等價、遞增子序列、R-S-K），11 個場景 F09–F19，同樣獨立。來源是使用者放在
`C:\mypython\manim\projects\ref\fulton\` 的各章 PDF（掃描＋OCR；全書 PDF 只有影像，只當參考），已機械轉成 Markdown（同資料夾的 `md\`）；
計畫表 `notes/fulton_plan_ch2-4.md`。
同一天再做第 5–6 章（Littlewood–Richardson 規則、對稱多項式），8 個場景 F20–F27，也是獨立的一組；計畫表 `notes/fulton_plan_ch5-6.md`。
2026-10-12 再做第 7 章（對稱群的表示），14 個場景 F28–F41，同樣獨立；分鏡來自使用者的 `C:\mypython\manim\projects\ref\fulton78_manim_大綱_合併版.md`，固定算例來自 `C:\mypython\manim\projects\fulton7_agent_pack`；定稿計畫 `notes/fulton_plan_ch7.md`。同日接著做第 8 章（一般線性群）4 個場景 F42–F45（使用者大綱的 F800–F803），計畫 `notes/fulton_plan_ch8.md`，連續播放 `FultonDemo5`。

**目前狀態：全部完成，可以直接使用。**

| 成品 | 位置 | 狀態 |
|---|---|---|
| 中文講義（40 頁） | `notes/chu1987_導讀.pdf`（原始檔 `.tex`） | 完成。第 1 節是卡塔蘭基礎模組（13 個小節，依序對應 00a–00m），第 7 節是 Raney 公式的完整證明，附錄 A 是 MIT 補充（A.1–A.14，依序對應 M01–M14） |
| Raney (1960) 導讀（33 頁） | `notes/raney1960_導讀.pdf`（原始檔 `.tex`，內文 `notes/raney/part1..6.tex`） | 完成（2026-10-13）。G. N. Raney, *Functional composition patterns and power series reversion*（1960）的逐節導讀，記號與 Chu 講義相容；附記號對照表、大量例子、Gessel (2016) 與 Problem 4983 的補充、練習與答案。數學在 `codes/utils/raney.py`，圖與數字檢查在 `notes/raney/make_figs.py` |
| Young 表講義（25 頁） | `notes/young_tableaux_導讀.pdf`（原始檔 `.tex`，內文 `notes/fulton/part1..6.tex`） | 完成（2026-10-11，從 Chu 講義的附錄 B 獨立出來並補上第 5–6 章；2026-10-12 補上第 7 章；2026-10-13 補上第 8 章）。第 1 節回顧 Fulton 第 1 章（F01–F08），第 2–8 節依序是第 2–8 章（F09–F45） |
| 卡塔蘭基礎模組 13 個場景 | `codes/scenes/scene00a…00m` | 完成（2026-10-03），都可單獨執行 |
| Chu 的部分 9 個場景 | `codes/scenes/scene01…09` | 完成，都可單獨執行 |
| MIT 補充 14 個場景 | `codes/scenes/sceneM01…M14` | 完成（2026-10-04），都可單獨執行 |
| Fulton 第 1 章 8 個場景 | `codes/scenes/sceneF01…F08` | 完成（2026-10-05），都可單獨執行；`FultonDemo` 連續播放 |
| Fulton 第 2–4 章 11 個場景 | `codes/scenes/sceneF09…F19` | 完成（2026-10-10），都可單獨執行；`FultonDemo2` 連續播放 |
| Fulton 第 5–6 章 8 個場景 | `codes/scenes/sceneF20…F27` | 完成（2026-10-10），都可單獨執行；`FultonDemo3` 連續播放 |
| Fulton 第 7 章 14 個場景 | `codes/scenes/sceneF28…F41` | 完成（2026-10-12），都可單獨執行；`FultonDemo4` 連續播放 |
| Fulton 第 8 章 4 個場景 | `codes/scenes/sceneF42…F45` | 完成（2026-10-12），都可單獨執行；`FultonDemo5` 連續播放 |
| 1080p 影片 92 支 | `codes/renders/` | 已輸出，見第 4 節的表 |
| 數學驗證程式 | `codes/utils/counting.py` | 全部通過 |
| 環境檢查程式 | `codes/check_env.py` | 開發機上全部通過（2026-10-05；也檢查 `tableaux.py`） |
| 版本控制 | 本資料夾是獨立的 git repo（2026-10-13 起；`.gitignore` 排除 `codes/renders/`、`codes/latex_cache/`、`__pycache__`、LaTeX 中間檔） | 見第 2 節最後的「版本控制」 |
| 一鍵輸出 | `codes/render_all.bat` | 2026-10-13 在 104 的複本上測過（從沒有 Anaconda 的 PATH 按兩下也能自己啟用 conda） |
| 全新安裝測試 | `catalan_portable_103` 的複本＋全新 Python 虛擬環境（102 測試時裝到的是 numpy 2.2.6、Pillow 12.3，比開發機新） | `.\install_windows.bat` 後 `check_env.py --render` 全部通過；M01–M14 用空的 LaTeX 快取、嚴格模式全部重新輸出成功（00a–00m 在 102 測過）；講義的圖重新產生後與原檔相同，講義可以編譯（2026-10-04） |

**工作資料夾與可攜版。** 開發機上的工作資料夾是 `C:\mypython\manim\projects\catalan930`，ManimGL 已經裝好，不需要第 2 節的安裝步驟。
可攜版是工作資料夾的複本，另外附上 ManimGL 原始碼與安裝腳本（見第 3 節），放在 `C:\mypython\manim\projects\`：

| 可攜版 | 日期 | 內容 |
|---|---|---|
| `catalan_portable_101.zip` | 2026-10-01 | 加入卡塔蘭模組**之前**的版本（講義 15 頁、9 個場景） |
| `catalan_portable_102` | 2026-10-03 | 卡塔蘭模組 13 個場景、講義 23 頁、26 支 1080p 影片（**不含** MIT 補充 M01–M14） |
| `catalan_portable_103` | 2026-10-04 | 再加上 MIT 補充 14 個場景、講義 40 頁（含附錄 A）、42 支 1080p 影片（**不含** Fulton 的 F01–F08） |
| `catalan_portable_104`（資料夾與 `.zip`） | 2026-10-13 | **目前最新**：全部 81 個場景與 10 組連續播放（含 Fulton F01–F45）、兩份講義（40 頁＋25 頁）、`codes/render_all.bat`。**不含影片**（8.7 MB），影片用 `render_all.bat` 自己輸出。在開發機的複本上測過 `check_env.py --render` 與 `render_all.bat 00h -l` |

之後專案若再修改，照第 2 節最後的「重做可攜版」做新的一份。

---

## 2. 在新電腦上快速開始（Windows）

**需要：** Windows、Anaconda（Python 3.10 以上）、MiKTeX。
字型用 Windows 內建的「微軟正黑體」與「標楷體」。

1. 解壓縮到一個**之後不會再搬動**的位置，例如 `C:\mypython\catalan_portable_104`。
   ManimGL 會以「可編輯模式」安裝，指向這個資料夾；搬動後要重新安裝。
2. 安裝 MiKTeX：https://miktex.org/download 。裝好後開新的終端機執行：
   ```bat
   miktex packages install cm-super
   ```
3. 開啟「Anaconda Prompt」，進入解壓縮後的資料夾，執行安裝腳本：
   ```bat
   .\install_windows.bat
   ```
   它會安裝 `third_party\manim`（固定版本的 ManimGL）、補裝缺少的套件 `av`，並在需要時用 conda 安裝 ffmpeg。
4. 檢查環境（約 1 分鐘）：
   ```bat
   cd codes
   python check_env.py --render
   ```
   看到「全部通過，可以開始使用。」就完成了。沒通過的項目後面會附修正指令。
5. 開始使用：
   ```bat
   manimgl main.py
   ```
   會列出所有場景，輸入編號後按 Enter。
6. 要輸出全部影片：在檔案總管裡對 `codes\render_all.bat` 按兩下，選 1（全部，1080p，要好幾個小時）或 4（480p 快速檢查）。
   可攜版 104 起不附影片，`codes\renders\` 是空的。

**重要：所有 `manimgl` 指令都要在 `codes\` 資料夾裡執行**，因為 ManimGL 會讀取執行位置的 `custom_config.yml`。

### 常用指令（都在 `codes\` 裡）

| 想做的事 | 指令 |
|---|---|
| 選一個場景預覽 | `manimgl main.py` |
| 預覽指定場景 | `manimgl main.py Scene05RootDecomposition` |
| 卡塔蘭基礎模組連續播放 | `manimgl main.py CatalanIntroDemo` |
| Chu 的九個場景連續播放 | `manimgl main.py FullDemo` |
| 完整版（卡塔蘭模組＋Chu 的 03–09） | `manimgl main.py CompleteDemo` |
| MIT 補充連續播放 | `manimgl main.py MITDemo` |
| MIT 完整版（00a–00k＋M01–M14＋00l、00m＋03–09） | `manimgl main.py MITCompleteDemo` |
| Fulton 第 1 章（獨立） | `manimgl main.py FultonDemo` |
| Fulton 第 2–4 章（獨立） | `manimgl main.py FultonDemo2` |
| Fulton 第 5–6 章（獨立） | `manimgl main.py FultonDemo3` |
| Fulton 第 7 章（獨立） | `manimgl main.py FultonDemo4` |
| Fulton 第 8 章（獨立） | `manimgl main.py FultonDemo5` |
| 只看 Raney 公式的證明 | `manimgl main.py Scene08RaneyProof` |
| 輸出某場景的 1080p 影片 | `manimgl main.py Scene05RootDecomposition -w --hd` |
| 快速低畫質輸出（檢查用） | 把 `--hd` 換成 `-l` |
| 一鍵輸出（選單） | 對 `render_all.bat` 按兩下；或 `render_all.bat --fulton5 -l`（參數照 `render_all.py`） |
| 一次輸出全部影片 | `python render_all.py --intro-demo --full --complete --mit-demo --mit-complete --fulton-demo --fulton2-demo --fulton3-demo --fulton4-demo --fulton5-demo` |
| 只輸出一部分 | `python render_all.py --intro`（00a–00m）、`--chu`（01–09、08r）、`--mit`（M01–M14）、`--fulton`（F01–F08）、`--fulton2`（F09–F19）、`--fulton3`（F20–F27）、`--fulton4`（F28–F41）、`--fulton5`（F42–F45）、`00c 05 M03 F04`（指定場景） |
| 只輸出連續播放的影片 | `python render_all.py --complete --demos-only` |
| 數學驗證 | `python utils/counting.py`；Fulton 部分：`python utils/tableaux.py`；Raney 導讀：`python utils/raney.py` |
| 環境檢查 | `python check_env.py --render` |
| 重新編譯講義 | 在 `notes\` 裡執行兩次 `xelatex chu1987_導讀.tex` |
| 重新產生講義第 1 節的圖 | 在 `notes\` 裡執行 `python make_catalan_figs.py`，再編譯講義 |
| 重新產生講義附錄 A 的圖 | 在 `notes\` 裡執行 `python make_mit_figs.py`（依序跑 `mit\make_figs_part1..4.py`），再編譯講義 |
| 重新產生 Raney 導讀 | 在 `notes\` 裡執行 `python raney\make_figs.py`（先檢查數字），再執行兩次 `xelatex raney1960_導讀.tex` |
| 重新產生 Young 表講義的圖 | 在 `notes\` 裡執行 `python fulton\make_figs.py`，再執行兩次 `xelatex young_tableaux_導讀.tex` |

預覽視窗操作：滾輪縮放；按住 `f` 拖曳平移；`r` 回到原位；`Ctrl+Q` 或視窗的 ✕ 關閉。
輸出參數：`-w` 寫成檔案、`-o` 寫完自動開啟、`-n 5` 從第 5 個動畫開始、`-n 3,6` 只做第 3 到 6 個。

### 重做可攜版（在開發機上）

`catalan_portable_101`～`104` 都是這樣做的。專案改過之後要再做一份，照做即可
（以下在 Git Bash、`C:\mypython\manim\projects` 裡執行，新資料夾以 `catalan_portable_105` 為例）：

1. 把 `catalan930` 整個複製成新資料夾。`.git/`、`codes/latex_cache/` 與各處的 `__pycache__/` 不必帶；
   `codes/renders/` 裡的影片很大（約 490 MB），104 起不帶，只留空資料夾（`render_all.bat` 已在 `codes/` 裡）。104 用的指令：
   ```bash
   mkdir catalan_portable_105
   tar -C catalan930 --exclude='./codes/latex_cache' --exclude='__pycache__' --exclude='./codes/renders/*' --exclude='./.git' -cf - . | tar -C catalan_portable_105 -xf -
   ```
2. 匯出固定版本的 ManimGL 原始碼：
   ```bash
   mkdir -p catalan_portable_105/third_party
   git -C C:/mypython/manim archive --format=tar --prefix=manim/ fafa083 | tar -x -C catalan_portable_105/third_party
   ```
3. 從上一份可攜版取出 `install_windows.bat`、`third_party/MANIM_VERSION.txt`、`setup_records/`，放到新資料夾的同一位置，
   並把 `MANIM_VERSION.txt` 裡的資料夾名稱改成新的。這三樣與專案內容無關，可以直接沿用
   （`setup_records/` 的兩個檔案也可以從 `C:\mypython\manim` 的 `install.log`、`manim使用說明.md` 複製）。
   再把 `C:\mypython\manim\環境與交接_ENVIRONMENT.md`（環境說明的正本）複製到新資料夾的最上層。
4. 壓縮。Windows 內建的壓縮用 cp950 存中文檔名（`catalan_portable_101.zip` 就是這樣），在繁中 Windows 上解壓縮沒問題；
   換到其他語系的電腦，中文檔名會變亂碼。`catalan_portable_104.zip` 改用 Python 的 `zipfile` 壓縮（中文檔名存成 UTF-8 並設好旗標），沒有這個問題：
   ```bash
   python -c "import shutil; shutil.make_archive('catalan_portable_105', 'zip', '.', 'catalan_portable_105')"
   ```

### 版本控制（git）

2026-10-13 起本資料夾（`catalan930/`）是一個獨立的 git repo，分支 `master`，沒有遠端。
它位在 `C:\mypython\manim`（ManimGL 本身的 repo）裡面，但兩者無關：外層 repo 只會把 `projects/` 看成未追蹤的資料夾，不要把專案加進外層。

- **不追蹤：** `codes/renders/`（影片，用 `render_all.bat` 重新輸出）、`codes/latex_cache/`、`__pycache__/`、LaTeX 的 `.aux/.log/.out/.toc`。講義 PDF 與 `ref/` 的原始資料**有**追蹤。
- **換行：** `.gitattributes` 設成 `* -text`，檔案原封不動存進去（這台電腦的 `core.autocrlf` 是 `true`，不設的話會改動換行）。`.bat` 必須維持 CRLF。
- **習慣：** 每完成一件事就 commit 一次（`git add -A`、`git commit -m "…"`）；要看改了什麼用 `git status`、`git diff`。
- 本 repo 的 git 使用者名稱設為 `newton313313`（只設在本資料夾，`git config user.name`）；信箱還是這台電腦預設的 `userEmail`，要改就在本資料夾執行 `git config user.email "…"`。

---

## 3. 檔案結構

```text
catalan930/                    開發機上的工作資料夾（可攜版的資料夾名稱是 catalan_portable_104）
├── 交接說明_HANDOFF.md        本文件
├── .gitignore, .gitattributes git 設定（只在開發機；見第 2 節「版本控制」）
├── 環境與交接_ENVIRONMENT.md  整台電腦的 ManimGL 環境說明（只在可攜版；正本在 C:\mypython\manim）
├── install_windows.bat        新電腦的安裝腳本（只在可攜版）
├── ref/                       原始資料（只讀，不要改）
│   ├── 1-s2.0-0012365X87902147-main.pdf     Chu 論文原文
│   ├── aybeyan-pdf.pdf                       卡塔蘭模組的內容來源（Selimi & Saračević 2019）
│   ├── ChatGPT-補充廣義卡塔蘭數筆記-….md      使用者與 ChatGPT 的討論筆記（理論補充＋動畫規劃）
│   ├── overview.txt                          動畫規劃書（Chu 部分 8+1 個場景的原始需求）
│   ├── 9781107108738_A23693136.pdf           Fulton《Young Tableaux》節錄（掃描，28 頁：目錄、序、Notation、第 1 章到 p.16）
│   └── fulton_ch1_text.md                    上面節錄的純文字版（Young 表改成文字表格；〔p. N〕 是書上頁碼）
│                                             （第 2 章以後的各章 PDF 與 Markdown 在 C:\mypython\manim\projects\ref\fulton\）
├── notes/                     中文講義與需求
│   ├── chu1987_導讀.tex                       LaTeX 原始檔（xelatex + xeCJK + TikZ）
│   ├── chu1987_導讀.pdf                       編譯好的講義，40 頁
│   ├── young_tableaux_導讀.tex / .pdf        Young 表講義（Fulton 第 1–8 章，25 頁；xelatex，內文在 fulton/）
│   ├── raney1960_導讀.tex / .pdf             Raney (1960) 論文導讀（33 頁；xelatex，內文在 raney/）
│   ├── raney/                                Raney 導讀的內文 part1..6.tex、make_figs.py（含數字檢查）與產生的 figs.tex（不要手改）
│   ├── make_catalan_figs.py                  產生第 1 節的 12 張 TikZ 圖（由 counting.py 的樹產生）
│   ├── catalan_figs.tex                      上面程式的輸出，講義用 \input 讀入（不要手改）
│   ├── make_mit_figs.py                      依序執行 mit/make_figs_part1..4.py，重新產生附錄 A 的圖
│   ├── mit/                                  附錄 A：part1..4.tex（A.1–A.4、A.5–A.8、A.9–A.11、A.12–A.14），
│   │                                         各自的 make_figs_partK.py（含數字檢查）與產生的 figs_partK.tex（不要手改）
│   ├── fulton/                               Young 表講義的內文：part1.tex（第 1–2 章）、part2.tex（第 3–4 章）、part3.tex（第 5 章）、
│   │                                         part4.tex（第 6 章）、part5.tex（第 7 章）、part6.tex（第 8 章）、make_figs.py（含數字檢查；
│   │                                         Young 表用 ytableau 套件）與產生的 figs.tex（不要手改）
│   ├── note1012.txt                          卡塔蘭基礎模組的製作指令（使用者提供，給 AI 助理的規格）
│   ├── MIT18212_1_4.txt                      MIT 18.212 L1–4 理論整理（使用者提供，長）
│   ├── note103how.txt                        MIT 補充的製作指令（使用者提供，長；依 101 版撰寫）
│   ├── MIT18212_L1-4_精簡.md                 上面理論的精簡版（先讀這個）
│   ├── mit_plan.md                           MIT 補充的盤點、決定、場景規格與實作規則（先讀這個）
│   ├── fulton_plan.md                        Fulton 演示的計畫表：範圍、步驟、F01–F08 規格、tableaux.py 的 API
│   ├── fulton_plan_ch2-4.md                  Fulton 第 2–4 章的計畫表：F09–F19 規格、tableaux.py 第 7 節與 fulton_draw.py 的 API
│   ├── fulton_plan_ch5-6.md                  Fulton 第 5–6 章的計畫表：F20–F27 規格與 tableaux.py 第 8 節的 API
│   ├── fulton_plan_ch7-8.md                  第 7–8 章的早期大綱（已被下面兩份取代，只留作紀錄）
│   ├── fulton_plan_ch7.md                    Fulton 第 7 章定稿計畫（14 幕、省 token 的調整、檔名、共用 API）
│   └── fulton_plan_ch8.md                    Fulton 第 8 章計畫（F42–F45 規格）
├── codes/                     Manim 專案（細節見 codes/README.md）
│   ├── README.md              專案說明（給使用者看的）
│   ├── main.py                總入口：列出所有場景、CatalanIntroDemo、FullDemo、CompleteDemo、MITDemo、MITCompleteDemo
│   ├── render_all.py          一次輸出很多支影片
│   ├── render_all.bat         一鍵輸出：按兩下出現選單（全部／只輸出連續播放／只輸出場景／480p），也可帶參數
│   ├── check_env.py           環境檢查
│   ├── custom_config.yml      ManimGL 設定（必須純 ASCII）
│   ├── scenes/                scene00a…00m（卡塔蘭模組）、scene01…09（Chu）、sceneM01…M14（MIT 補充）、sceneF01…F45（Fulton），一個檔案一個場景
│   ├── data/                  fulton7_math.json：第 7 章的固定算例（來自 fulton7_agent_pack，由 utils/rep_data.py 讀取）
│   ├── utils/                 共用工具
│   ├── latex_cache/           LaTeX 編譯的中間檔（ManimGL 自動產生，可以刪；做可攜版時不必帶）
│   └── renders/               已輸出的 1080p 影片（git 不追蹤；可攜版 104 起是空的）
├── third_party/               （只在可攜版）
│   ├── manim/                 ManimGL 原始碼，固定在 commit fafa083（2026-09-09）
│   └── MANIM_VERSION.txt      版本與來源說明
└── setup_records/             開發機的安裝紀錄（參考用，只在可攜版）
    ├── install.log            第一次安裝 ManimGL 的完整指令與輸出
    └── manim使用說明.md        ManimGL 的通用使用說明
```

---

## 4. 各程式的功能

### 4.1 場景（`codes/scenes/`）

**卡塔蘭基礎模組**（依 `notes/note1012.txt` 的敘事順序）：

| # | 檔案 / 類別 | 內容 | 1080p 影片長度 |
|---|---|---|---|
| 00a | `scene00a_catalan_definition.py` / `Scene00aCatalanDefinition` | 數列；為什麼到處出現；公式與 $C_0$–$C_4$ 驗算；歷史（Euler、Segner、明安圖、Catalan）；路線圖 | 36 秒 |
| 00b | `scene00b_triangulation.py` / `Scene00bTriangulation` | $T_3=1$、$T_4=2$、$T_5=5$（逐一畫出）、$T_6=14$（圖庫）；凸 $(n+2)$ 邊形有 $C_n$ 種 | 39 秒 |
| 00c | `scene00c_triangulation_recurrence.py` / `Scene00cTriangulationRecurrence` | 固定底邊、第三個頂點走一圈 → $C_n=\sum C_kC_{n-1-k}$；14 種分成 5+2+2+5 | 47 秒 |
| 00d | `scene00d_parenthesization.py` / `Scene00dParenthesization` | 括號由內而外長出來；依最後一次乘法分組 2+1+2；$n+1$ 個因子有 $C_n$ 種 | 36 秒 |
| 00e | `scene00e_binary_trees.py` / `Scene00eBinaryTrees` | 括號 ↔ 滿二元樹（乘號 → 內部節點、因子 → 葉子、最後一次乘法 → 樹根）；拿掉葉子的另一種說法 | 36 秒 |
| 00f | `scene00f_lattice_paths.py` / `Scene00fLatticePaths` | 20 條路徑中 5 條不越過 $y=x$；$\binom{2n}{n}-\binom{2n}{n-1}$；反射原理（補充說明） | 51 秒 |
| 00g | `scene00g_dyck_paths.py` / `Scene00gDyckPaths` | 格子路徑轉 45° 再上下翻轉 → Dyck 路徑；$n=0..3$ 有 1、1、2、5 條；第一個上坡的分解 | 32 秒 |
| 00h | `scene00h_balanced_parentheses.py` / `Scene00hBalancedParentheses` | 上坡「(」、下坡「)」；高度 = 還沒關上的左括號數；反例；兩種括號別搞混 | 26 秒 |
| 00i | `scene00i_ballot.py` / `Scene00iBallot` | 一般的 Bertrand 投票問題與卡塔蘭特例分開講；比分連成 Dyck 路徑 | 32 秒 |
| 00j | `scene00j_noncrossing_matchings.py` / `Scene00jNoncrossingMatchings` | 圓周 6 點的不交叉配對；固定一點 → 2 個獨立區域 → $C_0C_2+C_1C_1+C_2C_0$ | 36 秒 |
| 00k | `scene00k_one_number_many_objects.py` / `Scene00kOneNumberManyObjects` | 同一個 5：六種物件各 5 個，同一位置彼此一一對應；用顏色顯示「根＋左＋右」 | 26 秒 |
| 00l | `scene00l_catalan_generating_function.py` / `Scene00lCatalanGeneratingFunction` | 根 → $x$、兩側 → $C$，得 $C=1+xC^2$；展開驗算 | 38 秒 |
| 00m | `scene00m_bridge_to_chu.py` / `Scene00mBridgeToChu` | 配對 = 2 點群組；一條弦換成三角形 → $\vec n=(2,1),\vec v=(2,3)$；$C=1+xC^2\Rightarrow D=1+\sum x_iD^{v_i}$ | 45 秒 |

**Chu 的部分：**

| # | 檔案 / 類別 | 內容 | 1080p 影片長度 |
|---|---|---|---|
| 1 | `scene01_classical_catalan.py` / `Scene01ClassicalCatalan` | 卡塔蘭數；6 點的不交叉與交叉配對；$C_3=5$ | 34 秒 |
| 2 | `scene02_from_pairs_to_blocks.py` / `Scene02FromPairsToBlocks` | 弦→三角形→四邊形→五邊形；引入 $\vec v,\vec n$ | 30 秒 |
| 3 | `scene03_generalized_setup.py` / `Scene03GeneralizedSetup` | $\vec n=(2,1),\vec v=(2,3)$；$N=7$；定理；交叉反例；21 種 | 41 秒 |
| 4 | `scene04_paper_example.py` / `Scene04PaperExample` | 論文 Fig. 1：旋轉得 5 種；為何只有 5 種；公式也是 5 | 41 秒 |
| 5 | `scene05_root_decomposition.py` / `Scene05RootDecomposition` | **核心**：固定一點→根群組→切成 $v_i$ 段→各段獨立→$x_iD^{v_i}$ | 55 秒 |
| 6 | `scene06_recurrence.py` / `Scene06Recurrence` | $\vec r_1+\cdots+\vec r_{v_i}=\vec n-\vec e_i$；論文式 (5)；驗算 $2+3=5$ | 55 秒 |
| 7 | `scene07_generating_function.py` / `Scene07GeneratingFunction` | 生成函數 $D$；論文式 (6)；退化成 $D=1+xD^2$ | 51 秒 |
| 8 | `scene08_formula_verification.py` / `Scene08FormulaVerification` | **Raney 公式完整證明**（路徑、循環引理、切兩段），式 (10)，$D=C$ | 4 分 2 秒 |
| 9 | `scene09_summary.py` / `Scene09Summary` | 流程圖總結 | 22 秒 |
| | 同 8 / `Scene08RaneyProof` | 第 8 場景中只有 Raney 證明的部分 | 3 分 2 秒 |

**MIT 18.212 Lecture 1–4 補充**（`notes/mit_plan.md` 第 4 節是完整規格）：

| # | 類別 | 內容 | 1080p 影片長度 |
|---|---|---|---|
| M01 | `SceneM01CauchyProduct` | 乘法表的反對角線 → $[x^n]C^2=\sum C_kC_{n-k}$ → $C=1+xC^2$ | 51 秒 |
| M02 | `SceneM02ClosedForm` | 二次方程取減號；$\sqrt{1-4x}$ 的二項級數 → $C_n=\frac1{n+1}\binom{2n}{n}$ | 46 秒 |
| M03 | `SceneM03DrunkardsWalk` | 醉漢走路：第 $2n+1$ 步第一次掉下去有 $C_n$ 條；總機率 $\tfrac12C(\tfrac14)=1$ | 56 秒 |
| M04 | `SceneM04CyclicShift` | 古典循環引理（7 種讀法恰 1 種好）；預告第 8 場景的 Raney | 43 秒 |
| M05 | `SceneM05PlaneTrees` | 平面樹；$n+1$ 個頂點有 $C_n$ 棵 | 39 秒 |
| M06 | `SceneM06ArcDiagrams` | 圓上配對攤平成弧圖；不交叉 5 種、不巢狀 5 種 | 46 秒 |
| M07 | `SceneM07TriangulationDualTree` | 三角剖分的對偶圖 = 完全二元樹；二元樹 → 平面樹 | 48 秒 |
| M08 | `SceneM08TreeDyckMatching` | 平面樹 DFS → UUDUDD → 弧 (1,6),(2,3),(4,5)；整條對應鏈 | 48 秒 |
| M09 | `SceneM09StackQueueSorting` | 堆疊排序 ⇔ 避開 231；佇列＋插隊線 ⇔ 避開 321 | 1 分 2 秒 |
| M10 | `SceneM10PatternAvoidance` | 模式包含／迴避；$n=3,4$：5、14；六個長度 3 模式都是 $C_n$ | 45 秒 |
| M11 | `SceneM11PartitionsYoung` | 整數分割、合成；整數分割 ≠ Chu 的集合分割；Young 圖；SYT | 53 秒 |
| M12 | `SceneM12SYTDyck` | SYT$(n,n)$ ↔ Dyck；$f^{(n,n)}=C_n$；一般 λ 的格子路徑 | 47 秒 |
| M13 | `SceneM13HookLength` | 鉤長、鉤長公式、角落遞迴、化約成 $\sum_c\frac1n\frac{H(\lambda)}{H(\lambda-c)}=1$ | 1 分 1 秒 |
| M14 | `SceneM14HookWalk` | 鉤上漫步證明（五段，模組層級函式 `part1_walk` … `part5_conclusion`） | 2 分 34 秒 |

貫穿 M05–M12 的例子與 00k 第 4 欄相同：五邊形對角線 {1,4},{2,4} → 二元樹 ((•,(•,•)),•) → 平面樹（根 → A → 兩片葉子）→ UUDUDD → 配對 (1,6),(2,3),(4,5) → SYT ((1,2,4),(3,5,6))。

**Fulton《Young Tableaux》第 1 章**（獨立；規格見 `notes/fulton_plan.md` 第 3 節，例子都用書上的資料）：

| # | 類別 | 內容 | 1080p 影片長度 |
|---|---|---|---|
| F01 | `SceneF01YoungDiagrams` | Young 圖與分割、共軛 | 53 秒 |
| F02 | `SceneF02Tableaux` | 表、標準表、轉置、斜形狀與斜表（p.4 與 p.12 的斜表最後一列不同，書上本來就是兩個例子） | 53 秒 |
| F03 | `SceneF03Schur` | $x^T$、Schur 多項式、$s_{(2,1)}$ 的 8 個表、$h_n$、$e_n$ | 57 秒 |
| F04 | `SceneF04RowInsertion` | 列插入與反向擠出 | 1 分 3 秒 |
| F05 | `SceneF05BumpingLemma` | Row Bumping Lemma；水平條／垂直條 | 1 分 13 秒 |
| F06 | `SceneF06Product` | 表的字與乘積 $T\cdot U$；結合律 | 56 秒 |
| F07 | `SceneF07JeuDeTaquin` | 內角、外角、滑動、反向滑動、rectification 與挑法無關 | 1 分 17 秒 |
| F08 | `SceneF08RectifyProduct` | $\mathrm{Rect}(T*U)=T\cdot U$；三個 Claim | 1 分 14 秒 |

**Fulton《Young Tableaux》第 2–4 章**（獨立；規格見 `notes/fulton_plan_ch2-4.md` 第 4 節，例子都用書上的資料）：

| # | 類別 | 內容 | 1080p 影片長度 |
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

**Fulton《Young Tableaux》第 5–6 章**（獨立；規格見 `notes/fulton_plan_ch5-6.md` 第 3 節）：

| # | 類別 | 內容 | 1080p 影片長度 |
|---|---|---|---|
| F20 | `SceneF20FactorTableaux` | 表的因數分解：$V=T\cdot U$ 有幾種寫法只看形狀；滑成 $U_0$ 的斜表一樣多 → LR 數 $c^\nu_{\lambda\mu}$ | 1 分 13 秒 |
| F21 | `SceneF21LRSymmetry` | LR 數的三張臉（交換、轉置）；穿出 $\lambda*\mu$ 的框 → 0；表環裡的乘法 $S_\lambda S_\mu=\sum c\,S_\nu$ | 1 分 7 秒 |
| F22 | `SceneF22Yamanouchi` | 反格字＝倒著開票；LR 斜表滑成 $U(\mu)$（Lemma 1）；Knuth 變換保持反格字（Lemma 2）；命題 3 | 1 分 15 秒 |
| F23 | `SceneF23LRRule` | LR 計數機：(5,4,3,2)/(3,3,1) 的 15 個 LR 斜表分堆 → $s_{\nu/\lambda}$ 的展開；$s_{(2,1)}^2$；練習 2 | 1 分 18 秒 |
| F24 | `SceneF24LROther` | 反格字 ↔ 標準表 $U(w)$；Remmel–Whitney（189 個標準表裡恰 15 個過關）；彩蛋：卡塔蘭數 | 1 分 13 秒 |
| F25 | `SceneF25Bases` | 五組基底 $m,s,e,h,p$；$E(-t)H(t)=1$；Newton 恆等式；$z(\lambda)$ 與 $h_n=\sum p_\lambda/z(\lambda)$ | 1 分 18 秒 |
| F26 | `SceneF26JacobiTrudi` | 三條路到 $s_\lambda$：Jacobi–Trudi、對偶、雙交錯式；$s_{(2,1)}(1,q,q^2)$ 與 $q=1$ 的表數 | 1 分 13 秒 |
| F27 | `SceneF27SymFunctions` | 對稱函數環 $\Lambda$；Cauchy 核的三種展開；內積與 $\omega$；預告第 7 章的特徵標表 | 1 分 14 秒 |

**Fulton《Young Tableaux》第 7 章**（獨立；規格見 `notes/fulton_plan_ch7.md` 第 3 節）：

| # | 類別 | 內容 | 1080p 影片長度 |
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

**Fulton《Young Tableaux》第 8 章**（獨立；規格見 `notes/fulton_plan_ch8.md` 第 3 節）：

| # | 類別 | 內容 | 1080p 影片長度 |
|---|---|---|---|
| F42 | `SceneF42SchurModule` | 把數字換成向量：一列 → $\operatorname{Sym}^nE$、一行 → $\bigwedge^nE$；$E^{(2,1)}$＝$\bigwedge^2E\otimes E$ 模掉同一條交換關係；基底＝半標準表（$m=2$：2 個、$m=3$：8 個）；$f^\lambda$ 對 $d_\lambda(m)$ | 2 分 35 秒 |
| F43 | `SceneF43Weights` | 對角矩陣 $e_T\mapsto x^Te_T$；8 個表按權重排成六角形（中間 $2x_1x_2x_3$）；最高權重 11/2；$\operatorname{Char}E^{(2,1)}=s_{(2,1)}$；至多 $m$ 列 | 2 分 17 秒 |
| F44 | `SceneF44SchurWeyl` | $GL(E)$ 與 $S_3$ 在 $E^{\otimes3}$ 上可交換（交換圖）；$E^{\otimes n}\cong\bigoplus E^\lambda\otimes S^\lambda$；$8=4\cdot1+2\cdot2+0\cdot1$、$27=10\cdot1+8\cdot2+1\cdot1$；$E^\lambda\cong E^{\otimes n}\otimes_{\mathbb C[S_n]}S^\lambda$ | 2 分 6 秒 |
| F45 | `SceneF45QuadraticRelations` | 同一條交換關係的三個身分：Specht、Schur 模、$2\times4$ 矩陣的子式；Plücker $p_{12}p_{34}-p_{13}p_{24}+p_{14}p_{23}=-3-9+12=0$；預告第 9 章 Grassmannian；總結第 7–8 章 | 2 分 15 秒 |

**連續播放**（`main.py`）：

| 類別 | 內容 | 1080p 影片長度 |
|---|---|---|
| `CatalanIntroDemo` | 卡塔蘭模組 00a–00m | 8 分 15 秒 |
| `FullDemo` | Chu 的九個場景 01–09 | 9 分 40 秒 |
| `CompleteDemo` | 完整版：00a–00m 之後接 03–09。01（經典卡塔蘭與配對）已由 00a、00j 取代，02（從弦到多邊形、兩個向量）已由 00m 取代 | 16 分 50 秒 |
| `MITDemo` | MIT 補充 M01–M14 | 13 分 33 秒 |
| `MITCompleteDemo` | 00a–00k → M01–M14 → 00l（$C=1+xC^2$ 的根＋左＋右讀法，提問「一組不只 2 點呢？」）→ 00m → 03–09 | 30 分 24 秒 |
| `FultonDemo` | Fulton 第 1 章 F01–F08（獨立） | 8 分 34 秒 |
| `FultonDemo2` | Fulton 第 2–4 章 F09–F19（獨立） | 13 分 18 秒 |
| `FultonDemo3` | Fulton 第 5–6 章 F20–F27（獨立） | 10 分 0 秒 |
| `FultonDemo4` | Fulton 第 7 章 F28–F41（獨立） | 36 分 15 秒 |
| `FultonDemo5` | Fulton 第 8 章 F42–F45（獨立） | 9 分 17 秒 |

第 8 場景分成 8 段（`part0_roadmap` 路線圖，接著 `part1_statement` … `part7_conclusion`），每段結束時清空畫面，可以用 `-n` 跳著看。
M14 也分段（`part1_walk` … `part5_conclusion`），但寫成模組層級的函式。

卡塔蘭模組的所有物件都由同一棵二元樹產生（`counting.py` 第 5 節），所以不同物件的「第 k 個」彼此一一對應，00k 就是靠這點把六種物件排在同一位置。

### 4.2 工具（`codes/utils/`）

| 檔案 | 功能 |
|---|---|
| `styles.py` | 顏色、字型、尺寸常數；`zh()` 中文字、`mixed()` 中文與 LaTeX 混排、`boxed()` 加框 |
| `scene_base.py` | `ChuScene` 基底類別：`show_header()` 左上標題、`say()` 底部字幕（鏡頭移動時固定不動）、`clear_stage()` 清掉標題以外的東西 |
| `circle_points.py` | 圓與圓周等距點（從正上方順時針、0 起算）、弦、點標籤、兩弦交點 |
| `polygon_groups.py` | 依點編號畫群組（2 點=弦，3 點以上=多邊形）；`Configuration`（圓＋群組＋點）；根群組切出的弓形區域 |
| `root_figure.py` | 第 5–9 場景共用的「根分解」示意圖（12 點、三角形根群組）；群組小圖示；00m 也用到 |
| `lattice_paths.py` | Raney 證明用的路徑圖（`PathMob`）、步驟方塊、路徑小圖 |
| `catalan_draw.py` | 卡塔蘭模組的圖形：`TriangulationMob`、`BinaryTreeMob`、`paren_mob`（含括號由內而外長出的動畫）、格子／Dyck 路徑、配對；`catalan_item(family, tree, scale, colored)` 是統一入口；根／左／右的顏色 |
| `mit_draw.py` | MIT 補充的圖形：`ArcDiagramMob`（直線上的弧圖）、`YoungDiagramMob`（英式 Young 圖、填數、鉤）、`PlaneTreeMob`（平面樹）、數字方塊列；Fulton 的場景也用它畫 Young 表 |
| `rep_data.py` | **純 Python**：第 7 章的固定算例（`load(key)` 讀 `codes/data/fulton7_math.json`）與置換、tabloid、polytabloid、表示矩陣、群環；`python -m utils.rep_data` 交叉核對 |
| `rep_draw.py` | 第 7 章的圖形：`TabloidMob`、`ColumnTabloidMob`、`signed_sum`、`MatrixMob`、`perm_tex` |
| `fulton_draw.py` | Fulton 第 2–4 章的圖形：`WordMob`（字母方塊，`.apply_move` 播放一步 Knuth 變換）、`SkewMob`（斜表、有洞的表）、`tableau_mob`、`TwoRowArray`、`BallMatrixMob`、版面檢查 `assert_in_frame`／`assert_apart` |
| `raney.py` | **純 Python**：Raney (1960) 的字串、秩、字列（Rosenbloom 判別法與遞迴定義互相核對）、循環引理與 Raney 證明的每一步、$L(n;a)$ 公式與暴力、定理 2.3/2.4、和 Chu 講義路徑互換（`to_chu_path`）、不交叉分法 ↔ 字（`partition_to_word`）、$L^*$、Lagrange 反演、三項式與 Problem 4983、卷積與 Gould 公式；`python utils/raney.py` 自我檢查。Raney 導讀的數字都出自這裡 |
| `tableaux.py` | **純 Python**：Fulton 第 1–4 章的 Young 表運算（第 7 節：字、Knuth 等價、L(w,k)、R-S-K、矩陣球；API 摘要在 `notes/fulton_plan_ch2-4.md` 第 2 節；第 8 節：LR 規則與對稱多項式，API 在 `notes/fulton_plan_ch5-6.md` 第 2 節）。第 1 章部分（格子 0 起算；列插入與路徑、反向擠出、表的字、乘積、jeu de taquin、rectification、Schur 多項式、Kostka 數）與暴力驗證；API 摘要在 `notes/fulton_plan.md` 第 3.5 節 |
| `formulas.py` | 常用公式的 Tex 物件（卡塔蘭數、廣義公式、生成函數方程、遞迴式） |
| `counting.py` | **純 Python、不需 manim**：公式、暴力列舉、遞迴、路徑與 Raney 證明的每一步檢查；第 5 節是卡塔蘭模組的物件（樹、三角剖分、括號、格子／Dyck 路徑、投票、配對）與彼此的一一對應；第 6 節是 MIT 補充（平面樹、對偶樹、弧圖、堆疊／佇列排序、模式、整數分割、SYT、鉤長、鉤上漫步的精確機率、醉漢走路）。動畫與講義的數字都出自這裡 |

### 4.3 其他

| 檔案 | 功能 |
|---|---|
| `main.py` | 為每個場景做同名子類別（ManimGL 只列出定義在該檔案裡的場景）；`INTRO_SCENES`、`ALL_SCENES`、`COMPLETE_SCENES`、`MIT_SCENES`、`MIT_COMPLETE_SCENES`、`FULTON_SCENES`、`FULTON2_SCENES`、`FULTON3_SCENES`、`FULTON4_SCENES`、`FULTON5_SCENES` 十個清單與 `CatalanIntroDemo`、`FullDemo`、`CompleteDemo`、`MITDemo`、`MITCompleteDemo`、`FultonDemo`、`FultonDemo2`、`FultonDemo3`、`FultonDemo4`、`FultonDemo5` 十個連續播放 |
| `render_all.py` | 依序呼叫 `manimgl … -w`；參數 `-l/-m/--hd/--uhd`、`--intro`、`--chu`、`--mit`、`--fulton`、`--fulton2`、`--fulton3`、`--fulton4`、`--fulton5`、場景代號（`00c`、`05`、`08r`、`M03`、`F04`）、`--intro-demo`、`--full`、`--complete`、`--mit-demo`、`--mit-complete`、`--fulton-demo`、`--fulton2-demo`、`--fulton3-demo`、`--fulton4-demo`、`--fulton5-demo`、`--demos-only` |
| `render_all.bat` | 一鍵輸出（包裝 `render_all.py`）：按兩下會出現選單——1 全部 81 個場景＋10 個連續播放（1080p）、2 只輸出連續播放、3 只輸出單一場景、4 全部用 480p 快速檢查；也可以帶參數，例如 `render_all.bat --fulton5 -l`。找不到 `manimgl` 時會自己啟用 Anaconda／Miniconda。檔案必須純 ASCII、CRLF 換行 |
| `check_env.py` | 檢查 Python、ManimGL、套件、ffmpeg、LaTeX、cm-super、字型、設定檔、數學驗證；`--render` 實際渲染一小段 |
| `custom_config.yml` | 輸出資料夾 `renders/`、背景色、fps、預設字型 |
| `notes/make_catalan_figs.py` | 產生講義第 1 節的 TikZ 圖 `catalan_figs.tex`：物件由 `counting.py` 的樹產生，排列順序與根／左／右配色和動畫相同；產生前先檢查第 1 節寫到的數字（明安圖級數、Bertrand 公式、$\sqrt{1-4x}$ 的係數等） |
| `notes/make_mit_figs.py` | 依序執行 `notes/mit/make_figs_part1..4.py`：每支先檢查附錄 A 該段寫到的數字，再寫出 `figs_partK.tex` |
| `notes/fulton/make_figs.py` | Young 表講義的圖與表：先檢查 `fulton/part1..6.tex` 寫到的每一個數字（資料來自 `codes/utils/tableaux.py` 第 7–8 節；第 7 章用 `codes/utils/rep_data.py`），再寫出 `fulton/figs.tex` |

**可攜到別的計畫的工具包：** `codes/utils/` 的數學與畫圖模組、以及講義的 TikZ 函式，已另外打包成
`C:\mypython\manim\projects\combkit`（import 名稱 `combkit.X`；說明見該資料夾的 `README.md`）。它是 2026-10-06 的複本；
這裡的 `codes/utils/` 改過之後，在 combkit 資料夾執行 `python tools/sync_from_catalan930.py` 重新同步。

---

## 5. 簡短理論介紹

**經典卡塔蘭數（卡塔蘭模組）。** $C_n=\frac{1}{n+1}\binom{2n}{n}$：1, 1, 2, 5, 14, 42, …。下面每一種都恰有 $C_n$ 個：

| 物件 | 精確說法（全模組統一） |
|---|---|
| 三角剖分 | 凸 $(n+2)$ 邊形的三角剖分（凸 $m$ 邊形是 $C_{m-2}$） |
| 括號 | $n+1$ 個因子的完全括號化（$n$ 次乘法） |
| 二元樹 | $n$ 個內部節點的滿二元樹（$n+1$ 片葉子）；拿掉葉子 = $n$ 個節點、左右小孩可有可無的二元樹 |
| 格子路徑 | $(0,0)\to(n,n)$、只走 R、U、不走到 $y=x$ 上方 |
| Dyck 路徑 | $n$ 個上坡、$n$ 個下坡、不低於起點 |
| 平衡括號字串 | $n$ 對括號 |
| 投票（卡塔蘭特例） | 兩人各 $n$ 票，每開一張後 A 的票數 $\ge$ B |
| 圓上配對 | 圓周 $2n$ 點的不交叉完美配對 |

它們數目相同，是因為結構相同：**固定一個「根」，剩下的切成左、右兩個獨立的小卡塔蘭結構**，
所以 $C_n=\sum_{k=0}^{n-1}C_kC_{n-1-k}$，生成函數滿足 $C=1+xC^2$。Chu 的推廣就是把「切成 2 塊」換成「切成 $v_i$ 塊」。

**問題。** 圓周上放 $N=\sum_i n_iv_i$ 個點，分成 $n_i$ 個「$v_i$ 點群組」（$i=1,\dots,k$）。
同一群組的點連成凸多邊形（2 點就是弦），要求不同群組的多邊形在圓內不相交。分法有幾種？

**定理（Chu 1987）。** 分法數等於廣義卡塔蘭數
$$
C_{\vec v}(\vec n)=\frac{1}{N+1}\binom{N+1}{n_1,\dots,n_k,\,L}=\frac{N!}{n_1!\cdots n_k!\,(N+1-b)!},
$$
其中 $L=1+\sum_i n_i(v_i-1)$，$b=\sum_i n_i$ 是群組總數。
只有弦時（$\vec v=(2)$）就是經典卡塔蘭數 $C_n$。論文例子 $\vec n=(1,1),\vec v=(2,3)$（一條弦＋一個三角形）答案是 5。

**證明三步。**
1. **固定一點。** 它所在的 $v_i$ 點群組把其餘的點切成 $v_i$ 段，各段互不干擾。
   得到遞迴（論文式 (5)）：$d(\vec n)=\sum_i\sum_{\vec r_1+\cdots+\vec r_{v_i}=\vec n-\vec e_i}d(\vec r_1)\cdots d(\vec r_{v_i})$。
2. **生成函數。** 獨立→相乘，多用一個第 $i$ 型群組→乘 $x_i$，得到論文式 (6)：$D=1+\sum_i x_iD^{v_i}$。
3. **公式那邊也滿足同一條方程。** 令 $C=\sum C_{\vec v}(\vec n)x^{\vec n}$。用 Raney 公式（式 (9)）算出
   $[x^{\vec n}]C^t=\frac{t}{N+t}\binom{N+t}{\vec n}$，取 $t=v_i$ 加總得式 (10)，所以 $C$ 也滿足式 (6)。
   方程的解唯一，所以 $D=C$。

**Raney 公式的證明**（論文沒有，講義第 7 節、第 8 場景有）。
把 ↑ 步（$+1$）和第 $i$ 型步（$1-v_i$）排成路徑，「好路徑」是出發後高度一直 $>0$。
循環引理說每條路徑的 $N+t$ 種循環讀法中恰有 $t$ 種是好路徑，雙重計數得到好路徑數 $=A_t(\vec n)=\frac{t}{N+t}\binom{N+t}{\vec n}$。
好路徑在「最後一次落在高度 $s$」處切成兩段，一一對應，就是 Raney 公式 $A_{s+t}=\sum A_sA_t$。

**補充觀點**（不在原文）：方程 $T=1+\sum x_iT^{v_i}$ 也是平面樹的方程；$L$ 是樹的葉子數；
也可以用 Lagrange 反演直接得到公式（論文最後的 Remark）。詳見講義第 8 節。

**卡塔蘭模組和指令、來源不同的地方**（都已在畫面上處理，`codes/README.md` 有同樣的說明）：
- **格子路徑 → Dyck 路徑的方向。** `note1012.txt` 要求格子路徑「不走到 $y=x$ 上方」，又寫 U → ↗、R → ↘；照這樣對應，路徑會在地面以下。正確是 **R → ↗、U → ↘**（轉 45° 之後再上下翻轉）。
- **二元樹的說法。** 來源論文寫「$n$ 個頂點的二元樹」；動畫統一說「$n$ 個內部節點的滿二元樹」，並在 00e 示範拿掉葉子後就是論文說的那一種。
- **括號化的指標。** 來源論文的 $M_n$ 以「$n$ 個數」計數，照它的遞迴是 $C_{n-1}$，它卻寫成 $M_n=C_n$；動畫與講義一律說「$n+1$ 個因子有 $C_n$ 種」。
- **投票問題。** 來源論文給的是 $k$ 倍的推廣 $\frac{a-kb}{a+b}$，而且把機率說成「數目」。動畫把一般的 Bertrand 問題（嚴格領先的機率 $\frac{a-b}{a+b}$）和卡塔蘭特例（同票、不落後，$C_n$ 種）分開講。
- **反射原理** 是補充說明：來源論文只給 $\binom{2n}{n}-\binom{2n}{n-1}$，沒有證明。

---

## 6. 怎麼確認東西是對的

- `python utils/counting.py`：三種獨立方法（公式、暴力列舉、遞迴）算同一批例子並比對；
  再逐步檢查 Raney 證明（排法總數、循環引理、好路徑數 $=A_t$、切開一一對應、Raney 公式本身）；
  最後檢查卡塔蘭模組：每種物件都用「由樹產生」與「暴力列舉」兩種方法列舉，$n=0$ 到 $6$ 都等於 $C_n$，
  並檢查彼此的一一對應、反射原理、一般投票定理與 $k$ 倍推廣、$C=1+xC^2$ 的係數。
  第 6 節（MIT 補充）的每一種計數也用兩種方法算，並檢查貫穿例子的每個值。
  最後應印出「全部一致」、「Raney 公式證明的每一步都通過」、「卡塔蘭基礎模組：所有物件的數目與一一對應都通過」與「MIT 補充模組：所有計數與一一對應都通過」。
- MIT 補充（2026-10-04）由多個 AI 代理人分工：一個建 `counting.py` 第 6 節與 `mit_draw.py`、另一個用獨立的程式驗證；
  每個場景由一個代理人製作、另一個代理人重算畫面上的數字並逐格檢查排版。所有 M 場景都用嚴格 LaTeX 模式輸出過。
- 每個場景開頭有 `assert`，數字不對時渲染會直接失敗，不會產生錯的影片。卡塔蘭模組有幾個場景另外用 `assert` 檢查排版不出框、不重疊。
- 在 `notes/` 裡執行 `python make_catalan_figs.py` 會先檢查講義第 1 節的數字，印出「講義第 1 節的數字檢查通過」後才產生圖；
  `python make_mit_figs.py` 對附錄 A 的四段做同樣的事（任何一段的數字不對就停下來）；`python fulton/make_figs.py` 對 Young 表講義也一樣。
- 所有分法與路徑都用寫死的點編號或固定順序列舉，沒有亂數，每次渲染結果相同。
- 2026-10-03 檢查過 `CompleteDemo` 的 19 個場景交界：每個場景開始時畫面乾淨、鏡頭歸位，沒有上一個場景的殘留。
- 2026-10-03 在全新安裝的環境裡用空的 LaTeX 快取重新輸出 00a–00m，而且每次編譯前先刪掉舊的 DVI
  （所以任何公式編譯失敗都會直接報錯，不會發生第 7 節第 12 點的問題），13 個場景全部成功；
  再和 `renders/` 的影片逐格比較，內容完全相同。
- `python utils/tableaux.py`（Fulton 部分）用暴力列舉檢查 Row Bumping Lemma、水平條／垂直條、乘積的結合律、Rect 與挑法無關、Rect(T∗U)=T·U、
  Schur 多項式的對稱性與 $h_n$、$e_n$，以及書上第 2、7–8、12–16 頁的每個例子；最後印出「Fulton 第 1 章：插入、乘積、jeu de taquin 全部驗證通過」（`check_env.py` 也檢查）。
  F01–F08 由 8 個代理人各做一幕，再由一個代理人重算全部數字並檢查場景間的銜接。
  第 2–4 章（第 7 節）另外驗證：Knuth 對列插入的拆解、主定理（長 4 的字全部）、滑動保持等價、三種乘積相同、Pieri 公式、
  Kostka 矩陣與支配序（n ≤ 6）、L(w,k) 的動態規劃對暴力、Greene 定理、唯一性演算法、R-S-K 與反向、對稱定理、矩陣球 = R-S-K（隨機 300 個矩陣）、
  練習 4、16、17 與 §4.3 的計數恆等式；最後印出「Fulton 第 2–4 章：Knuth 等價、L(w,k)、R-S-K、矩陣球全部驗證通過」。
  F09–F19 由 4 個代理人各做 2–3 幕，每幕都用嚴格模式試渲染並看過總覽圖，主對話再逐一檢查數字。
  第 5–6 章（第 8 節）驗證：書上 (5,4,3,2)/(3,3,1) 的 15 個 LR 斜表與各係數、$s_{(2,1)}^2$、LR 數與分解數／斜表數相同且與 V、U0 無關、
  交換與共軛對稱、Remmel–Whitney、反格字與卡塔蘭數、五組基底（轉換矩陣行列式 ±1）、Newton 恆等式、Jacobi–Trudi 與雙交錯式、
  主特殊化（練習 5、6）、特徵標的正交關係、內積與 ω；最後印出「Fulton 第 5–6 章：Littlewood–Richardson 規則、對稱函數全部驗證通過」。
  F20–F27 由 3 個代理人各做 2–3 幕，同樣自查後由主對話檢查。
  第 7 章（F28–F41）：固定算例由使用者的工作包提供並自帶 selfcheck；`python -m utils.rep_data` 再用 `tableaux.py` 獨立重算核對（polytabloid 座標、$\rho(12)$、$\rho(23)$、$S_3$ 特徵標、Kostka、$c^2=3c$、LR、分支）。4 個代理人各做 3–4 幕。
   第 8 章（F42–F45）：數字由 `tableaux.py` 現算並在場景的 `check_math()` assert（半標準表與權重、$d_\lambda(m)$、$m^n=\sum d_\lambda(m)f^\lambda$、Plücker 子式）；1 個代理人做 4 幕。
- 2026-10-04 檢查過 `MITCompleteDemo` 的 33 個場景交界（同樣乾淨），並在 103 的全新安裝環境用空的 LaTeX 快取、嚴格模式重新輸出 M01–M14，全部成功。

---

## 7. 已知問題與注意事項（踩過的坑）

1. **這是 ManimGL（3b1b 版），不是 Manim Community。** `ref/overview.txt` 與 `notes/note1012.txt` 有時用 Community 版的寫法
   （`manim -pql`、`Create`），這裡一律用 ManimGL（`manimgl`、`ShowCreation`、`from manimlib import *`）。
   網路上的範例大多是 Community 版，不能直接用。
2. **ManimGL 版本固定在 commit fafa083。** 新版 API 可能變動。請用 `third_party/manim`，不要 `pip install manimgl`（PyPI 版本不同）。
3. **缺套件 `av`**：該版 `setup.cfg` 漏列，所以安裝後要再 `pip install -r requirements.txt`（安裝腳本已處理）。
4. **LaTeX 場景出現 `SVG has no content to measure`**：MiKTeX 缺 `cm-super`。
   裝好後務必 `manimgl --clear-cache`，否則快取裡的空白 SVG 會讓錯誤繼續出現。
5. **`custom_config.yml` 只能寫英文。** ManimGL 在繁中 Windows 上用 cp950 讀它，有中文就當掉。批次檔同理。
6. **`-s -w`（存最後一格成 PNG）需要較新的 Pillow。** 開發機的 Pillow 9.4 會出錯（`frombytes` 不接受 memoryview）；
   照第 2 節全新安裝會裝到 Pillow 12.3，實測可以正常存 PNG。若遇到這個錯誤，執行 `pip install -U Pillow`。
   另一個做法是輸出影片後用 ffmpeg 抽格：`ffmpeg -sseof -0.1 -i renders\X.mp4 -frames:v 1 last.png`。
7. **公式著色**：`t2c` 要整個因子一起上色（例如 `x_1^{n_1}`），只給 `x_1` 上色會讓指數位置跑掉。
8. **連續播放借用各場景的 `construct`。** 若某場景把內容拆成輔助方法（如第 8 場景的 `part1_statement`），
   連續播放的類別必須繼承該場景類別（五個連續播放類別都繼承 `Scene08FormulaVerification`），否則會 `AttributeError`。
   所以卡塔蘭模組與 MIT 補充的輔助函式都寫成模組層級的函式；新增場景也請這樣做。
9. **`manimgl` 會解析 `sys.argv`**：自己寫的 Python 腳本若 import manimlib 又有自己的參數，要先清掉 `sys.argv`（見 `check_env.py`）。
10. **非 Windows 系統**：要把 `codes/utils/styles.py` 的 `CJK_FONT`、`custom_config.yml` 的字型、講義的 `\setCJKmainfont` 改成該系統有的中文字型（例如 Noto Sans CJK TC）。
11. **給 AI 助理**：在這台開發機上，Bash 工具對很長的 heredoc 會失敗，而且會吃掉雙反斜線；
    長檔案或含很多反斜線的 LaTeX 請用檔案寫入工具，不要用 shell heredoc。
12. **Tex 快取會存到錯的圖形。** Tex 字串的開頭、結尾若有 `\;`、`\,` 之類的間距指令，ManimGL 編譯「帶顏色標記」的版本會失敗，
    但它不報錯，而是沿用上一個公式留下的 DVI，把錯的 SVG 存進快取（例如箭頭變成上一句的公式）。
    遇到公式顯示成別的東西：先改掉字串，再執行 `manimgl --clear-cache`。
13. **多段字串的 `Tex("a", "b")[1]` 是第 2 個字形，不是第 2 段。** 要上色請用 `t2c` 或依字形位置（例如 `catalan_draw.catalan_product_tex`）；
    `t2c` 的鍵重複時（例如 $C_1C_1$），兩個會變成同一個顏色。
14. **輸出影片偶爾在最後一步失敗**：`PermissionError: [WinError 32]`（檔案正由另一個程序使用），發生在 ManimGL 把 `renders/X_temp.mp4` 改名成 `X.mp4` 時，
    可能是防毒軟體正在掃描剛寫好的檔案（2026-10-03 輸出 00a 時遇過一次）。`render_all.py` 會把它記成失敗；
    重新輸出那一個場景，再刪掉留下的 `X_temp.mp4`。
15. **不要同時在同一個資料夾跑多個 `manimgl`。** 每個 Tex 都在 `latex_cache/working.tex` 編譯，兩個程式同時寫會互相覆蓋，
    得到錯的公式卻不報錯。要平行輸出，就讓每個程式在不同的工作資料夾執行（各放一份 `custom_config.yml`）。
16. **`t2c` 上色的 Tex 不要用 `\left( … \right)`**：帶顏色標記的那次編譯可能失敗（Missing delimiter），在一般模式下就會變成第 12 點的錯圖。改用 `\Big( … \Big)`。
17. **自訂 Mobject 的屬性名稱不要和 ManimGL 撞名**（例如 `.parents`、`.color`、`.stroke_width`），否則動畫會當掉；
    放在 dict／list 屬性裡的子物件不會跟著 `.copy()` 複製，要用索引或 property 取（見 `mit_draw.py`）。
18. **ManimGL 的公式快取可能損毀**：預設的快取 `%LOCALAPPDATA%\manim\manim\Cache` 是全機共用的 SQLite，
    2026-10-06 在多個程式同時渲染後損毀（錯誤 `sqlite3.DatabaseError: database disk image is malformed`）。
    已把壞掉的那份改名為 `Cache_corrupt_20261006`（可以刪掉），ManimGL 會自動重建。
    平行渲染時讓每個程式用自己的快取：在它的 `custom_config.yml` 的 `directories:` 下加 `cache: "某個資料夾"`
    （`C:\mypython\manim\projects\combkit\tools\render_check.py` 會自動這樣做）。

---

## 8. 想修改或延伸時

- **改字幕**：各場景的 `self.say(...)`。以 `$` 開頭的字串是 LaTeX，其餘是中文。
- **改例子**：場景檔最上方的常數就是點編號（從正上方順時針、0 起算）或路徑的步（`L`=↑、`CH`=弦型、`TR`=三角形型；卡塔蘭模組是 R/U、U/D、A/B 的字）。
  改了之後先用 `counting.py` 的函式確認數字，再改場景裡的 `assert`。
- **卡塔蘭物件**：都由 `counting.binary_trees(n)` 的樹產生；要畫某一種，用 `catalan_draw.catalan_item(family, tree, scale, colored)`。
- **改顏色字型**：`codes/utils/styles.py`。講義的顏色在 `.tex` 開頭的 `\colorlet`，兩邊刻意一致（弦藍、三角形黃／橘、交叉紅、固定點橘／桃紅）。
  卡塔蘭模組的根／左／右（橘／青／粉紅）在 `catalan_draw.py` 開頭，左／右沿用 Chu 部分區域 $R_1$／$R_2$ 的顏色。
- **新增場景**：繼承 `utils.scene_base.ChuScene`，檔頭照抄其他場景的 `sys.path.insert(...)`；輔助函式寫成模組層級的函式（見第 7 節第 8 點）；
  再到 `main.py` 加同名子類別並放進對應的清單（`INTRO_SCENES`、`ALL_SCENES`、`MIT_SCENES`、`FULTON_SCENES`…`FULTON5_SCENES`），到 `render_all.py` 對應的清單加一行；
  新增一組連續播放時，也要加進 `render_all.py` 的 `DEMOS` 和 `render_all.bat` 的 `DEMOS` 變數。
- **改講義第 1 節的圖**：改 `notes/make_catalan_figs.py`，執行後再編譯講義（`catalan_figs.tex` 是產生出來的，不要手改）。
  第 2–9 節的圖是直接寫在 `.tex` 裡的 TikZ；附錄 A 的圖也是程式產生的（見下面「改講義附錄 A」）。
- **開發流程建議**：一次做一個場景；先 `-w -l` 低畫質輸出，用 ffmpeg 抽幾格檢查排版，最後才 `--hd`。
- **MIT 補充**：規格與決定都在 `notes/mit_plan.md`；新場景照 `mit_plan.md` 第 6 節的實作規則寫。原始的 `MIT18212_1_4.txt`、`note103how.txt` 很長，需要時才看。
- **改講義附錄 A**：內文在 `notes/mit/partK.tex`，圖改 `notes/mit/make_figs_partK.py`（每支都有 `check_numbers()`），執行 `python make_mit_figs.py` 後再編譯。
- **改 Raney 導讀**：主檔 `notes/raney1960_導讀.tex`（導言區照抄 Chu 講義的顏色、盒子與記號），內文 `notes/raney/part1..6.tex`，圖與表改 `notes/raney/make_figs.py`（`check_numbers()`、`check_numbers_text()` 檢查正文寫到的每一個數字），執行後再編譯兩次。原始資料在 `C:\mypython\manim\projects\ref\raney\`：三個 PDF 由 `convert_to_md.py` 機械轉成 `md\`，Raney 原文另有依頁面影像逐字校對、公式改成 LaTeX 的 `md\raney1960_text.md`（讀原文用這份）。
- **改 Young 表講義**：主檔 `notes/young_tableaux_導讀.tex`，內文在 `notes/fulton/part1..6.tex`，圖改 `notes/fulton/make_figs.py`（有 `check_numbers()`、`check_numbers_ch56()`、`check_numbers_ch7()`、`check_numbers_ch8()`），執行後再編譯；
  行內的小 Young 表用該講義導言區的 `\yts{122,34}`（ytableau 的 `\ytableaushort`；兩位數要加大括號，如 `48{10}`）。
  Chu 講義的目錄放在第 1 頁靠的是導言區把目錄的節距縮成 0.45em（`\patchcmd{\l@section}`）；再加一節可能會擠到第 2 頁。
- **尚未做的事**（可選）：配音與背景音樂；英文版字幕；講義的英文版。

---

## 9. 來源與授權

- 論文 PDF（`ref/`）：Chu 的論文著作權屬 Elsevier；Selimi 與 Saračević 的論文著作權屬作者與期刊；
  Raney (1960) 的論文著作權屬 American Mathematical Society（JSTOR 下載），Gessel (2016) 屬 Elsevier；`C:\mypython\manim\projects\ref\raney\md\` 的轉檔與謄寫同樣只供個人研讀。
  Fulton《Young Tableaux》著作權屬 Cambridge University Press（`ref/fulton_ch1_text.md` 是它的謄寫，`C:\mypython\manim\projects\ref\fulton\` 的各章 PDF 與 Markdown 也一樣，同樣受著作權保護）。僅供個人研讀，不要公開散布。
- ManimGL（`third_party/manim`）為 MIT 授權，作者 3Blue1Brown（Grant Sanderson）與貢獻者，來源 https://github.com/3b1b/manim 。
- `ref/` 的 ChatGPT 筆記與 overview、`notes/note1012.txt`、`notes/MIT18212_1_4.txt`、`notes/note103how.txt` 是使用者提供的需求與參考資料；
  MIT 18.212 的內容依據使用者提供的整理，專案裡沒有該課程的原始講義。
- 講義、動畫程式、驗證程式由 Claude（Anthropic）依上述資料撰寫；理論內容以論文原文為準，
  講義與動畫中「不在原文」的部分（樹的觀點、Raney 公式的路徑證明、反射原理）都有標明。
