Video **“Guide, Verify, Solve — Anirban Chatterjee, Sonar”** trình bày cách xây dựng quy trình phát triển phần mềm bằng AI an toàn hơn. Luận điểm trung tâm là: **không nên để AI tự viết rồi chỉ dựa vào con người để kiểm tra; cần một hệ thống xác minh độc lập, tự động, nhiều lớp và lặp lại trong chính vòng lặp của AI**. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

## 1. Bối cảnh: AI tăng tốc nhưng tạo “verification debt”

Diễn giả dẫn lại một nghiên cứu của Carnegie Mellon trên các dự án GitHub sử dụng công cụ AI coding, cụ thể là Cursor:

- Năng suất tăng mạnh trong thời gian đầu.
- Mức tăng này chỉ kéo dài khoảng **3 tháng**.
- Sau đó, cảnh báo từ static analysis và độ phức tạp của mã nguồn tiếp tục tăng.
- Những vấn đề tích lũy này dần làm chậm đội ngũ phát triển.

Khoảng cách giữa **chất lượng mã AI tạo ra** và **chất lượng phần mềm thực tế cần đạt được** được diễn giả gọi là **verification debt** — “nợ xác minh”. Với prototype hoặc công cụ nội bộ ngắn hạn, khoản nợ này có thể chấp nhận được; nhưng với hệ thống lớn, nhiều người dùng, dữ liệu nhạy cảm hoặc người dùng có tính đối kháng, nó có thể trở thành rủi ro nghiêm trọng. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

### Vì sao AI tạo ra khoản nợ này?

Theo video, có một số nguyên nhân chính:

- **Mô hình vẫn có thể mắc lỗi**, dù khả năng sinh mã ngày càng tốt.
- **Thiếu ngữ cảnh hệ thống**: AI thường không biết đầy đủ mục tiêu kinh doanh, các quyết định kiến trúc, các cuộc họp trước đó hoặc những ràng buộc nằm ngoài prompt.
- **Mỗi mô hình có kiểu lỗi khác nhau**: mô hình này có thể mạnh về tính đúng đắn nhưng yếu về bảo mật hoặc khả năng bảo trì.
- **Mã nguồn tương tác phức tạp**: một đoạn code riêng lẻ có thể trông hợp lý nhưng gây lỗi khi kết hợp với các module, dependency hoặc luồng dữ liệu khác.

Nói cách khác, AI có thể tạo ra code “chạy được” nhưng chưa chắc tạo ra phần mềm **đúng yêu cầu, an toàn, dễ bảo trì và phù hợp với kiến trúc tổng thể**.

## 2. Không thể chỉ dựa vào code review của con người

Một phần quan trọng của video là hạn chế của human review trong thời đại AI-generated code.

Diễn giả dẫn một nghiên cứu của Wharton: người tham gia làm theo lời khuyên của AI **92,7% thời gian khi AI trả lời đúng**, nhưng vẫn làm theo gần **80% thời gian khi AI được hướng dẫn nói sai một cách tự tin**. Điều này cho thấy con người thường có xu hướng tin AI, đặc biệt khi:

- Lượng code cần review quá lớn.
- Nhiều coding agent hoạt động cùng lúc.
- Developer chịu áp lực phải giao hàng nhanh.
- Reviewer không đủ thời gian hiểu toàn bộ ngữ cảnh.
- Pull request chứa quá nhiều thay đổi nhỏ và lặp lại.

Vì vậy, code review thủ công có nguy cơ biến thành **rubber stamping** — reviewer chỉ xem lướt rồi phê duyệt. Video không cho rằng con người trở nên vô dụng, mà nhấn mạnh rằng con người cần được hỗ trợ bởi một lớp xác minh tự động và có hệ thống. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

## 3. Hai nguyên tắc xác minh cốt lõi

### Zero-trust verification

“Zero trust” ở đây có nghĩa là hệ thống xác minh phải giả định rằng code có thể đến từ bất kỳ nguồn nào:

- Developer viết thủ công.
- AI agent tạo ra.
- Một AI khác chỉnh sửa.
- Một công cụ hoặc pipeline bên thứ ba sinh ra.

Không nên dùng chính mô hình đã viết code để tự đánh giá code của nó như cơ chế duy nhất, vì mô hình có thể lặp lại chính các điểm mù và giả định sai ban đầu.

Một hệ thống xác minh zero-trust cần:

- Độc lập với công cụ đã sinh code.
- Có quy trình giống nhau cho mọi project và team.
- Có tính audit được.
- Có kết quả nhất quán và lặp lại.
- Dựa trên phương pháp khác với phương pháp tạo code.

