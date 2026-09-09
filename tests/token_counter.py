# Dev tool: measures how much of the model's context window FINAL_CONTEXT.txt uses.
# Requires: pip install transformers (downloads tokenizer files from HuggingFace on first run)
from pathlib import Path
from transformers import AutoTokenizer


FILE_PATH = Path(r"debug\FINAL_CONTEXT.txt")

MODEL = "Qwen/Qwen2.5-Coder-3B"
MAX_CONTEXT = 32_768


def main():

    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    text = FILE_PATH.read_text(encoding="utf-8")

    tokens = len(
        tokenizer.encode(
            text,
            add_special_tokens=False
        )
    )

    percent = tokens / MAX_CONTEXT * 100
    remaining = MAX_CONTEXT - tokens

    # Visual bar
    bar_length = 30
    filled = round((percent / 100) * bar_length)

    bar = "█" * filled + "░" * (bar_length - filled)

    # Status
    if percent < 50:
        status = "GOOD"
    elif percent < 75:
        status = "LARGE"
    elif percent < 90:
        status = "WARNING"
    else:
        status = "CRITICAL"

    print()
    print("╭──────────────────────────────────────╮")
    print("│          QWEN CONTEXT USAGE          │")
    print("├──────────────────────────────────────┤")
    print(f"│ {bar} │")
    print(f"│              {percent:.1f}%              │")
    print("├──────────────────────────────────────┤")
    print(f"│ Tokens    : {tokens:,} / {MAX_CONTEXT:,}")
    print(f"│ Remaining : {remaining:,}")
    print(f"│ Status    : {status}")
    print("╰──────────────────────────────────────╯")
    print()


if __name__ == "__main__":
    main()

