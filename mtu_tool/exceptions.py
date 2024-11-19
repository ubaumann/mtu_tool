from nornir.core.task import AggregatedResult


class MtuTool(Exception): ...


class NoHostFoundException(MtuTool): ...


class PathProcedureError(MtuTool):
    def __init__(
        self,
        error_str: str,
        aggregated_result: AggregatedResult,
    ) -> None:
        self.error_str = error_str
        self.aggregated_result = aggregated_result
        super().__init__(self.error_str)
