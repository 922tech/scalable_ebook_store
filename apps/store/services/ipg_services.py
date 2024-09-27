from abc import ABC, abstractmethod


class AbstractIPGService(ABC):
    @abstractmethod
    def verify_payment(self, *args, **kwargs):
        pass

    @abstractmethod
    def request_payment(self, *args, **kwargs):
        pass


class StripeService(AbstractIPGService):

    def verify_payment(self, *args, **kwargs):
        pass

    def request_payment(self, *args, **kwargs):
        pass
