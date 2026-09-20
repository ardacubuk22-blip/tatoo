-- Home Antique Home — Supabase schema
-- Supabase panelinde: SQL Editor > New query > bu dosyanın tamamını çalıştırın.

-- ---------------------------------------------------------------------------
-- Ürünler
-- ---------------------------------------------------------------------------
create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  title_en text,
  description_en text,
  price numeric(12, 2),
  image_url text,
  is_sold boolean not null default false,
  is_featured boolean not null default false,
  category text,
  subcategory text,
  sort_order integer not null default 0,
  created_at timestamptz not null default now()
);

-- Daha önce kurulmuş bir veritabanına kategori alanlarını ekler
alter table public.products add column if not exists category text;
alter table public.products add column if not exists subcategory text;
alter table public.products
  add column if not exists is_featured boolean not null default false;
alter table public.products add column if not exists title_en text;
alter table public.products add column if not exists description_en text;

alter table public.products enable row level security;

drop policy if exists "products_public_read" on public.products;
create policy "products_public_read"
  on public.products for select
  using (true);

drop policy if exists "products_admin_insert" on public.products;
create policy "products_admin_insert"
  on public.products for insert
  to authenticated
  with check (true);

drop policy if exists "products_admin_update" on public.products;
create policy "products_admin_update"
  on public.products for update
  to authenticated
  using (true)
  with check (true);

drop policy if exists "products_admin_delete" on public.products;
create policy "products_admin_delete"
  on public.products for delete
  to authenticated
  using (true);

-- ---------------------------------------------------------------------------
-- Site metinleri ve iletişim bilgileri (anahtar/değer)
-- ---------------------------------------------------------------------------
create table if not exists public.site_settings (
  key text primary key,
  value text
);

alter table public.site_settings enable row level security;

drop policy if exists "settings_public_read" on public.site_settings;
create policy "settings_public_read"
  on public.site_settings for select
  using (true);

drop policy if exists "settings_admin_write" on public.site_settings;
create policy "settings_admin_write"
  on public.site_settings for insert
  to authenticated
  with check (true);

drop policy if exists "settings_admin_update" on public.site_settings;
create policy "settings_admin_update"
  on public.site_settings for update
  to authenticated
  using (true)
  with check (true);

-- ---------------------------------------------------------------------------
-- Siparişler / bilgi talepleri
-- Ziyaretçiler sipariş bırakabilir ama başkalarının siparişlerini GÖREMEZ.
-- ---------------------------------------------------------------------------
create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(),
  product_id uuid references public.products(id) on delete set null,
  product_title text,
  customer_name text not null,
  customer_phone text not null,
  customer_email text,
  note text,
  status text not null default 'new'
    check (status in ('new', 'contacted', 'completed', 'cancelled')),
  created_at timestamptz not null default now()
);

alter table public.orders enable row level security;

drop policy if exists "orders_public_insert" on public.orders;
create policy "orders_public_insert"
  on public.orders for insert
  to anon, authenticated
  with check (true);

drop policy if exists "orders_admin_read" on public.orders;
create policy "orders_admin_read"
  on public.orders for select
  to authenticated
  using (true);

drop policy if exists "orders_admin_update" on public.orders;
create policy "orders_admin_update"
  on public.orders for update
  to authenticated
  using (true)
  with check (true);

drop policy if exists "orders_admin_delete" on public.orders;
create policy "orders_admin_delete"
  on public.orders for delete
  to authenticated
  using (true);

-- ---------------------------------------------------------------------------
-- Ürün görselleri için storage bucket
-- ---------------------------------------------------------------------------
insert into storage.buckets (id, name, public)
values ('product-images', 'product-images', true)
on conflict (id) do nothing;

drop policy if exists "product_images_public_read" on storage.objects;
create policy "product_images_public_read"
  on storage.objects for select
  using (bucket_id = 'product-images');

drop policy if exists "product_images_admin_insert" on storage.objects;
create policy "product_images_admin_insert"
  on storage.objects for insert
  to authenticated
  with check (bucket_id = 'product-images');

drop policy if exists "product_images_admin_update" on storage.objects;
create policy "product_images_admin_update"
  on storage.objects for update
  to authenticated
  using (bucket_id = 'product-images');

