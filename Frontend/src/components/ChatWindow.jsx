import { useEffect, useState } from "react";
import ChatInput from "./chatinput";
import MessageBubble from "./messagebubble";
import TypingIndicator from "./TypingIndicator";

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    setMessages([{ sender: "bot", text: "Hi there! I’m Fureal 🌿, your caring companion. How may I assist you today?" }]);
  }, []);

  const sendMessage = async (text) => {
    setMessages((prev) => [...prev, { sender: "user", text }]);
    setIsTyping(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      const data = await res.json();

      setIsTyping(false);

      setMessages((prev) => [...prev, {
        sender: "bot",
        text: data.text,
        audio: data.audio || null
      }]);
    } catch (error) {
      setIsTyping(false);
      setMessages((prev) => [...prev, {
        sender: "bot",
        text: "Oops! Something went wrong.",
      }]);
    }
  };

  return (
     <div className="relative h-full w-full bg-gradient-to-r from-teal-300 to-blue-900 text-white pt-16">

      <div className="flex flex-col items-end pr-15 h-full pt-4 pb-28 overflow-y-auto scrollbar-thin scrollbar-thumb-teal-500">
        <div className="w-[95%] sm:w-[90%] md:max-w-4xl flex flex-col space-y-2">
          {messages.map((msg, index) => (
            <MessageBubble
              key={index}
              message={msg.text}
              isUser={msg.sender === "user"}
              audio={msg.audio}
            />
          ))}

          {isTyping && (
            <div className="flex justify-start mb-2">
              <div className="bg-gray-200 text-gray-900 px-4 py-2 rounded-lg rounded-bl-none max-w-xs md:max-w-md">
                <TypingIndicator />
              </div>
            </div>
          )}
        </div>
      </div>

      <ChatInput onSend={sendMessage} />
    </div>
  );
};

export default ChatWindow;
