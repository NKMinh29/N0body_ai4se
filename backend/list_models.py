#!/usr/bin/env python3

import google.generativeai as genai

def list_available_models(api_key):
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        
        print("Available models:")
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"- {model.name}")
        
        return True
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        return False

if __name__ == "__main__":
    # Test with the general API key
    api_key = 'AIzaSyCH0KRPCl1bYk3nhjnJNcftWeFNBsk5mVI'
    list_available_models(api_key)
