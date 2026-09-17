import { SUPABASE_URL, SUPABASE_ANON_KEY, isSupabaseConfigured } from "./config.js";

const SDK_URL = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm";

let clientPromise;

// SDK yalnızca Supabase yapılandırılmışsa indirilir.
export function getSupabase() {
  if (!isSupabaseConfigured()) return Promise.resolve(null);
  if (!clientPromise) {
    clientPromise = import(SDK_URL).then(({ createClient }) =>
      createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
    );
  }
  return clientPromise;
}

export async function fetchProducts() {
  const supabase = await getSupabase();
  if (!supabase) return null;
  const { data, error } = await supabase
    .from("products")
    .select("*")
    .order("sort_order", { ascending: true })
    .order("created_at", { ascending: false });
  if (error) throw error;
  return data;
}

export async function fetchSettings() {
  const supabase = await getSupabase();
  if (!supabase) return null;
  const { data, error } = await supabase.from("site_settings").select("key, value");
  if (error) throw error;
  return Object.fromEntries(data.map(({ key, value }) => [key, value]));
}

export async function createOrder(order) {
  const supabase = await getSupabase();
  if (!supabase) throw new Error("Supabase yapılandırılmamış.");
  const { error } = await supabase.from("orders").insert(order);
  if (error) throw error;
}

// "0555 737 09 33" -> "+905557370933"
export function toPhoneLink(phone) {
  const digits = String(phone || "").replace(/\D/g, "");
  if (!digits) return "";
  if (digits.startsWith("90")) return `+${digits}`;
  return `+90${digits.replace(/^0/, "")}`;
}

export function formatPrice(price) {
  if (price === null || price === undefined || price === "") return "";
  return `${Number(price).toLocaleString("tr-TR")} ₺`;
}
