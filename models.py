from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        msg = "Counselor("
        for k, v in self.__dict__.items():
            if k != "_sa_instance_state":
                msg += f"{k}={v}, "
        msg += ")"
        return msg


class Restaurant(Base):
    __tablename__ = "restaurants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    website: Mapped[str] = mapped_column()


class Food(Base):
    __tablename__ = "foods"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id"))
    price: Mapped[int] = mapped_column()

    orders: Mapped["Order"] = mapped_column(ForeignKey("orders.food_id"))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    customer: Mapped["Customer"] = mapped_column(ForeignKey("customers.id"))
    food: Mapped[Food] = mapped_column(ForeignKey("foods.id"))


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    orders: Mapped[Order] = mapped_column(ForeignKey("orders.customer_id"))
