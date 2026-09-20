import {
  getSupabase,
  fetchProducts,
  fetchSettings,
  createOrder,
  toPhoneLink,
  formatPrice,
} from "./store.js";

const safeImageUrl = (url) =>
  /^(https?:\/\/|\.\.\/assets\/|assets\/)/.test(url || "") ? url : "";

// İngilizce sayfalar en/ altında; görsel yolları bir üst dizine bakar.
const LANG = document.documentElement.lang === "en" ? "en" : "tr";
const IMAGE_PREFIX = LANG === "en" ? "../" : "";

const T = {
  tr: {
    sold: "Satıldı",
    ask: "WhatsApp ile Sor",
    askSimilar: "Benzerini Sor",
    orderForm: "Sipariş / Bilgi Formu",
    waInterested: (t) => `Merhaba! Sitenizdeki ${t} ile ilgileniyorum.`,
    waSimilar: (t) =>
      `Merhaba! Sitenizdeki ${t} satılmış görünüyor, benzer bir parçanız var mı?`,
    showing: (n) => `${n} ürün gösteriliyor`,
    filtered: (parts, n) => `${parts} — ${n} ürün`,
    modalTitle: "Sipariş / Bilgi Talebi",
    close: "Kapat",
    name: "Ad Soyad",
    phone: "Telefon",
    email: "E-posta",
    note: "Notunuz",
    send: "Gönder",
    sending: "Gönderiliyor…",
    sent: "Talebiniz alındı, en kısa sürede size dönüş yapacağız.",
    failed: "Gönderilemedi. Lütfen WhatsApp veya telefon ile iletişime geçin.",
    loadError: "İçerik yüklenemedi:",
  },
  en: {
    sold: "Sold",
    ask: "Ask on WhatsApp",
    askSimilar: "Ask for Similar",
    orderForm: "Order / Enquiry Form",
    waInterested: (t) => `Hello! I am interested in the ${t} on your website.`,
    waSimilar: (t) =>
      `Hello! The ${t} on your website appears to be sold — do you have anything similar?`,
    showing: (n) => `${n} pieces shown`,
    filtered: (parts, n) => `${parts} — ${n} pieces`,
    modalTitle: "Order / Enquiry",
    close: "Close",
    name: "Full Name",
    phone: "Phone",
    email: "Email",
    note: "Your note",
    send: "Send",
    sending: "Sending…",
    sent: "We have your request and will come back to you shortly.",
    failed: "Could not send. Please reach us on WhatsApp or by phone.",
    loadError: "Could not load content:",
  },
}[LANG];

// Veritabanındaki ingilizce alan doluysa onu, değilse türkçesini kullanır.
const productTitle = (p) => (LANG === "en" && p.title_en) || p.title;
const productDescription = (p) =>
  (LANG === "en" && p.description_en) || p.description;

function buildProductCard(product) {
  const article = document.createElement("article");
  article.className = "item";
  if (product.category) article.dataset.category = product.category;
  if (product.subcategory) article.dataset.subcategory = product.subcategory;

  const imgWrap = document.createElement("div");
  imgWrap.className = "item-img";
  const src = safeImageUrl(product.image_url);
  if (src) {
    const img = document.createElement("img");
    img.src = src.startsWith("assets/") ? IMAGE_PREFIX + src : src;
    img.alt = productTitle(product);
    img.loading = "lazy";
    imgWrap.append(img);
  }
  if (product.is_sold) {
    const badge = document.createElement("span");
    badge.className = "badge-sold";
    badge.textContent = T.sold;
    imgWrap.append(badge);
  }

  const body = document.createElement("div");
  body.className = "item-body";

  const title = document.createElement("h3");
  title.textContent = productTitle(product);
  body.append(title);

  const description = productDescription(product);
  if (description) {
    const desc = document.createElement("p");
    desc.textContent = description;
    body.append(desc);
  }

  const price = formatPrice(product.price);
  if (price) {
    const priceEl = document.createElement("p");
    priceEl.className = "item-price";
    priceEl.textContent = product.is_sold ? `${price} — ${T.sold}` : price;
    body.append(priceEl);
  }

  const wa = document.createElement("a");
  wa.className = "btn btn-whatsapp";
  wa.target = "_blank";
  wa.rel = "noopener";
  wa.dataset.waProduct = "";
  wa.dataset.waText = product.is_sold
    ? T.waSimilar(productTitle(product))
    : T.waInterested(productTitle(product));
  wa.textContent = product.is_sold ? T.askSimilar : T.ask;
  wa.href = productWhatsAppHref(wa.dataset.waText);
  body.append(wa);

  if (!product.is_sold) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn-link";
    button.textContent = T.orderForm;
    button.addEventListener("click", () => openOrderModal(product));
    body.append(button);
  }

  article.append(imgWrap, body);
  return article;
}

