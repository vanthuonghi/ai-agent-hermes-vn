# Hướng dẫn Submit Sitemap vào Google Search Console (GSC)

Trang web: https://vanthuonghi.github.io/ai-agent-hermes-vn/
Sitemap:    https://vanthuonghi.github.io/ai-agent-hermes-vn/sitemap.xml

## Bước 1: Thêm property vào GSC
1. Vào https://search.google.com/search-console
2. Đăng nhập bằng Gmail của anh (vanthuonghi@gmail.com)
3. Chọn **"Thêm tài sản" (Add property)** → chọn **"URL prefix"**
4. Dán: `https://vanthuonghi.github.io/ai-agent-hermes-vn/`
5. Xác minh (verify) — GitHub Pages dùng HTTPS nên Google sẽ chọn 1 trong 2:
   - **Cách A (dễ nhất):** Google tìm thấy file HTML trong repo → nhưng mình không có quyền ghi file xác minh vào thư mục gốc nhanh → dùng Cách B.
   - **Cách B (khuyên dùng):** Chọn **"Google Analytics"** nếu anh đã liên kết, HOẶC
   - **Cách C (chắc chắn):** Tạo file `googleXXXX.html` Google cho → Hermes sẽ đặt vào repo root + push. Anh chỉ cần báo tôi tên file.

## Bước 2: Submit sitemap
1. Sau khi verify xong → menu trái chọn **"Sitemaps"**
2. Ô "Add a new sitemap" → dán: `sitemap.xml`
3. Nhấn **SUBMIT**
4. Google hiện trạng thái "Success" sau vài phút → bắt đầu index.

## Bước 3: Yêu cầu index nhanh (URL Inspection)
1. Menu trái → **"URL Inspection"**
2. Dán URL bài viết muốn index gấp (vd trang chủ)
3. Nhấn **"Request indexing"**
4. Làm với 3-4 URL quan trọng (trang chủ, blog, 2 bài đầu).

## Lưu ý
- GitHub Pages tự có HTTPS + CDN → Google thích, index nhanh.
- Có schema JSON-LD (Article/BlogPosting/FAQPage) → Google hiểu nội dung, dễ lên rich result.
- Chỉ cần làm Bước 1 + 2 một lần. Sau này anh viết bài mới, sitemap tự cập nhật, Google quét lại.

## Muốn Hermes tự động submit?
Hiện Hermes chưa có credential GSC (chỉ có Gemini key). Nếu anh:
- (A) Tạo **GSC API credential** (OAuth) → báo tôi, tôi script auto-submit mỗi khi có bài mới.
- (B) Dùng token có quyền GSC → tôi gọi API trực tiếp.
- (C) Cứ làm thủ công Bước 1-2 (1 lần duy nhất) → nhàn nhất.

---
*File này để anh tự làm 1 lần. Hermes đã chuẩn bị sẵn sitemap + schema chuẩn SEO.*
