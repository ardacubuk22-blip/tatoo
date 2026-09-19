export default function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-white/10 px-6 py-28 text-center">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(201,162,75,0.12),_transparent_60%)]" />
      <div className="relative mx-auto max-w-2xl">
        <p className="mb-3 text-sm uppercase tracking-[0.3em] text-gold">Dövme Stüdyosu</p>
        <h1 className="font-display text-4xl leading-tight text-white sm:text-6xl">
          Tenin Üzerine <span className="text-gold">Sanat</span>
        </h1>
        <p className="mt-6 text-neutral-400">
          Fine line, blackwork, traditional ve geometrik tarzlarda özgün tasarımlar.
          Aşağıda ekibimizin çalışmalarından bir seçki bulabilirsiniz.
        </p>
      </div>
    </section>
  );
}
