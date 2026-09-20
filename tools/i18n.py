"""İngilizce karşılıklar. Türkçe metinler build_site.py içinde durur."""

# Sayfa dosya adları: (türkçe dosya, ingilizce dosya, menüde mi)
PAGES = [
    ("index.html", "index.html", True),
    ("hakkimizda.html", "about.html", True),
    ("showroom.html", "showroom.html", True),
    ("galeri.html", "gallery.html", True),
    ("iletisim.html", "contact.html", True),
    ("sss.html", "faq.html", False),
    ("gizlilik.html", "privacy.html", False),
]

# Ana ve alt kategori etiketleri (slug -> ingilizce)
CATEGORY_LABELS_EN = {
    "gumus": "Silver & Silver Plate",
    "tepsiler": "Trays",
    "catal-bicak": "Cutlery & Spoons",
    "gumus-diger": "Other Silver Pieces",
    "aydinlatma": "Candlesticks & Candle Holders",
    "samdanlar": "Candlesticks",
    "mumluklar": "Candle Holders",
    "porselen": "Porcelain & Ceramics",
    "servis-takimlari": "Service Sets",
    "tabaklar": "Plates",
    "porselen-diger": "Other Porcelain",
    "cam": "Glass & Crystal",
    "dekoratif": "Decorative Objects",
}

# Türkçe başlık -> (ingilizce başlık, ingilizce açıklama)
PRODUCTS_EN = {
    "Mary Gregory Sürahi ve Bardak Takımı": (
        "Mary Gregory Pitcher and Tumbler Set",
        "An original Mary Gregory set: white enamel figures hand painted on blue glass, "
        "with gilding along the rim and foot. One of the most loved glass crafts of its day."),
    "Mary Gregory Başucu Sürahisi": (
        "Mary Gregory Bedside Carafe",
        "Clear glass carrying hand painted white enamel figures. An original bedside carafe, "
        "complete with its matching tumbler."),
    "Porselen Çay Servisi": (
        "Porcelain Tea Service",
        "A European white porcelain tea and coffee service with a relief pattern. Complete "
        "with teapot, sugar bowl, creamer and cups."),
    "WMF Kapaklı Kutu": (
        "WMF Lidded Box",
        "A footed lidded box marked by the German house WMF, with an embossed border. An "
        "original piece, distinguished by the cast handle on its lid."),
    "Manzara Desenli Tabak Seti": (
        "Scenic Plate Set",
        "A four piece plate set in the English blue and white tradition, engraved with "
        "castles and fortresses. Made with the classic transfer printing technique."),
    "Porselen Fincan Takımı": (
        "Porcelain Cup Set",
        "European porcelain with an angel relief body and a gilded border. A three piece "
        "set: cup, saucer and cake plate."),
    "Zincir Askılı Vintage Çanta": (
        "Vintage Bag with Chain Strap",
        "A decorative vintage bag with a chain strap, a bird figure on the clasp and a "
        "fluted brass body."),
    "Amber Cam Kadeh (6 Adet)": (
        "Amber Glass Goblets (Set of 6)",
        "Footed goblets in amber glass with a fluted body. A set of six that brings the warm "
        "tones of European glasswork to the table."),
    "Gümüş Çikolata Potu": (
        "Silver Chocolate Pot",
        "An 800 silver chocolate pot made in Paris between 1868 and 1888, marked Paillard "
        "Frères. A collector's piece, with embossed floral decoration and a wooden handle."),
    "Christofle Malmaison Tepsi": (
        "Christofle Malmaison Tray",
        "A serving tray with a pearl border from Christofle's iconic Malmaison collection. "
        "One of the French house's most sought after forms."),
    "Christofle Çatal Bıçak Takımı": (
        "Christofle Cutlery Set",
        "A silver plated cutlery set signed Christofle, together with serving pieces such as "
        "a ladle, a serving fork and a cake slice."),
    "Gümüş Kaplama Şamdan (Çift)": (
        "Silver Plated Candlesticks (Pair)",
        "A pair of tall, slender candlesticks with a pearl border. A classic of European "
        "table culture."),
    "Gümüş Kaplama Mumluk Koleksiyonu": (
        "Silver Plated Candle Holder Collection",
        "Silver plated candle holders in various sizes and forms, brought from Europe both "
        "as pairs and as single pieces."),
    "Şamdan ve Mumluk Grubu": (
        "Candlestick and Candle Holder Group",
        "A silver plated group reaching from tall candlesticks to chamber sticks, gathered "
        "from different periods and forms."),
    "Pirinç ve Gümüş Mumluklar": (
        "Brass and Silver Candle Holders",
        "A mixed group of brass and silver plated candle holders, some in pairs and some as "
        "single pieces."),
    "Pirinç Şamdan (Çift)": (
        "Brass Candlesticks (Pair)",
        "A pair of brass candlesticks with engraved leaf decoration and a wide base. The "
        "aged patina keeps the original form intact."),
    "Oval Gümüş Kaplama Tepsi": (
        "Oval Silver Plated Tray",
        "An oval serving tray with a pearl border and an embossed medallion at its centre."),
    "Kulplu Gümüş Kaplama Tepsi": (
        "Silver Plated Tray with Handles",
        "A serving tray with handles and embossed leaf work along the rim. Marked and "
        "original."),
    "Tepsi, Cevizlik ve Kıracak": (
        "Tray, Bowl and Nutcracker",
        "A serving group of a handled silver plated tray, a small bowl with an embossed rim "
        "and a nutcracker."),
    "Çiçek Desenli Çerezlik Tabaklar": (
        "Floral Serving Plates",
        "European porcelain serving plates with a rose pattern, together with openwork spice "
        "spoons. For coffee and refreshments."),
    "Mavi-Beyaz Servis Tabakları": (
        "Blue and White Serving Dishes",
        "Rectangular handled porcelain serving dishes with a printed scene. One of the best "
        "known forms of the classic blue and white pattern."),
    "Çay Kaşığı Takımı": (
        "Teaspoon Set",
        "A silver plated teaspoon set with a classic border pattern. An elegant European "
        "piece, suited to everyday use as well."),
    "Çay Süzgeci": (
        "Tea Strainer",
        "An over the cup tea strainer with a gilded bowl and an embossed handle."),
    "Melek Figürlü Süt Sürahisi": (
        "Milk Jug with Angel Figures",
        "A jasperware style porcelain milk jug, with white angel reliefs on a matte body."),
    "Kapaklı Bira Maşrapası": (
        "Lidded Beer Stein",
        "A German ceramic stein with relief figures on a cobalt blue ground. Original, with "
        "its hinged pewter lid."),
    "Çiçek Motifli Peçetelik": (
        "Floral Napkin Holder",
        "A silver plated napkin holder with openwork floral decoration."),
}