function renderProducts(products) {
  document.querySelectorAll("[data-products]").forEach((container) => {
    // Vitrin yalnızca panelde "Vitrinde göster" işaretlenen parçaları listeler;
    // ana sayfadaki "Yeni Ürünler" ise en son eklenenleri gösterir.
    let pool = products;
    if ("featured" in container.dataset) {
      pool = products.filter((product) => product.is_featured);
    } else if ("newest" in container.dataset) {
      pool = [...products].sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
      );
    }
    const limit = Number(container.dataset.limit) || pool.length;
    const visible = pool.slice(0, limit);
    if (!visible.length) return;
    container.replaceChildren(...visible.map(buildProductCard));
  });
}

// --- Kategori filtresi ---------------------------------------------------

const filterList = document.getElementById("filtersList");
const searchInput = document.getElementById("gallerySearch");

// Türkçe'de I/İ dönüşümü farklı olduğu için yerele duyarlı karşılaştırma.
const normalize = (text) => String(text ?? "").toLocaleLowerCase("tr");

let searchQuery = "";

function applyFilter(slug) {
  const cards = document.querySelectorAll("[data-products] .item");
  const term = normalize(searchQuery);
  let shown = 0;

  cards.forEach((card) => {
    const inCategory =
      slug === "all" ||
      card.dataset.category === slug ||
      card.dataset.subcategory === slug;
    const match = inCategory && (!term || normalize(card.textContent).includes(term));
    card.hidden = !match;
    if (match) shown += 1;
  });

  filterList.querySelectorAll("a").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.filter === slug);
  });

  const label = filterList.querySelector(`a[data-filter="${slug}"]`);
  const parts = [];
  if (slug !== "all") parts.push(label?.childNodes[0].textContent.trim() ?? "");
  if (searchQuery) parts.push(`"${searchQuery}"`);

  const count = document.getElementById("resultCount");
  count.textContent = parts.length
    ? T.filtered(parts.join(" · "), shown)
    : T.showing(shown);

  const empty = document.getElementById("noResults");
  if (empty) empty.hidden = shown > 0;
}

function currentFilter() {
  const slug = location.hash.replace("#", "");
  return slug && filterList.querySelector(`a[data-filter="${slug}"]`) ? slug : "all";
}

function refreshFilterCounts() {
  const cards = [...document.querySelectorAll("[data-products] .item")];
  filterList.querySelectorAll("a").forEach((link) => {
    const slug = link.dataset.filter;
    const total =
      slug === "all"
        ? cards.length
        : cards.filter(
            (c) => c.dataset.category === slug || c.dataset.subcategory === slug
          ).length;
    const badge = link.querySelector("span");
    if (badge) badge.textContent = total;
  });
}

if (filterList) {
  const toggle = document.getElementById("filtersToggle");
  toggle.addEventListener("click", () => {
    const open = filterList.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });

  filterList.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-filter]");
    if (!link) return;
    filterList.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  });

  window.addEventListener("hashchange", () => applyFilter(currentFilter()));

  if (searchInput) {
    // Başlıktaki kutu buraya ?q= ile gelir.
    searchQuery = (new URLSearchParams(location.search).get("q") ?? "").trim();
    searchInput.value = searchQuery;

    searchInput.form?.addEventListener("submit", (event) => event.preventDefault());
    searchInput.addEventListener("input", () => {
      searchQuery = searchInput.value.trim();
      applyFilter(currentFilter());
    });
  }

  applyFilter(currentFilter());
}

// Numara statik markup'tan gelir; yönetim panelinde değiştirilirse güncellenir.
// Veritabanından gelen kartlar da bu numarayla anında bağlantı alır.
let contactNumber =
  document.querySelector("[data-wa-product]")?.href.match(/wa\.me\/(\d+)/)?.[1] ?? "";

