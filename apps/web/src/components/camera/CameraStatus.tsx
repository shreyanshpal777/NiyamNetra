import { CheckCircle2 } from "lucide-react";

const statuses = [
  ["Marker", "Detected"],
  ["Label", "Detected"],
  ["Image", "Good"],
];

export function CameraStatus() {
  return (
    <div className="flex flex-wrap justify-center gap-3">
      {statuses.map(([label, value]) => (
        <div className="flex items-center gap-2 rounded-full bg-white px-4 py-2 text-xs shadow-sm ring-1 ring-line" key={label}>
          <CheckCircle2 className="size-4 text-pass" />
          <span className="font-semibold text-ink">{label}</span>
          <span className="text-muted">{value}</span>
        </div>
      ))}
    </div>
  );
}
