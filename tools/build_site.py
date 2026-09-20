"""Tek kaynaktan galeri, filtreler, site metinleri, kategori modülü ve schema seed'i üretir."""
import json
import pathlib
import re
from html import escape
from urllib.parse import quote

import i18n

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

# Ana sayfadaki kategori kartlarının kapak görselleri
CATEGORY_IMAGES = {
    "gumus": "gumus-cikolata-potu.jpg",
    "aydinlatma": "gumus-samdan-cift.jpg",
    "porselen": "porselen-cay-servisi.jpg",
    "cam": "amber-kadeh.jpg",
    "dekoratif": "pirinc-zincirli-canta.jpg",
}

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
    "sss_orijinallik":
        "Koleksiyonumuzdaki parçaların büyük bölümü Avrupa'dan tek tek seçilerek getirilen, "
        "dönemine ait orijinal eserlerdir. Bir parçanın üzerinde üretici imzası, damga ya da "
        "ayar işareti varsa bunu ürün açıklamasında belirtiyoruz. Kaynağından emin olmadığımız "
        "bir parça için \"orijinal\" ifadesini kullanmıyoruz.",
    "sss_odeme":
        "Site üzerinden ödeme alınmıyor. Siparişiniz WhatsApp üzerinden netleştikten sonra "
        "ödeme yöntemini birlikte belirliyoruz.",
    "sss_kargo":
        "Gönderimlerimizi Yurtiçi Kargo ile yapıyoruz; parçanız genellikle 2-3 gün içinde "
        "elinizde olur. Cam, porselen ve kristal gibi kırılabilir parçalar çift katmanlı ve "
        "dolgulu olarak özel paketlenir. İstanbul içinde elden teslim de mümkündür; "
        "ayrıntıları WhatsApp'tan konuşabiliriz.",
    "sss_iade":
        "Uzaktan yapılan satışlarda tüketici mevzuatının tanıdığı cayma hakkı geçerlidir. "
        "Parçayı teslim aldıktan sonra fikrinizi değiştirirseniz bizimle iletişime geçin; süreci "
        "birlikte yürütelim. Antika parçalarda yaşına bağlı kullanım izleri kusur sayılmaz, bu "
        "izleri ürün açıklamasında ve fotoğraflarda olabildiğince açık gösteriyoruz.",
    "sss_bakim":
        "Gümüş ve gümüş kaplama parçaları yumuşak bir bezle kuru olarak silin; aşındırıcı sünger "
        "ve bulaşık makinesi kaplamaya zarar verir. Kararmayı geciktirmek için havayla temasın "
        "azaldığı, kapalı bir yerde saklayın. Altın yaldızlı porselen ve cam eserleri ılık suda "
        "elde yıkayın; yaldız mikrodalgaya ve makineye dayanmaz. Kristal ve ince camı ani "
        "sıcaklık değişiminden koruyun.",
    "showroom_text":
        "Avrupa'nın farklı ülkelerinden getirdiğimiz gümüş kaplama sofra takımları, "
        "porselen servisler, cam eserler ve dekoratif objeler vitrinimizde sizi bekliyor. "
        "Koleksiyon sürekli yenileniyor; yeni gelen parçaları Instagram hesabımızdan "
        "takip edebilirsiniz.",
}


WHATSAPP_NUMBER = "905557370933"

# Üretim sırasında hangi dilde olduğumuzu tutar; her iki dil de aynı
# fonksiyonlardan geçer, yalnızca bu bağlam değişir.
LANG = None


def t(key):
    return LANG["ui"][key]


def page(tr_name):
    """Türkçe dosya adını geçerli dildeki karşılığına çevirir."""
    return LANG["pages"][tr_name]


def asset(path):
    """İngilizce sayfalar en/ altında olduğu için bir üst dizine çıkar."""
    return LANG["prefix"] + path


def label(slug, turkish):
    return turkish if LANG["code"] == "tr" else i18n.CATEGORY_LABELS_EN[slug]


def product_text(title, description):
    return (title, description) if LANG["code"] == "tr" else i18n.PRODUCTS_EN[title]

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
    return t("wa_similar" if sold else "wa_interested").format(title=title)


