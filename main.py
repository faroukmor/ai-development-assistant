import getpass

import core.assistant.ai_assistant as ai
from core.llm.external_llm_client import ExternalLLMClient

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt


DEFAULT_PROJECT_PATH = r"C:\Users\HP\Documents\Programming\GitHub repos\ai-development-assistant"

console = Console()

user_path = Prompt.ask("[bold blue]Project Path[/bold blue] [dim](Enter for default)[/dim]")

project_path = user_path.strip() or DEFAULT_PROJECT_PATH

use_external = Prompt.ask(
    "[bold blue]Use an external model via API key?[/bold blue] [dim](y/N)[/dim]",
    choices=["y", "n"],
    default="n",
)

llm = None
if use_external == "y":
    console.print(Panel(
        "[bold yellow]WARNING[/bold yellow]\n"
        "Your project context (source code excerpts) will be sent to the "
        "model provider and will [bold]not stay on this machine[/bold].\n\n"
        "The key is kept in memory only — it is never written to disk.",
        border_style="yellow",
    ))
    model_name = Prompt.ask("Model name [dim](e.g. openai/gpt-4o-mini)[/dim]")
    api_key = getpass.getpass("API key (hidden): ").strip()
    base_url = Prompt.ask(
        "API base URL [dim](Enter for OpenRouter)[/dim]",
        default="https://openrouter.ai/api/v1",
    )
    llm = ExternalLLMClient(model_name, api_key, base_url)
else:
    console.print("[dim]Running locally with Ollama — nothing leaves this machine.[/dim]")

assistant = ai.AIDevelopmentAssistant(project_path, llm_client=llm)


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