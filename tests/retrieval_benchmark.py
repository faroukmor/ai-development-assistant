RETRIEVAL_BENCHMARK = [
    {
        "question": "what does build_context do",
        "must": [("context_builder.py", "build_context")],
        "must_not": [("project_indexer.py", "build")],
    },
    {
        "question": "how does FileSearch work",
        "must": [("file_search.py", "FileSearch")],
        "must_not": [("embedding_search.py", "search"),
                     ("hybrid_retriever.py", "search"),
                     ("symbol_search.py", "search")],
    },
    {
        "question": "where do we load files",
        "must": [("project_loader.py", "load_files")],
        "must_not": [],
    },
    {
        "question": "what is read_file",
        "must": [("file_reader.py", "read_file")],
        "must_not": [],
    },
    {
        "question": "what is SymbolContextBuilder",
        "must": [("symbol_context_builder.py", "SymbolContextBuilder")],
        "must_not": [],
    },
    {
        "question": "build_context",
        "must": [("context_builder.py", "build_context")],
        "must_not": [],
    },
    {
        "question": "FileContextBuilder",
        "must": [("file_context_builder.py", "FileContextBuilder")],
        "must_not": [],
    },
    {
        "question": "what is a banana",
        "must": [],
        "must_not": [("test2.py", "A")],
        "expect_empty": True,
    },
    {
        "question": "where is the context built",
        "must": [("context_builder.py", None)],
        "must_not": [],
    },
    {
        "question": "how does read_file get called",
        "must": [("file_reader.py", None)],
        "must_not": [],
    },
]