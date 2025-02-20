// app/logs/page.tsx
'use client'
import React, { useState } from 'react';
import { Heading, Paragraph } from '@/components/ui/typography';
import { AiOutlineClockCircle, AiOutlineFileText } from 'react-icons/ai'; // Import icons from react-icons

interface Log {
  id: number;
  llm: string;
  message: string;
  timestamp: string;
}

const logData: Log[] = [
  { id: 1, llm: 'GPT-3', message: 'Inference completed successfully.', timestamp: '2024-10-20 12:30:00' },
  { id: 2, llm: 'GPT-4', message: 'Model training started.', timestamp: '2024-10-20 13:00:00' },
  { id: 3, llm: 'GPT-3', message: 'Error: Out of memory while processing.', timestamp: '2024-10-20 13:15:00' },
  { id: 4, llm: 'GPT-4', message: 'Inference result: { response: "Hello!" }', timestamp: '2024-10-20 14:00:00' },
  { id: 5, llm: 'LLM-5', message: 'Model accuracy updated to 95%.', timestamp: '2024-10-21 10:00:00' },
  { id: 6, llm: 'GPT-3', message: 'Checkpoint saved successfully.', timestamp: '2024-10-21 10:30:00' },
  { id: 7, llm: 'GPT-4', message: 'Training phase 1 completed.', timestamp: '2024-10-21 11:00:00' },
  { id: 8, llm: 'LLM-5', message: 'New configuration applied.', timestamp: '2024-10-21 11:15:00' },
  { id: 9, llm: 'GPT-3', message: 'Inference took longer than expected.', timestamp: '2024-10-21 11:30:00' },
  { id: 10, llm: 'GPT-4', message: 'Evaluation metrics logged.', timestamp: '2024-10-21 12:00:00' },
];

const timeframes = ['Live', 'Today', 'Week', 'Month', 'Quarter', 'Year'];

const LogsPage: React.FC = () => {
  const [selectedLLM, setSelectedLLM] = useState<string>('All');
  const [selectedTimeframe, setSelectedTimeframe] = useState<string>(timeframes[0]);
  const [isDropdownOpen, setIsDropdownOpen] = useState<boolean>(false);
  const [isLLMDropdownOpen, setIsLLMDropdownOpen] = useState<boolean>(false);

  const handleTimeframeChange = (timeframe: string) => {
    setSelectedTimeframe(timeframe);
    setIsDropdownOpen(false); // Close dropdown after selection
  };

  const handleLLMChange = (llm: string) => {
    setSelectedLLM(llm);
    setIsLLMDropdownOpen(false); // Close dropdown after selection
  };

  const toggleDropdown = () => setIsDropdownOpen((prev) => !prev);
  const toggleLLMDropdown = () => setIsLLMDropdownOpen((prev) => !prev);

  return (
    <div className="text-gray-900 dark:text-white p-4 sm:p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        <Heading size={2} className="text-center mb-8">LLM Logs</Heading>

        {/* Dropdowns for Timeframe and LLM */}
        <div className="flex justify-between mb-6">
          <div className="relative">
            <button
              onClick={toggleDropdown}
              className={`flex items-center border rounded-md p-2 ${isDropdownOpen ? 'border-blue-500' : 'border-gray-300 dark:border-gray-600'} transition-colors`}
            >
              <AiOutlineClockCircle className="inline mr-1" />
              Timeframe: {selectedTimeframe}
            </button>
            {isDropdownOpen && (
              <div className="absolute z-10 mt-1 w-full border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 shadow-lg">
                {timeframes.map((timeframe) => (
                  <button
                    key={timeframe}
                    onClick={() => handleTimeframeChange(timeframe)}
                    className="block w-full text-left p-2 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    {timeframe}
                  </button>
                ))}
              </div>
            )}
          </div>
          <div className="relative">
            <button
              onClick={toggleLLMDropdown}
              className={`flex items-center border rounded-md p-2 ${isLLMDropdownOpen ? 'border-blue-500' : 'border-gray-300 dark:border-gray-600'} transition-colors`}
            >
              <AiOutlineFileText className="inline mr-1" />
              LLM: {selectedLLM}
            </button>
            {isLLMDropdownOpen && (
              <div className="absolute z-10 mt-1 w-full border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 shadow-lg">
                {['All', 'GPT-3', 'GPT-4', 'LLM-5'].map((llm) => (
                  <button
                    key={llm}
                    onClick={() => handleLLMChange(llm)}
                    className="block w-full text-left p-2 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    {llm}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="border border-gray-700 dark:border-gray-300 p-4 rounded-lg shadow-lg">
          <pre className="whitespace-pre-wrap font-mono">
            {logData
              .filter(log => selectedLLM === 'All' || log.llm === selectedLLM) // Filter logs by LLM
              .map(log => (
                <div key={log.id} className={`mb-2 ${log.message.includes('Error') ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-300'}`}>
                  <span className="font-bold">{log.timestamp}</span> [{log.llm}]: {log.message}
                </div>
              ))}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default LogsPage;

