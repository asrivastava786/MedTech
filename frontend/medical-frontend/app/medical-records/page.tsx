"use client";
import { useAuth } from "../context/AuthContext";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Spinner from "../components/spinner";

import { MedicalRecord } from "../types/medical";


export default function MedicalRecordsPage() {
  const { user, isLoggedIn } = useAuth();
  const router = useRouter();
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  const [record, setRecord] = useState<MedicalRecord[]>([]);



  useEffect(() => {
    if (!isLoggedIn) router.push("/login");
    else fetchRecords();
  }, [isLoggedIn]);

  const fetchRecords = async () => {
    const token = localStorage.getItem("token");
    const res = await fetch("http://localhost:8000/medical-records", {
      headers: { Authorization: `Bearer ${token}` },
    });
    const data = await res.json();
    setRecords(data);
    setLoading(false);
  };

  if (loading) return <Spinner />;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Your Medical Records</h1>
      {records.length === 0 ? (
        <p>No records found.</p>
      ) : (
        <ul className="space-y-2">
          {records.map((record) => (
            <li key={record["id"]} className="p-3 border rounded shadow">
              <p><strong>{record["conditionName"]}</strong> ({record["recordType"]})</p>
              <p>Diagnosed: {record["diagnosedAt"?.slice(0, 10)]}</p>
              <p>Severity: {record["severity"]}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
