# -*- coding: utf-8 -*-
"""Rebuild blog/index.html AND index.html (homepage) post lists from all <slug>.html posts.
Single source of truth = post files in repo root. Removes deleted posts, adds new ones."""
import os, re
BASE="/Users/vanhi/ai-agent-hermes-vn"
SITE="https://vanthuonghi.github.io/ai-agent-hermes-vn"

def collect_posts():
    posts=[]
    for fn in sorted(os.listdir(BASE)):
        if fn.endswith(".html") and fn not in ("index.html","blog-template.html") and fn!="google806c304e629f0445.html":
            t=open(os.path.join(BASE,fn),encoding="utf-8").read()
            mt=re.search(r'<title>([^<]*)</title>',t)
            me=re.search(r'<p class="lead">([^<]*)</p>',t) or re.search(r'<p class="ex">([^<]*)</p>',t)
            mi=re.search(r'assets/img/([\w-]+\.png)',t)
            mc=re.search(r'<p class="meta">([^·]*?)·',t)
            md=re.search(r'<p class="meta">[^·]*·\s*([\d/]+)',t)
            if mt and me:
                posts.append({"slug":fn[:-5],"title":mt.group(1),"ex":me.group(1),
                    "img":mi.group(1) if mi else "cover.png",
                    "cat":(mc.group(1).strip() if mc else "Blog"),
                    "date":(md.group(1) if md else "27/07/2026")})
    return posts

def card_html(p, prefix=""):
    return f'''<div class="post"><div class="thumb"><img src="{SITE}/assets/img/{p['img']}" alt="{p['slug']}" style="width:120px;height:90px;border-radius:10px;object-fit:cover"></div><div class="body">
<span class="cat">{p['cat']}</span>
<h3><a href="{prefix}{p['slug']}.html" style="color:var(--ink);text-decoration:none">{p['title']}</a></h3>
<p class="ex">{p['ex']}</p>
<span class="meta">{p['date']}</span></div></div>
'''

def rebuild_blog(posts):
    bp=os.path.join(BASE,"blog","index.html")
    b=open(bp,encoding="utf-8").read()
    cards="".join(card_html(p,"../") for p in posts)
    # Replace everything from first <div class="post"> up to the closing </div> before <footer>
    # Keep header (split at first post card), then insert all cards, then footer
    head=b.split('<div class="post">',1)[0]
    foot=b.split('</footer>',1)[1] if '</footer>' in b else ''
    # ensure head ends with newline before cards
    new_b=head.rstrip()+"\n"+cards+"\n</div>\n<footer>"+foot
    open(bp,"w",encoding="utf-8").write(new_b)
    return len(posts)

def rebuild_home(posts):
    """Update homepage: replace the hardcoded 3-post list with all posts (latest first, max 6)."""
    hp=os.path.join(BASE,"index.html")
    h=open(hp,encoding="utf-8").read()
    # find a marker section for blog posts on homepage
    # We use a placeholder comment <!--BLOG_POSTS--> ... <!--/BLOG_POSTS-->
    if "<!--BLOG_POSTS-->" not in h:
        # insert before footer CTA / or before closing of wrap
        h=h.replace('</div>\n<footer>', '<!--BLOG_POSTS-->\n</div>\n<footer>',1)
    latest=posts[::-1][:6]
    cards="".join(card_html(p,"") for p in latest)
    h=re.sub(r'<!--BLOG_POSTS-->.*?<!--/BLOG_POSTS-->',
             '<!--BLOG_POSTS-->\n'+cards+'<!--/BLOG_POSTS-->', h, flags=re.S)
    if '<!--/BLOG_POSTS-->' not in h:
        h=h.replace('<!--BLOG_POSTS-->', '<!--BLOG_POSTS-->\n'+cards+'<!--/BLOG_POSTS-->')
    open(hp,"w",encoding="utf-8").write(h)
    return len(latest)

if __name__=="__main__":
    posts=collect_posts()
    print("found posts:",len(posts))
    n1=rebuild_blog(posts)
    n2=rebuild_home(posts)
    print(f"✅ blog index: {n1} cards | homepage: {n2} latest cards")
