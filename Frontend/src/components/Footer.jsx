import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-teal-300 to-blue-900 text-white py-6 mt-auto ">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <div className="text-sm text-center md:text-left">
          © {new Date().getFullYear()} <span className="font-semibold">Fureal</span>. All rights reserved.
        </div>

        <div className="flex space-x-6 text-sm">
          <Link to="/about" className="hover:underline">About</Link>
          <Link to="/faq" className="hover:underline">FAQ</Link>
          <Link to="/chat" className="hover:underline">Chat</Link>
        </div>
        <div className="text-sm text-center md:text-right">
          Built with ❤️
        </div>
      </div>
    </footer>
  );
};

export default Footer;
