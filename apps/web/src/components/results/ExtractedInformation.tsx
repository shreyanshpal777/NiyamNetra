import type { ProductLabelData } from "../../types/inspection";

interface ExtractedInformationProps {
  data: ProductLabelData;
}

export function ExtractedInformation({ data }: ExtractedInformationProps) {
  const fields = [
    ["MRP", data.mrp],
    ["Net Weight", data.netWeight],
    ["Manufacturer", data.manufacturer],
    ["Batch Number", data.batchNumber],
    ["Category", data.category],
    ["Packed On", data.packedOn],
    ["Customer Care", data.customerCare],
  ];

  return (
    <section className="rounded-[2rem] bg-white p-6 sm:p-8">
      <h2 className="text-2xl font-semibold text-ink">Extracted information</h2>
      <dl className="mt-8 grid gap-5 sm:grid-cols-2">
        {fields.map(([label, value]) => (
          <div className="rounded-3xl bg-canvas p-5" key={label}>
            <dt className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">{label}</dt>
            <dd className="mt-3 text-xl font-semibold text-ink">{value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
