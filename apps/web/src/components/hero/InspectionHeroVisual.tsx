import { Crosshair, Maximize2, ScanText } from "lucide-react";

export function InspectionHeroVisual() {
  return (
    <div className="soft-noise relative min-h-[330px] overflow-hidden rounded-[2rem] bg-[#d7d4ee] p-5 sm:min-h-[430px] sm:p-8">
      <div className="absolute inset-x-0 bottom-0 h-36 bg-gradient-to-t from-[#2a2338]/20 to-transparent" />
      <div className="absolute left-[8%] top-[20%] h-36 w-24 rotate-[-8deg] rounded-[1.6rem] bg-white/65 shadow-2xl ring-1 ring-white/80 sm:h-52 sm:w-36">
        <div className="m-4 h-4 rounded-full bg-plum/80" />
        <div className="mx-4 mt-5 h-3 rounded-full bg-plum/25" />
        <div className="mx-4 mt-3 h-3 w-20 rounded-full bg-plum/25" />
        <div className="absolute bottom-5 left-4 right-4 h-12 rounded-2xl bg-lavender-deep/60" />
      </div>
      <div className="absolute bottom-[-10%] left-[34%] h-56 w-40 rotate-[9deg] rounded-[1.9rem] bg-[#f8f6ef] shadow-2xl ring-1 ring-white sm:h-72 sm:w-56">
        <div className="absolute -left-4 top-8 rounded-full bg-plum px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-white">
          OCR 97%
        </div>
        <div className="mx-6 mt-7 h-5 rounded-full bg-plum" />
        <div className="mx-6 mt-6 grid gap-3">
          <span className="h-3 rounded-full bg-lavender-deep" />
          <span className="h-3 w-4/5 rounded-full bg-lavender-deep" />
          <span className="h-3 w-3/5 rounded-full bg-lavender-deep" />
        </div>
        <div className="absolute left-6 top-28 h-8 w-28 rounded-lg border-2 border-pass/70" />
        <div className="absolute bottom-14 right-7 h-9 w-24 rounded-lg border-2 border-review/80" />
        <div className="absolute bottom-6 left-7 grid size-10 grid-cols-2 gap-1 bg-ink p-1">
          <span className="bg-white" />
          <span className="bg-white" />
          <span className="bg-white" />
          <span className="bg-ink" />
        </div>
      </div>
      <div className="absolute right-[10%] top-[18%] h-40 w-32 rotate-[11deg] rounded-[1.6rem] bg-plum text-white shadow-2xl sm:h-56 sm:w-44">
        <div className="p-5">
          <ScanText className="size-6" />
          <p className="mt-8 text-sm font-semibold">Compliance trace</p>
          <p className="mt-2 text-xs leading-5 text-white/60">MRP, quantity and qualifier evidence linked to source pixels.</p>
        </div>
      </div>
      <div className="absolute left-[17%] top-[60%] h-px w-[58%] rotate-[-8deg] bg-white/80" />
      <div className="absolute right-8 top-8 flex gap-3">
        <span className="flex size-10 items-center justify-center rounded-full bg-white/55 text-plum">
          <Crosshair className="size-5" />
        </span>
        <span className="flex size-10 items-center justify-center rounded-full bg-white/55 text-plum">
          <Maximize2 className="size-5" />
        </span>
      </div>
      <div className="absolute bottom-8 right-8 rounded-full bg-white/80 px-4 py-2 text-xs font-semibold text-plum shadow-sm">
        Measurement calibrated
      </div>
    </div>
  );
}
