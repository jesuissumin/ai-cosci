# CoScientist

AI-powered research assistant for biomedical questions using multi-agent collaboration and tool-augmented reasoning.

## Quick Start

```bash
# Basic question
python -m src.cli --question "What is the role of TP53 in cancer?"

# Multi-agent virtual lab
python -m src.cli \
  --question "Design a CRISPR screen for drug resistance" \
  --virtual-lab \
  --rounds 2 \
  --team-size 3

# Combined mode with consensus
python -m src.cli \
  --question "예시질문" \
  --combined \
  --rounds 2 \
  --team-size 3 \
  --verbose
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install local paper-qa (editable)
pip install -e ext-tools/paper-qa

# Create .env file (see Configuration section)
cp .env.example .env  # then edit with your API keys
```

## Configuration

Create `.env` file in project root:

```bash
# === API Keys ===
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_KEY=sk-or-v1-your-key-here  # Same as above (for LiteLLM)

# === Models ===
# Main agent (format: provider/model)
OPENROUTER_MODEL=google/gemini-3-pro-preview

# PaperQA (format: openrouter/provider/model - note the prefix!)
PAPERQA_LLM=openrouter/google/gemini-3-pro-preview

# === Data Directories ===
DATABASE_DIR=/path/to/databases  # DrugBank, BindingDB, etc.
INPUT_DIR=./data/Q5  # Question-specific files
PAPER_LIBRARY_DIR=./papers  # Local PDF library

# === PaperQA Settings ===
PAPERQA_EMBEDDING=st-multi-qa-MiniLM-L6-cos-v1  # Local embeddings (free)
PAPERQA_MAX_SOURCES=5

# === Optional: PubMed ===
# PUBMED_EMAIL=your.email@example.com
# PUBMED_API_KEY=your_key
```

**Important**:
- `OPENROUTER_MODEL` uses format: `provider/model` (e.g., `google/gemini-3-pro-preview`)
- `PAPERQA_LLM` uses format: `openrouter/provider/model` (e.g., `openrouter/google/gemini-3-pro-preview`)
- Both use the same underlying model, just different API wrappers

## Usage Modes

### 1. Single Agent (Default)
Fast, direct answers using one AI agent.

```bash
python -m src.cli \
  --question "What is the mechanism of PARP inhibitors?" \
  --verbose
```

**When to use**: Simple questions, quick exploration

---

### 2. Virtual Lab (`--virtual-lab`)
Multi-agent collaboration with specialist roles.

```bash
python -m src.cli \
  --question "Design a clinical trial for CAR-T therapy" \
  --virtual-lab \
  --rounds 3 \
  --team-size 4
```

**How it works**:
1. PI (Principal Investigator) analyzes question and assembles team
2. Specialists work in parallel (e.g., computational biologist, clinician, wet-lab expert)
3. Multiple discussion rounds with cross-pollination of ideas
4. PI synthesizes final consensus answer

**When to use**: Complex questions requiring different expertise, experimental design

**Parameters**:
- `--rounds`: Number of discussion rounds (default: 2)
- `--team-size`: Max number of specialists (default: 3)

---

### 3. LangGraph Workflow (`--langgraph`)
Structured workflow with automatic question classification and routing.

```bash
python -m src.cli \
  --question "Analyze RNA-seq differential expression" \
  --langgraph \
  --verbose
```

**Features**:
- Automatic question classification (wet-lab/computational/literature/general)
- Routes to appropriate virtual lab configuration
- State persistence with checkpointing
- Execution path tracking

**When to use**: When you want structured workflows, state tracking

---

### 4. Combined Mode (`--combined`)
LangGraph + Consensus mechanism for robust answers.

```bash
python -m src.cli \
  --question "Evaluate safety of experimental CRISPR therapy" \
  --combined \
  --rounds 2 \
  --team-size 3
```

**How it works**:
1. Question classified by LangGraph
2. Multiple models run virtual labs **independently**
3. Consensus mechanism synthesizes answers
4. Agreement scoring identifies certainties and uncertainties

**Default consensus models** (from `src/virtuallab_workflow/consensus.py`):
- `google/gemini-3-pro-preview`
- `anthropic/claude-sonnet-4`

**When to use**: High-stakes questions, when you need robustness and uncertainty quantification

---

### 5. With Critic (`--with-critic`)
Single agent with self-critique and refinement.

```bash
python -m src.cli \
  --question "Propose a novel therapeutic target for Alzheimer's" \
  --with-critic
```

**Process**:
1. Generate initial answer
2. Critic reviews and provides feedback
3. Refined final answer

**When to use**: Quality validation, important answers that need review

## Available Tools

All agents have access to these tools:

### `execute_python`
Execute Python code for data analysis.

```python
# Agents can write code like this:
import pandas as pd
df = pd.read_csv('data.csv')
df.describe()
```

Available packages: pandas, numpy, biopython, matplotlib, seaborn

