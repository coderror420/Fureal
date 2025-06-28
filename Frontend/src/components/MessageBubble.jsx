import ReactMarkdown from 'react-markdown';
import { FaVolumeUp } from 'react-icons/fa';

const MessageBubble = ({ message, isUser, audio }) => {
  const playAudio = () => {
    if (audio) {
      const audioPlayer = new Audio(`http://localhost:8000${audio}`);
      audioPlayer.play();
    }
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
      <div className={`max-w-xs md:max-w-md px-4 py-2 rounded-lg flex items-center gap-2 ${
        isUser
          ? "bg-blue-600 text-white rounded-br-none"
          : "bg-gray-200 text-gray-900 rounded-bl-none"
      }`}>
        {!isUser && audio && (
          <button onClick={playAudio} className="text-gray-500 text-xl hover:text-gray-800">
            <FaVolumeUp />
          </button>
        )}
        <div className="break-words">
          <ReactMarkdown>{message}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
