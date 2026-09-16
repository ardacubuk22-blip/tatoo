# سایت عتیقه‌فروشی

یک سایت چندصفحه‌ای ساده و شیک برای معرفی یک کسب‌وکار عتیقه‌سازی/عتیقه‌فروشی
(به زبان ترکی)، با ساختار الهام‌گرفته از سایت‌های گالری عتیقه (منوی
Ana Sayfa / Hakkımızda / Vitrin / Galeri / İletişim، رنگ سبز زیتونی و
طلایی، فونت‌های Playfair Display و Poppins).

## ساختار پروژه

```
index.html          صفحه اصلی
hakkimizda.html      درباره ما (Hakkımızda)
showroom.html        ویترین (Vitrin)
galeri.html          گالری محصولات
iletisim.html        تماس با ما (İletişim)
css/style.css        استایل سایت
js/script.js         منوی موبایل و هایلایت لینک فعال
assets/images/        محل قرارگیری عکس‌های واقعی
```

## شخصی‌سازی

در تمام فایل‌های HTML موارد زیر را با اطلاعات واقعی جایگزین کنید:

- `[Antika Dükkanı Adı]` در تگ `<title>`، هدر و فوتر همه‌ی صفحات
- متن‌های `hakkimizda.html` و `showroom.html` (تاریخچه، سال تاسیس، تخصص)
- عکس‌ها: هر `placeholder-img` را با `<img src="assets/images/xxx.jpg" alt="...">` جایگزین کنید
- کارت‌های `galeri.html`: نام و توضیح هر قطعه (و برچسب `badge-sold` برای قطعات فروخته‌شده)
- در `iletisim.html`: `[Mağaza Adresi]`، `[E-posta Adresi]`، `[Telefon Numarası]`، لینک اینستاگرام و نقشه

## اجرای محلی

فایل `index.html` را مستقیم در مرورگر باز کنید، یا با یک سرور ساده:

```bash
npx serve .
```

## انتشار روی GitHub Pages

1. به تنظیمات ریپو در گیت‌هاب بروید: Settings → Pages
2. Source را روی شاخه‌ی مورد نظر (مثلاً `main`) و پوشه‌ی `/ (root)` قرار دهید
3. آدرس سایت بعد از چند دقیقه در همان صفحه نمایش داده می‌شود
