import { FaHeart } from "react-icons/fa";

const Cover = () => {
  return (
    <div className="flex flex-wrap items-center min-h-screen w-screen bg-gradient-to-r from-teal-300 to-blue-900 text-white px-4 py-8 pt-28 md:pt-8">
      {/* Left: Title and Heart */}
      <div className="w-full md:w-1/2 text-center md:text-left mb-10 md:mb-0">
        <h1 className="md:ml-10 font-bold text-4xl sm:text-5xl md:text-6xl lg:text-6xl xl:text-7xl leading-tight text-blue-800">
          SMART <br /> CUSTOMER <br /> SUPPORT <br /> ASSISTANT
        </h1>
        <p className="md:ml-10 mt-4 text-lg sm:text-xl font-bold font-serif">
          Built with{" "}
          <span className="text-purple-700 inline-block align-middle ml-1">
            <FaHeart className="inline text-xl" />
          </span>
        </p>
      </div>

      {/* Right: Descriptive Boxes */}
      <div className="w-full md:w-1/2 flex flex-col items-center gap-y-6">
        {/* Box 1 */}
        <div className="w-11/12 sm:w-3/5 sm:h-35 bg-white rounded-full text-gray-800 shadow-md px-6 py-6 text-center sm:mb-5">
          <h2 className="font-semibold text-blue-800 text-lg sm:text-xl mb-1">
            Smart Customer Assistant
          </h2>
          <p className="text-sm sm:text-base">
            Empathetic. Multilingual. Instant support that understands how you feel.
          </p>
        </div>

        {/* Box 2 */}
        <div className="w-11/12 sm:w-3/5 sm:h-35 bg-white rounded-full text-gray-800 shadow-md px-6 py-4 text-center sm:mt-5">
          <h2 className="font-semibold text-blue-800 text-lg sm:text-xl mb-1">
            Why it matters?
          </h2>
          <p className="text-sm sm:text-base">
            Detects emotions, responds with care, and speaks your language.
            Simplifying every interaction.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Cover;
