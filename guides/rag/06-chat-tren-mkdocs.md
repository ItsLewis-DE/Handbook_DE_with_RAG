# Phase 06 — Tích hợp khung chat vào MkDocs

[Trước](05-danh-gia-hybrid-search.md) · [Lộ trình](README.md)

## Mục tiêu

Bạn đã có `/chat` trả về `answer`, `sources` và `status` theo phase 04, cùng chế độ retrieval đã chọn ở phase 05. Phase này chỉ thêm giao diện và kết nối trình duyệt; không đổi ingestion hoặc model.

Đầu ra là một nút “Hỏi tài liệu” trên các trang, khung nhập câu hỏi, trạng thái chờ và các nguồn mở được. Mỗi câu hỏi độc lập; chưa có memory hay viết lại câu hỏi theo hội thoại.

## 1. Cho phép frontend local gọi backend

Trong `backend/app.py`, thêm import:

```python
from fastapi.middleware.cors import CORSMiddleware
```

Ngay sau dòng `app = FastAPI(...)`, thêm:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
```

Cổng 8000 và 8001 là hai origin khác nhau dù cùng máy. Middleware xử lý preflight `OPTIONS`; không cần viết endpoint OPTIONS riêng. CORS là cơ chế của trình duyệt, không phải xác thực hay giới hạn request. [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)

## 2. Tạo `docs/javascripts/chat.js`

```javascript
(() => {
  // URL của script là <site-root>/javascripts/chat.js.
  // Suy ra site root để nguồn vẫn đúng khi website có tiền tố /architecture-notes/.
  const scriptUrl = document.currentScript.src;
  const siteRoot = new URL("../", scriptUrl);
  const endpoint = "http://127.0.0.1:8001/chat";

  function mountChat() {
    if (document.getElementById("rag-chat-dialog")) return;

    function element(tag, className, text) {
      const node = document.createElement(tag);
      if (className) node.className = className;
      if (text) node.textContent = text;
      return node;
    }

    const launcher = element("button", "rag-launcher", "Hỏi tài liệu");
    launcher.type = "button";
    launcher.setAttribute("aria-haspopup", "dialog");
    launcher.setAttribute("aria-controls", "rag-chat-dialog");

    const dialog = element("dialog", "rag-dialog");
    dialog.id = "rag-chat-dialog";
    dialog.setAttribute("aria-labelledby", "rag-chat-title");

    const heading = element("h2", "", "Hỏi Behind the Pipeline");
    heading.id = "rag-chat-title";
    const close = element("button", "rag-close", "Đóng");
    close.type = "button";
    const help = element(
      "p", "rag-help",
      "Hỏi về nội dung các bài viết. Mỗi câu hỏi được xử lý độc lập."
    );
    const form = element("form", "rag-form");
    const label = element("label", "", "Câu hỏi của bạn");
    label.htmlFor = "rag-question";
    const input = element("textarea", "rag-input");
    input.id = "rag-question";
    input.required = true;
    input.maxLength = 1000;
    input.rows = 3;
    input.placeholder = "Ví dụ: shared_buffers dùng để làm gì?";
    const submit = element("button", "rag-submit", "Gửi câu hỏi");
    submit.type = "submit";

    const status = element("p", "rag-status");
    status.setAttribute("role", "status");
    const answer = element("div", "rag-answer");
    const sources = element("ul", "rag-sources");
    sources.setAttribute("aria-label", "Nguồn tham khảo");
    form.append(label, input, submit);
    dialog.append(close, heading, help, form, status, answer, sources);
    document.body.append(launcher, dialog);

    launcher.addEventListener("click", () => {
      dialog.showModal();
      input.focus();
    });
    close.addEventListener("click", () => dialog.close());
    dialog.addEventListener("close", () => launcher.focus());

    let busy = false;
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (busy) return;
      const question = input.value.trim();
      if (!question) {
        status.textContent = "Bạn hãy nhập một câu hỏi.";
        input.focus();
        return;
      }

      busy = true;
      submit.disabled = true;
      input.disabled = true;
      answer.textContent = "";
      sources.replaceChildren();
      status.textContent = "Đang tìm tài liệu và tạo câu trả lời…";
      const controller = new AbortController();
      const timer = window.setTimeout(() => controller.abort(), 210000);

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question }),
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(`Backend trả HTTP ${response.status}. Hãy kiểm tra backend.`);
        }
        const data = await response.json();
        if (typeof data.answer !== "string" || !Array.isArray(data.sources)) {
          throw new Error("Response không đúng định dạng của phase 04.");
        }

        // Model output là văn bản, không được đưa thẳng vào innerHTML.
        answer.textContent = data.answer;
        for (const source of data.sources) {
          const url = new URL(source.url, siteRoot);
          if (url.origin !== siteRoot.origin ||
              !url.pathname.startsWith(siteRoot.pathname)) continue;
          const item = element("li", "");
          const link = element(
            "a", "", `[${source.id}] ${source.title} — ${source.heading}`
          );
          link.href = url.href;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          item.append(link);
          sources.append(item);
        }
        status.textContent = data.status === "answered"
          ? "Đã trả lời. Bạn có thể mở nguồn để đọc thêm."
          : "Chưa tạo được câu trả lời có đủ nguồn.";
      } catch (error) {
        status.textContent = error.name === "AbortError"
          ? "Chờ quá lâu. Model có thể đang bận; hãy thử lại sau."
          : `Không gửi được câu hỏi. ${error.message}`;
      } finally {
        window.clearTimeout(timer);
        busy = false;
        submit.disabled = false;
        input.disabled = false;
        if (dialog.open) input.focus();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountChat, { once: true });
  } else {
    mountChat();
  }
})();
```

Đoạn JS dùng `<dialog>` của trình duyệt để có focus trong hộp thoại và đóng bằng Escape. Nguồn được mở ở tab mới để bạn không mất câu trả lời hiện tại. Thời gian chờ phía trình duyệt không bảo đảm hủy được generation đang chạy trên backend.

Code dành cho cấu hình navigation hiện tại của repo. Nếu sau này bật instant navigation, kiểm tra lại vòng đời widget và chỉ đăng ký event một lần. Không có dữ liệu chat được lưu vào localStorage trong phase này.

## 3. Tạo `docs/stylesheets/chat.css`

```css
.rag-launcher {
  position: fixed;
  right: 1rem;
  bottom: 1rem;
  z-index: 100;
  padding: .8rem 1rem;
  border: 0;
  border-radius: 999px;
  background: #4338ca;
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 20px #0003;
}

