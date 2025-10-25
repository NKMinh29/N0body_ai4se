import axios from "axios";

const apiKeys = {
  math: "AIzaSyDaZXDLN4sbU1q7HCrK5SIAll8Spn8FYeM",
  english: "AIzaSyDGrrx5uWIn9Cn3xq_wgQWS9LFaa3CeKJ4",
  history: "AIzaSyBhluv3wI9OuR1KGzzAtk--xqqRXXVT2Wk",
  default: "AIzaSyCH0KRPCl1bYk3nhjnJNcftWeFNBsk5mVI",
};

export const fetchAIResponse = async (mode: keyof typeof apiKeys, query: string) => {

  const apiKey = apiKeys[mode] || apiKeys.default;
  const url = `https://gemini-1-5-flash-api.example.com/query`;

  try {
    const response = await axios.post(
      url,
      { query },
      { headers: { Authorization: `Bearer ${apiKey}` } }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching AI response:", error);
    throw error;
  }
};
