# ACDC × Engineer Pack — phân tích, capability map, và kế hoạch hệ thống hoá

**Ngày:** 2026-08-10 · **Phạm vi đọc:** `ACDC.md` (232 dòng) + 10 SKILL.md load-bearing của Engineer Pack + inventory 60 skill.

> **Giới hạn nguồn.** Video `03l29gJXpCE` không lấy được nội dung (trang trả về footer/nav, không transcript, không description). Toàn bộ phân tích dưới đây dựa trên `ACDC.md`. Các số liệu trong đó — CMU "3 tháng", Wharton "92,7% / ~80%" — được xử lý như **trích dẫn chưa xác minh độc lập**, không dùng làm căn cứ cho bất kỳ đề xuất nào bên dưới. Mọi đề xuất đều đứng vững trên lập luận cấu trúc, không trên số liệu.

---

## 1. ACDC thật sự nói gì — sau khi bóc lớp vendor

`ACDC.md` là bản ghi một talk của Sonar. Phần cuối (mục 7) là product pitch, và chính tài liệu đã tự đánh dấu điều đó. Bóc lớp thương mại ra, còn lại **ba luận điểm** — và chỉ ba:

| # | Luận điểm | Mức độ mới |
|---|---|---|
| **A** | **Independent verification:** thứ kiểm định artifact không được cùng phương pháp với thứ sinh ra artifact. LLM review code do LLM viết = **blind spot tương quan**. | Đây là luận điểm mạnh nhất, và là luận điểm duy nhất thật sự sắc. |
| **B** | **Verification thuộc về inner loop:** kiểm tra khi agent **còn ngữ cảnh để sửa**, không đợi CI. | Đúng, nhưng là "shift-left" đóng gói lại. |
| **C** | **Bounded autonomy theo criticality:** prototype nhẹ, payment/auth/PII nghiêm. Không một mức kiểm soát cho mọi thứ. | Cũ, nhưng là chỗ pack đang hụt cụ thể nhất. |

Ba tên gọi `Guide / Verify / Solve` bản thân chúng **không mang thông tin mới**. "Guide" = context engineering. "Verify" = shift-left analysis. "Solve" = auto-fix loop. Giá trị nằm ở A, B, C — không nằm ở cái vòng ba pha.

### Chỗ ACDC yếu, mà pack đã mạnh

Đây là phần quan trọng để **không** tái cấu trúc pack quanh ACDC:

- **ACDC không có trục "đúng yêu cầu".** Toàn bộ "Verify" của ACDC là code-level: quality, security, complexity, architecture rules, compliance. Không có bước nào trả lời *"đoạn code này có làm đúng cái đã được đặc tả không?"*. Pack có — trục **Spec** của `inspect-change`, đi từng requirement ID.
- **ACDC không có traceability spine.** Không requirement ID, không `Satisfies:`, không `_Requirements:`. Pack có, và đó là xương sống.
- **ACDC không có TDD gate.** Không có khái niệm "không code trước khi có test đỏ".
- **ACDC không có behavioral acceptance.** Không có bước lái hệ thống đang chạy như một client thật. Pack có `validate-feature` / `validate-api` / `validate-ui` / `run-product-walkthrough`.
- **ACDC không có audit trail bất biến cho quyết định con người.** Pack có `record-verdict` (payload bất biến + envelope append-only, record-before-crossing).

**Kết luận chiến lược: pack không thiếu ACDC. Pack thiếu đúng *một lớp* mà ACDC gọi đúng tên — computational verification — cộng với hai cơ chế phụ trợ (criticality zoning, debt tracking). Còn lại pack đã chặt hơn ACDC.**

---

## 2. Capability map: ACDC → Engineer Pack

Cột "Trạng thái": ✅ đã có và chặt hơn ACDC · 🟡 có nhưng lỏng/đặt sai chỗ · ❌ không tồn tại.

### Pha GUIDE

