#!/usr/bin/env python3

import google.generativeai as genai
import sys

def test_api_key(api_key, mode):
    try:
        print(f"Testing {mode} API key...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        response = model.generate_content("Hello, this is a test message.")
        print(f"✅ {mode} API key works! Response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ {mode} API key failed: {str(e)}")
        return False

if __name__ == "__main__":
    api_keys = {
        'math': 'AIzaSyDaZXDLN4sbU1q7HCrK5SIAll8Spn8FYeM',
        'english': 'AIzaSyDGrrx5uWIn9Cn3xq_wgQWS9LFaa3CeKJ4',
        'history': 'AIzaSyBhluv3wI9OuR1KGzzAtk--xqqRXXVT2Wk',
        'general': 'AIzaSyCH0KRPCl1bYk3nhjnJNcftWeFNBsk5mVI'
    }
    
    print("Testing Gemini API Keys...")
    print("=" * 50)
    
    results = {}
    for mode, key in api_keys.items():
        results[mode] = test_api_key(key, mode)
        print()
    
    print("Summary:")
    print("=" * 50)
    for mode, success in results.items():
        status = "✅ Working" if success else "❌ Failed"
        print(f"{mode.capitalize()}: {status}")
    
    working_keys = sum(results.values())
    print(f"\nTotal working keys: {working_keys}/4")