Về mặt kỹ thuật, điều này tương tự nguyên tắc **separation of concerns** và **independent validation**: component tạo ra artifact không nên là nguồn kiểm định duy nhất của artifact đó.

### Multi-layered verification

Một phương pháp duy nhất không thể phát hiện mọi vấn đề. Video đề xuất kết hợp nhiều lớp:

- **Computational analysis**: static analysis, kiểm tra syntax, data flow, control flow, dependency và architectural rules.
- **LLM-based review**: đánh giá theo reasoning, ngữ cảnh, ý định của thay đổi và các vấn đề khó biểu diễn bằng rule cố định.
- **Quality analysis**: maintainability, reliability và complexity.
- **Security analysis**: phát hiện lỗ hổng, pattern nguy hiểm và vấn đề dependency.
- **Compliance checks**: bảo đảm các quy tắc nội bộ hoặc yêu cầu ngành được áp dụng nhất quán.

Điểm quan trọng là các lớp này **bổ sung cho nhau**, chứ không phải cạnh tranh để tìm một “mô hình tốt nhất”. Một mô hình có thể tối ưu correctness, trong khi mô hình khác hoặc công cụ khác phát hiện maintainability, security và complexity tốt hơn. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

## 4. Framework ACDC: Guide, Verify, Solve

Video giới thiệu mô hình **ACDC — Agent-Centric Development Cycle**, gồm ba pha.

### 1. Guide — hướng dẫn

Trước khi agent viết code, cần cung cấp:

- Mục tiêu của task.
- Kiến trúc mong muốn.
- Coding standards.
- Pattern được phép sử dụng.
- Dependency được phép hoặc bị cấm.
- Quy tắc logging, observability và tracing.
- Tiêu chuẩn bảo mật.
- Tiêu chí quality gate.
- Các ràng buộc liên quan đến codebase.

Đây là bước giúp agent không bắt đầu từ “trang giấy trắng”. Thay vì đưa toàn bộ codebase vào context window, hệ thống nên cung cấp **đúng phần ngữ cảnh cần thiết cho task hiện tại**. Việc nạp toàn bộ repository có thể khiến agent tốn token, mất thời gian khám phá và dễ bị nhiễu.

### 2. Verify — xác minh

Sau hoặc ngay trong lúc sinh code, hệ thống phải chạy xác minh:

- Tìm lỗi chất lượng.
- Tìm vấn đề bảo mật.
- Kiểm tra độ phức tạp.
- Kiểm tra khả năng bảo trì.
- Kiểm tra tính phù hợp với kiến trúc.
- Kiểm tra các quy tắc compliance.
- Đánh giá bằng phương pháp độc lập với mô hình tạo code.

Verification không nên chỉ xuất hiện ở cuối pipeline. Video nhấn mạnh rằng nó cần chạy trong **inner agentic loop**, tức vòng lặp bên trong khi agent đang viết và chỉnh sửa code. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

### 3. Solve — giải quyết

Các vấn đề được phát hiện nên được trả ngược lại cho agent để agent:

1. Đọc danh sách lỗi.
2. Phân tích nguyên nhân.
3. Lập kế hoạch sửa.
4. Cập nhật code.
5. Chạy verification lần nữa.
6. Lặp lại cho đến khi đạt quality gate.

Cách này tốt hơn việc để lỗi tồn tại rồi đẩy toàn bộ backlog cho developer xử lý sau. Nó ngăn lỗi lan sang các vòng lặp tiếp theo và giảm lượng technical debt phát sinh.

## 5. Inner loop và outer CI/CD loop

Một insight quan trọng là verification cần được thực hiện ở **hai cấp độ**.

### Inner loop: vòng lặp của AI agent

Quy trình khái quát:

```text
Task
  ↓
Cung cấp context + constraints
  ↓
AI sinh code
  ↓
Chạy verification
  ↓
Có lỗi? ── Có ──> AI sửa lỗi
  │                  ↓
  └── Không <── Chạy verification lại
```

Mục tiêu là phát hiện lỗi càng sớm càng tốt, khi agent vẫn còn đủ ngữ cảnh để sửa.

### Outer loop: vòng lặp CI/CD và pull request

Sau khi các inner loop hoàn tất:

1. Tạo pull request.
2. Chạy review tự động trên toàn bộ thay đổi.
3. Thực hiện cả LLM-based review và computational analysis.
4. Kiểm tra quality, security và maintainability.
5. Chặn PR nếu không đạt quality gate.
6. Cho phép fix agent sửa lỗi.
7. Chỉ build, test và deploy sau khi đạt tiêu chuẩn.

