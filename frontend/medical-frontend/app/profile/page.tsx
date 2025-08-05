"use client";
import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const { user, isLoggedIn } = useAuth();
  const router = useRouter();
  useEffect(() => {
    if (!isLoggedIn) router.push("/login");
  }, [isLoggedIn]);
  if (!user) return null;
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-2">Profile</h1>
      <p>Email: {user.email}</p>
      <p>Name: {user.name}</p>
      <p>Role: {user.role}</p>
    </div>
  );
}