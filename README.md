## GitDocs: Automated GitHub Repository Documentation

This repository contains the code for GitDocs, a tool that automatically generates documentation for GitHub repositories. GitDocs leverages large language models (LLMs) to analyze code, generate README files, add docstrings, and provide a conversational interface for interacting with the codebase.

### Project Structure

```
├── gitdocs
│   ├── code_analyzer.py
│   ├── docstring_generator.py
│   ├── repository_scraper.py
│   ├── readme_generator.py
│   ├── chat_interface.py
│   ├── main.py
│   ├── code_extensions.txt
│   └── environment.yml
└── README.md
```

### Dependencies

- Python 3.12+
- `google-generativeai`
- `rich`
- `dotenv`
- `gitpython`
- `argparse`

### Installation

1. Clone the repository.
2. Install the required packages:

```bash
conda env create -f environment.yml
conda activate gitdocs
```

3. Create a `.env` file in the root directory and set the `GEMINI_API_KEY` environment variable. You can obtain a Google Generative AI API key from [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

### Usage

To generate documentation for a GitHub repository, run the following command:

```bash
python gitdocs/main.py <repository_url> [--generate-readme] [--generate-docstrings] [--chat]
```

**Example:**

```bash
python gitdocs/main.py https://github.com/google/python-fire --generate-readme --generate-docstrings --chat
```

**Flags:**

- `--generate-readme`: Generates a README.md file for the repository.
- `--generate-docstrings`: Adds docstrings to the code files.
- `--chat`: Starts an interactive chat session where you can ask questions about the codebase.

### Features

- **Code Analysis:** Uses a large language model to analyze the code and generate a structured representation of the codebase.
- **README Generation:** Automatically creates a comprehensive README.md file based on the code analysis.
- **Docstring Generation:** Adds docstrings to code files, explaining the functionality of functions, classes, and methods.
- **Interactive Chat Interface:** Provides a conversational way to explore the codebase, ask questions, and get insights.

### Contributing

Contributions are welcome! Please feel free to open issues and submit pull requests.

### License

This project is licensed under the Apache 2.0 License. See the LICENSE file for more information.


---
Generated with ❤️ using [GitDocs](https://github.com/mikhail-ram/gitdocs).