| Yêu cầu ACDC | Skill / artifact trong pack | Trạng thái |
|---|---|---|
| Mục tiêu task | `frame-change` → `specify-behavior` (EARS + ID) | ✅ vượt xa |
| Kiến trúc mong muốn | `define-project` → `docs/architecture/` spine `**ARCH-N**`; `design.md` `Respects:` | ✅ vượt xa |
| Coding standards | `docs/standards/` qua `define-system-doc`; fallback `docs/product/guidelines.md` | ✅ |
| Pattern được phép | `standards-baseline.md` (12 smells) + `CONTEXT.md` glossary | ✅ |
| Dependency policy | — có thể nằm trong standards, nhưng **không có slot bắt buộc** | 🟡 |
| Logging / observability / tracing | `define-system-doc standards/errors-logging` — **opt-in, không ai gọi** | 🟡 |
| Security standards | `define-system-doc standards/security-coding` — tồn tại nhưng **không skill nào consult** | 🟡 |
| Quality gate criteria | ❌ không tồn tại khái niệm ngưỡng | ❌ |
| Context có chọn lọc, không nạp cả repo | `load-subgraph` (ask-time derivation), brief-per-task trong `build-in-waves` ("the brief is its world"), "Never the plan file" | ✅ **vượt ACDC rõ rệt** |
| Phân loại criticality hệ thống | `Delivery intent` + `Lifecycle stage` trong `project.md` — nhưng chỉ chỉnh *ceremony*, **không chỉnh độ nghiêm của verify**, và **không theo vùng code** | 🟡 |

### Pha VERIFY

| Lớp ACDC | Skill trong pack | Trạng thái |
|---|---|---|
| **Computational analysis** (static analysis, data/control flow, dependency, architectural rules) | **Không có gì.** `grep -ri 'semgrep\|SAST\|CodeQL\|npm audit\|gitleaks\|trivy\|static analysis'` trên `skills/` → **0 hit**. Lint/typecheck chỉ tồn tại như tên lệnh trong `project.md`, chạy ở `prove-claim` và `land-branch` — không bao giờ chạy trên **diff của một task**. | ❌ **gap chính** |
| **LLM-based review** | `inspect-change` (2 trục song song, subagent riêng, read-only, cấm pre-judge) + `polish-diff` (4 góc) + `review-invariants` | ✅ **vượt xa ACDC** |
| **Quality analysis** (maintainability, complexity) | `standards-baseline.md` 12 smells — nhưng là *judgment call của LLM*, không phải số đo | 🟡 |
| **Security analysis** | `standards-baseline.md` mục 13–18 — chỉ kích hoạt "when the diff crosses a trust boundary", và **"always a judgment call, never a hard violation"** | 🟡 lỏng |
| **Compliance checks** | `audit-trace` (docs-only, grep + set-difference — **kết quả giống nhau bất kể ai chạy**, đúng chuẩn "repeatable" của ACDC) | ✅ |
| Verification trong **inner loop** | Task reviewer sau mỗi task trong `build-in-waves` ✅ · nhưng `test-first` "Verify GREEN" chỉ chạy **test suite**, không typecheck/lint/scan | 🟡 nửa vời |
| **Zero-trust** (không để thứ sinh code tự chấm) | Rất mạnh: implementer ≠ reviewer, fresh subagent, "Never fix in controller context", "Let implementer self-review substitute for task review" là **Red Flag** | ✅ **vượt ACDC** |
| Phương pháp khác với phương pháp sinh code | ❌ **Reviewer vẫn là LLM đọc diff — cùng loại phương pháp.** Tests là lớp độc lập duy nhất, nhưng test cũng do agent viết. | ❌ |

### Pha SOLVE

| Yêu cầu ACDC | Skill trong pack | Trạng thái |
|---|---|---|
| Trả lỗi có cấu trúc về agent | Task reviewer report + `.skills/<CODE>/task-N-report.md` | ✅ |
| Agent phân tích nguyên nhân | `root-cause` (Iron Law: no fix without root cause) | ✅ vượt ACDC |
| Sửa và verify lại | Fix loop trong `build-in-waves` bước 8, **bắt buộc re-review** | ✅ |
| Lặp đến khi đạt gate | Có vòng lặp, **nhưng không có "gate" định lượng** — điều kiện dừng là "reviewer hết Critical/Important", tức LLM judgment | 🟡 |
| Chống lặp vô hạn | "Same finding survives 3 cycles → stop"; cap 2 redispatch; `reroute-plan` khi plan sai | ✅ **vượt ACDC** (ACDC không nói gì về vòng lặp không hội tụ) |
| Không dồn nợ cho developer | 🟡 Ngược lại: Minors → ledger `.skills/` (**git-ignored**); `polish-diff` dropped findings → chỉ trong report phiên đó. **Nợ bốc hơi thay vì được ghi.** | ❌ |

