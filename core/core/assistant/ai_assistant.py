import core.core.projectContextBuilder as PCB
import core.core.llm.llm_client as llm_client
import core.core.analyzers.ProjectAnalyzer as PA
class AIDevelopmentAssistant:
    def __init__(self,project):
        self.project = project

    def ask(self,user_promt):
        self.project.load_files()
        self.project.build_index()
        PA.ProjectAnalyzer(self.project).analyze()
        context = PCB.ProjectContextBuilder(self.project).build_context()

        system_prompt = f"""
                        أنت مساعد برمجي متخصص.

                        أجب دائمًا باللغة العربية الفصحى.

                        اعتمد فقط على المعلومات الموجودة في سياق المشروع.
                        إذا لم تجد معلومة، فقل: "لا أملك معلومات كافية."

                        {context}
                        """
        model = llm_client.LLMClient()
        response = model.ask(system_prompt=system_prompt,user_prompt=user_promt)
        return response
