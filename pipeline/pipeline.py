from typing import List
from pipeline.algorithms.pipeline_algorithm_interface import PipelineAlgorithmInterface
from pipeline.global_algoritm_params import GlobalAlgoritmParams

class Pipeline:
    def __init__(
        self,
        algorithms: List[PipelineAlgorithmInterface],
        global_algorithm_params: GlobalAlgoritmParams,
        disjunctive: bool = False
    ):
        self.algorithms = algorithms
        self.global_algorithm_params = global_algorithm_params
        self.disjunctive = disjunctive
    
    def execute(self):
        for algorithm in self.algorithms:
            try:
                if isinstance(algorithm, SubPipeline):
                    sub_pipeline = Pipeline(algorithm.algorithms, self.global_algorithm_params, algorithm.disjunctive)
                    sub_pipeline.execute()
                else:
                    print("Process: ", algorithm)
                    algorithm.execute(self.global_algorithm_params)
                    
                if self.disjunctive:
                    return
            
            except Exception as exception:
                if not self.disjunctive:
                    raise exception
        
        if self.disjunctive:
            raise Exception('No complete any process')

class SubPipeline:
    def __init__(
        self,
        algorithms: List[PipelineAlgorithmInterface],
        disjunctive: bool = False
    ):
        self.algorithms = algorithms
        self.disjunctive = disjunctive

        