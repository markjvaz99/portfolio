from llama_index.core.postprocessor.types import BaseNodePostprocessor
from pydantic import Field

class ScoreThresholdPostprocessor(BaseNodePostprocessor):
    threshold: float = Field(default=0.0)

    def _postprocess_nodes(self, nodes, query_bundle=None):
        filtered = [
            n for n in nodes
            if n.score is not None and n.score >= self.threshold
        ]

        return filtered if filtered else nodes[:1]
