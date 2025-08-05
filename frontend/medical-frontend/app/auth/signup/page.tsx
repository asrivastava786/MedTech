"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    email: "",
    name: "",
    password: "",
    role: "USER", // or "DOCTOR"
    licenseNumber: "",
  });
  const [error, setError] = useState("");

  const isDoctor = form.role === "DOCTOR";

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const endpoint = isDoctor ? "http://localhost:8000/auth/doctor-signup" : "http://localhost:8000/signup";
    const payload = isDoctor
      ? { email: form.email, name: form.name, password: form.password, licenseNumber: form.licenseNumber }
      : { email: form.email, name: form.name, password: form.password };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || "Signup failed");
        return;
      }

      router.push("/login");
    } catch {
      setError("Signup error");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-6 border rounded-xl shadow-xl">
      <h1 className="text-2xl font-bold mb-4">Signup</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="email"
          type="email"
          placeholder="Email"
          className="w-full border p-2 rounded"
          value={form.email}
          onChange={handleChange}
          required
        />
        <input
          name="name"
          placeholder="Full Name"
          className="w-full border p-2 rounded"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded"
          value={form.password}
          onChange={handleChange}
          required
        />

        <select
          name="role"
          value={form.role}
          onChange={handleChange}
          className="w-full border p-2 rounded"
        >
          <option value="USER">User</option>
          <option value="DOCTOR">Doctor</option>
        </select>

        {isDoctor && (
          <input
            name="licenseNumber"
            placeholder="Doctor License Number"
            className="w-full border p-2 rounded"
            value={form.licenseNumber}
            onChange={handleChange}
            required
          />
        )}

        {error && <p className="text-red-500">{error}</p>}
        <button type="submit" className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700">
          Signup
        </button>
      </form>
    </div>
  );
}
