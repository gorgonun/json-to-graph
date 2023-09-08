# from main.python import operation
# from main.python.processing_api import ProcessingAPI


# class OperationController():
#     def __init__(self, processing_api: ProcessingAPI) -> None:
#         self.processing_api = processing_api
    
#     def operation_is_ready(self, operation: operation.InsertOperation):
#         return self.processing_api.finished(operation.table) and all([self.processing_api.finished(relation) for relation in operation.relations])
