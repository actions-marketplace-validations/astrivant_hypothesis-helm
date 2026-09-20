"""
Public operation descriptors, dependency scheduling, and process ownership contracts.
"""

from pipeline.feedback import FeedbackGraph as FeedbackGraph
from pipeline.graph import Graph as Graph
from pipeline.operations import Operation as Operation
from pipeline.operations import OperationQueue as OperationQueue
from pipeline.operations import ProcessOwner as ProcessOwner
from pipeline.policy import FIFO as FIFO
from pipeline.policy import BreadthFirst as BreadthFirst
from pipeline.policy import DepthFirst as DepthFirst
from pipeline.policy import ShortestRemaining as ShortestRemaining
from pipeline.scheduler import Scheduler as Scheduler
from pipeline.shutdown import Finalizer as Finalizer
from pipeline.shutdown import ShutdownContract as ShutdownContract
from pipeline.shutdown import ShutdownState as ShutdownState
from pipeline.workloads import Control as Control
from pipeline.workloads import Estimate as Estimate
from pipeline.workloads import Outcome as Outcome
from pipeline.workloads import Statistics as Statistics
from pipeline.workloads import Work as Work
from pipeline.workloads import Workload as Workload

# Re-export project contracts here; executors and threading primitives stay in their defining libraries.
__all__ = (
    "BreadthFirst",
    "Control",
    "DepthFirst",
    "Estimate",
    "FIFO",
    "FeedbackGraph",
    "Finalizer",
    "Graph",
    "Operation",
    "OperationQueue",
    "Outcome",
    "ProcessOwner",
    "Scheduler",
    "ShortestRemaining",
    "ShutdownContract",
    "ShutdownState",
    "Statistics",
    "Work",
    "Workload",
)