drop policy if exists "product_images_admin_delete" on storage.objects;
create policy "product_images_admin_delete"
  on storage.objects for delete
  to authenticated
  using (bucket_id = 'product-images');

-- ---------------------------------------------------------------------------
-- Başlangıç içeriği (sitedeki mevcut metinler ve ürünler)
-- ---------------------------------------------------------------------------
insert into public.site_settings (key, value) values
  ('hero_title', 'Otantik Antikalar, Kalıcı Hikâyeler'),
  ('about_short', 'Home Antique Home, Avrupa''dan tek tek seçilerek getirilen antika ve koleksiyon parçalarını İstanbul''da sizlerle buluşturuyor. Gümüş, porselen ve cam eserlerin büyük bölümü orijinal dönem parçalarıdır.'),
  ('about_long_1', 'Home Antique Home, İstanbul merkezli bir antika ve koleksiyon markasıdır. Koleksiyonumuzdaki parçaların büyük bölümü Avrupa''dan, tek tek seçilerek getirilmiştir: Fransız gümüş kaplamaları, Alman porselenleri, İngiliz mavi-beyaz tabakları ve dönemin cam işçiliği örnekleri.'),
  ('about_long_2', 'Her parçanın orijinalliğine ve durumuna önem veriyoruz; ürünlerimizin çoğu imzalı ya da damgalı dönem eserleridir. Amacımız, geçmişin özenle işlenmiş eserlerini günümüz evlerine taşımak ve müşterilerimize güvenilir bir alışveriş deneyimi sunmaktır.'),
  ('showroom_text', 'Avrupa''nın farklı ülkelerinden getirdiğimiz gümüş kaplama sofra takımları, porselen servisler, cam eserler ve dekoratif objeler vitrinimizde sizi bekliyor. Koleksiyon sürekli yenileniyor; yeni gelen parçaları Instagram hesabımızdan takip edebilirsiniz.'),
  ('sss_orijinallik', 'Koleksiyonumuzdaki parçaların büyük bölümü Avrupa''dan tek tek seçilerek getirilen, dönemine ait orijinal eserlerdir. Bir parçanın üzerinde üretici imzası, damga ya da ayar işareti varsa bunu ürün açıklamasında belirtiyoruz. Kaynağından emin olmadığımız bir parça için "orijinal" ifadesini kullanmıyoruz.'),
  ('sss_odeme', 'Site üzerinden ödeme alınmıyor. Siparişiniz WhatsApp üzerinden netleştikten sonra ödeme yöntemini birlikte belirliyoruz.'),
  ('sss_kargo', 'Gönderimlerimizi Yurtiçi Kargo ile yapıyoruz; parçanız genellikle 2-3 gün içinde elinizde olur. Cam, porselen ve kristal gibi kırılabilir parçalar çift katmanlı ve dolgulu olarak özel paketlenir. İstanbul içinde elden teslim de mümkündür; ayrıntıları WhatsApp''tan konuşabiliriz.'),
  ('sss_iade', 'Uzaktan yapılan satışlarda tüketici mevzuatının tanıdığı cayma hakkı geçerlidir. Parçayı teslim aldıktan sonra fikrinizi değiştirirseniz bizimle iletişime geçin; süreci birlikte yürütelim. Antika parçalarda yaşına bağlı kullanım izleri kusur sayılmaz, bu izleri ürün açıklamasında ve fotoğraflarda olabildiğince açık gösteriyoruz.'),
  ('sss_bakim', 'Gümüş ve gümüş kaplama parçaları yumuşak bir bezle kuru olarak silin; aşındırıcı sünger ve bulaşık makinesi kaplamaya zarar verir. Kararmayı geciktirmek için havayla temasın azaldığı, kapalı bir yerde saklayın. Altın yaldızlı porselen ve cam eserleri ılık suda elde yıkayın; yaldız mikrodalgaya ve makineye dayanmaz. Kristal ve ince camı ani sıcaklık değişiminden koruyun.'),
  ('address', 'Bağdat Caddesi, İstanbul'),
  ('phone', '0555 737 09 33'),
  ('email', 'homeantiquehome@gmail.com'),
  ('instagram_url', 'https://www.instagram.com/homeantiquehome')
