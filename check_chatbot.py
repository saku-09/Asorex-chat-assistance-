import sys
import os

# Add 'app' to path
sys.path.append(os.path.join(os.getcwd(), 'app'))

from chatbot import get_response

def test_chatbot():
    test_queries = [
        "hi",
        "What is the price of OPC cement in Pune?",
        "steel Fe500 price in Nashik",
        "future price of cement",
        "bye"
    ]

    print("--- Asorex Chatbot Functionality Test ---")
    for query in test_queries:
        print(f"\nUser: {query}")
        response = get_response(query)
        print(f"Bot: {response}")

if __name__ == "__main__":
    test_chatbot()