Inner loop giúp agent viết code tốt hơn ngay từ đầu; outer loop đóng vai trò **cổng kiểm soát độc lập cuối cùng** trước khi code đi vào production. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

## 6. Ý nghĩa thực tế với kiến trúc và quy trình phát triển

Từ nội dung video, có thể rút ra một quy trình phù hợp cho team sử dụng AI coding agent:

### Trước khi coding

- Viết rõ architectural constraints.
- Chuẩn hóa coding standards.
- Định nghĩa dependency policy.
- Quy định security và observability.
- Chọn quality gate cho từng loại project.
- Phân loại mức độ criticality của hệ thống.

Không nên áp dụng cùng một mức kiểm soát cho mọi thứ. Prototype có thể dùng quy trình nhẹ hơn, còn hệ thống thanh toán, authentication, dữ liệu cá nhân hoặc infrastructure cần tiêu chuẩn nghiêm ngặt hơn.

### Trong lúc coding

- Cung cấp context có chọn lọc.
- Dùng agent để sinh code và test.
- Chạy static analysis sớm.
- Chạy security scan ngay trong inner loop.
- Trả lỗi có cấu trúc cho agent.
- Bắt agent tự sửa và xác minh lại.

### Trước khi merge

- Chạy independent verification.
- Kiểm tra toàn bộ diff, không chỉ file agent vừa sửa.
- Áp dụng quality gate tập trung.
- Ghi lại audit trail.
- Không cho phép agent tự phê duyệt mà không có rào chắn.
- Với code nhạy cảm, vẫn cần human review có trách nhiệm.

## 7. Các sản phẩm Sonar được đề cập

Vì diễn giả là đại diện Sonar, phần cuối video tập trung vào hệ sinh thái sản phẩm của Sonar:

- **SonarQube**: nền tảng phân tích và xác minh mã nguồn, bao phủ các vấn đề như syntax, data flow, architecture và control flow.
- **Gitarr**: công cụ AI code review và tự động hóa CI workflow, có thể phát hiện lỗi, hỗ trợ tạo bản sửa và dần tự động hóa việc phê duyệt/merge khi tổ chức đã đủ tin cậy.
- **Sonar Vortex**: cung cấp context, guardrail và verification trực tiếp bên trong agentic loop.
- **Remediation agent**: hỗ trợ xử lý technical debt và các lỗi tồn đọng trong legacy code ở quy mô lớn.

Các tuyên bố về sản phẩm và số liệu sử dụng trong phần này nên được xem là **thông tin do nhà cung cấp trình bày**, không phải đánh giá độc lập. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)

## 8. Những điểm nên áp dụng và điểm cần phản biện

### Điều đáng áp dụng

- Đừng đo hiệu quả AI chỉ bằng số dòng code hoặc tốc độ hoàn thành task.
- Đo thêm defect rate, complexity, security issues, maintainability và thời gian xử lý technical debt.
- Tách biệt công cụ sinh code và công cụ xác minh.
- Đưa verification vào inner loop, không đợi đến CI.
- Dùng quality gate tập trung cho toàn bộ team và AI tool.
- Cho agent quyền sửa lỗi nhưng vẫn giới hạn quyền bằng policy và approval gate.
- Quản lý context window có chủ đích thay vì nạp toàn bộ codebase.

### Điều cần thận trọng

- Không phải mọi cảnh báo static analysis đều có cùng mức độ quan trọng.
- LLM-based review vẫn có thể hallucinate hoặc bỏ sót lỗi.
- Tự động hóa merge cần được triển khai tăng dần, dựa trên dữ liệu thực tế.
- Các số liệu nghiên cứu được trình bày trong video cần được đọc cùng phương pháp nghiên cứu gốc.
- Sonar có lợi ích thương mại trực tiếp, nên không nên xem các sản phẩm của Sonar là giải pháp duy nhất.
- Verification không thay thế hoàn toàn architectural review, threat modeling, integration testing và hiểu biết nghiệp vụ.

## Kết luận

Thông điệp cốt lõi của video là **bounded autonomy**: cho AI quyền tự chủ để tăng tốc phát triển, nhưng phải đặt nó trong một hệ thống có context, ràng buộc, xác minh độc lập và khả năng tự sửa lỗi. Mô hình hiệu quả không phải là “AI viết code → con người xem qua”, mà là:

```text
Guide → Generate → Verify → Solve → Verify lại → Review/CI → Ship
```

Đặc biệt với các hệ thống production, distributed system hoặc có yêu cầu bảo mật cao, đây là cách tiếp cận hợp lý để tránh việc tốc độ ngắn hạn của AI biến thành technical debt và verification debt dài hạn. [youtube](https://www.youtube.com/watch?v=03l29gJXpCE)