SETTINGS_EN = {
    "hero_title": "Authentic Antiques, Lasting Stories",
    "about_short":
        "Home Antique Home brings antique and collectable pieces, chosen one by one in "
        "Europe, to İstanbul. Most of the silver, porcelain and glass in the collection are "
        "original period pieces.",
    "about_long_1":
        "Home Antique Home is an antiques and collectables house based in İstanbul. The "
        "greater part of the collection has been brought from Europe, selected piece by "
        "piece: French silver plate, German porcelain, English blue and white plates and "
        "examples of period glasswork.",
    "about_long_2":
        "We care about the authenticity and the condition of every piece; most of what we "
        "offer are signed or marked works of their period. Our aim is to carry the carefully "
        "made objects of the past into present day homes, and to give our customers a "
        "purchase they can trust.",
    "showroom_text":
        "Silver plated tableware, porcelain services, glass works and decorative objects "
        "brought from across Europe are waiting for you in our showcase. The collection is "
        "renewed continually; you can follow new arrivals on our Instagram account.",
    "sss_orijinallik":
        "The greater part of our collection consists of original period pieces, selected one "
        "by one in Europe. Where a piece carries a maker's signature, a hallmark or a "
        "standard mark, we state it in the description. We do not use the word original for "
        "a piece whose origin we are not certain of.",
    "sss_odeme":
        "No payment is taken through the site. Once your order is settled over WhatsApp, we "
        "agree on the payment method together.",
    "sss_kargo":
        "We ship with Yurtiçi Kargo, and your piece usually reaches you within two or three "
        "days. Fragile pieces such as glass, porcelain and crystal are packed specially, in "
        "two layers with padding. Hand delivery within İstanbul is also possible; we can "
        "arrange the details over WhatsApp.",
    "sss_iade":
        "The right of withdrawal granted by consumer law applies to distance sales. If you "
        "change your mind after receiving a piece, get in touch and we will work it through "
        "together. On antiques, traces of use that come with age are not counted as faults; "
        "we show them as openly as we can in the description and the photographs.",
    "sss_bakim":
        "Wipe silver and silver plated pieces dry with a soft cloth; abrasive sponges and "
        "dishwashers damage the plating. To slow tarnishing, keep them somewhere closed, "
        "away from the air. Wash gilded porcelain and glass by hand in warm water; gilding "
        "does not survive the microwave or the dishwasher. Protect crystal and fine glass "
        "from sudden changes of temperature.",
}

