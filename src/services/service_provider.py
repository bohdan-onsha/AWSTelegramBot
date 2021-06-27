from services.environment_service import EnvironmentService


class ServiceProvider:
    class __Services:
        __environment_service = None

        def __str__(self):
            return id(self)

        def environment_service(self):
            if not self.__environment_service:
                self.__environment_service = EnvironmentService()
            return self.__environment_service

    instance = None

    def __init__(self):
        if not ServiceProvider.instance:
            ServiceProvider.instance = ServiceProvider.__Services()

    def __getattr__(self, item):
        return getattr(self.instance, item)