---

### `search_pubmed`
Search PubMed for scientific literature.

```python
search_pubmed(
    query="PARP inhibitors breast cancer",
    max_results=10
)
```

Returns: Title, abstract, authors, journal, DOI

---

### `search_literature`
**Advanced AI-powered literature search using PaperQA.**

```python
search_literature(
    question="What are mechanisms of EGFR inhibitor resistance?",
    mode="auto",  # local -> online -> hybrid
    max_sources=5
)
```

**Modes**:
- `local`: Search only local PDF library
- `online`: Search PubMed/arXiv (downloads papers)
- `auto`: **Recommended** - tries local first, supplements with online if needed
- `hybrid`: Search both simultaneously

**Features**:
- Reads full-text papers (not just abstracts)
- LLM-powered answer generation with citations
- Embedding-based semantic search
- Downloads and processes papers automatically

**Note**: Uses LiteLLM internally (warnings are normal and harmless)

---

### `query_database`
Query biological databases.

```python
query_database(
    db_name="drugbank",
    query="drug_name:Imatinib",
    limit=10
)
```

**Available databases**:
- `drugbank`: Drug-target interactions
- `bindingdb`: Binding affinity data
- `pharos`: Target information
- `string`: Protein-protein interactions
- `gwas`: GWAS catalog

**Special queries**:
- `info`: Database structure and columns
- `all`: Sample rows
- `Column:value`: Search (auto-chunks large files)

---

### `read_file`
Read files from input directory.

```python
read_file(file_path="gene_expression.csv")
```

Supports: CSV, TSV, Parquet, TXT, JSON

**Important**: File path is relative to `INPUT_DIR` configured in `.env`

---

### `find_files`
Intelligently search for files.

```python
find_files(
    pattern="**/Q5/*.csv",
    extension="csv",
    name_contains="exhaustion",
    question_context="T cell exhaustion genes"  # AI-powered relevance ranking
)
```

**Much more efficient than `execute_python` with `os.listdir()`**

Use this FIRST before reading files to discover what's available.

## Project Structure

```
coscientist/
├── src/
│   ├── cli.py                      # Command-line interface
│   │
│   ├── agent/
│   │   ├── agent.py                # Core agent implementation
│   │   ├── meeting.py              # Virtual Lab logic
│   │   ├── openrouter_client.py    # OpenRouter API
│   │   ├── anthropic_client.py     # Anthropic API
│   │   └── team_manager.py         # Team composition
│   │
│   ├── virtuallab_workflow/
│   │   ├── workflow.py             # LangGraph workflows
│   │   ├── state.py                # State definitions
│   │   ├── classifier.py           # Question classification
│   │   ├── nodes.py                # Standard nodes
│   │   ├── nodes_consensus.py      # Consensus nodes
│   │   ├── consensus.py            # Consensus mechanism
│   │   └── visualization.py        # Workflow diagrams
│   │
│   ├── tools/
│   │   └── implementations.py      # Tool implementations
│   │
│   ├── utils/
│   │   └── file_index.py           # File indexing
│   │
│   └── config.py                   # Configuration
│
├── ext-tools/
│   └── paper-qa/                   # Local PaperQA (editable install)
│
├── data/                           # Input data
├── papers/                         # Local PDF library
├── .env                            # Environment config (create this!)
└── requirements.txt
```

## Command-Line Options

```bash
python -m src.cli [OPTIONS]

Core Options:
  --question, -q        Research question
  --interactive, -i     Interactive mode
  --model, -m          Override model (e.g., "anthropic/claude-sonnet-4")
  --verbose, -v        Show tool calls and reasoning
  --output, -o         Save answer to file (auto-generates if omitted)

Mode Selection (choose one):
  [none]               Single agent (default)
  --virtual-lab, -vl   Multi-agent collaboration
  --langgraph          LangGraph workflow
  --combined           LangGraph + Consensus
  --with-critic, -c    Single agent with critic

Virtual Lab Options:
  --rounds, -r         Discussion rounds (default: 2)
  --team-size, -t      Max specialists (default: 3)

Data Paths:
  --data-dir, -d       Override DATABASE_DIR
  --input-dir          Override INPUT_DIR
  --api-key            Override API key from .env
```

## Examples

### Example 1: Drug Repositioning
```bash
python -m src.cli \
  --question "Identify FDA-approved drugs that could target EGFR mutations in lung cancer" \
  --virtual-lab \
  --rounds 2 \
  --team-size 3 \
  --verbose \
  --output results/drug_repositioning.md
```

**What happens**:
1. PI assembles team (computational biologist, pharmacologist, oncologist)
2. Agents query DrugBank, search literature, analyze mutations
3. Python code for statistical analysis
4. Synthesized answer with ranked candidates + citations

---

### Example 2: Experimental Design
```bash
python -m src.cli \
  --question "Design a genome-wide CRISPR screen for cisplatin resistance in ovarian cancer" \
  --combined \
  --rounds 3 \
  --team-size 4
```