# Üretilen işaretlemedeki arayüz metinleri
UI = {
    "tr": {
        "code": "tr",
        "nav": {"index.html": "Ana Sayfa", "hakkimizda.html": "Hakkımızda",
                "showroom.html": "Vitrin", "galeri.html": "Galeri",
                "iletisim.html": "İletişim", "sss.html": "Sıkça Sorulan Sorular",
                "gizlilik.html": "Gizlilik ve Kişisel Veriler"},
        "search_placeholder": "Ara&#8230;",
        "search_label": "Koleksiyonda ara",
        "search_button": "Ara",
        "submenu_label": "Galeri kategorileri",
        "instagram_label": "Instagram sayfamız",
        "ask": "WhatsApp ile Sor",
        "ask_similar": "Benzerini Sor",
        "sold": "Satıldı",
        "wa_interested": "Merhaba! Sitenizdeki {title} ile ilgileniyorum.",
        "wa_similar": "Merhaba! Sitenizdeki {title} satılmış görünüyor, "
                      "benzer bir parçanız var mı?",
        "pieces": "{n} parça",
        "all": "Tümü",
        "footer_company": "Kurumsal",
        "footer_collection": "Koleksiyon",
        "footer_contact": "Bize Ulaşın",
        "footer_all": "Tüm Parçalar",
        "rights": "Tüm hakları saklıdır.",
        "other_lang": "English",
        "other_lang_short": "EN",
        "lang_label": "Switch to English",
    },
    "en": {
        "code": "en",
        "nav": {"index.html": "Home", "about.html": "About",
                "showroom.html": "Showcase", "gallery.html": "Gallery",
                "contact.html": "Contact", "faq.html": "Frequently Asked Questions",
                "privacy.html": "Privacy & Personal Data"},
        "search_placeholder": "Search&#8230;",
        "search_label": "Search the collection",
        "search_button": "Search",
        "submenu_label": "Gallery categories",
        "instagram_label": "Our Instagram page",
        "ask": "Ask on WhatsApp",
        "ask_similar": "Ask for Similar",
        "sold": "Sold",
        "wa_interested": "Hello! I am interested in the {title} on your website.",
        "wa_similar": "Hello! The {title} on your website appears to be sold — "
                      "do you have anything similar?",
        "pieces": "{n} pieces",
        "all": "All",
        "footer_company": "Company",
        "footer_collection": "Collection",
        "footer_contact": "Contact Us",
        "footer_all": "All Pieces",
        "rights": "All rights reserved.",
        "other_lang": "Türkçe",
        "other_lang_short": "TR",
        "lang_label": "Türkçe'ye geç",
    },
}


