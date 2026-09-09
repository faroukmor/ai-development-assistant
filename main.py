import core.assistant.ai_assistant as ai

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt


DEFAULT_PROJECT_PATH = r"C:\Users\HP\Documents\PYTHON Project\ai-development-assistant"

console = Console()

user_path = Prompt.ask("[bold blue]Project Path[/bold blue] [dim](Enter for default)[/dim]")

project_path = user_path.strip() or DEFAULT_PROJECT_PATH

assistant = ai.AIDevelopmentAssistant(project_path)


console.print(
    Panel.fit(
        "[bold cyan]AI Development Assistant[/bold cyan]\n"
        "[dim]Offline software engineering assistant[/dim]\n"
        "[dim]Type 'q' to quit[/dim]",
        border_style="cyan"
    )
)

while True:

    try:
        user_input = Prompt.ask("[bold green]You[/bold green]")

        if user_input.lower() == "q" or user_input == "ض":
            console.print("[dim]Goodbye.[/dim]")
            break

        with console.status(
            "[bold cyan]Analyzing project...[/bold cyan]",
            spinner="dots"
        ):
            answer = assistant.ask(user_input)

        console.print(
            Panel(
                Markdown(answer),
                title="[bold cyan]AI Assistant[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            )
        )

    except KeyboardInterrupt:
        console.print("\n[dim]Goodbye.[/dim]")
        break

    except Exception as e:
        console.print(
            Panel(
                f"[bold red]{type(e).__name__}[/bold red]\n{e}",
                title="Error",
                border_style="red"
            )
        )