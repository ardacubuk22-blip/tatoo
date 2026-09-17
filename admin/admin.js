import { getSupabase, formatPrice } from "../js/store.js";

const el = (id) => document.getElementById(id);
const BUCKET = "product-images";

const setupNotice = el("setupNotice");
const loginView = el("loginView");
const appView = el("appView");
const logoutButton = el("logoutButton");
const productForm = el("productForm");
const productList = el("productList");
const orderList = el("orderList");
const settingsForm = el("settingsForm");

let supabase = null;

try {
  supabase = await getSupabase();
} catch (error) {
  console.error(error);
  setupNotice.querySelector("h2").textContent = "Bağlantı kurulamadı";
  setupNotice.querySelector("p").textContent =
    "Supabase kütüphanesi yüklenemedi. İnternet bağlantınızı kontrol edip sayfayı yenileyin.";
}

if (supabase) {
  start();
} else {
  setupNotice.hidden = false;
}

async function start() {
  const { data } = await supabase.auth.getSession();
  showView(Boolean(data.session));

  el("loginForm").addEventListener("submit", handleLogin);
  logoutButton.addEventListener("click", handleLogout);
  productForm.addEventListener("submit", handleProductSubmit);
  el("productFormReset").addEventListener("click", resetProductForm);
  settingsForm.addEventListener("submit", handleSettingsSubmit);

  document.querySelectorAll(".admin-tab").forEach((tab) => {
    tab.addEventListener("click", () => selectTab(tab.dataset.tab));
  });
}

function showView(isLoggedIn) {
  loginView.hidden = isLoggedIn;
  appView.hidden = !isLoggedIn;
  logoutButton.hidden = !isLoggedIn;
  if (isLoggedIn) {
    loadProducts();
    loadOrders();
    loadSettings();
  }
}

function selectTab(name) {
  document.querySelectorAll(".admin-tab").forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.tab === name);
  });
  document.querySelectorAll(".admin-panel").forEach((panel) => {
    panel.hidden = panel.dataset.panel !== name;
  });
}

// --- Oturum -------------------------------------------------------------

async function handleLogin(event) {
  event.preventDefault();
  const status = el("loginStatus");
  const { email, password } = Object.fromEntries(new FormData(event.currentTarget));
  status.textContent = "Giriş yapılıyor…";

  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) {
    status.textContent = "Giriş başarısız. E-posta veya şifre hatalı.";
    return;
  }
  status.textContent = "";
  event.currentTarget.reset();
  showView(true);
}

async function handleLogout() {
  await supabase.auth.signOut();
  showView(false);
}

// --- Ürünler ------------------------------------------------------------

async function loadProducts() {
  const { data, error } = await supabase
    .from("products")
    .select("*")
    .order("sort_order", { ascending: true })
    .order("created_at", { ascending: false });

  if (error) {
    productList.textContent = "Ürünler yüklenemedi.";
    return;
  }
  renderProducts(data);
}

function renderProducts(products) {
  if (!products.length) {
    productList.textContent = "Henüz ürün eklenmemiş.";
    return;
  }

  productList.replaceChildren(
    ...products.map((product) => {
      const row = document.createElement("div");
      row.className = "admin-row";

      const thumb = document.createElement("div");
      thumb.className = "admin-thumb";
      if (product.image_url) {
        const img = document.createElement("img");
        img.src = product.image_url;
        img.alt = product.title;
        thumb.append(img);
      }

      const info = document.createElement("div");
      info.className = "admin-row-info";
      const title = document.createElement("strong");
      title.textContent = product.title;
      const meta = document.createElement("span");
      meta.textContent = [formatPrice(product.price), product.is_sold ? "Satıldı" : "Satışta"]
        .filter(Boolean)
        .join(" · ");
      info.append(title, meta);

      const actions = document.createElement("div");
      actions.className = "admin-row-actions";
      actions.append(
        makeButton("Düzenle", () => fillProductForm(product)),
        makeButton(product.is_sold ? "Satışa Al" : "Satıldı", () =>
          toggleSold(product)
        ),
        makeButton("Sil", () => deleteProduct(product), "danger")
      );

      row.append(thumb, info, actions);
      return row;
    })
  );
}

function makeButton(label, onClick, variant) {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = label;
  if (variant) button.classList.add(variant);
  button.addEventListener("click", onClick);
  return button;
}