# Sayfa gövdelerindeki sabit metinler: türkçe parça -> ingilizce parça.
# İngilizce sayfalar her derlemede türkçelerinden yeniden üretilir, bu yüzden
# buraya eklenen her parçanın türkçe sayfada birebir bulunması gerekir.
STATIC_EN = {
    # ana sayfa
    'aria-label="Home Antique Home koleksiyonundan Mary Gregory el işlemeli cam sürahi"':
        'aria-label="A Mary Gregory hand painted glass pitcher from the Home Antique Home collection"',
    '<a href="gallery.html" class="btn">Galeriyi Görüntüle</a>':
        '<a href="gallery.html" class="btn">View the Gallery</a>',
    'alt="Home Antique Home koleksiyonundan oval gümüş kaplama tepsi"':
        'alt="An oval silver plated tray from the Home Antique Home collection"',
    "<h2>Hakkımızda</h2>": "<h2>About Us</h2>",
    '<a href="about.html" class="btn">Devamını Oku</a>':
        '<a href="about.html" class="btn">Read More</a>',
    '<h2 class="section-title">Koleksiyon</h2>':
        '<h2 class="section-title">Collection</h2>',
    "Her parçanın anlatacak bir hikâyesi var.":
        "Every piece has a story to tell.",
    "Fransız gümüş kaplamalarından Alman porselenlerine, İngiliz mavi-beyaz\n"
    "          tabaklarından dönemin cam işçiliğine — Avrupa'nın dört bir yanından\n"
    "          tek tek seçilmiş eserler.":
        "From French silver plate to German porcelain, from English blue and white\n"
        "          plates to the glasswork of the period — pieces chosen one by one\n"
        "          from across Europe.",
    '<h2 class="section-title">Yeni Ürünler</h2>':
        '<h2 class="section-title">New Arrivals</h2>',
    '<a href="gallery.html" class="btn">Tüm Koleksiyonu Gör</a>':
        '<a href="gallery.html" class="btn">See the Whole Collection</a>',
    '<h2 class="section-title">Koleksiyondan Kareler</h2>':
        '<h2 class="section-title">Frames from the Collection</h2>',
    "<h2>Ziyaretimize Bekleriz</h2>": "<h2>Come and Visit Us</h2>",
    '<a href="contact.html" class="btn">İletişim Bilgileri</a>':
        '<a href="contact.html" class="btn">Contact Details</a>',
    # mozaik görsel açıklamaları
    'alt="Christofle çatal bıçak takımı"': 'alt="Christofle cutlery set"',
    'alt="Çiçek desenli çerezlik tabaklar"': 'alt="Floral serving plates"',
    'alt="Mavi-beyaz servis tabakları"': 'alt="Blue and white serving dishes"',
    'alt="Gümüş kaplama çay kaşığı takımı"': 'alt="Silver plated teaspoon set"',
    'alt="Christofle Malmaison servis tepsisi"': 'alt="Christofle Malmaison serving tray"',
    'alt="Kulplu gümüş kaplama tepsi"': 'alt="Silver plated tray with handles"',
    'alt="Altın yaldızlı hazneli çay süzgeci"': 'alt="Tea strainer with a gilded bowl"',
    'alt="Şamdan ve mumluk grubu"': 'alt="Candlestick and candle holder group"',
    # hakkımızda
    "<h1>Hakkımızda</h1>": "<h1>About Us</h1>",
    'alt="Paillard Frères damgalı gümüş çikolata potu"':
        'alt="A silver chocolate pot marked Paillard Frères"',
    "<h2 class=\"section-title\">Bizi Instagram'da Takip Edin</h2>":
        '<h2 class="section-title">Follow Us on Instagram</h2>',
    "Yeni gelen parçaları ve koleksiyonumuzu günlük olarak":
        "You can follow new arrivals and the collection day by day on our",
    "hesabımızdan takip edebilirsiniz.": "account.",
    # vitrin
    "<h1>Vitrin</h1>": "<h1>Showcase</h1>",
    '<h2 class="section-title">Öne Çıkan Parçalar</h2>':
        '<h2 class="section-title">Featured Pieces</h2>',
    'Tüm koleksiyonu görmek için <a href="gallery.html">galeriye göz atın</a>.':
        'To see everything, <a href="gallery.html">browse the gallery</a>.',
    # galeri
    "<h1>Galeri</h1>": "<h1>Gallery</h1>",
    'placeholder="Koleksiyonda ara&#8230;" aria-label="Koleksiyonda ara"':
        'placeholder="Search the collection&#8230;" aria-label="Search the collection"',
    "            Filtreler\n": "            Filters\n",
    "Aramanıza uygun ürün bulunamadı.": "No pieces match your search.",
    # iletişim
    "<h1>İletişim</h1>": "<h1>Contact</h1>",
    "<h2>Bize Ulaşın</h2>": "<h2>Contact Us</h2>",
    "<strong>Adres:</strong>": "<strong>Address:</strong>",
    "<strong>E-posta:</strong>": "<strong>Email:</strong>",
    "<strong>Telefon:</strong>": "<strong>Phone:</strong>",
    'title="Bağdat Caddesi, İstanbul konum haritası"':
        'title="Map showing Bağdat Caddesi, İstanbul"',
    ">Haritalarda Aç</a>": ">Open in Maps</a>",
}