def card(product, indent="            "):
    image, tr_title, tr_description, price, sold, cat, sub = product
    title, description = product_text(tr_title, tr_description)
    badge = (f'\n                <span class="badge-sold">{t("sold")}</span>'
             if sold else "")
    price_line = f'\n                <p class="item-price">{tl(price)}</p>' if price else ""
    sub_attr = f' data-subcategory="{sub}"' if sub else ""
    text = whatsapp_text(title, sold)
    button = t("ask_similar") if sold else t("ask")
    href = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}"
    lines = [
        f'<article class="item" data-category="{cat}"{sub_attr}>',
        '  <div class="item-img">',
        f'    <img src="{asset("assets/images/")}{image}" alt="{title}" loading="lazy" />{badge}',
        '  </div>',
        '  <div class="item-body">',
        f'    <h3>{title}</h3>',
        f'    <p>{description}</p>{price_line}',
        f'    <a class="btn btn-whatsapp" href="{href}" target="_blank" rel="noopener"',
        f'       data-wa-product data-wa-text="{escape(text, quote=True)}">{button}</a>',
        '  </div>',
        '</article>',
    ]
    return "\n".join(indent + line for line in lines)


def submenu_markup(indent="            "):
    """Menüdeki Galeri başlığının altına düşen kategori ve alt kategori listesi."""
    gallery = page("galeri.html")
    lines = ['<ul class="submenu">']
    for slug, tr_label, subs in CATEGORIES:
        text = escape(label(slug, tr_label))
        if not subs:
            lines.append(f'  <li><a href="{gallery}#{slug}">{text}</a></li>')
            continue
        lines.append("  <li>")
        lines.append(f'    <a href="{gallery}#{slug}">{text}</a>')
        lines.append('    <ul class="submenu-sub">')
        for sub_slug, sub_tr in subs:
            sub_text = escape(label(sub_slug, sub_tr))
            lines.append(
                f'      <li><a href="{gallery}#{sub_slug}">{sub_text}</a></li>')
        lines.append("    </ul>")
        lines.append("  </li>")
    lines.append("</ul>")
    return "\n".join(indent + line for line in lines)


def write_category_cards():
    """Ana sayfadaki kategori kartları — parça sayıları sayımdan gelir."""
    path = LANG["dir"] / "index.html"
    html = path.read_text(encoding="utf-8")
    per = counts()
    gallery = page("galeri.html")
    cards = []
    for slug, tr_label, _ in CATEGORIES:
        text = escape(label(slug, tr_label))
        sayı = t("pieces").format(n=per.get(slug, 0))
        cards.append(
            f'          <a class="category-card" href="{gallery}#{slug}">\n'
            f'            <span class="category-card-img">\n'
            f'              <img src="{asset("assets/images/")}{CATEGORY_IMAGES[slug]}"'
            f' alt="{text}" loading="lazy" />\n'
            f'            </span>\n'
            f'            <span class="category-card-label">{text}'
            f'<em>{sayı}</em></span>\n'
            f'          </a>')
    start, end = find_block(html, r'<div class="category-grid">')
    path.write_text(
        html[:start] + "\n" + "\n".join(cards) + "\n        " + html[end:],
        encoding="utf-8")
    print(f"index.html: {len(cards)} kategori kartı")


