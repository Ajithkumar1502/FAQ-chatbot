from langgraph.graph import StateGraph, END # type: ignore
from langgraph.prebuilt import ToolNode # type: ignore
from typing import TypedDict, Optional
import difflib


faq_data = {
    "Hi,hiii?": "Hello Welcome",
    "What are your business hours?": "We are open from 9 AM to 5 PM, Monday to Friday.",
    "Where are you located?": "Our main office is located at 1234 Main Street, Springfield.",
    "How can I contact support?": "You can contact support by emailing support@example.com.",
    "What services do you offer?": "We offer web development, mobile app development, and IT consulting.",
    "How do I reset my password?": "Click on 'Forgot Password' on the login page and follow the instructions."
}

class FAQState(TypedDict):
    user_input: str
    matched_question: Optional[str]
    answer: Optional[str]

def match_question(state: FAQState) -> FAQState:
    user_question = state["user_input"]
    questions = list(faq_data.keys())
    best_match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)

    if best_match:
        matched_question = best_match[0]
        answer = faq_data[matched_question]
    else:
        matched_question = None
        answer = "Sorry, I couldn't find an answer to your question."

    return {
        "user_input": user_question,
        "matched_question": matched_question,
        "answer": answer
    }

graph = StateGraph(FAQState)
graph.add_node("match_question", match_question)
graph.set_entry_point("match_question")
graph.set_finish_point("match_question")

faq_bot = graph.compile()

def run_faq_bot():
    print("Hi! I'm your FAQ bot. Ask me a question or type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Bot: Goodbye!")
            break

        result = faq_bot.invoke({"user_input": user_input})
        print(f"Bot: {result['answer']}")

if __name__ == "__main__":
    run_faq_bot()
