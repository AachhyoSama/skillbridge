import { useEffect, useState } from "react";
import api from "../services/api";
import type { User } from "../types/user";

export default function Profile() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const res = await api.get("/me");
      setUser(res.data);
    };
    fetchUser();
  }, []);

  if (!user) return <div className="text-center mt-20">Loading profile...</div>;

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full space-y-4">
        <h2 className="text-2xl font-semibold text-indigo-700 text-center">
          Welcome, {user.username}
        </h2>
        <div>
          <p className="text-gray-600">
            <strong>Email:</strong> {user.email}
          </p>
          {user.bio && (
            <p className="text-gray-600 mt-1">
              <strong>Bio:</strong> {user.bio}
            </p>
          )}
        </div>
        <div>
          <p className="font-semibold text-indigo-600">Skills Offered:</p>
          <ul className="list-disc list-inside text-gray-700">
            {user.skills_offered?.map((skill, idx) => (
              <li key={idx}>{skill}</li>
            ))}
          </ul>
        </div>
        <div>
          <p className="font-semibold text-indigo-600">Skills Wanted:</p>
          <ul className="list-disc list-inside text-gray-700">
            {user.skills_wanted?.map((skill, idx) => (
              <li key={idx}>{skill}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
