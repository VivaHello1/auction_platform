from .health_controller import router as health_router
from .v1 import auction_vehicles_router, auctions_router, manufacturers_router, users_router

__all__ = [
    "health_router",
    "auctions_router",
    "auction_vehicles_router",
    "manufacturers_router",
    "users_router",
]
