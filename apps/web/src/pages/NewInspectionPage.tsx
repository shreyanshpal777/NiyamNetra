import { useRef, useState, type ChangeEvent } from "react";
import { useMutation } from "@tanstack/react-query";
import { Camera, ImageUp, PackageSearch } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { createInspection } from "../api/inspections";
import { PageContainer } from "../components/layout/PageContainer";
import { Button } from "../components/ui/button";
import { useInspectionStore } from "../store/inspectionStore";

export function NewInspectionPage() {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [productName, setProductName] = useState("");
  const [category, setCategory] = useState("");
  const { setCapturedImage, setCurrentInspection } = useInspectionStore();

  const mutation = useMutation({
    mutationFn: createInspection,
    onSuccess: (inspection) => {
      setCurrentInspection(inspection.id);
      navigate(`/inspection/${inspection.id}/capture`);
    },
  });

  async function startInspection() {
    mutation.mutate({
      productName: productName.trim() || "Premium Wheat Flour",
      category: category.trim() || "Package label",
    });
  }

  function handleUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") {
        setCapturedImage(reader.result);
        startInspection();
      }
    };
    reader.readAsDataURL(file);
  }

  return (
    <PageContainer>
      <section className="mx-auto max-w-5xl py-10 sm:py-16">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">New inspection</p>
          <h1 className="display-heading mt-5 text-5xl font-semibold text-ink sm:text-7xl">
            Start an inspection
          </h1>
          <p className="mt-6 text-lg leading-8 text-muted">
            Capture the label and let Inspector AI analyze the rest.
          </p>
        </div>

        <div className="mt-10 rounded-[2rem] bg-white p-5 shadow-sm sm:p-8">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="grid gap-2">
              <span className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">
                Product name
              </span>
              <input
                className="h-12 rounded-full border border-line bg-canvas px-5 text-sm text-ink"
                onChange={(event) => setProductName(event.target.value)}
                placeholder="Premium Wheat Flour"
                value={productName}
              />
            </label>
            <label className="grid gap-2">
              <span className="text-xs font-semibold uppercase tracking-[0.14em] text-muted">
                Product category
              </span>
              <input
                className="h-12 rounded-full border border-line bg-canvas px-5 text-sm text-ink"
                onChange={(event) => setCategory(event.target.value)}
                placeholder="Staple food"
                value={category}
              />
            </label>
          </div>

          <button
            className="mt-6 flex min-h-80 w-full flex-col items-center justify-center rounded-[2rem] border border-dashed border-lavender-deep bg-lavender/70 px-6 text-center transition hover:bg-lavender"
            onClick={() => inputRef.current?.click()}
            type="button"
          >
            <span className="flex size-14 items-center justify-center rounded-full bg-white text-plum shadow-sm">
              <PackageSearch className="size-7" />
            </span>
            <span className="mt-6 text-3xl font-semibold text-ink">Place package here</span>
            <span className="mt-3 max-w-sm text-sm leading-6 text-muted">Drag image or browse to begin with an uploaded label image.</span>
            <span className="mt-6 rounded-full bg-plum px-5 py-3 text-sm font-medium text-white">Browse image</span>
          </button>
          <input
            accept="image/*"
            aria-label="Browse package label image"
            className="hidden"
            onChange={handleUpload}
            ref={inputRef}
            type="file"
          />

          <div className="mt-6 flex flex-col items-center gap-4">
            <span className="text-sm text-muted">or</span>
            <Button disabled={mutation.isPending} onClick={startInspection} type="button">
              <Camera className="size-4" />
              Open Camera
            </Button>
            <Button onClick={() => inputRef.current?.click()} type="button" variant="ghost">
              <ImageUp className="size-4" />
              Upload instead
            </Button>
          </div>
        </div>
      </section>
    </PageContainer>
  );
}
