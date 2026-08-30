export function LoadingState({ message = "Loading" }: { message?: string }) {
  return <div className="rounded-3xl bg-white p-8 text-center text-sm text-muted">{message}</div>;
}
