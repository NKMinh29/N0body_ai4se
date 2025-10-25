import google.generativeai as genai
import os
from typing import Optional

class GeminiService:
    def __init__(self):
        # API Keys for different modes
        self.api_keys = {
            'math': 'AIzaSyDaZXDLN4sbU1q7HCrK5SIAll8Spn8FYeM',
            'english': 'AIzaSyDGrrx5uWIn9Cn3xq_wgQWS9LFaa3CeKJ4',
            'history': 'AIzaSyBhluv3wI9OuR1KGzzAtk--xqqRXXVT2Wk',
            'general': 'AIzaSyCH0KRPCl1bYk3nhjnJNcftWeFNBsk5mVI'
        }
        
        # Mode-specific system prompts
        self.system_prompts = {
            'math': """You are N0b0dy, an expert mathematics tutor. Your role is to:
- Help students understand mathematical concepts step by step
- Provide clear explanations with examples
- Break down complex problems into manageable steps
- Use appropriate mathematical notation and terminology
- Encourage learning and build confidence
- Always show your work and explain your reasoning
- Be patient and supportive in your teaching approach""",

            'english': """You are N0b0dy, an expert English language teacher. Your role is to:
- Help students improve their English language skills
- Explain grammar rules clearly with examples
- Provide vocabulary definitions and usage examples
- Help with pronunciation, writing, and communication
- Correct mistakes gently and explain why
- Encourage practice and provide constructive feedback
- Use appropriate teaching methods for different skill levels
- Be encouraging and supportive in your approach""",

            'history': """You are N0b0dy, an expert history teacher. Your role is to:
- Help students understand historical events and their significance
- Provide context and background information
- Explain cause-and-effect relationships in history
- Discuss different perspectives and interpretations
- Connect historical events to modern times
- Use engaging storytelling techniques
- Encourage critical thinking about historical sources
- Make history relevant and interesting for students""",

            'general': """You are N0b0dy, a helpful AI assistant. Your role is to:
- Provide accurate and helpful information
- Answer questions clearly and comprehensively
- Be friendly and approachable in your responses
- Offer practical advice and solutions
- Maintain a professional yet conversational tone
- Help users with a wide variety of topics
- Be honest about limitations when you don't know something"""
        }

    def get_response(self, user_message: str, mode: str = 'general', conversation_history: list = None) -> str:
        """
        Get AI response from Gemini based on the selected mode
        
        Args:
            user_message: The user's input message
            mode: The AI mode ('math', 'english', 'history', 'general')
            conversation_history: Previous messages in the conversation
            
        Returns:
            AI response string
        """
        try:
            # Get the appropriate API key for the mode
            api_key = self.api_keys.get(mode, self.api_keys['general'])
            
            # Configure the model
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Build the conversation context
            system_prompt = self.system_prompts.get(mode, self.system_prompts['general'])
            
            # Create conversation history if provided
            if conversation_history:
                # Build context from conversation history
                context = f"{system_prompt}\n\nConversation History:\n"
                for msg in conversation_history[-10:]:  # Last 10 messages for context
                    role = "User" if msg.get('sender') == 'user' else "N0b0dy"
                    context += f"{role}: {msg.get('content', '')}\n"
                context += f"\nCurrent User Message: {user_message}"
                
                # Generate response with context
                response = model.generate_content(context)
            else:
                # Generate response with system prompt
                prompt = f"{system_prompt}\n\nUser: {user_message}\nN0b0dy:"
                response = model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating Gemini response: {str(e)}")
            # Fallback response based on mode
            fallback_responses = {
                'math': f"I apologize, but I'm having trouble accessing the math tutoring system right now. However, I'd be happy to help you with your math question: '{user_message}'. Could you please try again in a moment?",
                'english': f"I'm experiencing some technical difficulties with the English teaching system. Your question about '{user_message}' is important to me. Please try again shortly.",
                'history': f"I'm having trouble accessing the history teaching resources at the moment. Your question about '{user_message}' deserves a proper historical perspective. Please try again soon.",
                'general': f"I'm experiencing some technical issues right now, but I want to help you with '{user_message}'. Please try again in a moment."
            }
            return fallback_responses.get(mode, f"I'm having technical difficulties. Please try again later.")

    def test_api_key(self, mode: str) -> bool:
        """
        Test if an API key is working
        
        Args:
            mode: The mode to test
            
        Returns:
            True if API key works, False otherwise
        """
        try:
            api_key = self.api_keys.get(mode, self.api_keys['general'])
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Simple test request
            response = model.generate_content("Hello, this is a test message.")
            return response.text is not None
            
        except Exception as e:
            print(f"API key test failed for mode {mode}: {str(e)}")
            return False

# Create a global instance
gemini_service = GeminiService()
