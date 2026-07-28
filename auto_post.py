# -*- coding: utf-8 -*-
"""Auto blog poster — chuẩn bài 'Hermes tự động hóa CSKH spa'.
Chạy mỗi 8h sáng VN. Ưu tiên lấy chủ đề từ file research sáng 7h30
(~/Desktop/Nới Rộng Hiểu Biết AI/YYYY-MM-DD.html), fallback vào queue cũ.
Viết bài theo template chuẩn, rebuild blog index, commit+push."""
import os, re, json, subprocess, datetime, sys, html

BASE = "/Users/vanhi/ai-agent-hermes-vn"
sys.path.insert(0, BASE)
import rebuild_all
from rebuild_all import collect_posts
SITE = "https://vanthuonghi.github.io/ai-agent-hermes-vn"
QUEUE = os.path.join(BASE, "blog_queue.json")
ASSETS = os.path.join(BASE, "assets", "img")
RESEARCH_DIR = "/Users/vanhi/Desktop/Nới Rộng Hiểu Biết AI"
TPL = open(os.path.join(BASE, "blog-template.html"), encoding="utf-8").read()

def slugify(s):
    s = re.sub(r'[^\w\s-]', '', s.lower()).strip().replace(' ', '-')
    return s[:50] or "bai-moi"

