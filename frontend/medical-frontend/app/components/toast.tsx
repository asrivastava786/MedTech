import { useEffect } from "react";

export default function Toast({ message, onClose }: { message: string; onClose: () => void }) {
  useEffect(() => {
    const timeout = setTimeout(() => onClose(), 3000);
    return () => clearTimeout(timeout);
  }, [onClose]);

  return (
    <div className="fixed top-4 right-4 bg-green-600 text-white px-4 py-2 rounded shadow-lg">
      {message}
    </div>
  );
}