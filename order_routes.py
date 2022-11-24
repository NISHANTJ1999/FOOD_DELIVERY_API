from fastapi import APIRouter ,Depends, HTTPException ,status
from fastapi_jwt_auth import AuthJWT
from models import User,Order
from schemas import OrderModel, OrderStatus
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_router= APIRouter(
    prefix='/order',
    tags=['order']
)


Session=Session(bind=engine)

@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):

    """
       ## A SAMPLE HELLO WORLD ROUTE
       This returns Hello World

    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")
    return {"message":"Hello World"}



@order_router.post('/PlaceOrder/', status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel, Authorize:AuthJWT=Depends()):

    """
    ## PLACING AN ORDER
    This requires following
    quantity : Integer
    pizza_size : String
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user=Authorize.get_jwt_subject()
    user=Session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
    )
    new_order.user=user

    Session.add(new_order)

    Session.commit()

    response={
        'pizza_size':new_order.pizza_size,
        'quantity':new_order.quantity,
        'id':new_order.id,
        'order_status':new_order.ORDER_STATUS,
    }
    return jsonable_encoder(response)

@order_router.get('/getAllOrders')
async def list_all_order(Authorize:AuthJWT=Depends()):


    """
    ## LIST ALL ORDERS
    This route list order which are made, and it can be only access by superuser

    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")

    current_user=Authorize.get_jwt_subject()

    user=Session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders=Session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not super user")

@order_router.get('/OrdersById/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
    ## GET AN ORDER BY ITS ID
    This route gets the order by Its ID, which can be only access by superuser
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    user=Authorize.get_jwt_subject()

    current_user=Session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=Session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not allowed to carryout request")

@order_router.get('/GetUserOrder/')
async def get_user_orders(Authorize:AuthJWT=Depends()):
    """
        ## GET A CURRENT USER'S ORDER
        This route lists the order of currently logged in user
        """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    user = Authorize.get_jwt_subject()
    current_user=Session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)

@order_router.get('/GetUserOrderById/{id}/')
async def get_specific_order(id:int,Authorize:AuthJWT=Depends()):
    """
       ## GET AN SPECIFIC ORDER BY THE CURRENTLY LOGGED IN USER
       This router returns order by its ID of the currently logged in user

       """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    subject=Authorize.get_jwt_subject()

    current_user=Session.query(User).filter(User.username==subject).first()

    orders=current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No Order with such id")

@order_router.put('/Update/{id}/')
async def update_order(id:int, order:OrderModel ,Authorize:AuthJWT=Depends()):
    """
           ## UPDATING AN ORDER
           This router requires the following fields:

           -quantity: Integer
           -pizza_size: string

           """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")

    order_to_update=Session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size

    Session.commit()

    return jsonable_encoder(order_to_update)


@order_router.patch('/UpdateStatus/{id}/')
async def update_order_status(id:int,order:OrderStatus,Authorize:AuthJWT=Depends()):
    """
           ## Update an Order Status
           This router returns order status by its id

           """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Token")

    username=Authorize.get_jwt_subject()

    current_user=Session.query(User).filter(User.username==username).first()


    if current_user.is_staff:
        order_to_update=Session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order.order_status

        Session.commit()

        response={
                "id":order_to_update.id,
                "quantity":order_to_update.quantity,
                "pizza_size":order_to_update.pizza_size,
                "order_status":order_to_update.order_status,
            }

        return jsonable_encoder(response)
@order_router.delete('/DeleteOrder/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int,Authorize:AuthJWT=Depends()):
    """
           ## DELETE AN ORDER
           This router deletes the previous order by its id

           """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")


    order_to_delete=Session.query(Order).filter(Order.id==id).first()

    Session.delete(order_to_delete)

    Session.commit()

    return order_to_delete