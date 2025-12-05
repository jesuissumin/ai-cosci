# CoScientist Project Overview

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │  CLI Interface   │  │ Jupyter Notebook │  │  Python    │ │
│  │  (src/cli.py)    │  │ Script Interface │  │  API       │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬───┘ │
└───────────┼──────────────────────┼──────────────────────┼────┘
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   BioinformaticsAgent       │
                    │   (src/agent/agent.py)      │
                    │                            │
                    │  • Conversation history     │
                    │  • Agent loop (max 10 iter) │
                    │  • Tool orchestration       │
                    └──────────────┬──────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
    ┌─────────────┐          ┌──────────────┐        ┌────────────┐
    │  OpenRouter │          │    Tools     │        │  System    │
    │  API Client │          │ Dispatcher   │        │  Prompt    │
    │             │          │              │        │            │
    │ • Auth      │          │ • execute_   │        │ • Reasoning│
    │ • Messages  │          │   python     │        │ • Rigor    │
    │ • Tool calls│          │ • search_    │        │ • Citations│
    │             │          │   pubmed     │        │ • Feasibility
    └──────┬──────┘          │ • query_     │        └────────────┘
           │                 │   database   │
           │                 │ • read_file  │
           │                 └──────┬───────┘
           │                        │
           ▼                        ▼
    ┌─────────────────────────────────────────┐
    │        Claude Sonnet 4 (via OpenRouter) │
    │                                         │
    │  Advanced Reasoning for Complex         │
    │  Biomedical Questions                   │
    └─────────────────────────────────────────┘
```

## Data Flow

### Single Question Flow
```
User Question
    ↓
System Prompt + History + Tools Definitions
    ↓
OpenRouter API → Claude Sonnet 4
    ↓
Response with potential tool calls
    ↓
Tool Calls? → YES → Execute Tools → Add Results to History
    ↓         ↓
   NO       Loop (max 10 times)
    ↓
Final Response to User
```

### Tool Execution Details
```
Tool Call (JSON)
    ↓
Tool Dispatcher in Agent
    ↓
    ├─→ execute_python → subprocess.run() → Result
    ├─→ search_pubmed → NCBI E-utilities API → Articles
    ├─→ query_database → pandas read_parquet → Data
    └─→ read_file → File I/O → Content
    ↓
Result Added to Conversation
    ↓
Loop continues (agent can refine or use results)
```

## Key Components

### 1. OpenRouter Client (`src/agent/openrouter_client.py`)
- Handles authentication and API communication
- Manages tool definitions and tool calling format
- Extracts responses and tool calls from API

**Key Methods:**
- `create_message()`: Send request with tools
- `extract_tool_calls()`: Parse tool calls from response
- `get_response_text()`: Extract text from response

### 2. BioinformaticsAgent (`src/agent/agent.py`)
- Main orchestration logic
- Conversation history management
- Tool execution and error handling
- System prompt with scientific reasoning guidelines

**Key Methods:**
- `run()`: Main agent loop
- `call_tool()`: Execute individual tools
- `process_response()`: Parse API responses
- `add_message()`: Manage conversation

### 3. Tool Implementations (`src/tools/implementations.py`)
- `execute_python()`: Run Python for analysis
- `search_pubmed()`: Query NCBI PubMed
- `query_database()`: Access competition databases
- `read_file()`: File I/O for data files

### 4. CLI Interface (`src/cli.py`)
- Command-line argument parsing
- Single question mode
- Interactive conversation mode
- Verbose debugging output

## File Organization

```
coscientist/
├── src/                          # Main source code
│   ├── agent/
│   │   ├── agent.py              # Core agent loop
│   │   ├── openrouter_client.py   # API client
│   │   └── __init__.py
│   ├── tools/
│   │   ├── implementations.py     # Tool functions
│   │   └── __init__.py
│   ├── cli.py                     # Command-line interface
│   ├── config/                    # Configuration (if needed)
│   ├── utils/                     # Utilities (if needed)
│   └── __init__.py
│
├── data/
│   └── databases/                 # Competition data files
│       ├── drugbank.parquet
│       ├── bindingdb.parquet
│       ├── pharos.parquet
│       ├── string.parquet
│       └── gwas.parquet
│
├── notebooks/                     # Jupyter examples
│   └── test_agent.py
│
├── tests/                         # Test suite
│   └── (test files here)
│
├── requirements.txt               # Dependencies
├── .env.example                   # Env template
├── README.md                      # Full documentation
├── GETTING_STARTED.md             # Setup guide
└── PROJECT_OVERVIEW.md            # This file
```

## System Prompt Structure

```
Role Definition: "CoScientist - Expert AI Research Assistant"
    ↓
