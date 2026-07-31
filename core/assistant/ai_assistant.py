import core.context.project_context_builder as PCB
import core.llm.llm_client as llm_client
import core.analyzers.analysis_pipeline as PA
import core.context.context_selector as cs
class AIDevelopmentAssistant:
    def __init__(self,project):
        self.project = project

    def ask(self,user_prompt):
        self.project.load_files()
        self.project.build_index()
        PA.ProjectAnalyzer(self.project).analyze()
        
        selector = cs.ContextSelector(self.project)

        relevant_files = selector.get_relevant_files(user_prompt)

        context = PCB.ProjectContextBuilder(self.project,relevant_files).build_context()
        system_prompt = f"""
                        أنت مساعد برمجي متخصص.

                        أجب دائمًا باللغة العربية الفصحى.

                        اعتمد فقط على المعلومات الموجودة في سياق المشروع.
                        إذا لم تجد معلومة، فقل: "لا أملك معلومات كافية."

                        {context}
                        """
        model = llm_client.LLMClient('qwen2.5:3b')
        response = model.ask(system_prompt=system_prompt,user_prompt=user_prompt)
        return response
