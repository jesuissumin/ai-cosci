# CoScientist - Complete Index

Welcome to CoScientist, your AI research assistant for the 바이오 AI 연구동료 경진대회 (Bio AI Co-Scientist Competition).

## 📖 Documentation Roadmap

### ⚡ Start Here (Pick Your Path)

**I just cloned the repo** → Read: [`GETTING_STARTED.md`](GETTING_STARTED.md) (5 min)
```bash
pip install -r requirements.txt
cp .env.example .env
# Add API key
python -m src.cli --question "What is aspirin?"
```

**I need a quick reference** → See: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) (2 min)
- Common commands
- Tool reference
- Troubleshooting table

**I want to understand the system** → Read: [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) (15 min)
- Architecture diagram
- Data flow
- Component details
- API integration points

**I need full documentation** → See: [`README.md`](README.md) (30 min)
- Complete feature list
- API reference
- Advanced usage
- All options explained

**I want to see what was built** → Read: [`BUILD_SUMMARY.md`](BUILD_SUMMARY.md) (10 min)
- What's included
- Code statistics
- Next steps
- Performance metrics

**I need to verify everything** → Check: [`VERIFICATION_CHECKLIST.md`](VERIFICATION_CHECKLIST.md) (5 min)
- Build checklist
- Component verification
- Ready to use confirmation

## 🚀 Quick Start (2 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API
cp .env.example .env
# Edit .env with your OpenRouter API key

# 3. Test
python -m src.cli --question "What databases are used in drug discovery?"

# 4. Go interactive
python -m src.cli --interactive
```

## 📁 Project Structure

```
CoScientist/
├── 📚 Documentation
│   ├── INDEX.md                    ← You are here
│   ├── GETTING_STARTED.md          ← Start here for setup
│   ├── QUICK_REFERENCE.md          ← Quick lookup
│   ├── README.md                   ← Full reference
│   ├── PROJECT_OVERVIEW.md         ← Architecture
│   ├── BUILD_SUMMARY.md            ← What's built
│   └── VERIFICATION_CHECKLIST.md   ← Verification
│
├── 💻 Source Code
│   └── src/
│       ├── agent/                  ← Core agent engine
│       │   ├── agent.py            ← Main agent loop
│       │   └── openrouter_client.py ← API client
│       ├── tools/                  ← Tool implementations
│       │   └── implementations.py  ← All 4 tools
│       └── cli.py                  ← Command-line interface
│
├── 📊 Data
│   └── databases/                  ← Your database files go here
│
├── 🧪 Testing
│   ├── notebooks/
│   │   └── test_agent.py           ← Example usage
│   └── tests/                      ← Test suite (ready)
│
└── ⚙️ Configuration
    ├── requirements.txt            ← Python dependencies
    └── .env.example               ← Environment template
