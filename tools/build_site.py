"""Tek kaynaktan galeri, filtreler, site metinleri, kategori modülü ve schema seed'i üretir."""
import json
import pathlib
import re
from html import escape
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent

# slug -> (etiket, [(alt slug, alt etiket), ...])
CATEGORIES = [
    ("gumus", "Gümüş & Gümüş Kaplama", [
        ("tepsiler", "Tepsiler"),
        ("catal-bicak", "Çatal Bıçak & Kaşık"),
        ("gumus-diger", "Diğer Gümüş Parçalar"),
    ]),
    ("aydinlatma", "Şamdan & Mumluk", [
        ("samdanlar", "Şamdanlar"),
        ("mumluklar", "Mumluklar"),
    ]),
    ("porselen", "Porselen & Seramik", [
        ("servis-takimlari", "Servis Takımları"),
        ("tabaklar", "Tabaklar"),
        ("porselen-diger", "Diğer Porselen"),
    ]),
    ("cam", "Cam & Kristal", []),
    ("dekoratif", "Dekoratif Objeler", []),
]

# (görsel, başlık, açıklama, fiyat, satıldı, kategori, alt kategori)
PRODUCTS = [
    ("hero-mary-gregory.jpg", "Mary Gregory Sürahi ve Bardak Takımı",
     "Mavi cam üzerine beyaz emaye figür işlemeli, ağız ve kaide kenarları altın yaldızlı "
     "orijinal Mary Gregory takımı. Dönemin en sevilen cam işçiliklerinden.",
     None, False, "cam", None),
    ("gallery-mary-gregory-clear.jpg", "Mary Gregory Başucu Sürahisi",
     "Şeffaf cam üzerine el işçiliği beyaz emaye figürlü, bardağıyla birlikte gelen "
     "orijinal başucu sürahisi.", None, True, "cam", None),
    ("porselen-cay-servisi.jpg", "Porselen Çay Servisi",
     "Avrupa yapımı, kabartma desenli beyaz porselen çay ve kahve servisi. Demlik, "
     "şekerlik, sütlük ve fincanlarıyla eksiksiz takım.",
     11500, False, "porselen", "servis-takimlari"),
    ("wmf-gumus-kutu.jpg", "WMF Kapaklı Kutu",
     "Alman WMF imzalı, kabartma bordürlü ve ayaklı kapaklı kutu. Kapağındaki döküm "
     "tutamağıyla dikkat çeken, orijinal bir parça.", 10000, False, "gumus", "gumus-diger"),
    ("manzara-tabak-seti.jpg", "Manzara Desenli Tabak Seti",
     "İngiliz mavi-beyaz geleneğinde, şato ve kale gravürlü 4 parçalık tabak seti. "
     "Klasik transfer baskı tekniğiyle üretilmiş.", 6500, False, "porselen", "tabaklar"),
    ("porselen-fincan-takimi.jpg", "Porselen Fincan Takımı",
     "Melek kabartmalı gövde ve altın yaldız bordürlü Avrupa porseleni. Fincan, tabak "
     "ve pasta tabağından oluşan 3 parça takım.", 5500, False, "porselen", "servis-takimlari"),
    ("pirinc-zincirli-canta.jpg", "Zincir Askılı Vintage Çanta",
     "Kuş figürlü kapak detayı ve dilimli pirinç gövdesiyle, zincir askılı dekoratif "
     "vintage çanta.", 5500, False, "dekoratif", None),
    ("amber-kadeh.jpg", "Amber Cam Kadeh (6 Adet)",
     "Amber renkli, dilimli gövdeli ayaklı kadeh. Avrupa cam işçiliğinin sıcak tonlarını "
     "sofranıza taşıyan 6'lı set.", 4750, False, "cam", None),
    ("gumus-cikolata-potu.jpg", "Gümüş Çikolata Potu",
     "1868-1888 arası Paris yapımı, Paillard Frères damgalı 800 ayar gümüş çikolata potu. "
     "Kabartma çiçek bezemeleri ve ahşap sapıyla koleksiyonluk bir eser.",
     None, False, "gumus", "gumus-diger"),
    ("gumus-servis-tepsisi.jpg", "Christofle Malmaison Tepsi",
     "Fransız Christofle'nin ikonik Malmaison koleksiyonundan, inci bordürlü servis "
     "tepsisi. Markanın en çok aranan formlarından biri.", None, False, "gumus", "tepsiler"),
    ("christofle-catal-bicak-takimi.jpg", "Christofle Çatal Bıçak Takımı",
     "Christofle imzalı, gümüş kaplama çatal-bıçak takımı. Kepçe, servis çatalı ve pasta "
     "spatulası gibi servis parçalarıyla birlikte.", None, False, "gumus", "catal-bicak"),
    ("gumus-samdan-cift.jpg", "Gümüş Kaplama Şamdan (Çift)",
     "İnci bordürlü, uzun ve zarif formlu şamdan çifti. Avrupa sofra kültürünün klasik "
     "parçalarından.", None, False, "aydinlatma", "samdanlar"),
    ("mumluk-koleksiyonu.jpg", "Gümüş Kaplama Mumluk Koleksiyonu",
     "Farklı boy ve formlarda gümüş kaplama mumluklar. Bir kısmı çift, bir kısmı tekli "
     "olarak Avrupa'dan getirildi.", None, False, "aydinlatma", "mumluklar"),
    ("mumluk-grubu.jpg", "Şamdan ve Mumluk Grubu",
     "Yüksek şamdanlardan el mumluklarına uzanan, farklı dönem ve formlardan oluşan "
     "gümüş kaplama grup.", None, False, "aydinlatma", "mumluklar"),
    ("pirinc-gumus-mumluklar.jpg", "Pirinç ve Gümüş Mumluklar",
     "Pirinç ve gümüş kaplama mumluklardan oluşan karma grup; kimi çift, kimi tekli "
     "parçalar halinde.", None, False, "aydinlatma", "mumluklar"),
    ("pirinc-samdan.jpg", "Pirinç Şamdan (Çift)",
     "Kazıma yaprak desenli, geniş kaideli çift pirinç şamdan. Yıllanmış patinasıyla "
     "orijinal formunu koruyor.", None, False, "aydinlatma", "samdanlar"),
    ("oval-gumus-tepsi.jpg", "Oval Gümüş Kaplama Tepsi",
     "İnci bordürlü, ortası kabartma madalyon işlemeli oval servis tepsisi.",
     None, False, "gumus", "tepsiler"),
    ("kulplu-gumus-tepsi.jpg", "Kulplu Gümüş Kaplama Tepsi",
     "Kenarları kabartma yaprak işlemeli, kulplu servis tepsisi. Damgalı ve orijinal.",
     None, False, "gumus", "tepsiler"),
    ("tepsi-ve-cevizlik.jpg", "Tepsi, Cevizlik ve Kıracak",
     "Kulplu gümüş kaplama tepsi, kabartma kenarlı küçük kase ve ceviz kıracağından "
     "oluşan ikram grubu.", None, False, "gumus", "tepsiler"),
    ("cicek-desenli-tabaklar.jpg", "Çiçek Desenli Çerezlik Tabaklar",
     "Gül desenli Avrupa porseleni çerezlik tabaklar ve ajur işlemeli baharat kaşıkları. "
     "Kahve ve ikram sunumları için.", None, False, "porselen", "tabaklar"),
    ("mavi-beyaz-servis-tabaklari.jpg", "Mavi-Beyaz Servis Tabakları",
     "Manzara baskılı, kulplu dikdörtgen porselen servis tabakları. Klasik mavi-beyaz "
     "desenin en bilinen formlarından.", None, False, "porselen", "tabaklar"),
    ("gumus-cay-kasiklari.jpg", "Çay Kaşığı Takımı",
     "Klasik bordür desenli, gümüş kaplama çay kaşığı takımı. Günlük kullanıma da uygun, "
     "zarif bir Avrupa parçası.", None, False, "gumus", "catal-bicak"),
    ("gumus-cay-suzgeci.jpg", "Çay Süzgeci",
     "Altın yaldızlı haznesi ve kabartma işlemeli sapıyla bardak üstü çay süzgeci.",
     None, False, "gumus", "gumus-diger"),
    ("melek-figurlu-surahi.jpg", "Melek Figürlü Süt Sürahisi",
     "Mat gövde üzerine beyaz melek kabartmalı, jasper tarzı porselen süt sürahisi.",
     None, False, "porselen", "porselen-diger"),
    ("bira-masrapasi.jpg", "Kapaklı Bira Maşrapası",
     "Kobalt mavi zemin üzerine kabartma figürlü Alman seramik maşrapa. Kalaylı menteşeli "
     "kapağıyla orijinal.", None, False, "porselen", "porselen-diger"),
    ("gumus-pecetelik.jpg", "Çiçek Motifli Peçetelik",
     "Gümüş kaplama, çiçek motifli ajur işlemeli peçetelik.",
     None, True, "gumus", "gumus-diger"),
]

