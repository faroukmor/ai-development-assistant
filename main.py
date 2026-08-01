import core.project.project as P
import core.assistant.ai_assistant as ai



project_path = input(r"enter project path:")

project = P.Project(project_path)

assistant = ai.AIDevelopmentAssistant(project)


while(1):
    user_input = input("                USER(q to quit):")
    if user_input.lower() == "q":
        break
    answer = assistant.ask(
        f"{user_input}."
    )

    print("AI ASSISTANT:" + answer)
