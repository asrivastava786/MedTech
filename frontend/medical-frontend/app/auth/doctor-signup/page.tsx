"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
  fullName: z.string().min(1),
  licenseNumber: z.string().min(5),
});

type FormData = z.infer<typeof schema>;

export default function DoctorSignupPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  async function onSubmit(data: FormData) {
    // TODO: call backend doctor signup API with license validation
    alert(JSON.stringify(data, null, 2));
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="max-w-md mt mx-auto space-y-4 bg-white p-6 rounded shadow"
    >
      <h1 className="text-xl font-semibold">Doctor Sign Up</h1>

      <div>
        <label className="block font-medium">Full Name</label>
        <input
          {...register("fullName")}
          className="mt-1 w-full rounded border px-3 py-2"
        />
        {errors.fullName && (
          <p className="text-sm text-red-600">{errors.fullName.message}</p>
        )}
      </div>

      <div>
        <label className="block font-medium">Email</label>
        <input
          {...register("email")}
          type="email"
          className="mt-1 w-full rounded border px-3 py-2"
        />
        {errors.email && (
          <p className="text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label className="block font-medium">Password</label>
        <input
          {...register("password")}
          type="password"
          className="mt-1 w-full rounded border px-3 py-2"
        />
        {errors.password && (
          <p className="text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      <div>
        <label className="block font-medium">Medical License Number</label>
        <input
          {...register("licenseNumber")}
          className="mt-1 w-full rounded border px-3 py-2"
        />
        {errors.licenseNumber && (
          <p className="text-sm text-red-600">{errors.licenseNumber.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
      >
        Sign Up as Doctor
      </button>
    </form>
  );
}
