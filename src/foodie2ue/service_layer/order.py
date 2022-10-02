from typing import List, Optional, Tuple

from . import ServiceError
from ..constants import ORDER_STATUSES
from ..domain.model import AddOn, MenuItem, Order
from ..domain.events import OrderCreatedEvent, OrderUpdatedEvent
from ..exceptions import (
    InvalidOrderStateException,
    MultipleItemsFoundException,
)
from .unit_of_work import AbstractUnitOfWork


def create_new_order(order: Order,
                     uow: AbstractUnitOfWork) -> Tuple[Optional[Order], Optional[ServiceError]]:
    """Create a new Order given an `Order` model.

    The `Order` models `MenuItems` as a list of dicts. This makes it simpler to manage in the
    persistence/DB layer.  The `AddOns` for a `MenuItem` is likewise an array of objects.

    All of those details should not matter at this layer as we are dealing with business logic an
    the `Order` model.
    """
    not_found_msg = 'A matching menu item could not be found. Did you forget to specify size? '
    not_found_msg += 'Menu items are case sensitive. Did you spell it correctly?'

    for item in order.items:
        try:
            menu_item: MenuItem = uow.repo.fetch_menu_item_by(name=item['name'],
                                                              size=item.get('size'))
        except MultipleItemsFoundException:
            return (None, ServiceError(not_found_msg, details=item))

        if not menu_item:
            return (None, ServiceError(not_found_msg, details=item))

        order.add_item_to_order(menu_item)

        for addon_item in item.get('addons', []):
            # TODO - pass in the menu_item to verify the addon is associated
            addon: AddOn = uow.repo.fetch_addon_by(name=addon_item['name'])
            if not addon:
                msg = 'A matching addon could not be found'
                return (None, ServiceError(msg, details=addon_item))
            order.add_addon_to_order(menu_item)

    uow.repo.create_order(order)
    uow.add_event(
        OrderCreatedEvent(
            id=order.id,
            recipient=order.customer_email,
            first_name=order.customer_first_name,
            order_id=order.id,
            order_total=order.total,
        ))

    return (order, None)


def list_new_orders(uow: AbstractUnitOfWork) -> List[Order]:
    return uow.repo.fetch_new_orders()


def list_ready_for_pickup_orders(uow: AbstractUnitOfWork) -> List[Order]:
    return uow.repo.fetch_ready_for_pickup_orders()


def get_order(item_id: int, uow: AbstractUnitOfWork) -> Order:
    return uow.repo.fetch_order(item_id=item_id)


def update_order_status(order: Order, status: str,
                        uow: AbstractUnitOfWork) -> Tuple[Optional[Order], Optional[ServiceError]]:
    try:
        uow.repo.update_order_status(order, status=status)
        uow.add_event(OrderUpdatedEvent(id=order.id, status=order.status))
        return order, None
    except InvalidOrderStateException:
        status_err = f"Must be one of: {(', ').join(ORDER_STATUSES)}"
        return (None, ServiceError('Invalid order state', {"status": [status_err]}))