import time

import core.assistant.ai_assistant as ai
from core.llm.external_llm_client import ExternalLLMClient, AuthError

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt


DEFAULT_PROJECT_PATH = r"C:\Users\HP\Documents\Programming\GitHub repos\ai-development-assistant"

console = Console()

def read_hidden(label):
    """Read a secret with a * per character, accepting typing and paste.

    rich's password mode and getpass both swallowed all input in the Windows
    terminal, so this reads the console directly via msvcrt; other platforms
    fall back to getpass.
    """
    try:
        import msvcrt
    except ImportError:
        import getpass
        return getpass.getpass(label).strip()

    print(label, end="", flush=True)
    chars = []
    while True:
        ch = msvcrt.getwch()
        if ch in ("\r", "\n"):
            print()
            return "".join(chars).strip()
        if ch in ("\b", "\x08"):
            if chars:
                chars.pop()
                print("\b \b", end="", flush=True)
            continue
        if ch == "\x03":  # Ctrl+C
            raise KeyboardInterrupt
        if ch in ("\x00", "\xe0"):  # special keys (arrows, F-keys): skip the pair
            msvcrt.getwch()
            continue
        chars.append(ch)
        print("*", end="", flush=True)

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
    base_url = Prompt.ask(
        "API base URL [dim](Enter for OpenRouter)[/dim]",
        default="https://openrouter.ai/api/v1",
    )
    api_key = read_hidden("API key (hidden, shown as *): ")
    if not api_key:
        console.print("[yellow]No key entered — running locally instead.[/yellow]")
        use_external = "n"

    if use_external == "y":
        llm = ExternalLLMClient(model_name, api_key, base_url)
    else:
        console.print("[dim]Running locally with Ollama — nothing leaves this machine.[/dim]")
else:
    console.print("[dim]Running locally with Ollama — nothing leaves this machine.[/dim]")

assistant = ai.AIDevelopmentAssistant(project_path, llm_client=llm)


console.print(
    Panel.fit(
        "[bold cyan]AI Development Assistant[/bold cyan]\n"
        "[dim]Offline software engineering assistant[/dim]\n"
        f"Model: {assistant.model_info}\n"
        "[dim]Type 'q' to quit[/dim]",
        border_style="cyan"
    )
)

def render_stream(question):
    """Stream as normal scrollable output while generating, then the complete
    answer once in a panel. Live redrawing is the only way to keep a growing
    box, and it consumes the scrollback — so the stream stays plain and the
    boxed version is printed once at the end.
    """
    stream = assistant.ask_stream(question)
    started = time.time()

    # the setup (index, retrieval, context) runs inside the first next();
    # errors here (401, unknown model, ollama down) surface immediately
    with console.status("[bold cyan]Analyzing project...[/bold cyan]", spinner="dots"):
        first = next(stream, None)
    if first is None:
        console.print("[yellow]The model returned no content.[/yellow]")
        return

    console.print("[bold cyan]AI Assistant[/bold cyan]")
    parts = [first]
    console.out(first, end="", highlight=False)
    for chunk in stream:
        parts.append(chunk)
        console.out(chunk, end="", highlight=False)
    console.print()

    console.print(
        Panel(
            Markdown("".join(parts)),
            title="[bold cyan]AI Assistant[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
    )
    console.print(
        f"[dim]answered in {time.time() - started:.1f}s · {assistant.model_info}[/dim]"
    )

while True:

    try:
        user_input = Prompt.ask("[bold green]You[/bold green]")

        if user_input.lower() == "q" or user_input == "ض":
            console.print("[dim]Goodbye.[/dim]")
            break

        render_stream(user_input)

    except KeyboardInterrupt:
        console.print("\n[dim]Goodbye.[/dim]")
        break

    except Exception as e:
        # The external provider rejected the key: offer to re-enter it in
        # place and retry the same question, without restarting the app.
        if isinstance(e, AuthError) and isinstance(assistant.llm_client, ExternalLLMClient):
            console.print(Panel(
                f"[bold red]{type(e).__name__}[/bold red]\n{e}",
                title="Error",
                border_style="red"
            ))
            new_key = read_hidden("New API key (hidden, shown as *, empty to cancel): ")
            if not new_key:
                console.print("[dim]No key entered — staying with the current one.[/dim]")
                continue
            try:
                assistant.llm_client.set_api_key(new_key)
            except RuntimeError as key_error:
                console.print(Panel(f"[bold red]Error[/bold red]\n{key_error}", border_style="red"))
                continue
            try:
                render_stream(user_input)
            except Exception as retry_error:
                console.print(Panel(f"[bold red]{type(retry_error).__name__}[/bold red]\n{retry_error}", border_style="red"))
            continue

        console.print(
            Panel(
                f"[bold red]{type(e).__name__}[/bold red]\n{e}",
                title="Error",
                border_style="red"
            )
        )