function fillProductForm(product) {
  productForm.id.value = product.id;
  productForm.title.value = product.title ?? "";
  productForm.description.value = product.description ?? "";
  productForm.price.value = product.price ?? "";
  productForm.sort_order.value = product.sort_order ?? 0;
  productForm.is_sold.checked = Boolean(product.is_sold);
  productForm.image.value = "";

  const hint = el("currentImageHint");
  hint.textContent = product.image_url
    ? "Mevcut fotoğraf korunur. Değiştirmek için yeni dosya seçin."
    : "";
  hint.hidden = !product.image_url;

  el("productFormTitle").textContent = "Ürünü Düzenle";
  el("productFormReset").hidden = false;
  productForm.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetProductForm() {
  productForm.reset();
  productForm.id.value = "";
  el("productFormTitle").textContent = "Yeni Ürün";
  el("productFormReset").hidden = true;
  el("currentImageHint").hidden = true;
  el("productStatus").textContent = "";
}

async function uploadImage(file) {
  const extension = file.name.split(".").pop().toLowerCase();
  const path = `${crypto.randomUUID()}.${extension}`;
  const { error } = await supabase.storage.from(BUCKET).upload(path, file);
  if (error) throw error;
  return supabase.storage.from(BUCKET).getPublicUrl(path).data.publicUrl;
}

async function handleProductSubmit(event) {
  event.preventDefault();
  const status = el("productStatus");
  const form = event.currentTarget;
  const file = form.image.files[0];

  status.textContent = "Kaydediliyor…";

  const product = {
    title: form.title.value.trim(),
    description: form.description.value.trim() || null,
    price: form.price.value === "" ? null : Number(form.price.value),
    sort_order: Number(form.sort_order.value) || 0,
    is_sold: form.is_sold.checked,
  };

  try {
    if (file) product.image_url = await uploadImage(file);

    const id = form.id.value;
    const { error } = id
      ? await supabase.from("products").update(product).eq("id", id)
      : await supabase.from("products").insert(product);
    if (error) throw error;

    resetProductForm();
    status.textContent = "Kaydedildi.";
    loadProducts();
  } catch (error) {
    console.error(error);
    status.textContent = "Kaydedilemedi. Lütfen tekrar deneyin.";
  }
}

async function toggleSold(product) {
  const { error } = await supabase
    .from("products")
    .update({ is_sold: !product.is_sold })
    .eq("id", product.id);
  if (error) {
    console.error(error);
    return;
  }
  loadProducts();
}

async function deleteProduct(product) {
  if (!confirm(`"${product.title}" silinsin mi?`)) return;
  const { error } = await supabase.from("products").delete().eq("id", product.id);
  if (error) {
    console.error(error);
    return;
  }
  loadProducts();
}

// --- Siparişler ---------------------------------------------------------

const STATUS_LABELS = {
  new: "Yeni",
  contacted: "İletişime geçildi",
  completed: "Tamamlandı",
  cancelled: "İptal",
};

async function loadOrders() {
  const { data, error } = await supabase
    .from("orders")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    orderList.textContent = "Siparişler yüklenemedi.";
    return;
  }
  renderOrders(data);
}

function renderOrders(orders) {
  if (!orders.length) {
    orderList.textContent = "Henüz sipariş yok.";
    return;
  }

  orderList.replaceChildren(
    ...orders.map((order) => {
      const row = document.createElement("div");
      row.className = "admin-row admin-row-order";

      const info = document.createElement("div");
      info.className = "admin-row-info";

      const name = document.createElement("strong");
      name.textContent = order.customer_name;

      const contact = document.createElement("span");
      contact.textContent = [order.customer_phone, order.customer_email]
        .filter(Boolean)
        .join(" · ");

      const meta = document.createElement("span");
      meta.textContent = [
        order.product_title,
        new Date(order.created_at).toLocaleString("tr-TR"),
      ]
        .filter(Boolean)
        .join(" · ");

      info.append(name, contact, meta);

      if (order.note) {
        const note = document.createElement("p");
        note.className = "admin-note";
        note.textContent = order.note;
        info.append(note);
      }

      const actions = document.createElement("div");
      actions.className = "admin-row-actions";

      const select = document.createElement("select");
      Object.entries(STATUS_LABELS).forEach(([value, label]) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = label;
        if (order.status === value) option.selected = true;
        select.append(option);
      });
      select.addEventListener("change", () => updateOrderStatus(order, select.value));

      actions.append(select, makeButton("Sil", () => deleteOrder(order), "danger"));

      row.append(info, actions);
      return row;
    })
  );
}

async function updateOrderStatus(order, status) {
  const { error } = await supabase.from("orders").update({ status }).eq("id", order.id);
  if (error) console.error(error);
}

async function deleteOrder(order) {
  if (!confirm(`${order.customer_name} kaydı silinsin mi?`)) return;
  const { error } = await supabase.from("orders").delete().eq("id", order.id);
  if (error) {
    console.error(error);
    return;
  }
  loadOrders();
}

// --- Ayarlar ------------------------------------------------------------

async function loadSettings() {
  const { data, error } = await supabase.from("site_settings").select("key, value");
  if (error) return;

  const settings = Object.fromEntries(data.map(({ key, value }) => [key, value]));
  Array.from(settingsForm.elements).forEach((field) => {
    if (field.name && settings[field.name] != null) field.value = settings[field.name];
  });
}

async function handleSettingsSubmit(event) {
  event.preventDefault();
  const status = el("settingsStatus");
  status.textContent = "Kaydediliyor…";

  const rows = Array.from(event.currentTarget.elements)
    .filter((field) => field.name)
    .map((field) => ({ key: field.name, value: field.value.trim() }));

  const { error } = await supabase.from("site_settings").upsert(rows);
  status.textContent = error ? "Kaydedilemedi." : "Kaydedildi.";
  if (error) console.error(error);
}
