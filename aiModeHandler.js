class AIHandler {
    constructor() {
        this.apiKeys = {
            math: "AIzaSyDaZXDLN4sbU1q7HCrK5SIAll8Spn8FYeM",
            english: "AIzaSyDGrrx5uWIn9Cn3xq_wgQWS9LFaa3CeKJ4",
            history: "AIzaSyBhluv3wI9OuR1KGzzAtk--xqqRXXVT2Wk",
            default: "AIzaSyCH0KRPCl1bYk3nhjnJNcftWeFNBsk5mVI"
        };
    }

    getApiKey(mode) {
        return this.apiKeys[mode] || this.apiKeys.default;
    }

    async fetchAIResponse(mode, input) {
        const apiKey = this.getApiKey(mode);
        const url = `https://gemini1.5flash.api/ai?key=${apiKey}`;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query: input })
            });

            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error("Error fetching AI response:", error);
            return "An error occurred while processing your request.";
        }
    }
}

module.exports = AIHandler;
