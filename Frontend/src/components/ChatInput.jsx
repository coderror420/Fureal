import { IoSendSharp } from "react-icons/io5";
import { useState } from "react";

const ChatInput = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="fixed bottom-4 left-0 right-0 px-2 md:ml-[200px] flex justify-center z-40">
      <div className="w-full sm:w-[94%] md:max-w-4xl bg-white rounded-full shadow-md flex items-center px-4 sm:px-6 py-3 sm:py-4 h-16 sm:h-20">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          className="flex-1 outline-none text-gray-800 bg-transparent placeholder-gray-500 text-sm sm:text-base h-full"
        />
        <button
          onClick={handleSend}
          className="ml-2 sm:ml-4 text-teal-600 hover:text-teal-800 text-xl"
        >
          <IoSendSharp />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
