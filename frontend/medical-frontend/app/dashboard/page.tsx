"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../context/AuthContext";

export default function DashboardPage() {
  const { user, isLoggedIn, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoggedIn) {
      router.push("/login");
    }
  }, [isLoggedIn]);

  if (!user) return null;

  return (
    <div className="max-w-2xl mx-auto mt-20 p-6 border rounded-xl shadow">
      <h1 className="text-3xl font-bold mb-4">Welcome, {user.name}</h1>
      <p className="mb-2">Email: {user.email}</p>
      <p className="mb-6">Role: {user.role}</p>

      <button
        onClick={logout}
        className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
      >
        Logout
      </button>
    </div>
  );
}
