import {
  getSupabase,
  fetchProducts,
  fetchSettings,
  createOrder,
  toPhoneLink,
  formatPrice,
} from "./store.js";

const safeImageUrl = (url) =>
  /^(https?:\/\/|assets\/)/.test(url || "") ? url : "";

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
    img.src = src;
    img.alt = product.title;
    img.loading = "lazy";
    imgWrap.append(img);
  }
  if (product.is_sold) {
    const badge = document.createElement("span");
    badge.className = "badge-sold";
    badge.textContent = "Satıldı";
    imgWrap.append(badge);
  }

  const body = document.createElement("div");
  body.className = "item-body";

  const title = document.createElement("h3");
  title.textContent = product.title;
  body.append(title);

  if (product.description) {
    const desc = document.createElement("p");
    desc.textContent = product.description;
    body.append(desc);
  }

  const price = formatPrice(product.price);
  if (price) {
    const priceEl = document.createElement("p");
    priceEl.className = "item-price";
    priceEl.textContent = product.is_sold ? `${price} — Satıldı` : price;
    body.append(priceEl);
  }

  const wa = document.createElement("a");
  wa.className = "btn btn-whatsapp";
  wa.target = "_blank";
  wa.rel = "noopener";
  wa.dataset.waProduct = "";
  wa.dataset.waText = product.is_sold
    ? `Merhaba! Sitenizdeki ${product.title} satılmış görünüyor, benzer bir parçanız var mı?`
    : `Merhaba! Sitenizdeki ${product.title} ile ilgileniyorum.`;
  wa.textContent = product.is_sold ? "Benzerini Sor" : "WhatsApp ile Sor";
  body.append(wa);

  if (!product.is_sold) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn-link";
    button.textContent = "Sipariş / Bilgi Formu";
    button.addEventListener("click", () => openOrderModal(product));
    body.append(button);
  }

  article.append(imgWrap, body);
  return article;
}

function renderProducts(products) {
  document.querySelectorAll("[data-products]").forEach((container) => {
    const limit = Number(container.dataset.limit) || products.length;
    const visible = products.slice(0, limit);
    if (!visible.length) return;
    container.replaceChildren(...visible.map(buildProductCard));
  });
}

// --- Kategori filtresi ---------------------------------------------------

const filterList = document.getElementById("filtersList");

function applyFilter(slug) {
  const cards = document.querySelectorAll("[data-products] .item");
  let shown = 0;

  cards.forEach((card) => {
    const match =
      slug === "all" ||
      card.dataset.category === slug ||
      card.dataset.subcategory === slug;
    card.hidden = !match;
    if (match) shown += 1;
  });

  filterList.querySelectorAll("a").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.filter === slug);
  });

  const label = filterList.querySelector(`a[data-filter="${slug}"]`);
  const count = document.getElementById("resultCount");
  count.textContent =
    slug === "all"
      ? `${shown} ürün gösteriliyor`
      : `${label?.childNodes[0].textContent.trim() ?? ""} — ${shown} ürün`;
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
  applyFilter(currentFilter());
}

// Her ürün kartındaki WhatsApp bağlantısını, güncel numara ve sayfa adresiyle kurar.
function wireProductWhatsApp(phone) {
  const number = toPhoneLink(phone).replace("+", "");
  if (!number) return;
  const pageUrl = location.origin + location.pathname;

  document.querySelectorAll("[data-wa-product]").forEach((link) => {
    const message = `${link.dataset.waText}\n${pageUrl}`;
    link.href = `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
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
      <button type="button" class="modal-close" aria-label="Kapat">&times;</button>
      <h3 id="orderModalTitle">Sipariş / Bilgi Talebi</h3>
      <p class="modal-product"></p>
      <form>
        <label>Ad Soyad *<input type="text" name="customer_name" required /></label>
        <label>Telefon *<input type="tel" name="customer_phone" required /></label>
        <label>E-posta<input type="email" name="customer_email" /></label>
        <label>Notunuz<textarea name="note" rows="3"></textarea></label>
        <button type="submit" class="btn">Gönder</button>
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
  modal.querySelector(".modal-product").textContent = product.title;
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
  status.textContent = "Gönderiliyor…";

  try {
    await createOrder({
      product_id: activeProduct?.id ?? null,
      product_title: activeProduct?.title ?? null,
      customer_name: data.customer_name,
      customer_phone: data.customer_phone,
      customer_email: data.customer_email || null,
      note: data.note || null,
    });
    status.textContent = "Talebiniz alındı, en kısa sürede size dönüş yapacağız.";
    form.reset();
  } catch (error) {
    console.error(error);
    status.textContent = "Gönderilemedi. Lütfen WhatsApp veya telefon ile iletişime geçin.";
  } finally {
    submitButton.disabled = false;
  }
}

// --- Başlat -------------------------------------------------------------

// Veri çekilemezse (veya Supabase henüz kurulmadıysa) sayfadaki statik
// içerik olduğu gibi kalır.
// Statik kartlardaki bağlantılara sayfa adresini ekle (numara zaten markup'ta).
const markupPhone = document
  .querySelector("[data-wa-product]")
  ?.href.match(/wa\.me\/(\d+)/)?.[1];
if (markupPhone) wireProductWhatsApp(markupPhone);

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
  console.error("İçerik yüklenemedi:", error);
}
