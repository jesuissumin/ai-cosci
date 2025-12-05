# CoScientist: AI Research Assistant for Biomedical Questions

An LLM-based AI system for answering complex multi-step biomedical research questions. Built for the 바이오 AI 연구동료 경진대회 (Bio AI Co-Scientist Competition).

## Features

- **Multi-step Reasoning**: Break down complex research questions into logical steps
- **Tool Integration**: Python code execution, literature search, database queries
- **PubMed Integration**: Search peer-reviewed literature to ground answers in evidence
- **Database Querying**: Access competition databases (DrugBank, BindingDB, Pharos, STRING, GWAS)
- **Scientific Rigor**: Distinguish between facts, hypotheses, and speculative ideas
- **OpenRouter API**: Uses Claude Sonnet 4 via OpenRouter for cost efficiency

## Project Structure

```
coscientist/
├── src/
│   ├── agent/              # Core agent loop
│   │   ├── agent.py        # Main BioinformaticsAgent class
│   │   └── openrouter_client.py  # OpenRouter API client
│   ├── tools/              # Tool implementations
│   │   └── implementations.py
│   └── cli.py              # Command-line interface
├── data/
│   └── databases/          # Competition database files (parquet/csv/tsv)
├── notebooks/              # Example usage and testing
├── tests/                  # Test suite
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Installation

1. **Clone/Download the repository**
   ```bash
   cd coscientist
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

4. **Prepare database files**
   Place your competition data files in `data/databases/`:
   - `drugbank.parquet` or similar
   - `bindingdb.parquet`
   - `pharos.parquet`
   - `string.parquet`
   - `gwas.parquet`

## Quick Start

### Using the CLI

```bash
# Ask a single question
python -m src.cli --question "How can gene signatures guide drug repositioning?"

# Interactive mode
python -m src.cli --interactive

# Verbose mode (see tool calls)
python -m src.cli --question "..." --verbose

# Use a different model
python -m src.cli --question "..." --model "openai/gpt-4"
```

### Using Python directly

```python
from src.agent import create_agent

agent = create_agent()
response = agent.run("Your research question here", verbose=True)
print(response)
```

### In a Jupyter notebook

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from dotenv import load_dotenv
from src.agent import create_agent

load_dotenv()
agent = create_agent()
response = agent.run("Question?", verbose=True)
```

## Available Tools

### 1. `execute_python`
Execute Python code for data analysis and visualization.

```python
code = """
import pandas as pd
import numpy as np

data = pd.DataFrame({'gene': ['BRCA1', 'TP53'], 'expression': [5.2, 3.1]})
print(data.describe())
"""
```

### 2. `search_pubmed`
Search PubMed for scientific articles.

```python
query = "SARS-CoV-2 vaccine effectiveness"
max_results = 10
```

Returns: Title, abstract, authors, PMID for each article.

### 3. `query_database`
Query competition databases.

```python
db_name = "drugbank"  # or: bindingdb, pharos, string, gwas
query = "protein_name:EGFR"  # Query format specific to database
```

### 4. `read_file`
Read data files directly.

```python
file_path = "databases/drugbank.parquet"
```

Returns: Column names, shape, preview of first rows (for parquet/CSV/TSV).

## System Prompt

The agent uses a specialized system prompt optimized for biomedical research that:

- Emphasizes distinguishing facts from speculation
- Encourages multi-step problem solving
- Emphasizes data exploration and pattern recognition
- Integrates literature to ground answers in evidence
- Assesses practical feasibility of proposed strategies
- Uses clear, structured communication with appropriate uncertainty

See `agent.get_system_prompt()` for the full prompt.

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `OPENROUTER_MODEL`: Model to use (default: `anthropic/claude-sonnet-4-20250514`)
- `DATA_DIR`: Path to database files (default: `./data`)

### Agent Parameters

```python
agent = create_agent(
    api_key="your_key",  # Optional, defaults to env var
    model="anthropic/claude-sonnet-4-20250514"
)

# Control response generation
response = agent.run(
    question="...",
    verbose=False  # Print intermediate steps
)
```

## Advanced Usage

### Custom Tool Integration

Add new tools by:

1. Implementing the tool function in `src/tools/implementations.py`
2. Add it to the `tools` dict in `BioinformaticsAgent.__init__`
3. Define its schema in `get_tool_definitions()`

### Conversation History

```python
agent = create_agent()
agent.add_message("user", "First question?")
response1 = agent.run("...")
# Continue conversation
agent.add_message("user", "Follow-up question?")
response2 = agent.run("...")
```

### Cost Optimization

Monitor API usage through OpenRouter dashboard. The Sonnet 4 model provides good balance between cost and capability for biomedical reasoning.

## Competition Notes

### Optimization Strategies

1. **Context Management**: Keep conversation history concise to reduce token usage
2. **Tool Selection**: Cache database queries to avoid redundant calls
3. **Citation Quality**: PubMed search results provide real citations (avoid hallucination)
4. **Time Management**: Set reasonable max_iterations limit for quick responses on competition day

### Example Competition Questions

The system is designed to handle:

- "Design a drug repositioning strategy for [disease] using [gene signature]"
- "Analyze protein-ligand interactions for [protein] and suggest candidates"
- "What experimental validation would you propose for [hypothesis]?"
- "Synthesize the literature on [topic] and propose next steps"

## Troubleshooting

### API Key Issues
```
Error: OPENROUTER_API_KEY not found in environment
```
Solution: Create `.env` file and add your OpenRouter API key.

### File Not Found
```
Error: File not found: databases/drugbank.parquet
```
Solution: Ensure database files are in `data/databases/` directory.

### Tool Execution Errors
Set `verbose=True` to see detailed tool output and debugging information.

### Timeout Issues
Adjust timeout in tool implementations if needed:
- `execute_python`: timeout parameter (default 30s)
- API calls: timeout in `openrouter_client.py` (default 120s)

## Development

### Running Tests
```bash
pytest tests/
```

### Adding Debug Output
```python
agent.run(question, verbose=True)
```

### Checking Tool Calls
Tool calls and results are logged in verbose mode and available in `agent.conversation_history`.

## Dependencies

- `requests`: HTTP requests for OpenRouter API and PubMed
- `python-dotenv`: Environment variable management
- `pandas`: Data manipulation for databases
- `pyarrow`: Parquet file reading
- `biopython`: Bioinformatics utilities
- `pytest`: Testing framework
- `jupyter`: Notebook support

## Performance Tips

1. **Caching**: Store frequently queried database results
2. **Smart Sampling**: For large datasets, start with summary statistics
3. **Parallel Requests**: Use `requests` with thread pools for multiple API calls
4. **Token Efficiency**: Reuse context where possible, summarize long outputs

## Competition Day Checklist

- [ ] API key configured and tested
- [ ] Database files downloaded and placed in `data/databases/`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] System tested with sample questions
- [ ] Conversation history clearing works correctly
- [ ] Verbose mode for debugging ready

## License

MIT License - See LICENSE file for details

## Contact

For issues or questions, refer to the competition documentation or contact the development team.
