export default function Header() {
  return (
    <header className="sticky top-0 z-10 border-b border-white/10 bg-ink/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <span className="font-display text-xl tracking-widest text-gold">TATOO</span>
        <nav className="hidden gap-8 text-sm text-neutral-300 sm:flex">
          <a href="#galeri" className="transition-colors hover:text-gold">
            Galeri
          </a>
          <a href="#sanatcilar" className="transition-colors hover:text-gold">
            Sanatçılar
          </a>
          <a href="#iletisim" className="transition-colors hover:text-gold">
            İletişim
          </a>
        </nav>
        <a
          href="#iletisim"
          className="rounded border border-gold px-4 py-2 text-sm text-gold transition-colors hover:bg-gold hover:text-ink"
        >
          Randevu Al
        </a>
      </div>
    </header>
  );
}