### Outer loop

| Yêu cầu ACDC | Pack | Trạng thái |
|---|---|---|
| Review tự động toàn bộ thay đổi | `inspect-change` với base = `git merge-base main HEAD` (cấm mid-branch sha) | ✅ |
| Kiểm tra toàn diff, không chỉ file agent sửa | ✅ đúng theo thiết kế | ✅ |
| Chặn PR nếu không đạt gate | `land-branch` bước 1: red → **chỉ còn discard/block**, giấu merge/PR | ✅ vượt ACDC |
| Audit trail | `record-verdict`: payload bất biến + envelope append-only, record-before-crossing, cấm citation bằng path | ✅ **vượt xa ACDC** |
| Không cho agent tự phê duyệt | `record-verdict` HARD-GATE: caller thuộc tập đóng, phải có **terminal human verdict** | ✅ |
| Human review có trách nhiệm với code nhạy cảm | 🟡 `select-review-sample` tồn tại và tốt (Iron Law: mọi unit hoặc được sample hoặc được đặt tên là residue) — nhưng `build-in-waves` ghi rõ **"Optional: /select-review-sample (not a gate)"** | 🟡 |
| Đo defect rate / complexity / security / thời gian trả nợ | ❌ không skill nào tích luỹ số liệu qua thời gian | ❌ |

---

## 3. Chẩn đoán — 7 gap, xếp theo mức độ đáng sửa

### G1 — Không có lớp computational verification *(gap chính, sửa trước tiên)*

Toàn bộ "Verify" của pack quy về hai thứ: **test do agent viết** và **LLM đọc diff**. `standards-baseline.md` với 18 mục là một cây rìu tốt, nhưng nó là *một prompt cho LLM*, không phải một phương pháp khác. Đây chính xác là điều luận điểm A của ACDC cấm: dùng cùng loại năng lực để chấm chính nó → sai lầm tương quan, không phải sai lầm độc lập.

Bằng chứng cụ thể trong pack:
- `test-first` "Verify GREEN" = *"Run the full suite … output pristine — zero warnings"*. Không typecheck. Không lint. Không scan.
- Bảng `Claim → evidence` của `prove-claim` có 6 hàng. **Không hàng nào** nói về security hay static analysis.
- `standards-baseline.md` §Security: *"each is a labeled judgment call, a documented repo standard or an existing scanner overrides it"* — pack **giả định** có scanner ở đâu đó, nhưng không skill nào chạy scanner, và không bước setup nào cấu hình scanner.

Đây là verification debt đúng nghĩa: pack đã thiết kế chỗ trống cho lớp này (câu "an existing scanner overrides it") rồi không bao giờ lấp.

### G2 — Verification chưa đủ sâu trong inner loop

Vòng lặp thật của `build-in-waves` là: dispatch → implementer → **package diff** → reviewer. Giữa implementer và reviewer **không có gì chạy**. Typecheck/lint chỉ xuất hiện ở `prove-claim` (khi có ai đó định tuyên bố xong) và `land-branch` (gate cuối). Nghĩa là một lỗi type có thể sống qua 5 task trước khi bị bắt — đúng lúc ngữ cảnh đã mất, đúng cái ACDC cảnh báo.

### G3 — Ceremony tier ≠ criticality tier

Pack có tier 0/1/2, nhưng đó là tier theo **kích thước thay đổi**. ACDC nói về tier theo **rủi ro của vùng code**. Hai trục hoàn toàn khác nhau: một sửa một dòng trong đường xác thực là tier 0 theo kích thước và tier cao nhất theo rủi ro.

Hệ quả cụ thể: một diff chạm `auth/` được xử lý **giống hệt** một diff chạm `docs/`. `Delivery intent: Production` trong `project.md` chỉ được `frame-change` và `clarify-decisions` đọc để chỉnh ceremony — nó **không** làm verify nghiêm hơn. Và mục 13–18 của `standards-baseline` "always a judgment call, never a hard violation" — kể cả secret hardcoded trong đường thanh toán.

