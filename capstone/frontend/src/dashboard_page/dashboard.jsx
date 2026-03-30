import React, { useEffect, useState } from "react";
import { Barchart, Linechart, Piechart } from "./components/charts";

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/dashboard/query");
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const result = await response.json();
  
        // Extract actual data
        const data = result.data;
        console.log("Fetched Data:", result);

        // Check if data is empty or missing
        if (!data || Object.keys(data).length === 0) {
          throw new Error("No data available");
        }
  
        setDashboardData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
  
    fetchData();
  }, []);
  

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  console.log(dashboardData)

  return (
    <div className="min-h-screen bg-gray-1 00 p-6">
      <h2 className="text-3xl font-bold mb-6">Dashboard</h2>

      {/* Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
          <p className="text-gray-500">จำนวนแชททั้งหมด</p>
          <h2 className="text-xl font-bold text-purple-700">{dashboardData.total_user[0].total_chat}</h2>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
          <p className="text-gray-500">เวลาเฉลี่ยในการอัพโหลดเอกสาร 1 หน้า</p>
          <h2 className="text-xl font-bold text-purple-700">{dashboardData.upload_time[0].time_usage_per_page}</h2>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
          <p className="text-gray-500">ความล่าช้าในการตอบ (วินาที)</p>
          <h2 className="text-xl font-bold text-purple-700">{dashboardData.avg_time_usage[0].average_time_usage.toFixed(2)}</h2>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4 text-center">
          <p className="text-gray-500">ความผิดพลาดของ AI (%)</p>
          <h2 className="text-xl font-bold text-green-700">{dashboardData.error_percentage[0].diff}%</h2>
        </div>
      </div>
      
      {/* Barchart: จำนวนผู้ใช้งานในแต่ละวัน */}
      <div className="bg-white rounded-lg p-4 shadow-md mb-6">
        <h3 className="text-lg text-center font-bold mb-2">Daily User</h3>
            <Barchart data={dashboardData.user_time} />
      </div>

      {/* Piechart: Category Distribution */}
      <div className="bg-white rounded-lg p-4 shadow-md mb-6">
        <h3 className="text-lg font-bold mb-2">Category</h3>
        <Piechart data={dashboardData.top_category} />
      </div>
      
      {/* Chathistory Table */}
      <div className="bg-white rounded-lg p-4 shadow-md mb-6">
        <h3 className="text-lg font-bold mb-2">Chathistory</h3>
        <div className="max-h-96 overflow-y-auto overflow-x-auto">
          <table className="table table-xs table-pin-rows">
            <thead className="bg-gray-200 sticky">
              <tr className="border border-gray-300">
                <th className="p-2 border border-gray-300">Model</th>
                <th className="p-2 border border-gray-300">Prompt</th>
                <th className="p-2 border border-gray-300">Question</th>
                <th className="p-2 border border-gray-300">Answer</th>
                <th className="p-2 border border-gray-300">Time Usage</th>
                <th className="p-2 border border-gray-300">Ask At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {dashboardData.history_table.map((chat, idx) => (
                <tr key={idx} className="border border-gray-300">
                  <td className="p-2 border border-gray-300">{chat.llm_model}</td>
                  <td className="p-2 border border-gray-300">{chat.prompt}</td>
                  <td className="p-2 border border-gray-300">{chat.question}</td>
                  <td className="p-2 border border-gray-300">{chat.answer}</td>
                  <td className="p-2 border border-gray-300">{chat.time_usage.toFixed(2)}</td>
                  <td className="p-2 border border-gray-300">{chat.datetime}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
      </div>

      
      {/* Documents Table */}
      <div className="bg-white rounded-lg p-4 shadow-md">
        <h3 className="text-lg font-bold mb-2">Documents</h3>
        <div className="max-h-96 overflow-y-auto">
          <table className="table table-xs table-pin-rows">
            <thead className="bg-gray-100 sticky top-0">
              <tr className="border border-gray-300">
                <th className="p-2 border border-gray-300">Document Name</th>
                <th className="p-2 border border-gray-300">Pages</th>
                <th className="p-2 border border-gray-300">Time Usage</th>
                <th className="p-2 border border-gray-300">Datetime</th>
                <th className="p-2 border border-gray-300">Embedding Model</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {dashboardData.document_table.map((doc, idx) => (
                <tr key={idx} className="border border-gray-300">
                  <td className="p-2 border border-gray-300">{doc.document_name}</td>
                  <td className="p-2 border border-gray-300">{doc.pages}</td>
                  <td className="p-2 border border-gray-300">{doc.time_usage.toFixed(2)}</td>
                  <td className="p-2 border border-gray-300">{doc.datetime}</td>
                  <td className="p-2 border border-gray-300">{doc.embedding_model}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
