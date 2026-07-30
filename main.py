import core.core.project as P
import core.core.assistant.ai_assistant as ai


path = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"
project = P.Project(path=path)

assistant = ai.AIDevelopmentAssistant(project)

while(1):
    user_input = input("المستخدم (خروج):")
    if user_input == "خروج":
        break
    answer = assistant.ask(
        f"{user_input}."
    )

    print("المساعد الذكي:" + answer)
