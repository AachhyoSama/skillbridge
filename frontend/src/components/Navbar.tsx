import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <nav className="bg-indigo-600 p-4 text-white flex justify-between">
      <Link to="/" className="font-bold text-xl">
        SkillBridge
      </Link>
      <div className="space-x-4">
        {isAuthenticated ? (
          <>
            <Link to="/profile" className="hover:underline">Profile</Link>
            <Link to="/edit-profile" className="hover:underline">Edit</Link>
            <button onClick={() => { logout(); navigate("/"); }} className="hover:underline">Logout</button>
          </>
        ) : (
          <>
            <Link to="/" className="hover:underline">Login</Link>
            <Link to="/register" className="hover:underline">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;