# <title> ve açıklama (türkçe dosya adına göre)
HEAD_EN = {
    "index.html": ("Home Antique Home | Authentic Antiques",
                   "İstanbul based antique silver, glass and porcelain, with provenance you can trust"),
    "hakkimizda.html": ("About Us | Home Antique Home",
                        "About Home Antique Home: our story and what we look for"),
    "showroom.html": ("Showcase | Home Antique Home",
                      "Featured pieces from the Home Antique Home collection"),
    "galeri.html": ("Gallery | Home Antique Home",
                    "The full Home Antique Home collection of antique silver, porcelain and glass"),
    "iletisim.html": ("Contact | Home Antique Home",
                      "Get in touch with Home Antique Home — address, phone and WhatsApp"),
    "sss.html": ("Frequently Asked Questions | Home Antique Home",
                 "Authenticity, ordering, shipping, returns and caring for antiques"),
    "gizlilik.html": ("Privacy & Personal Data | Home Antique Home",
                      "How Home Antique Home handles personal data"),
}

# Düz yazı ağırlıklı iki sayfanın gövdesi olduğu gibi yazılır
MAIN_EN = {
    "sss.html": '''  <main>
    <div class="page-header">
      <h1>Frequently Asked Questions</h1>
    </div>

    <section>
      <div class="container prose">
        <h2>Are your pieces genuine?</h2>
        <p data-setting="sss_orijinallik"></p>

        <h2>How do I place an order?</h2>
        <p>
          Tap the <strong>Ask on WhatsApp</strong> button under any piece you like; WhatsApp opens with a message about that piece already written. You can also reach us through the <strong>Order / Enquiry Form</strong>, and we will come back to you as soon as we can.
        </p>

        <h2>How is payment made?</h2>
        <p data-setting="sss_odeme"></p>

        <h2>How does shipping and delivery work?</h2>
        <p data-setting="sss_kargo"></p>

        <h2>Can I return or exchange a piece?</h2>
        <p data-setting="sss_iade"></p>

        <h2>How should antiques be cared for?</h2>
        <p data-setting="sss_bakim"></p>

        <p class="page-outro">
          If you could not find your answer, <a href="contact.html">write to us</a>.
        </p>
      </div>
    </section>
  </main>''',
    "gizlilik.html": '''  <main>
    <div class="page-header">
      <h1>Privacy &amp; Personal Data</h1>
    </div>

    <section>
      <div class="container prose">
        <p class="page-intro">
          This page explains which personal data the Home Antique Home website collects, and what we do with it.
        </p>

        <h2>Who is responsible</h2>
        <p>
          Home Antique Home — <span data-setting="address">Bağdat Caddesi, İstanbul</span><br />
          Email: <a href="mailto:homeantiquehome@gmail.com" data-setting="email" data-setting-href="email">homeantiquehome@gmail.com</a><br />
          Phone: <a href="tel:+905557370933" data-setting="phone" data-setting-href="tel">0555 737 09 33</a>
        </p>

        <h2>What we collect</h2>
        <p>
          We collect data in one place only: the <strong>order and enquiry form</strong>. It asks for your name, your phone number, optionally your email address, and any note you add. Which piece you are asking about is attached to the request.
        </p>
        <p>
          Nothing else is asked of you while you browse. When you tap a WhatsApp button the conversation continues on WhatsApp, where WhatsApp's own terms apply.
        </p>

        <h2>What we use it for</h2>
        <p>
          Only to answer your enquiry and to carry out your order. We do not use it for marketing, and we do not sell or pass it on to third parties.
        </p>

        <h2>Where it is kept</h2>
        <p>
          Form entries are held on Supabase, a database service, and can be reached only with an authorised account. No other visitor to the site can see them.
        </p>

        <h2>Do we use cookies?</h2>
        <p>
          <strong>No.</strong> This site carries no cookies, no tracking code, no advertising pixels and no visitor analytics.
        </p>

        <h2>Outside services</h2>
        <p>
          A few outside sources are used to render the page: Google Fonts for the typefaces, jsDelivr for a software library, and OpenStreetMap for the map on the contact page. As your browser downloads those files, these services technically see your IP address. Nothing identifying you is sent to them or to us beyond that.
        </p>

        <h2>Your rights</h2>
        <p>
          Under Turkish personal data protection law (KVKK, no. 6698) you may ask whether your data is being processed, and ask for it to be corrected or deleted. Write to the email address above for any such request.
        </p>

        <p class="page-outro">
          For questions or requests, see our <a href="contact.html">contact page</a>.
        </p>
      </div>
    </section>
  </main>''',
}
