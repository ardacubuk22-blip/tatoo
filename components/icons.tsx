type IconProps = {
  className?: string;
};

export function RoseIcon({ className }: IconProps) {
  const cx = 50;
  const cy = 30;
  const petal = "M50 30 C44 23 44 13 50 8 C56 13 56 23 50 30 Z";

  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <g strokeLinejoin="round">
        {[0, 72, 144, 216, 288].map((angle) => (
          <path key={angle} d={petal} transform={`rotate(${angle} ${cx} ${cy})`} />
        ))}
      </g>
      <circle cx={cx} cy={cy} r="3" />
      <path d="M50 51v32" strokeLinecap="round" />
      <path d="M50 63c8-1 14 4 16 9-8 3-15-1-16-9z" />
      <path d="M50 74c-8-1-14 5-16 10 8 3 15-2 16-10z" />
    </svg>
  );
}

export function SkullIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M50 22c-14 0-24 10-24 23 0 8 4 13 8 17v10h6v-6h6v6h8v-6h6v6h6V62c4-4 8-9 8-17 0-13-10-23-24-23z" />
      <circle cx="41" cy="46" r="5" />
      <circle cx="59" cy="46" r="5" />
      <path d="M47 55l3 6 3-6" />
      <path d="M38 65h24" />
    </svg>
  );
}

export function MandalaIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="1.5">
      <circle cx="50" cy="50" r="30" />
      <circle cx="50" cy="50" r="20" />
      <circle cx="50" cy="50" r="4" />
      {Array.from({ length: 12 }).map((_, i) => {
        const angle = (i * Math.PI) / 6;
        const x1 = 50 + 20 * Math.cos(angle);
        const y1 = 50 + 20 * Math.sin(angle);
        const x2 = 50 + 30 * Math.cos(angle);
        const y2 = 50 + 30 * Math.sin(angle);
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} />;
      })}
      {Array.from({ length: 8 }).map((_, i) => {
        const angle = (i * Math.PI) / 4;
        const x = 50 + 30 * Math.cos(angle);
        const y = 50 + 30 * Math.sin(angle);
        return <circle key={i} cx={x} cy={y} r="3" />;
      })}
    </svg>
  );
}

export function CompassIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="50" cy="50" r="28" />
      <circle cx="50" cy="50" r="2" />
      <path d="M50 22v10M50 68v10M22 50h10M68 50h10" strokeLinecap="round" />
      <path d="M50 32l6 15-6 3-6-3z" />
      <path d="M50 68l6-15-6-3-6 3z" />
    </svg>
  );
}

export function SnakeIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M25 75c10 5 15-5 10-12s-15-5-15-15 12-10 20-6 8 12 18 10 12-12 8-20" strokeLinecap="round" />
      <circle cx="66" cy="30" r="4" />
      <path d="M70 27l6-4" strokeLinecap="round" />
    </svg>
  );
}

export function DaggerIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M50 15v45" strokeLinecap="round" />
      <path d="M38 30h24" />
      <path d="M42 30l8 30 8-30" />
      <path d="M44 60h12v8h-12z" />
      <path d="M50 68v17" strokeLinecap="round" />
    </svg>
  );
}

export function WaveIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M15 40c8-10 16-10 24 0s16 10 24 0 16-10 24 0" strokeLinecap="round" />
      <path d="M15 55c8-10 16-10 24 0s16 10 24 0 16-10 24 0" strokeLinecap="round" />
      <path d="M15 70c8-10 16-10 24 0s16 10 24 0 16-10 24 0" strokeLinecap="round" />
    </svg>
  );
}

export function ArrowIcon({ className }: IconProps) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M20 50h55" strokeLinecap="round" />
      <path d="M60 38l15 12-15 12" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M30 44l-8 6 8 6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
