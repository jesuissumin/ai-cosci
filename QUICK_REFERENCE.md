# Quick Reference Card

## Installation & Setup (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env with your OpenRouter API key

# 3. Test
python -m src.cli --question "What is a simple bio question?"
```

## Usage Patterns

### Pattern 1: Command Line (Fastest)
```bash
python -m src.cli --question "Your question here?"
python -m src.cli --question "..." --verbose  # See tool calls
python -m src.cli --interactive               # Chat mode
```

### Pattern 2: Python Script
```python
from src.agent import create_agent
from dotenv import load_dotenv

load_dotenv()
agent = create_agent()
response = agent.run("Your question")
print(response)
```

### Pattern 3: Jupyter Notebook
```python
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv
from src.agent import create_agent

load_dotenv()
agent = create_agent()
agent.run("Your question", verbose=True)
```

## Tools Available

| Tool | Use For | Example |
|------|---------|---------|
| `execute_python` | Data analysis, calculations | Stats, visualizations |
| `search_pubmed` | Literature search | Find papers on topics |
| `query_database` | Access databases | Query DrugBank, STRING |
| `read_file` | Load data files | Parquet, CSV, TSV |

## Common Questions

### "How do I query a specific protein?"
Agent will call `query_database` with your specifications.

### "Can I search for papers on a topic?"
Agent will call `search_pubmed` and return real citations.

### "How do I analyze my data?"
Agent will write and execute Python code.

### "Can I load multiple databases?"
Agent can query multiple databases and combine results.

## Debugging Checklist

| Issue | Solution |
|-------|----------|
| "API key not found" | Create `.env` with key |
| "File not found" | Place data in `data/databases/` |
| "Tool failed" | Run with `--verbose` to see error |
| "Slow response" | Check internet, try simpler question |
| "Wrong answer" | Check verbose output for tool calls |

## Key Files

| File | Purpose |
|------|---------|
| `src/agent/agent.py` | Main agent loop |
| `src/agent/openrouter_client.py` | API communication |
| `src/tools/implementations.py` | Tool functions |
| `src/cli.py` | Command-line interface |
| `.env` | API key (create from `.env.example`) |

## Typical Workflow

```
1. Set up (2 min)
   └─ Install dependencies, configure API key

2. Test (2 min)
   └─ Run simple question to verify setup

3. Prepare data (5-10 min)
   └─ Add database files to data/databases/

4. Ask questions (1-2 min each)
   └─ CLI mode for quick tests
   └─ Jupyter mode for detailed analysis

5. Debug/Optimize (as needed)
   └─ Use --verbose for tool details
   └─ Adjust system prompt if needed
   └─ Cache repeated queries
```

## System Prompt Highlights

The agent is configured to:
- Distinguish facts from speculation
- Use peer-reviewed sources
- Propose validated strategies
- Acknowledge uncertainty
- Think through problems step-by-step

## API Costs

- **Budget**: 100만원
- **Model**: Claude Sonnet 4 (~$0.015/1K output tokens)
- **Typical query**: 1-3K tokens total
- **Budget allows**: 100+ multi-step queries

## Important Limits

- **Max iterations**: 10 (prevents infinite loops)
- **PubMed results**: Up to 10 per search
- **Timeout**: 30 seconds for code execution
- **API timeout**: 120 seconds

## Competition Day Tips

```
✓ Test everything before competition day
✓ Have database files ready
✓ Know your API budget remaining
✓ Use verbose mode if something fails
✓ Keep questions clear and specific
✓ Note response times for time management
```

## Environment Variables

```bash
OPENROUTER_API_KEY=your_key             # Required
OPENROUTER_MODEL=claude-sonnet-4...    # Optional
DATA_DIR=./data                         # Optional
```

## Performance Tips

1. **Caching**: Store DB query results
2. **Simplify**: Break complex questions into steps
3. **Specific**: Mention exact genes/proteins names
4. **Cite**: Agent will include real PMIDs
5. **Verify**: Cross-check results with literature

## Adding Custom Tools

1. Write function in `src/tools/implementations.py`
2. Add to `self.tools` dict in `BioinformaticsAgent`
3. Add definition to `get_tool_definitions()`

## Conversation History

```python
agent = create_agent()

# Single query
response = agent.run("Q1?")

# Follow-up (history maintained)
agent.add_message("user", "Follow-up Q2?")
response = agent.run("...")  # Includes Q1 context

# Clear history
agent.conversation_history = []
```

## Emergency Commands

```bash
# Test API connection
python -c "from src.agent import create_agent; create_agent()"

# Check Python env
python -m pip list | grep -E "requests|pandas|biopython"

# Quick test
echo "import requests; print(requests.__version__)" | python
```

## File Locations

```
Your Project Root (coscientist/)
├── src/                    ← Main code
├── data/databases/         ← Your data files
├── notebooks/              ← Testing scripts
├── .env                    ← Your API key (create this)
└── requirements.txt        ← Dependencies
```

## Next Steps After Setup

1. [ ] Run `python -m src.cli --question "simple test question"`
2. [ ] Try interactive mode: `python -m src.cli --interactive`
3. [ ] Prepare your database files
4. [ ] Test with real competition question
5. [ ] Customize system prompt if needed

---

For full details, see: README.md | GETTING_STARTED.md | PROJECT_OVERVIEW.md
