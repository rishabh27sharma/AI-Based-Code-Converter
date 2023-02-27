
class ExampleServiceImpl:
    def __init__(self, exampleRepository):
        self.exampleRepository = exampleRepository

    def getAllExample(self):
        return self.exampleRepository.findAll()

    def saveExample(self, exampleEntity):
        return self.exampleRepository.save(exampleEntity)