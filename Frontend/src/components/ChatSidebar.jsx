import { NavLink } from "react-router-dom";
import { FaHome, FaComments, FaInfoCircle } from "react-icons/fa";

const ChatSidebar = () => {
  return (
    <div className="w-64 min-w-[220px] h-screen bg-gradient-to-b from-teal-100 to-blue-100 shadow-xl p-6 flex flex-col justify-end">
      {/* Navigation */}
      <div>
        <nav className="space-y-4">
          <NavLink
            to="/home"
            className={({ isActive }) =>
              `flex items-center gap-3 text-lg px-3 py-2 rounded-lg transition-all duration-200 
              ${isActive ? "bg-teal-200 text-teal-800 font-semibold" : "text-gray-800 hover:bg-teal-100"}`
            }
          >
            <FaHome />
            Home
          </NavLink>

          <NavLink
            to="/chat"
            className={({ isActive }) =>
              `flex items-center gap-3 text-lg px-3 py-2 rounded-lg transition-all duration-200 
              ${isActive ? "bg-teal-200 text-teal-800 font-semibold" : "text-gray-800 hover:bg-teal-100"}`
            }
          >
            <FaComments />
            Chat
          </NavLink>

          <NavLink
            to="/about"
            className={({ isActive }) =>
              `flex items-center gap-3 text-lg px-3 py-2 rounded-lg transition-all duration-200 
              ${isActive ? "bg-teal-200 text-teal-800 font-semibold" : "text-gray-800 hover:bg-teal-100"}`
            }
          >
            <FaInfoCircle />
            About
          </NavLink>
        </nav>
      </div>

      {/* Footer */}
      <div className="text-xs text-gray-600 mt-6">
        © 2025 <span className="font-semibold text-teal-700">Fureal</span>. All rights reserved.
      </div>
    </div>
  );
};

export default ChatSidebar;