def write_footer():
    """Alt bilgi tüm sayfalarda aynı; kategoriler ve bağlantılar dile göre gelir."""
    gallery = page("galeri.html")
    kategoriler = "\n".join(
        f'            <li><a href="{gallery}#{slug}">{escape(label(slug, tr))}</a></li>'
        for slug, tr, _ in CATEGORIES)
    nav = LANG["ui"]["nav"]
    footer = f"""  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col">
        <h3>{t("footer_company")}</h3>
        <ul>
          <li><a href="{page("hakkimizda.html")}">{nav[page("hakkimizda.html")]}</a></li>
          <li><a href="{page("showroom.html")}">{nav[page("showroom.html")]}</a></li>
          <li><a href="{page("sss.html")}">{nav[page("sss.html")]}</a></li>
          <li><a href="{page("iletisim.html")}">{nav[page("iletisim.html")]}</a></li>
        </ul>
      </div>

      <div class="footer-col">
        <h3>{t("footer_collection")}</h3>
        <ul>
          <li><a href="{gallery}">{t("footer_all")}</a></li>
{kategoriler}
        </ul>
      </div>

      <div class="footer-col">
        <h3>{t("footer_contact")}</h3>
        <p class="footer-contact">
          <span data-setting="address">Bağdat Caddesi, İstanbul</span><br />
          <a href="tel:+905557370933" data-setting="phone" data-setting-href="tel">0555 737 09 33</a><br />
          <a href="mailto:homeantiquehome@gmail.com" data-setting="email" data-setting-href="email">homeantiquehome@gmail.com</a>
        </p>
        <div class="footer-links">
          <a href="https://wa.me/{WHATSAPP_NUMBER}" target="_blank" rel="noopener" class="footer-social" data-setting-href="whatsapp">WhatsApp</a>
          <a href="https://www.instagram.com/homeantiquehome" target="_blank" rel="noopener" class="footer-social" data-setting-href="instagram">Instagram</a>
        </div>
      </div>
    </div>

    <div class="container footer-bottom">
      <p>&copy; <span class="year"></span> Home Antique Home — {t("rights")}</p>
      <a href="{page("gizlilik.html")}">{nav[page("gizlilik.html")]}</a>
    </div>
  </footer>"""

    for path in sorted(LANG["dir"].glob("*.html")):
        html = path.read_text(encoding="utf-8")
        start = html.index('  <footer class="site-footer">')
        end = html.index("</footer>") + len("</footer>")
        path.write_text(html[:start] + footer + html[end:], encoding="utf-8")
    print(f'[{LANG["code"]}] alt bilgi yazıldı')


def nav_list(other_href):
    """Menü öğeleri; Galeri açılır listeyi, son öğe dil değiştiriciyi taşır."""
    nav = LANG["ui"]["nav"]
    items = []
    for tr_name, _, in_menu in i18n.PAGES:
        if not in_menu:
            continue
        name = page(tr_name)
        if tr_name == "galeri.html":
            items.append(
                '          <li class="has-submenu">\n'
                f'            <a href="{name}">{nav[name]}</a>\n'
                '            <button type="button" class="submenu-toggle"\n'
                f'                    aria-label="{t("submenu_label")}"'
                ' aria-expanded="false"></button>\n'
                + submenu_markup() + '\n'
                '          </li>')
        else:
            items.append(f'          <li><a href="{name}">{nav[name]}</a></li>')

    items.append(
        '          <li class="nav-social">\n'
        '            <a href="https://www.instagram.com/homeantiquehome" target="_blank"\n'
        '               rel="noopener" data-setting-href="instagram"\n'
        f'               aria-label="{t("instagram_label")}"><span>Instagram</span></a>\n'
        '          </li>')
    items.append(
        '          <li class="nav-lang">\n'
        f'            <a href="{other_href}" aria-label="{t("lang_label")}">\n'
        f'              <span class="lang-short">{t("other_lang_short")}</span>\n'
        f'              <span class="lang-long">{t("other_lang")}</span>\n'
        '            </a>\n'
        '          </li>')
    return "\n".join(items)


def write_alternates():
    """İki dilin aynı sayfası olduğunu arama motorlarına bildirir;
    aksi hâlde birbirinin kopyası sayılabilirler."""
    for tr_name, en_name, _ in i18n.PAGES:
        path = LANG["dir"] / page(tr_name)
        html = path.read_text(encoding="utf-8")
        tr_href = tr_name if LANG["code"] == "tr" else f"../{tr_name}"
        en_href = f"en/{en_name}" if LANG["code"] == "tr" else en_name
        tags = (f'  <link rel="alternate" hreflang="tr" href="{tr_href}" />\n'
                f'  <link rel="alternate" hreflang="en" href="{en_href}" />\n')
        html = re.sub(r'  <link rel="alternate" hreflang="[a-z]{2}" href="[^"]*" />\n', "", html)
        html = re.sub(r'(<meta name="description"[^>]*/>\n)', lambda m: m.group(1) + tags,
                      html, count=1)
        path.write_text(html, encoding="utf-8")
    print(f'[{LANG["code"]}] dil eşleri bildirildi')


