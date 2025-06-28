import { useState } from "react";
import faqData from "../assets/faqData.json";

const FAQ = () => {
  const [expanded, setExpanded] = useState(null);

  const toggleFAQ = (index) => {
    setExpanded(expanded === index ? null : index);
  };

  return (
    <div className="bg-gradient-to-r from-teal-300 to-blue-900 text-black py-10 px-6 sm:px-12 min-h-screen">
      <h2 className="text-3xl  mb-8 text-center text-white">Frequently Asked Questions</h2>
      <div className="max-w-3xl mx-auto bg-white bg-opacity-10 backdrop-blur-md p-6 shadow-lg space-y-4">
        {faqData.map((faq, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg transition duration-300 cursor-pointer ${
              expanded === index
                ? "bg-white bg-opacity-30"
                : "hover:bg-white hover:bg-opacity-20"
            }`}
            onClick={() => toggleFAQ(index)}
          >
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-blue-900">{faq.question}</h3>
              <span className="text-xl text-blue-900">
                {expanded === index ? "−" : "+"}
              </span>
            </div>
            {expanded === index && (
              <p className="mt-2 text-sm text-black">{faq.answer}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FAQ;