SETTINGS = {
    "about_short":
        "Home Antique Home, Avrupa'dan tek tek seçilerek getirilen antika ve koleksiyon "
        "parçalarını İstanbul'da sizlerle buluşturuyor. Gümüş, porselen ve cam eserlerin "
        "büyük bölümü orijinal dönem parçalarıdır.",
    "about_long_1":
        "Home Antique Home, İstanbul merkezli bir antika ve koleksiyon markasıdır. "
        "Koleksiyonumuzdaki parçaların büyük bölümü Avrupa'dan, tek tek seçilerek "
        "getirilmiştir: Fransız gümüş kaplamaları, Alman porselenleri, İngiliz mavi-beyaz "
        "tabakları ve dönemin cam işçiliği örnekleri.",
    "about_long_2":
        "Her parçanın orijinalliğine ve durumuna önem veriyoruz; ürünlerimizin çoğu imzalı "
        "ya da damgalı dönem eserleridir. Amacımız, geçmişin özenle işlenmiş eserlerini "
        "günümüz evlerine taşımak ve müşterilerimize güvenilir bir alışveriş deneyimi sunmaktır.",
    "showroom_text":
        "Avrupa'nın farklı ülkelerinden getirdiğimiz gümüş kaplama sofra takımları, "
        "porselen servisler, cam eserler ve dekoratif objeler vitrinimizde sizi bekliyor. "
        "Koleksiyon sürekli yenileniyor; yeni gelen parçaları Instagram hesabımızdan "
        "takip edebilirsiniz.",
}


