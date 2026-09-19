export type GalleryItem = {
  id: string;
  title: string;
  style: string;
  artist: string;
  icon: "rose" | "skull" | "mandala" | "compass" | "snake" | "dagger" | "wave" | "arrow";
  gradient: string;
};

export const galleryItems: GalleryItem[] = [
  {
    id: "1",
    title: "Ölümsüz Gül",
    style: "Fine Line",
    artist: "Deniz K.",
    icon: "rose",
    gradient: "from-rose-900 via-red-950 to-black",
  },
  {
    id: "2",
    title: "Sessiz Kafatası",
    style: "Blackwork",
    artist: "Mert A.",
    icon: "skull",
    gradient: "from-neutral-800 via-neutral-900 to-black",
  },
  {
    id: "3",
    title: "Ruhani Mandala",
    style: "Geometrik",
    artist: "Selin Y.",
    icon: "mandala",
    gradient: "from-indigo-950 via-purple-950 to-black",
  },
  {
    id: "4",
    title: "Kayıp Pusula",
    style: "Traditional",
    artist: "Deniz K.",
    icon: "compass",
    gradient: "from-amber-900 via-yellow-950 to-black",
  },
  {
    id: "5",
    title: "Bilge Yılan",
    style: "Japon",
    artist: "Cem T.",
    icon: "snake",
    gradient: "from-emerald-950 via-green-950 to-black",
  },
  {
    id: "6",
    title: "Sadık Hançer",
    style: "Traditional",
    artist: "Mert A.",
    icon: "dagger",
    gradient: "from-slate-800 via-slate-900 to-black",
  },
  {
    id: "7",
    title: "Sonsuz Dalga",
    style: "Minimal",
    artist: "Selin Y.",
    icon: "wave",
    gradient: "from-sky-950 via-blue-950 to-black",
  },
  {
    id: "8",
    title: "Doğru Yön",
    style: "Fine Line",
    artist: "Cem T.",
    icon: "arrow",
    gradient: "from-stone-800 via-stone-900 to-black",
  },
];
