import ChatSidebar from "./ChatSidebar";
import ChatWindow from "./ChatWindow";

const ChatLayout = () => {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar: hidden on small screens */}
      <div className="hidden md:block">
        <ChatSidebar />
      </div>

      {/* Chat window: full width on mobile, flex-1 on md+ */}
      <div className="flex-1 relative w-full">
        <ChatWindow />
      </div>
    </div>
  );
};

export default ChatLayout;
