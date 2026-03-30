import { useState } from "react";
import { FaRobot } from "react-icons/fa"; // ใช้ไอคอนบอท
import axios from "axios";

export default function Chatbot() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    setMessages([...messages, { text: message, type: "user" }]);
    setMessage("");

    setLoading(true);
    try {
      const response = await axios.post("/api/chatbot/infer", {
        question: message,
      });
      const botReply = response.data.answer || "ขออภัย ฉันไม่เข้าใจคำถามของคุณ";
      setMessages((prev) => [...prev, { text: botReply, type: "bot" }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: "เกิดข้อผิดพลาดในการเชื่อมต่อ AI", type: "bot" },
      ]);
    }
    setLoading(false);
  };

  return (
    <>
      {/* ปุ่มเปิด Chatbot (ไอคอนบอท) */}
      <button
        className="fixed bottom-6 right-6 bg-blue-600 text-white p-3 rounded-full shadow-lg flex items-center justify-center"
        onClick={() => document.getElementById("chatbot-modal").showModal()}
      >
        <FaRobot className="text-2xl" /> {/* ไอคอนบอท */}
      </button>

      {/* DaisyUI Modal */}
      <dialog id="chatbot-modal" className="modal">
        <div className="modal-box bg-gray-900 text-white w-[600px] max-w-2xl">
          {/* Header */}
          <div className="flex justify-between items-center bg-gray-800 px-4 py-3 rounded-t-lg">
            <h4 className="text-lg font-semibold">ChatKMITL - Ask a question</h4>
            <form method="dialog">
              <button className="text-2xl text-gray-400 hover:text-white">×</button>
            </form>
          </div>

          {/* Body - ส่วนแสดงข้อความแชท */}
          <div className="p-4 h-[300px] overflow-y-auto">
            {messages.map((msg, index) => (
              <div key={index} className={`mb-2 ${msg.type === "user" ? "text-right" : "text-left"}`}>
                <div className={`inline-block px-3 py-2 rounded-lg break-words max-w-[80%] text-left ${
                  msg.type === "user" ? "bg-blue-500 text-white" : "bg-gray-700"
                }`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {loading && <div className="text-left italic text-gray-400">AI กำลังพิมพ์...</div>}
          </div>

          {/* Footer - ส่วนพิมพ์ข้อความ */}
          <div className="flex px-4 py-3 border-t border-gray-700">
            <input
              type="text"
              placeholder="Ask anything"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="flex-1 bg-gray-800 text-white px-3 py-2 rounded-l-lg focus:outline-none"
            />
            <button
              onClick={sendMessage}
              className="bg-blue-500 text-white px-4 py-2 rounded-r-lg"
            >
              Ask AI
            </button>
          </div>

          {/* Copyright */}
          <div className="text-center text-gray-500 text-sm py-2">
            © Copyright 2025, The Jolf Team.
          </div>
        </div>
      </dialog>
    </>
  );
}
