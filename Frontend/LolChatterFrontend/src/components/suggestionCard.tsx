import React from "react";

interface SuggestionCardProps {
  prompt: string;
  onClick: () => void;
}

const SuggestionCard: React.FC<SuggestionCardProps> = ({ prompt, onClick }) => {
  return (
    <div
      className="bg-gray-100 dark:bg-gray-700 p-4 rounded-2xl border-2 shadow-lg cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-600 transition"
      onClick={onClick}
    >
      <p className="text-gray-900 dark:text-gray-100 text-sm font-medium">
        {prompt}
      </p>
    </div>
  );
};

export default SuggestionCard;
