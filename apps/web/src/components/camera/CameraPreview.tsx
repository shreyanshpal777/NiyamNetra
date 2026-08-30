import { useEffect, useRef, useState, type ChangeEvent } from "react";
import { ImageUp } from "lucide-react";
import { useInspectionStore } from "../../store/inspectionStore";
import { CameraOverlay } from "./CameraOverlay";
import { CaptureControls } from "./CaptureControls";

interface CameraPreviewProps {
  onAnalyze: () => void;
}

export function CameraPreview({ onAnalyze }: CameraPreviewProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const { capturedImage, setCameraPermission, setCapturedImage } = useInspectionStore();

  useEffect(() => {
    let mounted = true;

    let activeStream: MediaStream | null = null;

    async function startCamera() {
      if (!navigator.mediaDevices?.getUserMedia) {
        setCameraPermission("denied");
        return;
      }

      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" },
          audio: false,
        });
        if (!mounted) {
          mediaStream.getTracks().forEach((track) => track.stop());
          return;
        }
        activeStream = mediaStream;
        setStream(mediaStream);
        setCameraPermission("granted");
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
      } catch {
        setCameraPermission("denied");
      }
    }

    startCamera();

    return () => {
      mounted = false;
      activeStream?.getTracks().forEach((track) => track.stop());
    };
  }, [setCameraPermission]);

  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  function captureFrame() {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || video.videoWidth === 0) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context?.drawImage(video, 0, 0, canvas.width, canvas.height);
    setCapturedImage(canvas.toDataURL("image/png"));
  }

  function handleUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === "string") {
        setCapturedImage(reader.result);
      }
    };
    reader.readAsDataURL(file);
  }

  return (
    <div className="grid gap-6">
      <div className="relative aspect-[4/3] overflow-hidden rounded-[2rem] bg-[#121018] shadow-2xl">
        {capturedImage ? (
          <img alt="Captured package label preview" className="h-full w-full object-cover" src={capturedImage} />
        ) : (
          <video
            aria-label="Camera preview"
            autoPlay
            className="h-full w-full object-cover opacity-90"
            muted
            playsInline
            ref={videoRef}
          />
        )}
        {!capturedImage && <CameraOverlay />}
        <canvas className="hidden" ref={canvasRef} />
      </div>

      {!stream && !capturedImage && (
        <div className="mx-auto flex max-w-md items-center gap-3 rounded-3xl bg-lavender px-5 py-4 text-sm text-plum">
          <ImageUp className="size-5 shrink-0" />
          Camera access is unavailable here. Upload an image and the inspection flow will continue normally.
        </div>
      )}

      <input
        accept="image/*"
        aria-label="Upload package label image"
        className="hidden"
        onChange={handleUpload}
        ref={inputRef}
        type="file"
      />
      <CaptureControls
        hasPreview={Boolean(capturedImage)}
        onAnalyze={onAnalyze}
        onCapture={captureFrame}
        onRetake={() => setCapturedImage(undefined)}
        onUploadClick={() => inputRef.current?.click()}
      />
    </div>
  );
}
