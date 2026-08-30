import { Camera, ImageUp, RefreshCcw, Wand2 } from "lucide-react";
import { Button } from "../ui/button";

interface CaptureControlsProps {
  hasPreview: boolean;
  onAnalyze: () => void;
  onCapture: () => void;
  onRetake: () => void;
  onUploadClick: () => void;
}

export function CaptureControls({
  hasPreview,
  onAnalyze,
  onCapture,
  onRetake,
  onUploadClick,
}: CaptureControlsProps) {
  if (hasPreview) {
    return (
      <div className="flex flex-wrap justify-center gap-3">
        <Button onClick={onRetake} type="button" variant="secondary">
          <RefreshCcw className="size-4" />
          Retake
        </Button>
        <Button onClick={onAnalyze} type="button">
          <Wand2 className="size-4" />
          Analyze
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap justify-center gap-3">
      <Button onClick={onCapture} type="button">
        <Camera className="size-4" />
        Capture
      </Button>
      <Button onClick={onUploadClick} type="button" variant="secondary">
        <ImageUp className="size-4" />
        Upload image
      </Button>
    </div>
  );
}
