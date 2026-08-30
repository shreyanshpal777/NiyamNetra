export function CameraOverlay() {
  return (
    <div className="pointer-events-none absolute inset-0">
      <div className="absolute inset-6 rounded-[1.5rem] border border-white/35" />
      <div className="absolute left-[16%] right-[16%] top-[23%] h-[50%] rounded-3xl border-2 border-lavender-deep/80">
        <span className="absolute -left-2 -top-2 size-5 rounded-tl-xl border-l-2 border-t-2 border-white" />
        <span className="absolute -right-2 -top-2 size-5 rounded-tr-xl border-r-2 border-t-2 border-white" />
        <span className="absolute -bottom-2 -left-2 size-5 rounded-bl-xl border-b-2 border-l-2 border-white" />
        <span className="absolute -bottom-2 -right-2 size-5 rounded-br-xl border-b-2 border-r-2 border-white" />
      </div>
      <div className="absolute bottom-[18%] right-[18%] grid size-12 grid-cols-2 gap-1 bg-white p-1">
        <span className="bg-ink" />
        <span className="bg-ink" />
        <span className="bg-ink" />
        <span className="bg-white" />
      </div>
      <div className="absolute left-8 top-8 rounded-full bg-black/30 px-4 py-2 text-xs text-white backdrop-blur">
        Align label and reference marker
      </div>
    </div>
  );
}
