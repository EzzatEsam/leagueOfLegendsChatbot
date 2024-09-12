import React from "react";
import SuggestionCard from "./suggestionCard"; // Assuming SuggestionCard is in the same directory

interface SuggestionsProps {
  suggestions: string[];
  logoUrl: string;
  onSuggestionClick: (suggestion: string) => void;
}

const Suggestions: React.FC<SuggestionsProps> = ({
  suggestions,
  logoUrl,
  onSuggestionClick,
}) => {
  return (
    <div className="flex flex-col items-center space-y-4 m-8">
      {/* Logo */}
      <img src={logoUrl} alt="Logo" className="w-40 h-40 m-4" />

      {/* Suggestions */}
      <div className="grid grid-cols-1 gap-4 w-full md:grid-cols-2">
        {suggestions.map((suggestion, index) => (
          <SuggestionCard
            key={index}
            prompt={suggestion}
            onClick={() => onSuggestionClick(suggestion)}
          />
        ))}
      </div>
    </div>
  );
};

export default Suggestions;
