const About = () => {
  return (
    <div className="flex flex-wrap items-center min-h-screen w-full bg-gradient-to-r from-teal-300 to-blue-900 text-white px-4 py-8 pt-28 md:pt-8 justify-center">
      <div className="w-full sm:w-11/12 md:w-4/5 lg:w-3/4 xl:w-2/3 max-h-[85vh] bg-blue-800/90 backdrop-blur-md shadow-xl p-6 md:p-10  overflow-y-auto relative">
        
        {/* Stylized Heading */}
        <div className="absolute top-6 left-6 md:top-8 md:left-10">
          <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold leading-none">
            <span className="text-6xl sm:text-8xl md:text-9xl">A</span>bout
          </h1>
        </div>

        {/* Content */}
        <div className="mt-32 text-base sm:text-lg md:text-xl leading-relaxed px-2 md:px-6 text-justify">
          Our smart assistant is an AI-powered chatbot designed to streamline customer support and enhance user experience through natural, intelligent conversations. It can handle user queries, remember chat history, and provide contextual responses — all within a secure and user-friendly interface.
          <br /><br />
          With integrated authentication and a personalized chat environment, this assistant offers fast, reliable, and human-like interaction 24/7, making it an essential tool for modern digital platforms.
        </div>
      </div>
    </div>
  );
};

export default About;