**What happens**:
1. Classifier identifies as wet-lab + computational question
2. Multiple models independently design screen protocols
3. Consensus identifies common recommendations
4. Final answer includes agreement scores, alternatives, uncertainties

---

### Example 3: Literature Review
```bash
python -m src.cli \
  --question "What are the latest single-cell RNA-seq batch correction methods?" \
  --langgraph \
  --verbose
```

**What happens**:
1. Classifier routes to "literature" workflow
2. Searches local papers + PubMed
3. LLM synthesizes findings with citations
4. Method comparison table

## Output Files

Answers are automatically saved to timestamped markdown files:

```
answer_20251216_133700.md
```

Contains:
- Research question
- Final answer
- Metadata (mode, timestamp)

Specify custom path:
```bash
python -m src.cli --question "..." --output results/my_answer.md
```

## Common Issues

### LiteLLM Warnings
```
LiteLLM:WARNING: Cannot add callback - would exceed MAX_CALLBACKS limit of 30
```

**This is normal!** PaperQA uses LiteLLM internally. The warnings don't affect functionality.

---

### Model Name Formats

```bash
# Main agent (uses OpenRouter API directly)
OPENROUTER_MODEL=google/gemini-3-pro-preview

# PaperQA (uses LiteLLM, needs prefix)
PAPERQA_LLM=openrouter/google/gemini-3-pro-preview
```

Both use the same model, just different API wrappers.

---

### PaperQA Version

Check which paper-qa is loaded:
```bash
python -c "import paperqa; print(paperqa.__file__)"
```

Should show: `ext-tools/paper-qa/src/paperqa/__init__.py`

If not:
```bash
pip install -e ext-tools/paper-qa
```

---

### API Keys

Both `OPENROUTER_API_KEY` and `OPENROUTER_KEY` must be set:
- `OPENROUTER_API_KEY`: Used by main agents
- `OPENROUTER_KEY`: Used by LiteLLM (in PaperQA)

Set them to the **same value** in `.env`.

## Performance Tips

### Faster (Lower Cost)
- Use single agent mode
- Reduce `--rounds` and `--team-size`
- Use free models: `google/gemini-2.0-flash-exp:free`
- Set `PAPERQA_LLM=openrouter/google/gemini-2.0-flash-exp:free`

### Better Quality (Higher Cost)
- Use `--combined` mode
- Increase `--rounds` (3-4) and `--team-size` (4-5)
- Use premium models: `anthropic/claude-sonnet-4`
- Increase `PAPERQA_MAX_SOURCES=10`

### Cost Optimization
- Local embeddings: `PAPERQA_EMBEDDING=st-multi-qa-MiniLM-L6-cos-v1` (free)
- Use `search_literature` mode `auto` (checks local PDFs first)
- Reduce max_iterations in consensus (edit `src/virtuallab_workflow/consensus.py`)

## Development

### Adding a New Tool

1. **Implement in `src/tools/implementations.py`**:

```python
def my_tool(param1: str, param2: int) -> ToolResult:
    """Tool description."""
    try:
        # Your implementation
        result = do_something(param1, param2)
        return ToolResult(success=True, output=result)
    except Exception as e:
        return ToolResult(success=False, error=str(e))
```

2. **Add to `get_tool_definitions()`** in same file:

```python
{
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "What it does for the LLM",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "What param1 is for"
                },
                "param2": {
                    "type": "integer",
                    "description": "What param2 is for"
                }
            },
            "required": ["param1", "param2"]
        }
    }
}
```

3. **Register in `BioinformaticsAgent.__init__()`** in `src/agent/agent.py`:

```python
self.tools = {
    # ... existing tools
    "my_tool": my_tool,
}
```

### Testing

```bash
# Run tests
python -m pytest tests/

# Test specific mode
python demo_langgraph.py
python test-script/test_consensus.py
```

## FAQ

**Q: Why does PaperQA use LiteLLM?**
A: PaperQA library uses LiteLLM as a unified interface to support multiple LLM providers (OpenAI, Anthropic, OpenRouter, etc.) without needing separate code for each.

**Q: Can I use a different model for consensus?**
A: Yes! Edit `DEFAULT_CONSENSUS_MODELS` in `src/virtuallab_workflow/consensus.py`, or pass `consensus_models` parameter when calling programmatically.

**Q: Where are the databases?**
A: Set `DATABASE_DIR` in `.env` to point to your database directory containing DrugBank, BindingDB, etc.

**Q: Can I add my own PDFs to the library?**
A: Yes! Put PDF files in the directory specified by `PAPER_LIBRARY_DIR` (default: `./papers`). PaperQA will automatically index them.

**Q: How do I suppress LiteLLM warnings?**
A: Add to your code or `.env`:
```python
import logging
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
```

## License

See LICENSE file.

---

**Last Updated**: December 2025
