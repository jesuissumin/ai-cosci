# Getting Started with CoScientist

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure OpenRouter API
1. Get your API key from [OpenRouter](https://openrouter.io)
2. Create a `.env` file:
```bash
cp .env.example .env
```
3. Edit `.env` and add your key:
```
OPENROUTER_API_KEY=your_key_here
```

### Step 3: Test the Installation
```bash
# Single question test
python -m src.cli --question "What are the main databases used in drug discovery?"

# Interactive mode
python -m src.cli --interactive
```

## First Steps

### Option A: Command Line (Simplest)
```bash
python -m src.cli --question "Your research question here?"
```

### Option B: Python Script
Create `test_my_question.py`:
```python
from src.agent import create_agent
from dotenv import load_dotenv

load_dotenv()
agent = create_agent()
response = agent.run("Your question here")
print(response)
```

Run it:
```bash
python test_my_question.py
```

### Option C: Interactive Notebook
```bash
jupyter notebook
```

Then create a new cell:
```python
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
from src.agent import create_agent

load_dotenv()
agent = create_agent()
response = agent.run("Your question here", verbose=True)
print(response)
```

## Using Tools

### Python Code Execution
The agent can write and execute Python code:
```
Question: "Write Python code to calculate the mean and standard deviation of gene expression values [1.2, 2.3, 1.8, 3.5, 2.1]"
```

### PubMed Search
The agent can search for scientific literature:
```
Question: "Search for recent papers on CRISPR gene therapy and summarize key findings"
```

### Database Queries
Query your competition databases (if files are in `data/databases/`):
```
Question: "Query DrugBank to find all drugs targeting EGFR"
```

### File Reading
Read data files:
```
Question: "Read the DrugBank data and analyze the distribution of drug types"
```

## Verbose Mode for Debugging

To see what the agent is doing:
```bash
python -m src.cli --question "..." --verbose
```

This shows:
- Each iteration of the agent loop
- Tools being called and their parameters
- Tool results and outputs
- Final response

## Example Questions for Testing

Try these to verify everything works:

1. **Simple Knowledge Question**
   ```
   What are the main criteria for evaluating drug candidates in early-stage discovery?
   ```

2. **Tool Usage: Python**
   ```
   Write Python code to calculate the geometric mean of these binding affinities (Kd values): 100nM, 50nM, 200nM, 75nM
   ```

3. **Tool Usage: Literature**
   ```
   Search PubMed for papers on protein structure prediction and summarize the top findings
   ```

## Next Steps

### 1. Prepare Your Data
Place your competition databases in `data/databases/`:
- `drugbank.parquet` or `drugbank.csv`
- `bindingdb.parquet` or `bindingdb.csv`
- `pharos.parquet` or `pharos.csv`
- `string.parquet` or `string.csv`
- `gwas.parquet` or `gwas.csv`

### 2. Customize the System Prompt (Optional)
Edit the `get_system_prompt()` method in `src/agent/agent.py` to add domain-specific instructions.

### 3. Add Custom Tools (Optional)
Add new tool functions to `src/tools/implementations.py` for domain-specific functionality.

### 4. Test with Competition Questions
Once you have your setup ready, test with realistic competition questions to ensure everything works.

## Common Issues

### "OPENROUTER_API_KEY not found"
- Ensure you created `.env` file
- Check that you added your API key correctly
- Reload your terminal or notebook kernel

### "File not found: databases/..."
- Create `data/databases/` directory if it doesn't exist
- Place your parquet/CSV files there
- Use correct filenames matching the tool code

### Agent is slow or timing out
- Check your internet connection
- Verify OpenRouter API is working
- Try a simpler question first
- Increase `max_iterations` if needed

### Tool execution errors
- Run with `--verbose` flag to see detailed errors
- Check that the tool's parameters match what it expects
- Verify file paths are correct and accessible

## Performance Tips

1. **Start simple**: Test basic questions before complex multi-step reasoning
2. **Use verbose mode**: Understand what tools are being called
3. **Monitor API usage**: Check OpenRouter dashboard to see token usage
4. **Cache results**: For repeated queries, consider caching database results

## Next: Competition Preparation

Once you're comfortable with the basics:

1. Read through `README.md` for advanced features
2. Test with realistic competition question types
3. Prepare your database files
4. Create any custom tools needed for your domain
5. Optimize system prompt based on your feedback
6. Set up a testing harness for rapid iteration

## Questions?

Check the README.md for:
- Detailed architecture
- Tool specifications
- Advanced usage patterns
- Troubleshooting guide
