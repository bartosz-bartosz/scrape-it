from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


metadata_obj = MetaData(schema="p_saver")


class Base(DeclarativeBase):
    metadata = metadata_obj


class MECategories(Base):
    __tablename__ = "me_categories"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    category_path: Mapped[str] = mapped_column(nullable=False)
    time_discovered: Mapped[datetime]
    last_check: Mapped[datetime]
    product_count: Mapped[int]
    regular_check: Mapped[bool] = mapped_column(default=False)
    check_freq: Mapped[int] = mapped_column(default=0)

    # Relationships
    products: Mapped[List["MEProducts"]] = relationship()


class MEProducts(Base):
    __tablename__ = 'me_products'

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    product_code: Mapped[str] = mapped_column(unique=True)
    product_name: Mapped[str] = mapped_column()
    monitoring: Mapped[bool] = mapped_column(default=False)
    monitoring_freq: Mapped[int] = mapped_column()
    path: Mapped[str] = mapped_column(unique=True)
    last_update: Mapped[datetime]
    category_id: Mapped[int] = mapped_column(ForeignKey('me_categories.id'))

    # Relationships
    category: Mapped["MECategories"] = relationship(back_populates='products')
    prices: Mapped[List["MEPrices"]] = relationship()


class MEPrices(Base):
    __tablename__ = 'me_prices'

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('me_products.id'))
    price: Mapped[int]
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now())

    # Relationships
    products: Mapped["MEProducts"] = relationship(back_populates='prices')
