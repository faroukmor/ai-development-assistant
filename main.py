import core.core.project as P
import core.core.assistant.ai_assistant as ai


path = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"
project = P.Project(path=path)

assistant = ai.AIDevelopmentAssistant(project)

answer = assistant.ask(
    "اشرح هذا المشروع."
)

print(answer)