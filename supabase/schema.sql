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

insert into public.products (title, description, image_url, is_sold, sort_order) values
  ('Mary Gregory Sürahi ve Bardak Takımı', 'El yapımı beyaz emaye figürlü, mavi cam üzerine altın yaldız detaylı antika set', 'assets/images/hero-mary-gregory.jpg', false, 1),
  ('Mary Gregory Başucu Sürahisi', 'Şeffaf cam üzerine el boyaması figürlü antika başucu sürahisi', 'assets/images/gallery-mary-gregory-clear.jpg', true, 2),
  ('Gümüş İşlemeli Servis Kaşığı', 'Melek figürlü, oyma işçilikli antika gümüş kaşık', 'assets/images/gallery-spoon-1.jpg', false, 3),
  ('Gümüş İşlemeli Kaşık', 'Çiçek desenli sap işçiliğine sahip antika gümüş kaşık', 'assets/images/gallery-spoon-2.jpg', false, 4),
  ('Gümüş Ayaklı Bardak Tutucusu', 'Filigran işlemeli, cam bardaklı antika set parçası', 'assets/images/gallery-cup-holder.jpg', false, 5),
  ('Gümüş Peçetelik', 'Melek figürlü, dökme gümüş antika peçetelik', 'assets/images/gallery-napkin-holder.jpg', false, 6)
on conflict do nothing;
