import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import type { User } from "../types/user";

const EditProfile = () => {
  const [form, setForm] = useState<User>({} as User);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      const res = await api.get("/me");
      setForm(res.data);
    };
    fetchProfile();
  }, []);

  const updateField = (field: string, value: string) => {
    setForm({ ...form, [field]: value });
  };

  const updateSkills = (field: "skills_offered" | "skills_wanted", index: number, value: string) => {
    const newSkills = [...(form[field] || [])];
    newSkills[index] = value;
    setForm({ ...form, [field]: newSkills });
  };

  const addSkill = (field: "skills_offered" | "skills_wanted") => {
    setForm({ ...form, [field]: [...(form[field] || []), ""] });
  };

  const removeSkill = (field: "skills_offered" | "skills_wanted", index: number) => {
    const updatedSkills = [...(form[field] || [])];
    updatedSkills.splice(index, 1);
    setForm({ ...form, [field]: updatedSkills });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.put("/me", form);
    navigate("/profile");
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100 p-4">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-lg w-full max-w-md space-y-4">
        <h2 className="text-xl font-semibold text-indigo-700 text-center">Edit Profile</h2>

        <input value={form.bio || ""} onChange={(e) => updateField("bio", e.target.value)} placeholder="Bio" className="w-full p-2 border rounded" />

        <div>
          <label className="font-medium">Skills Offered</label>
          {(form.skills_offered || []).map((skill, idx) => (
            <div key={idx} className="flex items-center gap-2 mb-2">
              <input value={skill} onChange={(e) => updateSkills("skills_offered", idx, e.target.value)} className="w-full p-2 border rounded" />
              <button type="button" onClick={() => removeSkill("skills_offered", idx)} className="text-red-500">✕</button>
            </div>
          ))}
          <button type="button" onClick={() => addSkill("skills_offered")} className="text-sm text-indigo-600 mt-1">+ Add</button>
        </div>

        <div>
          <label className="font-medium">Skills Wanted</label>
          {(form.skills_wanted || []).map((skill, idx) => (
            <div key={idx} className="flex items-center gap-2 mb-2">
              <input value={skill} onChange={(e) => updateSkills("skills_wanted", idx, e.target.value)} className="w-full p-2 border rounded" />
              <button type="button" onClick={() => removeSkill("skills_wanted", idx)} className="text-red-500">✕</button>
            </div>
          ))}
          <button type="button" onClick={() => addSkill("skills_wanted")} className="text-sm text-indigo-600 mt-1">+ Add</button>
        </div>

        <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded">Update</button>
      </form>
    </div>
  );
};

export default EditProfile;