```

## 🎯 Documentation by Role

### For Competition Participants
1. **Day 1**: Read `GETTING_STARTED.md` and get it running
2. **Day 2-3**: Prepare databases, test with example questions
3. **Day 7-14**: Optimize and customize as needed
4. **Dec 22**: Use QUICK_REFERENCE for fast lookup

**Key files**: `GETTING_STARTED.md`, `QUICK_REFERENCE.md`, `README.md`

### For Developers/Engineers
1. **Understanding**: Read `PROJECT_OVERVIEW.md`
2. **Implementation**: Review `src/agent/` and `src/tools/`
3. **Extending**: Add tools following `implementations.py` pattern
4. **Deploying**: Check `BUILD_SUMMARY.md` and `VERIFICATION_CHECKLIST.md`

**Key files**: `PROJECT_OVERVIEW.md`, Code in `src/`

### For Team Leads/Managers
1. **Status**: See `BUILD_SUMMARY.md` (what's done)
2. **Timeline**: See competition prep section
3. **Readiness**: See `VERIFICATION_CHECKLIST.md`
4. **Troubleshooting**: See `QUICK_REFERENCE.md`

**Key files**: `BUILD_SUMMARY.md`, `VERIFICATION_CHECKLIST.md`

## 📋 File Descriptions

### Documentation Files (7 files, ~46KB)

| File | Size | Purpose | Read Time |
|------|------|---------|-----------|
| `GETTING_STARTED.md` | 4.9K | Setup guide for new users | 5 min |
| `QUICK_REFERENCE.md` | 5.5K | Command reference & lookup | 2 min |
| `README.md` | 8.0K | Complete API reference | 30 min |
| `PROJECT_OVERVIEW.md` | 11K | System architecture & design | 15 min |
| `BUILD_SUMMARY.md` | 11K | What was built & next steps | 10 min |
| `VERIFICATION_CHECKLIST.md` | 6.6K | Build verification | 5 min |
| `INDEX.md` | 5K | This navigation guide | 5 min |

### Source Code (4 main files, ~955 lines)

| File | Lines | Purpose |
|------|-------|---------|
| `src/agent/agent.py` | 410 | Core agent orchestration |
| `src/tools/implementations.py` | 305 | Tool implementations |
| `src/agent/openrouter_client.py` | 120 | API client |
| `src/cli.py` | 120 | Command-line interface |

### Configuration (3 files)

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |
| `src/__init__.py` etc | Package markers |

## 🛠️ Available Tools

The system includes 4 powerful tools:

### 1. Python Code Execution
```python
# Agent can write and execute Python code
"Calculate the mean expression level from [1.2, 2.3, 1.8]"
```
- Sandboxed execution
- Timeout protection (30s)
- Data analysis & visualization

### 2. PubMed Search
```python
# Real peer-reviewed literature
"Search for papers on CRISPR gene therapy"
```
- No hallucinations (real PMIDs)
- Abstracts and author info
- Citation ready

### 3. Database Querying
```python
# Access your databases
"Query DrugBank for EGFR inhibitors"
```
- Parquet/CSV/TSV support
- Multiple databases
- Smart result formatting

### 4. File Reading
```python
# Load your data
"Read the binding affinity data"
```
- Path-safe file access
- Format detection
- Preview generation

## 🚦 Usage Modes

### Mode 1: Single Question (Fastest)
```bash
python -m src.cli --question "Your question?"
```
Best for: Quick answers, testing, integration

### Mode 2: Interactive Chat (Most Natural)
```bash
python -m src.cli --interactive
```
Best for: Exploration, follow-ups, conversation

### Mode 3: Python Script (Most Flexible)
```python
from src.agent import create_agent
agent = create_agent()
response = agent.run("Your question")
```
Best for: Integration, automation, custom workflows

### Mode 4: Jupyter Notebook (Most Visual)
```python
from src.agent import create_agent
agent = create_agent()
agent.run("Your question", verbose=True)
```
Best for: Analysis, visualization, documentation

## 📊 System Capabilities

### Questions It Handles Well
- Drug repositioning strategies
- Protein-ligand interaction analysis
- Nanopore sequencing interpretation
- Literature synthesis
- Experimental design proposals
- Database queries and analysis

### Response Quality Features
- Multi-step reasoning
- Scientific rigor (facts vs. speculation)
- Real citations (PubMed)
- Python-based analysis
- Feasibility assessment
- Uncertainty acknowledgment

## ⚙️ Configuration

### Essential (.env)
```bash
OPENROUTER_API_KEY=your_key_here
```

### Optional
```bash
OPENROUTER_MODEL=anthropic/claude-sonnet-4-20250514
DATA_DIR=./data
```

## 📈 Performance Profile

| Task Type | Time | Tokens | Cost |
|-----------|------|--------|------|
| Simple Q&A | 3-5s | 500-1K | $0.01 |
| With tools | 10-20s | 1-3K | $0.03 |
| Analysis | 15-30s | 2-5K | $0.05 |

## 🔒 Security

- API key stored securely (.env not versioned)
- File access restricted to data/ directory
- Code execution timeout (30s)
- Network timeouts (120s)
- Safe error messages

## 📞 Getting Help

### Common Issues

**"API key not found"**
→ See QUICK_REFERENCE.md → Debugging

**"File not found"**
→ Place files in data/databases/

**"Slow response"**
→ Try simpler question, check internet

**"Wrong tool called"**
→ Run with --verbose to debug

### Detailed Resources

- Setup questions → `GETTING_STARTED.md`
- Quick answers → `QUICK_REFERENCE.md`
- Technical details → `PROJECT_OVERVIEW.md`
- Full reference → `README.md`
- What's available → `BUILD_SUMMARY.md`

## 🎓 Learning Path

### Complete Beginner (30 minutes)
1. Read `GETTING_STARTED.md` (5 min)
2. Run setup commands (3 min)
3. Ask your first question (2 min)
4. Read `QUICK_REFERENCE.md` (2 min)
5. Try interactive mode (5 min)
6. Explore tools (10 min)

### Intermediate (2 hours)
1. Read `README.md` (30 min)
2. Review code structure (30 min)
3. Customize system prompt (15 min)
4. Test with real questions (45 min)

### Advanced (4+ hours)
1. Study `PROJECT_OVERVIEW.md` (30 min)
2. Deep dive into code (1 hour)
3. Add custom tools (1 hour)
4. Optimize and test (1+ hours)

## 🎯 Pre-Competition Checklist

- [ ] Repository cloned and installed
- [ ] API key configured in .env
- [ ] Ran test question successfully
- [ ] Database files prepared
- [ ] Tested with real competition questions
- [ ] Customized system prompt (if needed)
- [ ] Verified response times
- [ ] Checked API budget status
- [ ] Created test harness
- [ ] Ready for Dec 22!

## 📚 Quick Reference Table

| Need | File | Time |
|------|------|------|
| Get it working | GETTING_STARTED.md | 5 min |
| Run a command | QUICK_REFERENCE.md | 1 min |
| Understand design | PROJECT_OVERVIEW.md | 15 min |
| Full API | README.md | 30 min |
| What's built | BUILD_SUMMARY.md | 10 min |
| Verify it works | VERIFICATION_CHECKLIST.md | 5 min |
| Understand this | INDEX.md | 5 min |

## 🚀 Next Step

Pick where you are:

**I'm brand new** → [`GETTING_STARTED.md`](GETTING_STARTED.md)

**I have 5 minutes** → [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)

**I want to understand everything** → [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md)

**I need complete docs** → [`README.md`](README.md)

**I want to see what's here** → [`BUILD_SUMMARY.md`](BUILD_SUMMARY.md)

**I need to verify** → [`VERIFICATION_CHECKLIST.md`](VERIFICATION_CHECKLIST.md)

---

**Ready to go?**

```bash
python -m src.cli --question "Your first question"
```

Good luck with the competition! 🎉
