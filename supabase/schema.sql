-- Home Antique Home — Supabase schema
-- Supabase panelinde: SQL Editor > New query > bu dosyanın tamamını çalıştırın.

-- ---------------------------------------------------------------------------
-- Ürünler
-- ---------------------------------------------------------------------------
create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  price numeric(12, 2),
  image_url text,
  is_sold boolean not null default false,
  category text,
  subcategory text,
  sort_order integer not null default 0,
  created_at timestamptz not null default now()
);

-- Daha önce kurulmuş bir veritabanına kategori alanlarını ekler
alter table public.products add column if not exists category text;
alter table public.products add column if not exists subcategory text;

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
  ('address', 'Bağdat Caddesi, İstanbul'),
  ('phone', '0555 737 09 33'),
  ('email', 'homeantiquehome@gmail.com'),
  ('instagram_url', 'https://www.instagram.com/homeantiquehome')
on conflict (key) do nothing;

insert into public.products (title, description, price, image_url, is_sold, category, subcategory, sort_order) values
  ('Mary Gregory Sürahi ve Bardak Takımı', 'Mavi cam üzerine beyaz emaye figür işlemeli, ağız ve kaide kenarları altın yaldızlı orijinal Mary Gregory takımı. Dönemin en sevilen cam işçiliklerinden.', null, 'assets/images/hero-mary-gregory.jpg', false, 'cam', null, 1),
  ('Mary Gregory Başucu Sürahisi', 'Şeffaf cam üzerine el işçiliği beyaz emaye figürlü, bardağıyla birlikte gelen orijinal başucu sürahisi.', null, 'assets/images/gallery-mary-gregory-clear.jpg', true, 'cam', null, 2),
  ('Porselen Çay Servisi', 'Avrupa yapımı, kabartma desenli beyaz porselen çay ve kahve servisi. Demlik, şekerlik, sütlük ve fincanlarıyla eksiksiz takım.', 11500, 'assets/images/porselen-cay-servisi.jpg', false, 'porselen', 'servis-takimlari', 3),
  ('WMF Kapaklı Kutu', 'Alman WMF imzalı, kabartma bordürlü ve ayaklı kapaklı kutu. Kapağındaki döküm tutamağıyla dikkat çeken, orijinal bir parça.', 10000, 'assets/images/wmf-gumus-kutu.jpg', false, 'gumus', 'gumus-diger', 4),
  ('Manzara Desenli Tabak Seti', 'İngiliz mavi-beyaz geleneğinde, şato ve kale gravürlü 4 parçalık tabak seti. Klasik transfer baskı tekniğiyle üretilmiş.', 6500, 'assets/images/manzara-tabak-seti.jpg', false, 'porselen', 'tabaklar', 5),
  ('Porselen Fincan Takımı', 'Melek kabartmalı gövde ve altın yaldız bordürlü Avrupa porseleni. Fincan, tabak ve pasta tabağından oluşan 3 parça takım.', 5500, 'assets/images/porselen-fincan-takimi.jpg', false, 'porselen', 'servis-takimlari', 6),
  ('Zincir Askılı Vintage Çanta', 'Kuş figürlü kapak detayı ve dilimli pirinç gövdesiyle, zincir askılı dekoratif vintage çanta.', 5500, 'assets/images/pirinc-zincirli-canta.jpg', false, 'dekoratif', null, 7),
  ('Amber Cam Kadeh (6 Adet)', 'Amber renkli, dilimli gövdeli ayaklı kadeh. Avrupa cam işçiliğinin sıcak tonlarını sofranıza taşıyan 6''lı set.', 4750, 'assets/images/amber-kadeh.jpg', false, 'cam', null, 8),
  ('Gümüş Çikolata Potu', '1868-1888 arası Paris yapımı, Paillard Frères damgalı 800 ayar gümüş çikolata potu. Kabartma çiçek bezemeleri ve ahşap sapıyla koleksiyonluk bir eser.', null, 'assets/images/gumus-cikolata-potu.jpg', false, 'gumus', 'gumus-diger', 9),
  ('Christofle Malmaison Tepsi', 'Fransız Christofle''nin ikonik Malmaison koleksiyonundan, inci bordürlü servis tepsisi. Markanın en çok aranan formlarından biri.', null, 'assets/images/gumus-servis-tepsisi.jpg', false, 'gumus', 'tepsiler', 10),
  ('Christofle Çatal Bıçak Takımı', 'Christofle imzalı, gümüş kaplama çatal-bıçak takımı. Kepçe, servis çatalı ve pasta spatulası gibi servis parçalarıyla birlikte.', null, 'assets/images/christofle-catal-bicak-takimi.jpg', false, 'gumus', 'catal-bicak', 11),
  ('Gümüş Kaplama Şamdan (Çift)', 'İnci bordürlü, uzun ve zarif formlu şamdan çifti. Avrupa sofra kültürünün klasik parçalarından.', null, 'assets/images/gumus-samdan-cift.jpg', false, 'aydinlatma', 'samdanlar', 12),
  ('Gümüş Kaplama Mumluk Koleksiyonu', 'Farklı boy ve formlarda gümüş kaplama mumluklar. Bir kısmı çift, bir kısmı tekli olarak Avrupa''dan getirildi.', null, 'assets/images/mumluk-koleksiyonu.jpg', false, 'aydinlatma', 'mumluklar', 13),
  ('Şamdan ve Mumluk Grubu', 'Yüksek şamdanlardan el mumluklarına uzanan, farklı dönem ve formlardan oluşan gümüş kaplama grup.', null, 'assets/images/mumluk-grubu.jpg', false, 'aydinlatma', 'mumluklar', 14),
  ('Pirinç ve Gümüş Mumluklar', 'Pirinç ve gümüş kaplama mumluklardan oluşan karma grup; kimi çift, kimi tekli parçalar halinde.', null, 'assets/images/pirinc-gumus-mumluklar.jpg', false, 'aydinlatma', 'mumluklar', 15),
  ('Pirinç Şamdan (Çift)', 'Kazıma yaprak desenli, geniş kaideli çift pirinç şamdan. Yıllanmış patinasıyla orijinal formunu koruyor.', null, 'assets/images/pirinc-samdan.jpg', false, 'aydinlatma', 'samdanlar', 16),
  ('Oval Gümüş Kaplama Tepsi', 'İnci bordürlü, ortası kabartma madalyon işlemeli oval servis tepsisi.', null, 'assets/images/oval-gumus-tepsi.jpg', false, 'gumus', 'tepsiler', 17),
  ('Kulplu Gümüş Kaplama Tepsi', 'Kenarları kabartma yaprak işlemeli, kulplu servis tepsisi. Damgalı ve orijinal.', null, 'assets/images/kulplu-gumus-tepsi.jpg', false, 'gumus', 'tepsiler', 18),
  ('Tepsi, Cevizlik ve Kıracak', 'Kulplu gümüş kaplama tepsi, kabartma kenarlı küçük kase ve ceviz kıracağından oluşan ikram grubu.', null, 'assets/images/tepsi-ve-cevizlik.jpg', false, 'gumus', 'tepsiler', 19),
  ('Çiçek Desenli Çerezlik Tabaklar', 'Gül desenli Avrupa porseleni çerezlik tabaklar ve ajur işlemeli baharat kaşıkları. Kahve ve ikram sunumları için.', null, 'assets/images/cicek-desenli-tabaklar.jpg', false, 'porselen', 'tabaklar', 20),
  ('Mavi-Beyaz Servis Tabakları', 'Manzara baskılı, kulplu dikdörtgen porselen servis tabakları. Klasik mavi-beyaz desenin en bilinen formlarından.', null, 'assets/images/mavi-beyaz-servis-tabaklari.jpg', false, 'porselen', 'tabaklar', 21),
  ('Çay Kaşığı Takımı', 'Klasik bordür desenli, gümüş kaplama çay kaşığı takımı. Günlük kullanıma da uygun, zarif bir Avrupa parçası.', null, 'assets/images/gumus-cay-kasiklari.jpg', false, 'gumus', 'catal-bicak', 22),
  ('Çay Süzgeci', 'Altın yaldızlı haznesi ve kabartma işlemeli sapıyla bardak üstü çay süzgeci.', null, 'assets/images/gumus-cay-suzgeci.jpg', false, 'gumus', 'gumus-diger', 23),
  ('Melek Figürlü Süt Sürahisi', 'Mat gövde üzerine beyaz melek kabartmalı, jasper tarzı porselen süt sürahisi.', null, 'assets/images/melek-figurlu-surahi.jpg', false, 'porselen', 'porselen-diger', 24),
  ('Kapaklı Bira Maşrapası', 'Kobalt mavi zemin üzerine kabartma figürlü Alman seramik maşrapa. Kalaylı menteşeli kapağıyla orijinal.', null, 'assets/images/bira-masrapasi.jpg', false, 'porselen', 'porselen-diger', 25),
  ('Çiçek Motifli Peçetelik', 'Gümüş kaplama, çiçek motifli ajur işlemeli peçetelik.', null, 'assets/images/gumus-pecetelik.jpg', true, 'gumus', 'gumus-diger', 26)
on conflict do nothing;
