const AIHandler = require("./aiModeHandler");

const aiHandler = new AIHandler();

async function handleUserInput(mode, input) {
    const response = await aiHandler.fetchAIResponse(mode, input);
    console.log(`AI Response for mode "${mode}":`, response);
}

// Example usage
handleUserInput("math", "What is the derivative of x^2?");
handleUserInput("english", "Can you write a poem about the sea?");
handleUserInput("history", "Tell me about the French Revolution.");
handleUserInput("science", "Explain the theory of relativity."); // Will use default API key
