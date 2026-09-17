// Supabase bağlantı bilgileri.
// Supabase panelinde: Project Settings > API bölümünden alın ve buraya yapıştırın.
// anon key herkese açık olacak şekilde tasarlanmıştır; veriler RLS ile korunur.
// (Kurulum adımları için SETUP.md dosyasına bakın.)

export const SUPABASE_URL = "";
export const SUPABASE_ANON_KEY = "";

export const isSupabaseConfigured = () =>
  Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);
