import ArtCard from "./ArtCard";
import { galleryItems } from "./gallery-data";

export default function Gallery() {
  return (
    <section id="galeri" className="mx-auto max-w-6xl px-6 py-20">
      <div className="mb-12 text-center">
        <h2 className="font-display text-3xl text-white sm:text-4xl">Portföyümüz</h2>
        <p className="mt-3 text-neutral-400">
          Stüdyomuzda yapılan çalışmalardan örnekler. (Örnek/placeholder görseller)
        </p>
      </div>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {galleryItems.map((item) => (
          <ArtCard key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}
