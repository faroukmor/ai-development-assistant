import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.retrieval.tokenizer import tokenize, match_tokens


def run_checks():
    # stopwords are dropped from questions, so generic words never match
    assert tokenize("what is a banana") == ["banana"], \
        "stopwords must be dropped, leaving only meaningful tokens"

    # snake_case and CamelCase both split correctly
    assert tokenize("build_context") == ["build", "context"]
    assert tokenize("FileContextBuilder") == ["file", "context", "builder"]
    assert tokenize("HTTPServer") == ["http", "server"]

    # splitting enables human phrasing to hit code names
    assert match_tokens(tokenize("load_files"), tokenize("where do we load files"))
    assert match_tokens(tokenize("FileSearch"), tokenize("how does FileSearch work"))

    # and the banana question must no longer match single-letter class A
    assert not match_tokens(tokenize("A"), tokenize("what is a banana")), \
        "single-letter class name must not match a question without it"

    print("ALL TOKENIZER CHECKS PASSED")


if __name__ == "__main__":
    run_checks()

