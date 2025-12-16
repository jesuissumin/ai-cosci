"""
Configuration module for Virtual Lab data sources.

Manages paths and settings for:
- Drug databases (DrugBank, BindingDB, etc.)
- User input directories
- Local paper library for PaperQA
- Internet search settings
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class DataConfig:
    """Configuration for all data sources used by the Virtual Lab."""

    # Database directory (DrugBank, BindingDB, Pharos, GWAS, StringDB)
    database_dir: str

    # Input directory for question-specific data files
    input_dir: str

    # Local paper library directory for PaperQA
    paper_library_dir: str

    # PubMed search settings
    pubmed_email: Optional[str] = None
    pubmed_api_key: Optional[str] = None

    # PaperQA settings
    paperqa_llm: str = "openrouter/google/gemini-3-pro-preview"  # Model for PaperQA (via OpenRouter) - PAID model
    paperqa_embedding: str = "st-multi-qa-MiniLM-L6-cos-v1"  # Local embedding (free, no API calls)
    paperqa_max_sources: int = 5  # Maximum contexts to retrieve

    def __post_init__(self):
        """Validate that directories exist or can be created."""
        # Convert to Path objects
        self.database_dir = str(Path(self.database_dir).resolve())
        self.input_dir = str(Path(self.input_dir).resolve())
        self.paper_library_dir = str(Path(self.paper_library_dir).resolve())

        # Verify database directory exists
        if not Path(self.database_dir).exists():
            raise ValueError(f"Database directory does not exist: {self.database_dir}")

        # Create input directory if it doesn't exist
        Path(self.input_dir).mkdir(parents=True, exist_ok=True)

        # Create paper library directory if it doesn't exist
        Path(self.paper_library_dir).mkdir(parents=True, exist_ok=True)


def get_default_config() -> DataConfig:
    """
    Get default configuration from environment variables or fallback values.

    Environment variables (can be set in .env file):
    - DATABASE_DIR: Path to database directory (DrugBank, etc.)
    - INPUT_DIR: Path to input data directory
    - PAPER_LIBRARY_DIR: Path to local PDF library
    - PUBMED_EMAIL: Email for PubMed API
    - PUBMED_API_KEY: API key for PubMed (optional, increases rate limit)
    - PAPERQA_LLM: LLM model for PaperQA
    - PAPERQA_EMBEDDING: Embedding model for PaperQA

    Returns:
        DataConfig object with configured paths
    """
    return DataConfig(
        database_dir=os.getenv(
            "DATABASE_DIR",
            "/home.galaxy4/sumin/project/aisci/Competition_Data"
        ),
        input_dir=os.getenv("INPUT_DIR", "./data"),
        paper_library_dir=os.getenv("PAPER_LIBRARY_DIR", "./papers"),
        pubmed_email=os.getenv("PUBMED_EMAIL"),
        pubmed_api_key=os.getenv("PUBMED_API_KEY"),
        paperqa_llm=os.getenv("PAPERQA_LLM", "openrouter/google/gemini-3-pro-preview"),
        paperqa_embedding=os.getenv("PAPERQA_EMBEDDING", "st-multi-qa-MiniLM-L6-cos-v1"),
        paperqa_max_sources=int(os.getenv("PAPERQA_MAX_SOURCES", "5"))
    )


def create_custom_config(
    database_dir: Optional[str] = None,
    input_dir: Optional[str] = None,
    paper_library_dir: Optional[str] = None,
    **kwargs
) -> DataConfig:
    """
    Create a custom configuration, overriding default values.

    Args:
        database_dir: Override database directory
        input_dir: Override input directory
        paper_library_dir: Override paper library directory
        **kwargs: Additional configuration parameters

    Returns:
        DataConfig object with custom configuration
    """
    default = get_default_config()

    return DataConfig(
        database_dir=database_dir or default.database_dir,
        input_dir=input_dir or default.input_dir,
        paper_library_dir=paper_library_dir or default.paper_library_dir,
        pubmed_email=kwargs.get("pubmed_email", default.pubmed_email),
        pubmed_api_key=kwargs.get("pubmed_api_key", default.pubmed_api_key),
        paperqa_llm=kwargs.get("paperqa_llm", default.paperqa_llm),
        paperqa_embedding=kwargs.get("paperqa_embedding", default.paperqa_embedding),
        paperqa_max_sources=kwargs.get("paperqa_max_sources", default.paperqa_max_sources)
    )


# Global configuration instance (can be overridden)
_global_config: Optional[DataConfig] = None


def set_global_config(config: DataConfig):
    """Set the global configuration instance."""
    global _global_config
    _global_config = config


def get_global_config() -> DataConfig:
    """Get the global configuration instance, creating default if not set."""
    global _global_config
    if _global_config is None:
        _global_config = get_default_config()
    return _global_config
