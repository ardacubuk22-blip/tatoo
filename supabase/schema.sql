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
  sort_order integer not null default 0,
  created_at timestamptz not null default now()
);

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
  ('hero_title', 'Otantik Antikalar, Kalıcı Hikayeler'),
  ('hero_subtitle', 'Özgünlüğü ve geçmişi garantili, özenle seçilmiş antika ve koleksiyon eşyaları'),
  ('about_short', 'Home Antique Home, İstanbul merkezli bir antika ve koleksiyon markasıdır. Gümüş, kristal ve porselenden oluşan özenle seçilmiş parçaları, birer hikaye taşıyan otantik eserler olarak sizlerle buluşturuyoruz.'),
  ('about_long_1', 'Home Antique Home, İstanbul merkezli bir antika ve koleksiyon markasıdır. Gümüş işlemeler, kristal cam eşyalar ve porselen takımlar başta olmak üzere, özenle seçilmiş ve her biri kendi döneminin zanaatkarlığını yansıtan parçaları sizlerle buluşturuyoruz.'),
  ('about_long_2', 'Amacımız, geçmişin özenle işlenmiş eserlerini günümüz evlerine taşımak; her parçanın özgünlüğünü ve hikayesini koruyarak müşterilerimize güvenilir bir alışveriş deneyimi sunmaktır.'),
  ('showroom_text', 'Antikaya tutkunuz ve İstanbul''dan özenle seçilmiş gümüş, kristal ve porselen parçalar sunuyoruz. Koleksiyonumuzda servis kaşıklarından peçeteliklere, bardak takımlarından dekoratif objelere kadar geniş bir yelpaze bulunmaktadır.'),
  ('address', 'Bağdat Caddesi, İstanbul'),
  ('phone', '0555 737 09 33'),
  ('email', 'homeantiquehome@gmail.com'),
  ('instagram_url', 'https://www.instagram.com/homeantiquehome')
on conflict (key) do nothing;

insert into public.products (title, description, price, image_url, is_sold, sort_order) values
  ('Mary Gregory Sürahi ve Bardak Takımı', 'El yapımı beyaz emaye figürlü, mavi cam üzerine altın yaldız detaylı antika set', null, 'assets/images/hero-mary-gregory.jpg', false, 1),
  ('Mary Gregory Başucu Sürahisi', 'Şeffaf cam üzerine el boyaması figürlü antika başucu sürahisi', null, 'assets/images/gallery-mary-gregory-clear.jpg', true, 2),
  ('Porselen Çay Servisi', 'Kabartma desenli, beyaz porselen çay ve kahve servisi', 11500, 'assets/images/porselen-cay-servisi.jpg', false, 3),
  ('WMF Kapaklı Kutu', 'WMF imzalı, kabartma desenli ayaklı kapaklı kutu', 10000, 'assets/images/wmf-gumus-kutu.jpg', false, 4),
  ('Manzara Desenli Tabak Seti', 'Mavi-beyaz manzara desenli, 4 parça tabak seti', 6500, 'assets/images/manzara-tabak-seti.jpg', false, 5),
  ('Porselen Fincan Takımı', 'Melek kabartmalı, altın yaldız detaylı 3 parça porselen takım', 5500, 'assets/images/porselen-fincan-takimi.jpg', false, 6),
  ('Zincir Askılı Vintage Çanta', 'Kuş figürlü kapak detaylı, zincir askılı çanta', 5500, 'assets/images/pirinc-zincirli-canta.jpg', false, 7),
  ('Amber Cam Kadeh (6 Adet)', 'Amber renkli, dilimli gövdeli ayaklı kadeh', 4750, 'assets/images/amber-kadeh.jpg', false, 8),
  ('Pirinç Şamdan (Çift)', 'Kazıma desenli, çift pirinç şamdan', null, 'assets/images/pirinc-samdan.jpg', false, 9),
  ('Christofle Çatal Bıçak Takımı', 'Christofle imzalı çatal bıçak ve servis takımı', null, 'assets/images/christofle-catal-bicak-takimi.jpg', false, 10),
  ('Çiçek Desenli Çerezlik Tabaklar', 'Gül desenli porselen çerezlik tabaklar ve işlemeli baharat kaşıkları', null, 'assets/images/cicek-desenli-tabaklar.jpg', false, 11),
  ('Mavi-Beyaz Servis Tabakları', 'Manzara desenli, kulplu dikdörtgen porselen servis tabakları', null, 'assets/images/mavi-beyaz-servis-tabaklari.jpg', false, 12),
  ('Çay Kaşığı Takımı', 'Klasik desenli, işlemeli çay kaşığı takımı', null, 'assets/images/gumus-cay-kasiklari.jpg', false, 13),
  ('Çay Süzgeci', 'Altın yaldızlı hazneli, kabartma saplı çay süzgeci', null, 'assets/images/gumus-cay-suzgeci.jpg', false, 14),
  ('Christofle Malmaison Tepsi', 'Christofle''nin ikonik Malmaison koleksiyonundan, inci bordürlü servis tepsisi', null, 'assets/images/gumus-servis-tepsisi.jpg', false, 15),
  ('Kapaklı Bira Maşrapası', 'Kalaylı kapaklı, kabartma figürlü seramik bira maşrapası', null, 'assets/images/bira-masrapasi.jpg', false, 16),
  ('Gümüş Çikolata Potu', '1868-1888 Paris yapımı, Paillard Frères damgalı 800 ayar gümüş çikolata potu', null, 'assets/images/gumus-cikolata-potu.jpg', false, 17),
  ('Gümüş Kaplama Şamdan (Çift)', 'İnci bordürlü, uzun formlu gümüş kaplama şamdan çifti', null, 'assets/images/gumus-samdan-cift.jpg', false, 18),
  ('Gümüş Kaplama Mumluk Koleksiyonu', 'Farklı boy ve formlarda gümüş kaplama mumluklar; bazıları çift olarak', null, 'assets/images/mumluk-koleksiyonu.jpg', false, 19),
  ('Oval Gümüş Kaplama Tepsi', 'İnci bordürlü, ortası kabartma madalyonlu oval servis tepsisi', null, 'assets/images/oval-gumus-tepsi.jpg', false, 20),
  ('Melek Figürlü Süt Sürahisi', 'Mat gövde üzerine beyaz melek kabartmalı porselen süt sürahisi', null, 'assets/images/melek-figurlu-surahi.jpg', false, 21),
  ('Çiçek Motifli Peçetelik', 'Gümüş kaplama, çiçek motifli ajur işlemeli peçetelik', null, 'assets/images/gumus-pecetelik.jpg', true, 22)
on conflict do nothing;
