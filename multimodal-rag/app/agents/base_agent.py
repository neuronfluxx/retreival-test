"""Base agent for agentic document extraction"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from app.utils.logger import app_logger


class AgentStatus(str, Enum):
    """Agent execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentResult:
    """Result from agent execution"""
    agent_name: str
    status: AgentStatus
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str] = None
    confidence: float = 1.0


class BaseAgent(ABC):
    """Base class for document processing agents"""

    def __init__(self, name: str):
        """
        Initialize agent

        Args:
            name: Agent name
        """
        self.name = name
        self.status = AgentStatus.PENDING

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute agent logic

        Args:
            input_data: Input data for processing

        Returns:
            AgentResult with processed data
        """
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data

        Args:
            input_data: Input data to validate

        Returns:
            True if valid, False otherwise
        """
        return True

    def log_execution(self, message: str):
        """Log agent execution"""
        app_logger.info(f"[{self.name}] {message}")

    def log_error(self, error: str):
        """Log agent error"""
        app_logger.error(f"[{self.name}] {error}")