def write_nav():
    """Menüyü, aramayı ve dil değiştiriciyi her sayfaya yazar."""
    search_form = (
        f'      <form class="header-search" action="{page("galeri.html")}" role="search">\n'
        f'        <input type="search" name="q" placeholder="{t("search_placeholder")}"\n'
        f'               aria-label="{t("search_label")}" />\n'
        f'        <button type="submit" aria-label="{t("search_button")}"></button>\n'
        '      </form>')

    for tr_name, en_name, _ in i18n.PAGES:
        path = LANG["dir"] / page(tr_name)
        html = path.read_text(encoding="utf-8")

        other = f"en/{en_name}" if LANG["code"] == "tr" else f"../{tr_name}"
        start, end = find_block(html, r'<ul class="nav-list">', "ul")
        html = (html[:start] + "\n" + nav_list(other) + "\n        " + html[end:])

        # Varsa değiştir, yoksa ekle — böylece ingilizce sayfada türkçe
        # yer tutucu metni kalmaz.
        if 'class="header-search"' in html:
            html = re.sub(r'      <form class="header-search".*?</form>',
                          lambda m: search_form, html, count=1, flags=re.DOTALL)
        else:
            html = html.replace(
                '      <button class="nav-toggle" id="navToggle"',
                search_form + '\n\n      <button class="nav-toggle" id="navToggle"', 1)

        path.write_text(html, encoding="utf-8")
    print(f'[{LANG["code"]}] menü, arama ve dil değiştirici yazıldı')


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
             f'  <li><a href="#tumu" data-filter="all" class="is-active">{t("all")}'
             f' <span>{per["all"]}</span></a></li>']
    for slug, tr_label, subs in CATEGORIES:
        lines.append(f'  <li>')
        lines.append(f'    <a href="#{slug}" data-filter="{slug}">{label(slug, tr_label)}'
                     f' <span>{per.get(slug, 0)}</span></a>')
        if subs:
            lines.append('    <ul>')
            for sub_slug, sub_tr in subs:
                lines.append(f'      <li><a href="#{sub_slug}" data-filter="{sub_slug}">'
                             f'{label(sub_slug, sub_tr)} <span>{per.get(sub_slug, 0)}</span>'
                             f'</a></li>')
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


def find_block(html, open_pattern, tag_name="div"):
    """Açılış etiketini bulur ve iç içe etiketleri sayarak kapanışını döndürür."""
    match = re.search(open_pattern, html)
    assert match, f"açılış etiketi bulunamadı: {open_pattern}"
    depth, i = 1, match.end()
    for tag in re.finditer(rf"<(/?){tag_name}\b", html[match.end():]):
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
    texts = SETTINGS if LANG["code"] == "tr" else i18n.SETTINGS_EN
    for path in LANG["dir"].glob("*.html"):
        html = path.read_text(encoding="utf-8")
        changed = False
        for key, value in texts.items():
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

    rows = []
    for order, (image, title, description, price, sold, cat, sub) in enumerate(
            PRODUCTS, start=1):
        title_en, description_en = i18n.PRODUCTS_EN[title]
        rows.append(
            f"  ({sql_value(title)}, {sql_value(description)}, {price if price else 'null'}, "
            f"{sql_value('assets/images/' + image)}, {'true' if sold else 'false'}, "
            f"{sql_value(cat)}, {sql_value(sub) if sub else 'null'}, {order}, "
            f"{'true' if title in FEATURED else 'false'}, "
            f"{sql_value(title_en)}, {sql_value(description_en)})")
    block = (
        "insert into public.products "
        "(title, description, price, image_url, is_sold, category, subcategory, sort_order, "
        "is_featured, title_en, description_en) values\n"
        + ",\n".join(rows) + "\non conflict do nothing;\n"
    )
    pattern = re.compile(
        r"insert into public\.products \(title, description, price, image_url, is_sold,"
        r".*?on conflict do nothing;\n", re.DOTALL)
    sql, count = pattern.subn(block, sql)
    assert count == 1, f"schema.sql: ürün bloğu için {count} eşleşme"

    path.write_text(sql, encoding="utf-8")
    print(f"schema.sql: {len(PRODUCTS)} ürün")


