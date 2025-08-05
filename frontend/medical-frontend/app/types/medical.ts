// types/medical.ts
export interface MedicalRecord {
  id: string;
  conditionName: string;
  recordType: string;
  category: string;
  ageOfOnset?: number;
  severity?: string;
  isGenetic: boolean;
  treatmentNotes?: string;
  diagnosedAt?: string;
  userId?: string;
  familyMemberId?: string;
  recordedById: string;
  createdAt: string;
}
