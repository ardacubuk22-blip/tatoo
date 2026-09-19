import {
  ArrowIcon,
  CompassIcon,
  DaggerIcon,
  MandalaIcon,
  RoseIcon,
  SkullIcon,
  SnakeIcon,
  WaveIcon,
} from "./icons";
import type { GalleryItem } from "./gallery-data";

const iconMap = {
  rose: RoseIcon,
  skull: SkullIcon,
  mandala: MandalaIcon,
  compass: CompassIcon,
  snake: SnakeIcon,
  dagger: DaggerIcon,
  wave: WaveIcon,
  arrow: ArrowIcon,
};

export default function ArtCard({ item }: { item: GalleryItem }) {
  const Icon = iconMap[item.icon];

  return (
    <div className="group relative overflow-hidden rounded-lg border border-white/10 bg-neutral-900 transition-transform duration-300 hover:-translate-y-1 hover:border-gold/50">
      <div
        className={`flex aspect-square items-center justify-center bg-gradient-to-br ${item.gradient}`}
      >
        <Icon className="h-24 w-24 text-gold/90 drop-shadow-[0_0_12px_rgba(201,162,75,0.35)] transition-transform duration-300 group-hover:scale-110" />
      </div>
      <div className="p-4">
        <div className="flex items-center justify-between">
          <h3 className="font-display text-lg text-white">{item.title}</h3>
          <span className="rounded-full border border-gold/40 px-2 py-0.5 text-xs uppercase tracking-wide text-gold">
            {item.style}
          </span>
        </div>
        <p className="mt-1 text-sm text-neutral-400">Sanatçı: {item.artist}</p>
      </div>
    </div>
  );
}