WHATSAPP_NUMBER = "905557370933"

# Vitrin sayfasında öne çıkarılan parçalar (başlıkla eşleşir).
# Yönetim panelinden de her ürün için "Vitrinde göster" kutusu var.
FEATURED = [
    "Mary Gregory Sürahi ve Bardak Takımı",
    "Christofle Malmaison Tepsi",
    "Porselen Çay Servisi",
    "Gümüş Kaplama Şamdan (Çift)",
    "Christofle Çatal Bıçak Takımı",
]


def tl(price):
    return f"{price:,}".replace(",", ".") + " ₺"


def whatsapp_text(title, sold):
    if sold:
        return f"Merhaba! Sitenizdeki {title} satılmış görünüyor, benzer bir parçanız var mı?"
    return f"Merhaba! Sitenizdeki {title} ile ilgileniyorum."


def card(product, indent="            "):
    image, title, description, price, sold, cat, sub = product
    badge = '\n                <span class="badge-sold">Satıldı</span>' if sold else ""
    price_line = f'\n                <p class="item-price">{tl(price)}</p>' if price else ""
    sub_attr = f' data-subcategory="{sub}"' if sub else ""
    text = whatsapp_text(title, sold)
    label = "Benzerini Sor" if sold else "WhatsApp ile Sor"
    href = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}"
    lines = [
        f'<article class="item" data-category="{cat}"{sub_attr}>',
        '  <div class="item-img">',
        f'    <img src="assets/images/{image}" alt="{title}" loading="lazy" />{badge}',
        '  </div>',
        '  <div class="item-body">',
        f'    <h3>{title}</h3>',
        f'    <p>{description}</p>{price_line}',
        f'    <a class="btn btn-whatsapp" href="{href}" target="_blank" rel="noopener"',
        f'       data-wa-product data-wa-text="{escape(text, quote=True)}">{label}</a>',
        '  </div>',
        '</article>',
    ]
    return "\n".join(indent + line for line in lines)


