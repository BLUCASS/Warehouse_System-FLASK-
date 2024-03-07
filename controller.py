from model import Category, Product, engine
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()


class DbManagement():

    def get_categories(self) -> str:
        data = session.query(Category).all()
        return data

    def get_products(self) -> str:
        data = session.query(Product).all()
        session.close()
        return data
    
    def get_totals(self) -> float:
        products = session.query(Product).all()
        total = 0
        qnt = 0
        for product in products:
            total += float(product.total)
            qnt += int(product.amount)
        return {'total': total, 'qnt': qnt}

    def insert_product(self, name, price, amount, category) -> None:
        total = round(int(amount) * float(price), 2)
        product = Product(name=name,
                          price=price,
                          amount=amount,
                          total=total,
                          category_name=category)
        self.__add_data(product)

    def reduce_inventory(self, data) -> None:
        from datetime import datetime
        print(data)
        items = self.__search_product(data["name"].title())
        qnt = int(data["amount"])
        for item in items:
            if item.amount >= qnt:
                item.amount -= qnt
                item.total = item.amount * item.price
                item.exit_date = datetime.utcnow()
                if item.amount == 0: session.delete(item)
                break
            else:
                if qnt == 0: break
                qnt -= item.amount
                session.delete(item)
        session.commit()
        session.close()

    def __search_product(self, name) -> object:
        products = session.query(Product).filter(Product.name == name).all()
        session.close()
        if len(products) != 0: return products
        return False
    
    def __search_category(self, name) -> object:
        categories = session.query(Category).filter(Category.category_name == name).first()
        if categories != None: return categories
        return False

    def insert_category(self, name) -> None:
        category = Category(category_name=name)
        exists = self.__search_category(name)
        if not exists: self.__add_data(category)

    def __add_data(self, data) -> None:
        try:
            session.add(data)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

    def remove_product(self, name) -> None:
        products = self.__search_product(name)
        try:
            for product in products:
                session.delete(product)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

    def remove_category(self, name) -> None:
        category = self.__search_category(name)
        try:
            session.delete(category)
        except:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()