def load_topics_from_research():
    """Đọc file research sáng nay, trích tiêu đề các tin → chủ đề blog."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    fp = os.path.join(RESEARCH_DIR, f"{today}.html")
    if not os.path.exists(fp):
        return []
    t = open(fp, encoding="utf-8").read()
    # tiêu đề nằm trong <h3><a ...>Tiêu đề</a></h3> hoặc <h3>Tiêu đề</h3>
    titles = re.findall(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>.*?</h3>', t, re.S)
    if not titles:
        titles = re.findall(r'<h3>(.*?)</h3>', t, re.S)
    topics = []
    for ti in titles:
        ti = re.sub(r'<[^>]+>', '', ti).strip()
        ti = html.unescape(ti)
        if not ti or len(ti) < 10:
            continue
        slug = slugify(ti)
        # tránh trùng slug đã có
        if os.path.exists(os.path.join(BASE, f"{slug}.html")):
            slug = slug + "-" + today[-2:]
        topics.append({
            "slug": slug,
            "cat": "AI Trend",
            "img": "ai-agent-la-gi.png",
            "title": ti,
            "ex": f"Tổng hợp từ tin AI ngày {today}: {ti}. Hermes chọn lọc để anh và chủ DN cùng học.",
            "intro": f"Hôm nay ({today}) có một thông tin đáng chú ý trong thế giới AI: {ti}. Dưới đây là góc nhìn thực tế cho chủ DN Việt.",
        })
    return topics

def load_queue():
    """Fallback: nếu không có research, dùng queue cũ."""
    if not os.path.exists(QUEUE):
        return []
    return json.load(open(QUEUE))

def save_queue(q):
    json.dump(q, open(QUEUE, "w"), ensure_ascii=False, indent=2)

def gen_body(topic):
    """Build body following CSKH spa structure:
    hook intro -> 5-6 H2 days/sections -> evidence box with numbers -> table before/after -> note -> FAQ."""
    slug, cat, title, ex, intro = topic["slug"], topic["cat"], topic["title"], topic["ex"], topic["intro"]
    body = f'''
<h2>Thông tin là gì</h2>
<p>{ex} Đây là tin được Hermes tổng hợp từ research sáng nay, chọn lọc vì liên quan trực tiếp đến chủ DN Việt.</p>

<h2>Tại sao chủ DN nên quan tâm</h2>
<p>AI không còn là chuyện xa xỉ. Mỗi cập nhật mô hình, mỗi công cụ agent mới ra đời đều là cơ hội để chủ spa, shop, BĐS, trung tâm đào tạo tiết kiệm thời gian và chi phí. Bỏ qua xu hướng nghĩa là tụt lại so với đối thủ biết dùng.</p>

<h2>Áp dụng thực tế thế nào</h2>
<p>Không cần đợi công nghệ hoàn thiện. Chủ DN có thể bắt đầu bằng Hermes — agent chạy trên máy, miễn phí, giao việc bằng tiếng Việt. Tin trên là minh chứng thêm: AI đang rẻ đi và dễ tiếp cận hơn mỗi ngày.</p>

<div class="evidence"><b>Góc nhìn thực tế:</b>
<ul>
<li>Tin được chọn từ research sáng {datetime.date.today().strftime('%d/%m/%Y')}</li>
<li>Không cần biết code để áp dụng AI vào vận hành</li>
<li>Hermes miễn phí, chạy local, data an toàn</li>
</ul></div>

<h2>So sánh: biết vs không biết</h2>
<table><tr><th></th><th>Chủ DN không cập nhật</th><th>Chủ DN theo kịp trend</th></tr>
<tr><td>Công cụ</td><td>Làm tay, thuê người</td><td>Dùng agent tự động</td></tr>
<tr><td>Chi phí</td><td>5-10 triệu/tháng</td><td>0 (Hermes miễn phí)</td></tr>
<tr><td>Tốc độ</td><td>Chậm, hay quên</td><td>Nhanh, 24/7</td></tr></table>

<h2>Lưu ý cho chủ DN</h2>
<p>Hermes làm được vì chạy trên máy bạn, kết nối được tài khoản. Nhưng cần thiết lập đúng quyền, và bạn vẫn duyệt nội dung nhạy cảm. Tự động hóa không thay thế sự chăm sóc thật — nó gánh phần lặp lại để bạn có thời gian cho khách.</p>
'''
    return body

def gen_faq(topic):
    title = topic["title"]
    faq_html = f'''<div class="faq"><h3>Dùng Hermes có tốn tiền không?</h3><p>Hermes bản cơ bản miễn phí, chạy trên máy bạn. Tạo ảnh qua FAL cũng có free tier, không hết token chat.</p>
<h3>Chủ DN không biết code thì dùng sao?</h3><p>Giao việc bằng tiếng Việt như nhắn người thật. Không cần viết 1 dòng code.</p>
<h3>Có an toàn cho data khách không?</h3><p>Hermes chạy local trên máy chủ, thiết lập quyền vừa đủ là an toàn.</p>
<h3>Bắt đầu từ đâu?</h3><p>Một việc nhỏ: "{topic['ex'][:40]}...". Thấy nó làm được, mới giao việc lớn hơn.</p></div>'''
    faq_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage",
"mainEntity":[
{"@type":"Question","name":"Dùng Hermes có tốn tiền không?","acceptedAnswer":{"@type":"Answer","text":"Hermes bản cơ bản miễn phí, chạy trên máy bạn. Tạo ảnh qua FAL có free tier, không hết token chat."}},
{"@type":"Question","name":"Chủ DN không biết code thì dùng sao?","acceptedAnswer":{"@type":"Answer","text":"Giao việc bằng tiếng Việt như nhắn người thật, không cần code."}},
{"@type":"Question","name":"Có an toàn cho data khách không?","acceptedAnswer":{"@type":"Answer","text":"Hermes chạy local trên máy chủ, thiết lập quyền vừa đủ là an toàn."}}
]}
</script>'''
    return faq_html, faq_schema


def main():
    # Ưu tiên 1: chủ đề từ file research sáng 7h30
    topics = load_topics_from_research()
    # Ưu tiên 2: fallback queue cũ nếu research trống
    if not topics:
        q = load_queue()
        if not q:
            print("No research file and queue empty — nothing to post today."); return
        topics = [q.pop(0)]
        save_queue(q)
        qleft = len(q)
    else:
        qleft = len(topics)
    topic = topics[0]
    slug, cat, title, ex, intro = topic["slug"], topic["cat"], topic["title"], topic["ex"], topic["intro"]
    date = datetime.date.today().isoformat()
    date_human = datetime.date.today().strftime("%d/%m/%Y")
    metadesc = ex[:155]
    body = gen_body(topic)
    faq_html, faq_schema = gen_faq(topic)
    page = (TPL
        .replace("__TITLE__", title).replace("__METADESC__", metadesc)
        .replace("__SLUG__", slug).replace("__DATE__", date)
        .replace("__DATE_HUMAN__", date_human).replace("__CATEGORY__", cat)
        .replace("__READTIME__", "7").replace("__INTRO__", intro)
        .replace("__QUOTE__", "Chatbot nói cho bạn cách làm. AI Agent làm luôn cho bạn.")
        .replace("__BODY__", body).replace("__FAQ_HTML__", faq_html)
        .replace("__FAQ_SCHEMA__", faq_schema))
    open(os.path.join(BASE, f"{slug}.html"),"w",encoding="utf-8").write(page)
    # hero image
    img = topic.get("img","cover.png")
    if os.path.exists(os.path.join(ASSETS, img)):
        page = page.replace('</h1>', f'</h1>\n<img src="{SITE}/assets/img/{img}" alt="{slug}" style="width:100%;max-width:680px;border-radius:14px;margin:20px 0" loading="lazy">')
        open(os.path.join(BASE, f"{slug}.html"),"w",encoding="utf-8").write(page)
    n = rebuild_all.rebuild_blog(collect_posts())
    # sitemap
    sm = open(os.path.join(BASE,"sitemap.xml"),encoding="utf-8").read()
    if slug not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>{SITE}/{slug}.html</loc><lastmod>{date}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>')
        open(os.path.join(BASE,"sitemap.xml"),"w",encoding="utf-8").write(sm)
    # commit + push
    subprocess.run(["git","-C",BASE,"add","-A"], check=True)
    subprocess.run(["git","-C",BASE,"commit","-q","-m",f"auto: blog {slug}"], check=True)
    subprocess.run(["git","-C",BASE,"push","origin","main"], check=True)
    src = "research" if len(load_topics_from_research())>0 else "queue"
    print(f"✅ Posted: {slug} | source: {src} | blog now has {n} posts")

if __name__ == "__main__":
    main()
