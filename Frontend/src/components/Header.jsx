import { useState } from "react";
import { NavLink, Link, useLocation } from "react-router-dom";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { Menu, X } from "lucide-react";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const path = location.pathname;

  return (
    <header className="z-40 fixed top-0 left-0 right-0">
      <div className="flex justify-between items-center w-full h-16 text-white p-4 bg-transparent">
        {/* Logo + Title */}
        <div className="flex items-center space-x-2">
          <Link to="/">
            <img className="h-12 w-12" src="/logo.svg" alt="logo" />
          </Link>
          <NavLink
            to="/"
            className="text-3xl font-semibold italic bg-gradient-to-r from-green-500 via-blue-500 to-yellow-500 bg-clip-text text-transparent"
          >
            fureal
          </NavLink>
        </div>

        {/* 👇 Hamburger Menu (Only on mobile) */}
        <div className="md:hidden">
          <button onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X className="w-6 h-6 text-white" /> : <Menu className="w-6 h-6 text-white" />}
          </button>
        </div>

        {/* 👇 Desktop Buttons (Only on medium+ screens) */}
        <div className="hidden md:flex items-center space-x-4">
          {(path === "/home" || path === "/") && (
            <>
              <a href="/#about">
                <button className="bg-white text-black text-sm px-4 py-2 rounded-full shadow hover:bg-gray-100 transition hover:cursor-pointer">
                  About Us
                </button>
              </a>
              <a href="/#faq">
                <button className="bg-white text-black text-sm px-4 py-2 rounded-full shadow hover:bg-gray-100 transition hover:cursor-pointer">
                  FAQ
                </button>
              </a>
              <Link to="/chat">
                <button className="bg-white text-black text-sm px-4 py-2 rounded-full shadow hover:bg-gray-100 transition hover:cursor-pointer">
                  Get Started
                </button>
              </Link>
            </>
          )}
        </div>
      </div>

      {/* 👇 Mobile Sidebar Menu */}
      {isOpen && (
        <div className="fixed top-16 right-0 h-full w-2/3 md:hidden bg-sky-700 shadow-lg z-40 p-4 space-y-4 text-white">
          <NavLink to="/" onClick={() => setIsOpen(false)} className="block text-lg font-semibold">
            Home
          </NavLink>
          <NavLink to="/chat" onClick={() => setIsOpen(false)} className="block text-lg font-semibold">
            Chat
          </NavLink>
          <NavLink to="/about" onClick={() => setIsOpen(false)} className="block text-lg font-semibold">
            About Us
          </NavLink>
          <NavLink to="/faq" onClick={() => setIsOpen(false)} className="block text-lg font-semibold">
            FAQ
          </NavLink>
        </div>
      )}
    </header>
  );
};

export default Header;