def submenu_markup(indent="            "):
    """Menüdeki Galeri başlığının altına düşen kategori ve alt kategori listesi."""
    lines = ['<ul class="submenu">']
    for slug, label, subs in CATEGORIES:
        if not subs:
            lines.append(f'  <li><a href="galeri.html#{slug}">{escape(label)}</a></li>')
            continue
        lines.append("  <li>")
        lines.append(f'    <a href="galeri.html#{slug}">{escape(label)}</a>')
        lines.append('    <ul class="submenu-sub">')
        for sub_slug, sub_label in subs:
            lines.append(
                f'      <li><a href="galeri.html#{sub_slug}">{escape(sub_label)}</a></li>')
        lines.append("    </ul>")
        lines.append("  </li>")
    lines.append("</ul>")
    return "\n".join(indent + line for line in lines)


def write_nav():
    """Galeri bağlantısını, kategorileri taşıyan açılır menüye çevirir."""
    plain = '<li><a href="galeri.html">Galeri</a></li>'
    block = (
        '<li class="has-submenu">\n'
        '            <a href="galeri.html">Galeri</a>\n'
        '            <button type="button" class="submenu-toggle"\n'
        '                    aria-label="Galeri kategorileri" aria-expanded="false"></button>\n'
        + submenu_markup() + "\n"
        '          </li>'
    )
    pattern = re.compile(
        r'<li class="has-submenu">.*?</li>(?=\s*<li><a href="iletisim\.html")', re.DOTALL)
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        if plain in html:
            html = html.replace(plain, block)
        else:
            html, n = pattern.subn(lambda m: block, html)
            if not n:
                print(f"!! {path.name}: Galeri menüsü bulunamadı")
                continue
        path.write_text(html, encoding="utf-8")
    print("menüye kategori listesi yazıldı")


def featured_products():
    chosen = [p for p in PRODUCTS if p[1] in FEATURED]
    missing = set(FEATURED) - {p[1] for p in chosen}
    assert not missing, f"FEATURED içinde eşleşmeyen başlık: {missing}"
    return chosen


def counts():
    per = {"all": len(PRODUCTS)}
    for _, _, _, _, _, cat, sub in PRODUCTS:
        per[cat] = per.get(cat, 0) + 1
        if sub:
            per[sub] = per.get(sub, 0) + 1
    return per


def filter_markup(indent="          "):
    per = counts()
    lines = ['<ul class="filter-group">',
             f'  <li><a href="#tumu" data-filter="all" class="is-active">Tümü'
             f' <span>{per["all"]}</span></a></li>']
    for slug, label, subs in CATEGORIES:
        lines.append(f'  <li>')
        lines.append(f'    <a href="#{slug}" data-filter="{slug}">{label}'
                     f' <span>{per.get(slug, 0)}</span></a>')
        if subs:
            lines.append('    <ul>')
            for sub_slug, sub_label in subs:
                lines.append(f'      <li><a href="#{sub_slug}" data-filter="{sub_slug}">'
                             f'{sub_label} <span>{per.get(sub_slug, 0)}</span></a></li>')
            lines.append('    </ul>')
        lines.append('  </li>')
    lines.append('</ul>')
    return "\n".join(indent + line for line in lines)


def replace_block(path, start_marker, end_pattern, content):
    html = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(start_marker) + r".*?" + end_pattern, re.DOTALL)
    new_html, count = pattern.subn(
        lambda m: start_marker + "\n" + content + "\n" + m.group(1), html
    )
    assert count == 1, f"{path.name}: {count} eşleşme"
    path.write_text(new_html, encoding="utf-8")


def find_block(html, open_pattern):
    """Açılış etiketini bulur ve iç içe <div>'leri sayarak kapanışını döndürür."""
    match = re.search(open_pattern, html)
    assert match, f"açılış etiketi bulunamadı: {open_pattern}"
    depth, i = 1, match.end()
    for tag in re.finditer(r"<(/?)div\b", html[match.end():]):
        depth += -1 if tag.group(1) else 1
        if depth == 0:
            i = match.end() + tag.start()
            break
    else:
        raise AssertionError("kapanış </div> bulunamadı")
    return match.end(), i