.rag-dialog {
  width: min(38rem, calc(100vw - 2rem));
  max-height: 85vh;
  overflow-y: auto;
  padding: 1.25rem;
  border: 1px solid #d1d5db;
  border-radius: 1rem;
  background: #fff;
  color: #111827;
}

.rag-dialog::backdrop { background: #11182780; }
.rag-close { float: right; cursor: pointer; }
.rag-help, .rag-status { color: #4b5563; font-size: .85rem; }
.rag-form { display: grid; gap: .6rem; }
.rag-input {
  width: 100%;
  box-sizing: border-box;
  padding: .7rem;
  border: 1px solid #9ca3af;
  border-radius: .5rem;
  font: inherit;
  resize: vertical;
}
.rag-submit {
  justify-self: start;
  padding: .6rem 1rem;
  border-radius: .5rem;
  background: #4338ca;
  color: #fff;
  cursor: pointer;
}
.rag-submit:disabled { opacity: .6; cursor: wait; }
.rag-answer { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.7; }
.rag-sources { padding-left: 1.2rem; }
.rag-sources a { color: #4338ca; text-decoration: underline; }
.rag-dialog :focus-visible, .rag-launcher:focus-visible {
  outline: 3px solid #818cf8;
  outline-offset: 3px;
}
```

## 4. Đăng ký asset trong `mkdocs.yml`

Thêm `stylesheets/chat.css` vào danh sách `extra_css` **đang có**, và `javascripts/chat.js` vào `extra_javascript` **đang có**. Không tạo thêm khóa YAML trùng và không xóa các asset hiện tại:

```yaml
# Thêm một item vào extra_css:
- stylesheets/chat.css

# Thêm một item vào extra_javascript:
- javascripts/chat.js
```

Đây là hai item minh họa, không phải toàn bộ cấu hình để ghi đè `mkdocs.yml`. MkDocs sẽ tải JS/CSS trên các trang. [MkDocs extra_javascript](https://www.mkdocs.org/user-guide/configuration/#extra_javascript)

## 5. Chạy ba phần

Ollama chạy trên cổng 11434. Tại `backend`, khởi động API với chế độ bạn đã chọn:

```bash
RETRIEVAL_MODE=hybrid uv run uvicorn app:app --host 127.0.0.1 --port 8001
```

Nếu phase 05 cho thấy vector tốt hơn, đổi thành `RETRIEVAL_MODE=vector`. Trong terminal khác tại root repo:

```bash
uv run mkdocs serve --dev-addr 127.0.0.1:8000
```

Mở `http://127.0.0.1:8000`, bấm “Hỏi tài liệu” và gửi câu hỏi. Không cần ingest lại chỉ vì thêm widget: corpus vẫn là bốn bài allowlist và parser chỉ đọc vùng nội dung.

## 6. Kiểm tra tích hợp

| Thao tác | Kỳ vọng |
| --- | --- |
| Mở chat bằng bàn phím | Focus vào ô nhập, Escape đóng được |
| Gửi một câu hỏi | Nút gửi bị khóa trong lúc chờ, không gửi trùng |
| Hỏi `shared_buffers dùng để làm gì?` | Có câu trả lời cùng link nguồn phù hợp |
| Mở nguồn từ trang bài viết lồng nhiều cấp | URL vẫn đúng, không bị nối vào thư mục bài hiện tại |
| Hỏi ngoài phạm vi | Hiển thị trạng thái và câu từ chối nếu backend nhận biết đúng |
| Tắt backend | Hiển thị lỗi, nút gửi được mở lại |
| Để Ollama lỗi/timeout | Không treo UI vô thời hạn |
| Kiểm tra DevTools Network | Một POST mỗi lần gửi; có thể có OPTIONS preflight |
| Mở trên màn hình hẹp | Hộp thoại nằm trong viewport và cuộn được |

Tại root, kiểm tra build tài liệu mà không ghi đè `site/` đang có:

```bash
uv run mkdocs build --strict --site-dir /tmp/behind-the-pipeline-rag-preview
```

Nếu repo vốn có cảnh báo strict từ nội dung cũ, phân biệt với lỗi mới do JS/CSS hoặc cấu hình vừa thêm. Build thành công chỉ chứng minh site build được, không chứng minh endpoint/model đang hoạt động.

## 7. Khi đưa lên website thật

`127.0.0.1` trong JavaScript là máy của người đang mở trình duyệt. Khi public, đổi `endpoint` sang backend HTTPS của bạn, hoặc dùng reverse proxy cùng origin như `/api/chat`; đồng thời cập nhật CORS nếu khác origin.

Website tĩnh không tự chạy Python hoặc Ollama. Cần máy chạy backend + model, giữ chỉ mục cùng phiên bản với tài liệu đã xuất bản. Trước khi mở public, bổ sung giới hạn request và số lần generation đồng thời, timeout phía server và theo dõi tài nguyên. Không expose trực tiếp cổng Ollama cho trình duyệt; frontend chỉ gọi backend.

**Hoàn thành phase khi:** hỏi được trên website local, nguồn đến đúng mục, lỗi được xử lý rõ ràng và không thay đổi chất lượng retrieval đã đo ở phase 05.