function productWhatsAppHref(text) {
  if (!contactNumber) return "";
  const message = `${text}\n${location.origin + location.pathname}`;
  return `https://wa.me/${contactNumber}?text=${encodeURIComponent(message)}`;
}

function wireProductWhatsApp(phone) {
  const number = toPhoneLink(phone).replace("+", "");
  if (number) contactNumber = number;

  document.querySelectorAll("[data-wa-product]").forEach((link) => {
    link.href = productWhatsAppHref(link.dataset.waText);
  });
}

function applySettings(settings) {
  document.querySelectorAll("[data-setting]").forEach((el) => {
    const value = settings[el.dataset.setting];
    if (value) el.textContent = value;
  });

  const phoneLink = toPhoneLink(settings.phone);
  document.querySelectorAll("[data-setting-href]").forEach((el) => {
    const kind = el.dataset.settingHref;
    if (kind === "tel" && phoneLink) el.href = `tel:${phoneLink}`;
    if (kind === "whatsapp" && phoneLink) {
      const message = el.dataset.waText
        ? `?text=${encodeURIComponent(el.dataset.waText)}`
        : "";
      el.href = `https://wa.me/${phoneLink.replace("+", "")}${message}`;
    }
    if (kind === "email" && settings.email) el.href = `mailto:${settings.email}`;
    if (kind === "map" && settings.address)
      el.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(settings.address)}`;
    if (kind === "instagram" && settings.instagram_url)
      el.href = settings.instagram_url;
  });
}

// --- Sipariş formu ------------------------------------------------------

let modal;
let activeProduct = null;

function buildModal() {
  const backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop";
  backdrop.hidden = true;
  backdrop.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="orderModalTitle">
      <button type="button" class="modal-close" aria-label="${T.close}">&times;</button>
      <h3 id="orderModalTitle">${T.modalTitle}</h3>
      <p class="modal-product"></p>
      <form>
        <label>${T.name} *<input type="text" name="customer_name" required /></label>
        <label>${T.phone} *<input type="tel" name="customer_phone" required /></label>
        <label>${T.email}<input type="email" name="customer_email" /></label>
        <label>${T.note}<textarea name="note" rows="3"></textarea></label>
        <button type="submit" class="btn">${T.send}</button>
        <p class="form-status" role="status"></p>
      </form>
    </div>`;

  backdrop.addEventListener("click", (event) => {
    if (event.target === backdrop) closeOrderModal();
  });
  backdrop.querySelector(".modal-close").addEventListener("click", closeOrderModal);
  backdrop.querySelector("form").addEventListener("submit", submitOrder);

  document.body.append(backdrop);
  return backdrop;
}

function openOrderModal(product) {
  if (!modal) modal = buildModal();
  activeProduct = product;
  modal.querySelector(".modal-product").textContent = productTitle(product);
  modal.querySelector("form").reset();
  modal.querySelector(".form-status").textContent = "";
  modal.hidden = false;
}

function closeOrderModal() {
  if (modal) modal.hidden = true;
}

async function submitOrder(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const status = form.querySelector(".form-status");
  const submitButton = form.querySelector("button[type='submit']");
  const data = Object.fromEntries(new FormData(form));

  submitButton.disabled = true;
  status.textContent = T.sending;

  try {
    await createOrder({
      product_id: activeProduct?.id ?? null,
      product_title: activeProduct?.title ?? null,
      customer_name: data.customer_name,
      customer_phone: data.customer_phone,
      customer_email: data.customer_email || null,
      note: data.note || null,
    });
    status.textContent = T.sent;
    form.reset();
  } catch (error) {
    console.error(error);
    status.textContent = T.failed;
  } finally {
    submitButton.disabled = false;
  }
}

// --- Başlat -------------------------------------------------------------

// Veri çekilemezse (veya Supabase henüz kurulmadıysa) sayfadaki statik
// içerik olduğu gibi kalır.
// Statik kartlardaki bağlantılara sayfa adresini ekle.
wireProductWhatsApp(contactNumber);

try {
  if (await getSupabase()) {
    const [products, settings] = await Promise.all([fetchProducts(), fetchSettings()]);
    if (products?.length) {
      renderProducts(products);
      if (filterList) {
        refreshFilterCounts();
        applyFilter(currentFilter());
      }
    }
    if (settings) {
      applySettings(settings);
      wireProductWhatsApp(settings.phone);
    }
  }
} catch (error) {
  console.error(T.loadError, error);
}
