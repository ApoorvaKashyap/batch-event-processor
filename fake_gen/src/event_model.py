from datetime import datetime


class Event:
    """
    Generic event class to represent an event with the following attributes:
    {
        "timestamp": "2024-10-07T14:30:00",
        "userId": "user123",
        "eventType": "pageView",
        "productId": "product456",
        "sessionDuration": 180
    }
    """

    timestamp: datetime
    userId: str
    eventType: str
    productId: str
    sessionDuration: int

    def __init__(
        self,
        timestamp: datetime,
        userId: str,
        eventType: str,
        productId: str,
        sessionDuration: int,
    ):
        self.timestamp = timestamp
        self.userId = userId
        self.eventType = eventType
        self.productId = productId
        self.sessionDuration = sessionDuration

    def __repr__(self) -> str:
        return f"Event(timestamp={self.timestamp.isoformat(timespec='seconds')}, userId={self.userId}, eventType={self.eventType}, productId={self.productId}, sessionDuration={self.sessionDuration})"