on conflict (key) do nothing;

insert into public.products (title, description, price, image_url, is_sold, category, subcategory, sort_order, is_featured, title_en, description_en) values
  ('Mary Gregory Sürahi ve Bardak Takımı', 'Mavi cam üzerine beyaz emaye figür işlemeli, ağız ve kaide kenarları altın yaldızlı orijinal Mary Gregory takımı. Dönemin en sevilen cam işçiliklerinden.', null, 'assets/images/hero-mary-gregory.jpg', false, 'cam', null, 1, true, 'Mary Gregory Pitcher and Tumbler Set', 'An original Mary Gregory set: white enamel figures hand painted on blue glass, with gilding along the rim and foot. One of the most loved glass crafts of its day.'),
  ('Mary Gregory Başucu Sürahisi', 'Şeffaf cam üzerine el işçiliği beyaz emaye figürlü, bardağıyla birlikte gelen orijinal başucu sürahisi.', null, 'assets/images/gallery-mary-gregory-clear.jpg', true, 'cam', null, 2, false, 'Mary Gregory Bedside Carafe', 'Clear glass carrying hand painted white enamel figures. An original bedside carafe, complete with its matching tumbler.'),
  ('Porselen Çay Servisi', 'Avrupa yapımı, kabartma desenli beyaz porselen çay ve kahve servisi. Demlik, şekerlik, sütlük ve fincanlarıyla eksiksiz takım.', 11500, 'assets/images/porselen-cay-servisi.jpg', false, 'porselen', 'servis-takimlari', 3, true, 'Porcelain Tea Service', 'A European white porcelain tea and coffee service with a relief pattern. Complete with teapot, sugar bowl, creamer and cups.'),
  ('WMF Kapaklı Kutu', 'Alman WMF imzalı, kabartma bordürlü ve ayaklı kapaklı kutu. Kapağındaki döküm tutamağıyla dikkat çeken, orijinal bir parça.', 10000, 'assets/images/wmf-gumus-kutu.jpg', false, 'gumus', 'gumus-diger', 4, false, 'WMF Lidded Box', 'A footed lidded box marked by the German house WMF, with an embossed border. An original piece, distinguished by the cast handle on its lid.'),
  ('Manzara Desenli Tabak Seti', 'İngiliz mavi-beyaz geleneğinde, şato ve kale gravürlü 4 parçalık tabak seti. Klasik transfer baskı tekniğiyle üretilmiş.', 6500, 'assets/images/manzara-tabak-seti.jpg', false, 'porselen', 'tabaklar', 5, false, 'Scenic Plate Set', 'A four piece plate set in the English blue and white tradition, engraved with castles and fortresses. Made with the classic transfer printing technique.'),
  ('Porselen Fincan Takımı', 'Melek kabartmalı gövde ve altın yaldız bordürlü Avrupa porseleni. Fincan, tabak ve pasta tabağından oluşan 3 parça takım.', 5500, 'assets/images/porselen-fincan-takimi.jpg', false, 'porselen', 'servis-takimlari', 6, false, 'Porcelain Cup Set', 'European porcelain with an angel relief body and a gilded border. A three piece set: cup, saucer and cake plate.'),
  ('Zincir Askılı Vintage Çanta', 'Kuş figürlü kapak detayı ve dilimli pirinç gövdesiyle, zincir askılı dekoratif vintage çanta.', 5500, 'assets/images/pirinc-zincirli-canta.jpg', false, 'dekoratif', null, 7, false, 'Vintage Bag with Chain Strap', 'A decorative vintage bag with a chain strap, a bird figure on the clasp and a fluted brass body.'),
  ('Amber Cam Kadeh (6 Adet)', 'Amber renkli, dilimli gövdeli ayaklı kadeh. Avrupa cam işçiliğinin sıcak tonlarını sofranıza taşıyan 6''lı set.', 4750, 'assets/images/amber-kadeh.jpg', false, 'cam', null, 8, false, 'Amber Glass Goblets (Set of 6)', 'Footed goblets in amber glass with a fluted body. A set of six that brings the warm tones of European glasswork to the table.'),
  ('Gümüş Çikolata Potu', '1868-1888 arası Paris yapımı, Paillard Frères damgalı 800 ayar gümüş çikolata potu. Kabartma çiçek bezemeleri ve ahşap sapıyla koleksiyonluk bir eser.', null, 'assets/images/gumus-cikolata-potu.jpg', false, 'gumus', 'gumus-diger', 9, false, 'Silver Chocolate Pot', 'An 800 silver chocolate pot made in Paris between 1868 and 1888, marked Paillard Frères. A collector''s piece, with embossed floral decoration and a wooden handle.'),
  ('Christofle Malmaison Tepsi', 'Fransız Christofle''nin ikonik Malmaison koleksiyonundan, inci bordürlü servis tepsisi. Markanın en çok aranan formlarından biri.', null, 'assets/images/gumus-servis-tepsisi.jpg', false, 'gumus', 'tepsiler', 10, true, 'Christofle Malmaison Tray', 'A serving tray with a pearl border from Christofle''s iconic Malmaison collection. One of the French house''s most sought after forms.'),
  ('Christofle Çatal Bıçak Takımı', 'Christofle imzalı, gümüş kaplama çatal-bıçak takımı. Kepçe, servis çatalı ve pasta spatulası gibi servis parçalarıyla birlikte.', null, 'assets/images/christofle-catal-bicak-takimi.jpg', false, 'gumus', 'catal-bicak', 11, true, 'Christofle Cutlery Set', 'A silver plated cutlery set signed Christofle, together with serving pieces such as a ladle, a serving fork and a cake slice.'),
  ('Gümüş Kaplama Şamdan (Çift)', 'İnci bordürlü, uzun ve zarif formlu şamdan çifti. Avrupa sofra kültürünün klasik parçalarından.', null, 'assets/images/gumus-samdan-cift.jpg', false, 'aydinlatma', 'samdanlar', 12, true, 'Silver Plated Candlesticks (Pair)', 'A pair of tall, slender candlesticks with a pearl border. A classic of European table culture.'),
  ('Gümüş Kaplama Mumluk Koleksiyonu', 'Farklı boy ve formlarda gümüş kaplama mumluklar. Bir kısmı çift, bir kısmı tekli olarak Avrupa''dan getirildi.', null, 'assets/images/mumluk-koleksiyonu.jpg', false, 'aydinlatma', 'mumluklar', 13, false, 'Silver Plated Candle Holder Collection', 'Silver plated candle holders in various sizes and forms, brought from Europe both as pairs and as single pieces.'),
  ('Şamdan ve Mumluk Grubu', 'Yüksek şamdanlardan el mumluklarına uzanan, farklı dönem ve formlardan oluşan gümüş kaplama grup.', null, 'assets/images/mumluk-grubu.jpg', false, 'aydinlatma', 'mumluklar', 14, false, 'Candlestick and Candle Holder Group', 'A silver plated group reaching from tall candlesticks to chamber sticks, gathered from different periods and forms.'),
  ('Pirinç ve Gümüş Mumluklar', 'Pirinç ve gümüş kaplama mumluklardan oluşan karma grup; kimi çift, kimi tekli parçalar halinde.', null, 'assets/images/pirinc-gumus-mumluklar.jpg', false, 'aydinlatma', 'mumluklar', 15, false, 'Brass and Silver Candle Holders', 'A mixed group of brass and silver plated candle holders, some in pairs and some as single pieces.'),
  ('Pirinç Şamdan (Çift)', 'Kazıma yaprak desenli, geniş kaideli çift pirinç şamdan. Yıllanmış patinasıyla orijinal formunu koruyor.', null, 'assets/images/pirinc-samdan.jpg', false, 'aydinlatma', 'samdanlar', 16, false, 'Brass Candlesticks (Pair)', 'A pair of brass candlesticks with engraved leaf decoration and a wide base. The aged patina keeps the original form intact.'),
  ('Oval Gümüş Kaplama Tepsi', 'İnci bordürlü, ortası kabartma madalyon işlemeli oval servis tepsisi.', null, 'assets/images/oval-gumus-tepsi.jpg', false, 'gumus', 'tepsiler', 17, false, 'Oval Silver Plated Tray', 'An oval serving tray with a pearl border and an embossed medallion at its centre.'),
  ('Kulplu Gümüş Kaplama Tepsi', 'Kenarları kabartma yaprak işlemeli, kulplu servis tepsisi. Damgalı ve orijinal.', null, 'assets/images/kulplu-gumus-tepsi.jpg', false, 'gumus', 'tepsiler', 18, false, 'Silver Plated Tray with Handles', 'A serving tray with handles and embossed leaf work along the rim. Marked and original.'),
  ('Tepsi, Cevizlik ve Kıracak', 'Kulplu gümüş kaplama tepsi, kabartma kenarlı küçük kase ve ceviz kıracağından oluşan ikram grubu.', null, 'assets/images/tepsi-ve-cevizlik.jpg', false, 'gumus', 'tepsiler', 19, false, 'Tray, Bowl and Nutcracker', 'A serving group of a handled silver plated tray, a small bowl with an embossed rim and a nutcracker.'),
  ('Çiçek Desenli Çerezlik Tabaklar', 'Gül desenli Avrupa porseleni çerezlik tabaklar ve ajur işlemeli baharat kaşıkları. Kahve ve ikram sunumları için.', null, 'assets/images/cicek-desenli-tabaklar.jpg', false, 'porselen', 'tabaklar', 20, false, 'Floral Serving Plates', 'European porcelain serving plates with a rose pattern, together with openwork spice spoons. For coffee and refreshments.'),
  ('Mavi-Beyaz Servis Tabakları', 'Manzara baskılı, kulplu dikdörtgen porselen servis tabakları. Klasik mavi-beyaz desenin en bilinen formlarından.', null, 'assets/images/mavi-beyaz-servis-tabaklari.jpg', false, 'porselen', 'tabaklar', 21, false, 'Blue and White Serving Dishes', 'Rectangular handled porcelain serving dishes with a printed scene. One of the best known forms of the classic blue and white pattern.'),
  ('Çay Kaşığı Takımı', 'Klasik bordür desenli, gümüş kaplama çay kaşığı takımı. Günlük kullanıma da uygun, zarif bir Avrupa parçası.', null, 'assets/images/gumus-cay-kasiklari.jpg', false, 'gumus', 'catal-bicak', 22, false, 'Teaspoon Set', 'A silver plated teaspoon set with a classic border pattern. An elegant European piece, suited to everyday use as well.'),
  ('Çay Süzgeci', 'Altın yaldızlı haznesi ve kabartma işlemeli sapıyla bardak üstü çay süzgeci.', null, 'assets/images/gumus-cay-suzgeci.jpg', false, 'gumus', 'gumus-diger', 23, false, 'Tea Strainer', 'An over the cup tea strainer with a gilded bowl and an embossed handle.'),
  ('Melek Figürlü Süt Sürahisi', 'Mat gövde üzerine beyaz melek kabartmalı, jasper tarzı porselen süt sürahisi.', null, 'assets/images/melek-figurlu-surahi.jpg', false, 'porselen', 'porselen-diger', 24, false, 'Milk Jug with Angel Figures', 'A jasperware style porcelain milk jug, with white angel reliefs on a matte body.'),
  ('Kapaklı Bira Maşrapası', 'Kobalt mavi zemin üzerine kabartma figürlü Alman seramik maşrapa. Kalaylı menteşeli kapağıyla orijinal.', null, 'assets/images/bira-masrapasi.jpg', false, 'porselen', 'porselen-diger', 25, false, 'Lidded Beer Stein', 'A German ceramic stein with relief figures on a cobalt blue ground. Original, with its hinged pewter lid.'),
  ('Çiçek Motifli Peçetelik', 'Gümüş kaplama, çiçek motifli ajur işlemeli peçetelik.', null, 'assets/images/gumus-pecetelik.jpg', true, 'gumus', 'gumus-diger', 26, false, 'Floral Napkin Holder', 'A silver plated napkin holder with openwork floral decoration.')
on conflict do nothing;