### G4 — Nợ xác minh bốc hơi thay vì tích luỹ

Ba đường rò rỉ:
- `inspect-change` Minors → `.skills/<CODE>/progress.md` → **git-ignored**, và `build-in-waves` tự nói *"if wiped, reconstruct from git log"* — không reconstruct được findings.
- `polish-diff` bước 4: *"Record each drop with its one-line reason"* → chỉ nằm trong report của phiên đó.
- `configure-repo` bước 6 "content failures" (lỗi có sẵn của repo) → *"Record these for the user"* → không có nơi ghi.

Không có `docs/` artifact nào sống sót. Đúng nghịch lý ACDC mô tả: mỗi vòng lặp sạch cục bộ, tổng thể nợ tăng, và không ai đo được.

### G5 — Không có metric theo thời gian

`assess-milestone` đánh giá *"milestone có giao đúng lời hứa không"* — đó là outcome, không phải chất lượng. Không có gì trả lời: defect rate đang đi lên hay xuống? complexity đang tăng ở đâu? bao nhiêu finding bị drop tháng này? ACDC nói thẳng: đừng đo AI bằng tốc độ, đo bằng những chỉ số đó. Pack hiện **không đo gì cả**.

### G6 — Rubber-stamping phía con người chưa có phòng thủ bắt buộc

Pack phòng thủ agent-side rất tốt (gate-session, 4 Iron Law, các bảng rationalization ghi lại nguyên văn lời tự biện của agent — đây là kỹ thuật thiết kế xuất sắc). Nhưng phía **con người**, mọi quyết định đều là phê duyệt trần: menu 5 lựa chọn của `land-branch`, *"the user approves the drafts"* của `configure-repo`. `select-review-sample` là đúng liều thuốc — và nó bị đánh dấu **"not a gate"**.

### G7 — Model diversity chưa được dùng làm zero-trust

`build-in-waves` §Model Tiering phân theo **giá/độ khó** (cheap / mid floor / top). Không có dòng nào nói reviewer nên **khác model family** với implementer. ACDC: *"mỗi mô hình có kiểu lỗi khác nhau"*. Đây là lớp independent verification **rẻ nhất** hiện có và pack chưa lấy.

---

## 4. Kế hoạch — ADD / UPGRADE / RESTRUCTURE / REMOVE

Nguyên tắc: pack đã có 60 skill engineering. **Thêm skill là chi phí.** Mọi thứ có thể làm bằng cách sửa skill sẵn có thì sửa, không tạo mới.

### ADD — 2 skill mới (không phải 5)

#### `scan-code` → `skills/execution/scan-code/` **[P0]**

Lớp computational verification còn thiếu. Nhận một range diff, chạy các lệnh phân tích từ `docs/agents/project.md`, trả **structured findings** — không phải judgment.

- Chạy: typecheck, lint, secret scan, dependency audit, SAST nếu repo có cấu hình, complexity delta nếu có tool.
- Xuất: `{ tool, severity, file:line, rule_id, message }` — có `rule_id`, khác hẳn finding của LLM.
- **Nguyên tắc kế thừa từ pack:** *"skip anything tooling already enforces"* đảo chiều — ở đây tooling **là** nguồn, và LLM reviewer mới là thứ phải bỏ qua những gì tool đã bắt. Điều này còn **giảm** noise cho `inspect-change`.
- No-op sạch khi repo không cấu hình tool nào — báo "no analysis layer configured", không bịa.

Được gọi từ: `test-first` (sau GREEN), `build-in-waves`/`by-story`/`inline` (trước khi đóng gói diff cho reviewer), `inspect-change` (bước 3.5), `land-branch` (gate), `prove-claim`.

#### `track-quality-debt` → `skills/track/track-quality-debt/` **[P1]**

Sổ nợ **bền** tại `docs/quality/debt.md`, mỗi mục một `**DEBT-N**` (đúng ngữ pháp ID của pack, để `audit-trace` soi được).

Nhận đầu vào từ: Minors của `inspect-change`, dropped findings của `polish-diff`, content failures của `configure-repo` bước 6, findings bị `vet-feedback` phân loại là "đúng nhưng hoãn".
Được đọc bởi: `assess-milestone` (xu hướng), `cut-release` (nợ chưa trả trước khi phát hành), `plan-milestones` (nợ thành hạng mục roadmap).

