import dataclasses


@dataclasses.dataclass()
class ServiceError:
    message: str = 'Error'
    details: dict = dataclasses.field(default_factory=dict)

    def __str__(self) -> str:
        return self.message