def sync_en_skeletons():
    """İngilizce sayfaları her derlemede türkçelerinden yeniden üretir.
    Böylece türkçe bir sayfa değişince ingilizcesi geride kalmaz."""
    out = ROOT / "en"
    out.mkdir(exist_ok=True)
    used = set()

    for tr_name, en_name, _ in i18n.PAGES:
        html = (ROOT / tr_name).read_text(encoding="utf-8")
        html = html.replace('<html lang="tr"', '<html lang="en"', 1)

        title, desc = i18n.HEAD_EN[tr_name]
        html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1)
        html = re.sub(r'<meta name="description" content="[^"]*" />',
                      f'<meta name="description" content="{desc}" />', html, count=1)

        # Sayfa bağlantıları ingilizce dosya adlarına
        for other_tr, other_en, _ in i18n.PAGES:
            if other_tr != other_en:
                html = html.replace(f'href="{other_tr}', f'href="{other_en}')

        # en/ bir alt dizin olduğu için varlık yolları bir üste çıkar
        html = re.sub(r'(href|src)="(css/|js/|assets/)', r'\1="../\2', html)
        html = html.replace("url('assets/", "url('../assets/")

        if tr_name in i18n.MAIN_EN:
            start = html.index("  <main>")
            end = html.index("  </main>") + len("  </main>")
            html = html[:start] + i18n.MAIN_EN[tr_name] + html[end:]

        for tr_text, en_text in i18n.STATIC_EN.items():
            if tr_text in html:
                html = html.replace(tr_text, en_text)
                used.add(tr_text)

        (out / en_name).write_text(html, encoding="utf-8")

    unused = set(i18n.STATIC_EN) - used
    assert not unused, f"türkçe sayfalarda bulunamayan çeviri: {sorted(unused)[:3]}"
    print(f"en/: {len(i18n.PAGES)} sayfa türkçeden üretildi")


LANGS = {
    "tr": {"code": "tr", "dir": ROOT, "prefix": "",
           "pages": {tr: tr for tr, _, _ in i18n.PAGES}, "ui": i18n.UI["tr"]},
    "en": {"code": "en", "dir": ROOT / "en", "prefix": "../",
           "pages": {tr: en for tr, en, _ in i18n.PAGES}, "ui": i18n.UI["en"]},
}

sync_en_skeletons()

for _code in ("tr", "en"):
    LANG = LANGS[_code]
    LANG["dir"].mkdir(exist_ok=True)

    replace_grid(LANG["dir"] / page("galeri.html"), PRODUCTS)
    replace_grid(LANG["dir"] / page("showroom.html"), featured_products(),
                 indent="          ")
    replace_grid(LANG["dir"] / page("index.html"), PRODUCTS, limit=6, indent="          ")
    update_settings_html()
    write_nav()
    write_alternates()
    write_footer()
    write_category_cards()

    # Filtre listesi galeri sayfasına
    _gal = LANG["dir"] / page("galeri.html")
    _html = _gal.read_text(encoding="utf-8")
    _pattern = re.compile(
        r'(<nav class="filters-list" id="filtersList">).*?(</nav>)', re.DOTALL)
    _html, _n = _pattern.subn(
        lambda m: m.group(1) + "\n" + filter_markup() + "\n          " + m.group(2), _html)
    assert _n == 1, f"{_gal.name}: filtre listesi için {_n} eşleşme"
    _gal.write_text(_html, encoding="utf-8")
    print(f'[{_code}] filtre listesi yazıldı')

# Yönetim paneli yalnızca Türkçe
LANG = LANGS["tr"]
write_categories_module()
write_seed()