### UPGRADE — 9 chỉnh sửa vào skill sẵn có

| # | Skill | Thay đổi | Ưu tiên |
|---|---|---|---|
| 1 | `configure-repo` | **Decision C mở rộng:** ngoài verify commands, hỏi thêm *analysis commands* (SAST/secret/dep-audit/complexity) và *quality gate thresholds*. **Decision K mới — Criticality zones:** glob → risk tier (`standard` / `sensitive`), gợi ý từ cấu trúc repo (`auth/`, `payment/`, `migrations/`, `infra/`, xử lý PII). Bước 6 chứng minh cả analysis commands là **wired**, đúng kỷ luật sẵn có. | **P0** |
| 2 | `build-in-waves` (+ `build-by-story`, `build-inline`) | Chèn **bước 5.5** vào Per-Task Loop: `scan-code` trên `$BASE..HEAD` **trước** khi đóng gói diff. Findings computational vào **cùng fix loop** bước 8 (cùng cap 3 cycles). Đây chính là inner loop của ACDC, và chi phí gần bằng 0 vì reviewer đằng nào cũng chạy. | **P0** |
| 3 | `test-first` | "Verify GREEN" hiện định nghĩa pristine = suite xanh + zero warnings. Mở rộng thành **suite + typecheck + lint** — cả ba rẻ, nhanh, và đây là vòng lặp trong cùng nhất. | **P0** |
| 4 | `prove-claim` | Thêm hàng vào bảng `Claim → evidence`: `"Không có regression chất lượng/bảo mật"` → `scan-code` sạch trên diff · *Never sufficient:* "tests xanh", "lint chạy ở CI". Bảng hiện thiếu hẳn trục này. | **P0** |
| 5 | `inspect-change` | Thêm **lane thứ tư `## Analysis`** — computational, và **là hard finding**, khác ba lane kia. Cấu trúc mới: Standards (judgment) / Spec (judgment) / **Analysis (computational, hard)** / Invariants (advisory). Giữ nguyên luật cấm merge-và-rerank. Đồng thời: khi diff chạm **sensitive zone**, mục 13–18 chuyển từ judgment call thành **hard finding**. | **P0** |
| 6 | `standards-baseline.md` | Tách 6 mục security ra `security-baseline.md` riêng, với quy tắc leo thang theo criticality zone. Hiện chúng bị chôn dưới 12 mục quality và bị hạ cấp vĩnh viễn thành judgment call — kể cả secret hardcoded. | **P1** |
| 7 | `land-branch` | Gate bước 1 hiện = verify commands + `audit-trace` + `validate-feature`. Thêm: **quality gate** (ngưỡng từ `scan-code`) và — khi diff chạm sensitive zone — **`select-review-sample` là bắt buộc**, không cho phép merge/PR bằng phê duyệt trần. Đây là phòng thủ trực tiếp cho G6. | **P1** |
| 8 | `build-in-waves` §Model Tiering | Thêm quy tắc: *"reviewer nên khác model family với implementer khi harness cho phép; ghi rõ cả hai model trong ledger."* Lớp independent verification rẻ nhất. | **P1** |
| 9 | `vet-feedback` | Mở rộng phạm vi sang findings của `scan-code`. Bước 3 (PROVE CLAIM từng claim) đã là **đúng cơ chế** để lọc false positive của static analysis — chỉ cần nói rõ nó áp dụng cho tool findings, và item "đúng nhưng hoãn" đi vào `track-quality-debt` thay vì bốc hơi. | **P1** |

### RESTRUCTURE — đặt tên ba lớp verification

Hiện các skill verification bị rải theo bucket **thời điểm** chứ không theo **phương pháp**:

```
execution/  audit-trace, test-first, prove-claim
review/     inspect-change, polish-diff, review-invariants, select-review-sample
acceptance/ validate-feature, validate-api, validate-ui, review-product-flow, ...
```

Đọc inventory không ai thấy được "pack này có mấy lớp xác minh độc lập". Đề xuất **không đổi thư mục** (tốn kém, phá symlink, phá `npx skills`) mà thêm **một trang docs**: `docs/guide/concepts/verification-layers.md`, đặt cạnh `gates.md` và `traceability.md`:

```
Lớp 1 — Computational   scan-code · test-first · audit-trace
                        (lặp lại được, cùng kết quả bất kể ai chạy)
Lớp 2 — Judgment        inspect-change · polish-diff · review-invariants
                        (LLM; độc lập với implementer, không độc lập về phương pháp)
Lớp 3 — Behavioral      validate-feature/api/ui · run-product-walkthrough
                        (lái hệ thống đang chạy)
Lớp 4 — Human           select-review-sample · record-verdict
                        (chống rubber-stamp; bắt buộc ở sensitive zone)
```

Đây là đóng góp lớn nhất của ACDC vào pack: **không phải thêm quy trình, mà là đặt tên cho các lớp để thấy được lớp nào đang trống.** Bốn Iron Law hiện đã có `docs/guide/concepts/gates.md`; trang này là cặp song sinh của nó.

### REMOVE — không có gì bắt buộc bỏ

Không skill nào mâu thuẫn với ACDC. Hai ứng viên hợp nhất, **không liên quan ACDC**, chỉ là quan sát về sự phình:

- `build-in-waves` / `build-by-story` / `build-inline` — ba biến thể của **cùng một loop**, khác nhau ở mode và có/không subagent. Ứng viên gộp thành một skill + tham số route. Rủi ro: cả ba đã có mode-ownership table rất kỹ; gộp có thể làm mất độ sắc đó. **Khuyến nghị: chưa động.**
- `review-product-flow` / `vet-product-flow` / `run-product-walkthrough` — ba skill quanh một guide file. Ứng viên gộp `vet-product-flow` vào `review-product-flow` như một mode. **Khuyến nghị: cân nhắc, không gấp.**

---

## 5. Thứ tự thực hiện

**Đợt 1 — lấp lớp computational (đây là toàn bộ giá trị của ACDC với pack này):**
`scan-code` → `configure-repo` Decision C mở rộng + Decision K → `test-first` GREEN mở rộng → `prove-claim` thêm hàng → `build-in-waves` bước 5.5 → `inspect-change` lane Analysis.

Sau đợt 1, pack đã hệ thống hoá đủ A và B của ACDC. Đợt 2 (`security-baseline` tách, `land-branch` quality gate + sample bắt buộc, model diversity, `vet-feedback` mở rộng) phủ C. Đợt 3 (`track-quality-debt`, `verification-layers.md`) đóng vòng đo lường.

---

## 6. Ý kiến thẳng

**Về ACDC:** đây là một talk vendor với một luận điểm thật sự tốt (independent verification method ≠ generation method) được gói trong một framework ba chữ không cần thiết. Đừng nhận cái framework. Nhận cái luận điểm.

**Về pack của bạn:** phần bạn làm tốt nhất là chỗ ACDC không chạm tới — traceability spine, các Iron Law viết dưới dạng cấm tuyệt đối kèm bảng ghi lại nguyên văn lời tự biện của agent, zero-trust giữa implementer và reviewer, `record-verdict` với record-before-crossing. Đó là thiết kế trên mức của talk này.

Chỗ hụt của pack, ACDC gọi đúng tên và pack thậm chí **đã tự thú nhận** trong một mệnh đề: `standards-baseline.md` viết *"an existing scanner overrides it"* — pack giả định có scanner, rồi không bao giờ chạy scanner, không bao giờ cấu hình scanner. Cái mệnh đề đó là chỗ trống hình lớp-computational, đã được đục sẵn, chờ được lấp.

**Rủi ro cần canh:** nhồi static analysis vào inner loop dễ tạo noise — agent chạy theo cảnh báo vô nghĩa, đốt token, và tệ hơn là học được rằng finding có thể bỏ qua. Pack đã có sẵn hai thuốc giải: nguyên tắc *"skip anything tooling already enforces"* (chống trùng lặp) và `vet-feedback` bước 3 *"prove claim từng claim trước khi chấp nhận"* (chống false positive). Khi thêm `scan-code`, phải nối vào cả hai — nếu không thì đợt 1 sẽ làm pack chậm hơn mà không sạch hơn.
