import core.project.project as P
import core.assistant.ai_assistant as ai



project_path = input(r"enter project path:")

project = P.Project(project_path)

assistant = ai.AIDevelopmentAssistant(project)


while(1):
    user_input = input("المستخدم (خروج):")
    if user_input == "خروج":
        break
    answer = assistant.ask(
        f"{user_input}."
    )

    print("المساعد الذكي:" + answer)
