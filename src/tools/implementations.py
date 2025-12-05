"""Tool implementations for the bioinformatics agent."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Optional
import requests
import sys
from io import StringIO
import signal
from contextlib import contextmanager


class ToolResult:
    """Result wrapper for tool execution."""

    def __init__(self, success: bool, output: Any, error: Optional[str] = None):
        self.success = success
        self.output = output
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
        }


class PersistentPythonExecutor:
    """Maintains a persistent Python environment across execute_python calls.

    This allows variables, imports, and state to persist between calls,
    enabling multi-step data analysis without reloading data.
    """

    def __init__(self):
        """Initialize the persistent Python environment."""
        self.globals_dict = {
            '__builtins__': __builtins__,
        }
        self.locals_dict = {}

    def execute(self, code: str, timeout: int = 30) -> tuple[bool, Optional[str], Optional[str]]:
        """Execute code in the persistent environment.

        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds

        Returns:
            Tuple of (success, output, error)
        """
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        try:
            # Execute code in persistent namespace
            exec(code, self.globals_dict, self.locals_dict)

            # Get output
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()

            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            if error:
                return False, None, error

            return True, output.strip() if output else "Code executed successfully (no output)", None

        except Exception as e:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            return False, None, f"Execution error: {type(e).__name__}: {str(e)}"

    def reset(self):
        """Reset the persistent environment (clears all variables)."""
        self.globals_dict = {
            '__builtins__': __builtins__,
        }
        self.locals_dict = {}


# Global persistent executor instance
_persistent_executor = PersistentPythonExecutor()


def execute_python(code: str, timeout: int = 30, reset: bool = False) -> ToolResult:
    """Execute Python code in a persistent environment.

    Variables, imports, and state persist across calls, allowing multi-step
    analyses without reloading data.

    Args:
        code: Python code to execute
        timeout: Execution timeout in seconds (not strictly enforced in persistent mode)
        reset: If True, reset the persistent environment before execution

    Returns:
        ToolResult with output or error
    """
    global _persistent_executor

    if reset:
        _persistent_executor.reset()

    try:
        success, output, error = _persistent_executor.execute(code, timeout)

        if not success:
            return ToolResult(False, None, error)

        return ToolResult(True, output)

    except Exception as e:
        return ToolResult(False, None, f"Error executing code: {str(e)}")


def search_pubmed(query: str, max_results: int = 10, retmax: int = 100) -> ToolResult:
    """Search PubMed for articles.

    Args:
        query: Search query string
        max_results: Maximum results to return
        retmax: Maximum results to fetch from NCBI

    Returns:
        ToolResult with list of articles
    """
    try:
        # NCBI E-utilities endpoints
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

        # Search for PMIDs
        search_params = {
            "db": "pubmed",
            "term": query,
            "rettype": "json",
            "retmax": retmax,
        }

        search_response = requests.get(search_url, params=search_params, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()

        pmids = search_data.get("esearchresult", {}).get("idlist", [])[:max_results]

        if not pmids:
            return ToolResult(True, [])

        # Fetch article details
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "rettype": "abstract",
            "retmode": "json",
        }

        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=10)
        fetch_response.raise_for_status()
        fetch_data = fetch_response.json()

        articles = []
        for article in fetch_data.get("result", {}).get("uids", []):
            if article != "uids":
                doc = fetch_data["result"][article]
                articles.append({
                    "pmid": article,
                    "title": doc.get("title", "N/A"),
                    "abstract": doc.get("abstract", "N/A"),
                    "authors": doc.get("authors", [])[:3],  # First 3 authors
                })

        return ToolResult(True, articles)

    except Exception as e:
        return ToolResult(False, None, f"PubMed search error: {str(e)}")


def query_database(db_name: str, query: str, limit: int = 10, data_dir: str = "/home.galaxy4/sumin/project/aisci/Competition_Data") -> ToolResult:
    """Query a local database file.

    Args:
        db_name: Database name (e.g., 'drugbank', 'bindingdb', 'pharos', 'string', 'gwas')
        query: Query string - can be:
               - Column name to search (e.g., 'Target Name:EGFR')
               - 'info' to get database info (shape, columns, sample)
               - 'all' to get first N rows
        limit: Maximum rows to return (default: 100)
        data_dir: Path to database files

    Returns:
        ToolResult with query results
    """
    try:
        import pandas as pd

        db_name_lower = db_name.lower()
        data_path = Path(data_dir)

        # Handle different databases based on their actual file structure
        if db_name_lower == "bindingdb":
            file_path = data_path / "Drug" / "BindingDB" / "BindingDB_All.tsv"
            if not file_path.exists():
                return ToolResult(False, None, f"BindingDB file not found at {file_path}")

            # For large files, read with chunksize or nrows
            if query.lower() == "info":
                df_sample = pd.read_csv(file_path, sep="\t", nrows=5)
                return ToolResult(True, {
                    "database": "BindingDB",
                    "file": str(file_path),
                    "columns": df_sample.columns.tolist(),
                    "sample": df_sample.to_dict('records')
                })
            elif ":" in query:
                # Column-based search: "Target Name:EGFR"
                col, value = query.split(":", 1)
                df = pd.read_csv(file_path, sep="\t", nrows=10000)  # Read subset for performance
                filtered = df[df[col].astype(str).str.contains(value, case=False, na=False)].head(limit)
                return ToolResult(True, {
                    "count": len(filtered),
                    "results": filtered.to_dict('records')
                })
            else:
                df = pd.read_csv(file_path, sep="\t", nrows=limit)
                return ToolResult(True, df.to_dict('records'))

        elif db_name_lower == "drugbank":
            drugbank_path = data_path / "Drug" / "DrugBank"
            if not drugbank_path.exists():
                return ToolResult(False, None, f"DrugBank directory not found at {drugbank_path}")

            # List available files
            if query.lower() == "info":
                files = [f.name for f in drugbank_path.glob("*.parquet")]
                return ToolResult(True, {
                    "database": "DrugBank",
                    "available_files": files,
                    "message": "Use query like 'file:interactions' to query specific file"
                })
            elif query.lower().startswith("file:"):
                # Query specific file: "file:interactions"
                file_name = query.split(":", 1)[1].strip()
                file_path = drugbank_path / f"{file_name}.parquet"
                if not file_path.exists():
                    return ToolResult(False, None, f"File {file_name}.parquet not found")
                df = pd.read_parquet(file_path)
                return ToolResult(True, {
                    "file": file_name,
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "sample": df.head(limit).to_dict('records')
                })
            else:
                # Default to interactions file
                file_path = drugbank_path / "interactions.parquet"
                df = pd.read_parquet(file_path)
                return ToolResult(True, {
                    "file": "interactions",
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "sample": df.head(limit).to_dict('records')
                })

        elif db_name_lower == "pharos":
            pharos_path = data_path / "Drug" / "Pharos"
            if not pharos_path.exists():
                return ToolResult(False, None, f"Pharos directory not found at {pharos_path}")

            if query.lower() == "info":
                files = [f.name for f in pharos_path.glob("*.csv")]
                return ToolResult(True, {
                    "database": "Pharos",
                    "available_files": files,
                    "message": "Use query like 'file:pharos_drugs' to query specific file"
                })
            elif query.lower().startswith("file:"):
                file_name = query.split(":", 1)[1].strip()
                file_path = pharos_path / f"{file_name}.csv"
                if not file_path.exists():
                    return ToolResult(False, None, f"File {file_name}.csv not found")
                df = pd.read_csv(file_path, nrows=limit)
                return ToolResult(True, {
                    "file": file_name,
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "sample": df.to_dict('records')
                })
            else:
                # Default to drugs file
                file_path = pharos_path / "pharos_drugs.csv"
                df = pd.read_csv(file_path, nrows=limit)
                return ToolResult(True, {
                    "file": "pharos_drugs",
                    "columns": df.columns.tolist(),
                    "sample": df.to_dict('records')
                })

        elif db_name_lower == "gwas":
            file_path = data_path / "GWAS" / "gwas_catalog_association.tsv"
            if not file_path.exists():
                return ToolResult(False, None, f"GWAS file not found at {file_path}")

            if query.lower() == "info":
                df_sample = pd.read_csv(file_path, sep="\t", nrows=5)
                return ToolResult(True, {
                    "database": "GWAS",
                    "file": str(file_path),
                    "columns": df_sample.columns.tolist(),
                    "sample": df_sample.to_dict('records')
                })
            elif ":" in query:
                # Column-based search
                col, value = query.split(":", 1)
                df = pd.read_csv(file_path, sep="\t", nrows=50000)  # Read subset
                filtered = df[df[col].astype(str).str.contains(value, case=False, na=False)].head(limit)
                return ToolResult(True, {
                    "count": len(filtered),
                    "results": filtered.to_dict('records')
                })
            else:
                df = pd.read_csv(file_path, sep="\t", nrows=limit)
                return ToolResult(True, df.to_dict('records'))

        elif db_name_lower == "string" or db_name_lower == "stringdb":
            string_path = data_path / "PPI" / "StringDB"
            if not string_path.exists():
                return ToolResult(False, None, f"STRING directory not found at {string_path}")

            if query.lower() == "info":
                files = [f.name for f in string_path.glob("*.txt")]
                return ToolResult(True, {
                    "database": "STRING",
                    "available_files": files,
                    "message": "Use query like 'file:sapiens.9606.protein.info.v12.0' to query specific file"
                })
            elif query.lower().startswith("file:"):
                file_name = query.split(":", 1)[1].strip()
                file_path = string_path / f"{file_name}.txt"
                if not file_path.exists():
                    return ToolResult(False, None, f"File {file_name}.txt not found")
                # STRING files use space delimiter for interactions, tab for others
                sep = " " if "links" in file_name else "\t"
                df = pd.read_csv(file_path, sep=sep, nrows=limit)
                return ToolResult(True, {
                    "file": file_name,
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "sample": df.to_dict('records')
                })
            else:
                # Default to protein info
                file_path = string_path / "sapiens.9606.protein.info.v12.0.txt"
                df = pd.read_csv(file_path, sep="\t", nrows=limit)
                return ToolResult(True, {
                    "file": "protein.info",
                    "columns": df.columns.tolist(),
                    "sample": df.to_dict('records')
                })
        else:
            return ToolResult(False, None, f"Unknown database: {db_name}. Available: bindingdb, drugbank, pharos, gwas, string")

    except Exception as e:
        return ToolResult(False, None, f"Database query error: {str(e)}")


def read_file(file_path: str) -> ToolResult:
    """Read a file from the data directory.

    Args:
        file_path: Path to file (relative to data directory)

    Returns:
        ToolResult with file contents
    """
    try:
        data_dir = Path("./data")
        target_path = (data_dir / file_path).resolve()

        # Security check: ensure we're reading within data directory
        if not str(target_path).startswith(str(data_dir.resolve())):
            return ToolResult(False, None, "Access denied: path outside data directory")

        if not target_path.exists():
            return ToolResult(False, None, f"File not found: {file_path}")

        # Handle different file types
        if target_path.suffix == ".parquet":
            import pandas as pd
            df = pd.read_parquet(target_path)
            return ToolResult(True, {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "head": df.head().to_dict('records'),
            })

        elif target_path.suffix in [".csv", ".tsv"]:
            import pandas as pd
            sep = "\t" if target_path.suffix == ".tsv" else ","
            df = pd.read_csv(target_path, sep=sep)
            return ToolResult(True, {
                "shape": df.shape,
                "columns": df.columns.tolist(),
                "head": df.head().to_dict('records'),
            })

        else:
            # Text file
            with open(target_path, "r") as f:
                content = f.read()
            return ToolResult(True, content)

    except Exception as e:
        return ToolResult(False, None, f"File read error: {str(e)}")


def get_tool_definitions() -> list[dict[str, Any]]:
    """Get tool definitions for OpenRouter API.

    Returns:
        List of tool definition dicts
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "execute_python",
                "description": "Execute Python code to analyze data, perform calculations, or create visualizations. Use for bioinformatics analysis.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to execute. Assume pandas, numpy, biopython are available.",
                        }
                    },
                    "required": ["code"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_pubmed",
                "description": "Search PubMed for scientific articles related to a query. Returns titles, abstracts, and author information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "PubMed search query (e.g., 'SARS-CoV-2 vaccine', 'alzheimer's disease protein')",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10,
                        },
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "query_database",
                "description": "Query one of the competition databases (DrugBank, BindingDB, Pharos, STRING, GWAS). Use 'info' query to see database structure and available files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "db_name": {
                            "type": "string",
                            "description": "Database name: 'drugbank', 'bindingdb', 'pharos', 'string', or 'gwas'",
                        },
                        "query": {
                            "type": "string",
                            "description": "Query specification: 'info' for database info, 'file:filename' for specific file, 'Column:value' for search, or 'all' for sample rows",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of rows to return (default: 10, max: 50 recommended)",
                            "default": 10,
                        },
                    },
                    "required": ["db_name", "query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from the data directory. Supports parquet, CSV, TSV, and text files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to file relative to data directory",
                        }
                    },
                    "required": ["file_path"],
                },
            },
        },
    ]
