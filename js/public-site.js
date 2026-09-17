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

  if (!product.is_sold) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn btn-small";
    button.textContent = "Sipariş / Bilgi Al";
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
try {
  if (await getSupabase()) {
    const [products, settings] = await Promise.all([fetchProducts(), fetchSettings()]);
    if (products?.length) renderProducts(products);
    if (settings) applySettings(settings);
  }
} catch (error) {
  console.error("İçerik yüklenemedi:", error);
}