Core Capabilities (what it can do)
    ↓
Response Guidelines
    ├─ Scientific Rigor
    ├─ Multi-step Problem Solving
    ├─ Data Exploration
    ├─ Literature Integration
    └─ Practical Feasibility
    ↓
Communication Style
    └─ Precision, Terminology, Structure, Clarity, Uncertainty
```

## Tool Calling Workflow

```
1. Agent has conversation history + tools defined
2. Calls OpenRouter API with tool definitions
3. API returns choice:
   a) Text response only → return to user
   b) Text + tool calls → parse and execute
   c) Tool calls only → execute silently
4. For each tool call:
   - Parse tool name and arguments
   - Execute tool function
   - Format result as JSON
   - Add to conversation history
5. Loop continues (agent decides if more tools needed)
6. Max 10 iterations to prevent infinite loops
```

## API Integration Points

### OpenRouter API
- **Endpoint**: `https://openrouter.io/api/v1/chat/completions`
- **Model**: `anthropic/claude-sonnet-4-20250514`
- **Format**: OpenAI-compatible chat format
- **Features**: Tool calling, streaming optional
- **Cost**: Tracked via OpenRouter account

### NCBI E-utilities (PubMed)
- **Endpoint**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- **Services**: esearch (find), efetch (details)
- **Rate limit**: 3 requests/second (no API key needed)
- **Format**: JSON response

## Competition-Specific Notes

### Example Use Cases
1. **Drug Repositioning**: Use gene signatures + databases → propose candidates
2. **Protein Design**: Analyze structures + sequences → design pipelines
3. **Nanopore Analysis**: Execute Python → interpret sequencing data
4. **Literature Review**: Search PubMed → synthesize findings
5. **Experimental Design**: Multi-step reasoning → validation strategies

### Token Budget
- OpenRouter budget: 100만원 (sufficient for 100+ queries)
- Sonnet 4: ~$0.003 per 1K input tokens, $0.015 per 1K output tokens
- Average query: ~2-5K tokens total

### Competition Day
- Parallel vs sequential agent runs
- Error handling and fallbacks
- Citation quality (real PubMed results)
- Response timing (max 30s per query)

## Performance Metrics

### Typical Response Times
- Simple question: 3-5 seconds
- Multi-tool question: 10-20 seconds
- Database query + analysis: 15-30 seconds

### Token Usage
- Average question: 500-1000 input tokens
- Average response: 500-2000 output tokens
- Tool calls add 100-500 tokens per call

## Error Handling

### Graceful Degradation
- Tool failures don't crash agent
- Results wrapped in success/error format
- Agent can use errors to inform next steps
- Fallback to text-only response

### Debugging
- Verbose mode shows all steps
- Conversation history preserved
- Tool outputs logged in history
- Can inspect `agent.conversation_history`

## Next Iterations

### Short Term
- [ ] Add more sophisticated database query language
- [ ] Implement result caching for repeated queries
- [ ] Add streaming response support
- [ ] Create test suite with example questions

### Medium Term
- [ ] Custom tool for specific bioinformatics libraries
- [ ] Knowledge base integration
- [ ] Fine-tuning system prompt based on feedback
- [ ] Performance monitoring and analytics

### Long Term
- [ ] Multi-agent collaboration
- [ ] Persistent memory between sessions
- [ ] Specialized subagents for different domains
- [ ] Integration with research platforms
