# Home Antique Home — سایت عتیقه‌فروشی

یک سایت چندصفحه‌ای ساده و شیک برای معرفی کسب‌وکار عتیقه‌فروشی
**Home Antique Home** (استانبول، @homeantiquehome)، با ساختار الهام‌گرفته از
سایت‌های گالری عتیقه (منوی Ana Sayfa / Hakkımızda / Vitrin / Galeri /
İletişim، رنگ سبز زیتونی و طلایی، فونت‌های Playfair Display و Poppins).

## ساختار پروژه

```
index.html          صفحه اصلی
hakkimizda.html      درباره ما (Hakkımızda)
showroom.html        ویترین (Vitrin)
galeri.html          گالری محصولات
iletisim.html        تماس با ما (İletişim)
admin/               پنل ادمین (ورود با ایمیل و رمز عبور)
css/style.css        استایل سایت
js/script.js         منوی موبایل و هایلایت لینک فعال
js/config.js         کلیدهای Supabase (باید پر بشن — به SETUP.md نگاه کنید)
js/store.js          لایه‌ی داده (محصولات، تنظیمات، سفارش‌ها)
js/public-site.js    نمایش پویای محصولات و فرم سفارش در صفحات عمومی
supabase/schema.sql  ساختار دیتابیس و داده‌ی اولیه
assets/images/        عکس‌های واقعی محصولات (برش‌خورده از اینستاگرام @homeantiquehome)
```

## پنل ادمین

مشتری از مسیر `/admin/` با ایمیل و رمز عبور وارد می‌شه و می‌تونه محصولات
(عکس، قیمت، وضعیت فروش)، متن‌های سایت و اطلاعات تماس رو تغییر بده و سفارش‌های
ثبت‌شده رو ببینه. مراحل راه‌اندازی در **[SETUP.md](SETUP.md)** توضیح داده شده.

تا وقتی Supabase تنظیم نشده، سایت همین محتوای استاتیک فعلی رو نشون می‌ده.

## اطلاعات تماس

- آدرس: Bağdat Caddesi, İstanbul
- تلفن / واتساپ: 0555 737 09 33
- ایمیل: homeantiquehome@gmail.com
- اینستاگرام: [@homeantiquehome](https://www.instagram.com/homeantiquehome)

تمام محتوای سایت (نام برند، متن‌ها، عکس‌های محصولات، اطلاعات تماس و نقشه)
با اطلاعات واقعی پر شده است.

## اجرای محلی

فایل `index.html` را مستقیم در مرورگر باز کنید، یا با یک سرور ساده:

```bash
npx serve .
```

## انتشار روی GitHub Pages

1. به تنظیمات ریپو در گیت‌هاب بروید: Settings → Pages
2. Source را روی شاخه‌ی مورد نظر (مثلاً `main`) و پوشه‌ی `/ (root)` قرار دهید
3. آدرس سایت بعد از چند دقیقه در همان صفحه نمایش داده می‌شود
