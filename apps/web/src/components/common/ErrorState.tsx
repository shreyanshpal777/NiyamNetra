export function ErrorState({ message }: { message: string }) {
  return <div className="rounded-3xl bg-rose-50 p-8 text-center text-sm text-fail">{message}</div>;
}