def replace_grid(path, products, limit=None, indent="            "):
    html = path.read_text(encoding="utf-8")
    chosen = products[:limit] if limit else products
    cards = "\n".join(card(p, indent) for p in chosen)
    start, end = find_block(
        html, r'<div class="collection-grid" data-products[^>]*>')
    closing_indent = " " * (len(indent) - 2)
    path.write_text(
        html[:start] + "\n" + cards + "\n" + closing_indent + html[end:], encoding="utf-8")
    print(f"{path.name}: {len(chosen)} ürün")


def write_categories_module():
    path = ROOT / "js" / "categories.js"
    data = [{"slug": s, "label": l,
             "children": [{"slug": cs, "label": cl} for cs, cl in subs]}
            for s, l, subs in CATEGORIES]
    path.write_text(
        "// Bu dosya üretilmiştir — kategoriler tek yerden yönetilir.\n"
        "export const CATEGORIES = "
        + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8")
    print("js/categories.js yazıldı")


def update_settings_html():
    for path in ROOT.glob("*.html"):
        html = path.read_text(encoding="utf-8")
        changed = False
        for key, value in SETTINGS.items():
            pattern = re.compile(rf'(<p data-setting="{key}"[^>]*>)(.*?)(</p>)', re.DOTALL)
            html, count = pattern.subn(
                lambda m: f"{m.group(1)}\n            {value}\n          {m.group(3)}", html)
            changed = changed or count
        if changed:
            path.write_text(html, encoding="utf-8")


def sql_value(text):
    return "'" + text.replace("'", "''") + "'"


def write_seed():
    path = ROOT / "supabase" / "schema.sql"
    sql = path.read_text(encoding="utf-8")

    for key, value in SETTINGS.items():
        pattern = re.compile(rf"(\('{key}', ).*?(\),?\n)", re.DOTALL)
        sql, count = pattern.subn(lambda m: m.group(1) + sql_value(value) + m.group(2), sql)
        assert count == 1, f"schema.sql: {key} için {count} eşleşme"

    rows = [
        f"  ({sql_value(title)}, {sql_value(description)}, {price if price else 'null'}, "
        f"{sql_value('assets/images/' + image)}, {'true' if sold else 'false'}, "
        f"{sql_value(cat)}, {sql_value(sub) if sub else 'null'}, {order}, "
        f"{'true' if title in FEATURED else 'false'})"
        for order, (image, title, description, price, sold, cat, sub)
        in enumerate(PRODUCTS, start=1)
    ]
    block = (
        "insert into public.products "
        "(title, description, price, image_url, is_sold, category, subcategory, sort_order, "
        "is_featured) values\n"
        + ",\n".join(rows) + "\non conflict do nothing;\n"
    )
    pattern = re.compile(
        r"insert into public\.products \(title, description, price, image_url, is_sold,"
        r".*?on conflict do nothing;\n", re.DOTALL)
    sql, count = pattern.subn(block, sql)
    assert count == 1, f"schema.sql: ürün bloğu için {count} eşleşme"

    path.write_text(sql, encoding="utf-8")
    print(f"schema.sql: {len(PRODUCTS)} ürün")


replace_grid(ROOT / "galeri.html", PRODUCTS)
replace_grid(ROOT / "showroom.html", featured_products(), indent="          ")
replace_grid(ROOT / "index.html", PRODUCTS, limit=6, indent="          ")
update_settings_html()
write_nav()
write_categories_module()
write_seed()

# Filtre listesi galeri.html içine
galeri = ROOT / "galeri.html"
html = galeri.read_text(encoding="utf-8")
pattern = re.compile(
    r'(<nav class="filters-list" id="filtersList">).*?(</nav>)', re.DOTALL)
new_html, n = pattern.subn(
    lambda m: m.group(1) + "\n" + filter_markup() + "\n          " + m.group(2), html)
assert n == 1, f"galeri.html: filtre listesi için {n} eşleşme"
galeri.write_text(new_html, encoding="utf-8")
print("galeri.html: filtre listesi yazıldı")
