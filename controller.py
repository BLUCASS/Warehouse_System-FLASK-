from model import Category, Product, session


class DbManagement():
    """This classe will manage all the interactions with the database"""
    def get_categories(self) -> str:
        """It only returns the categories"""
        data = session.query(Category).all()
        return data

    def get_products(self) -> str:
        """It return all the products with their details"""
        data = session.query(Product).all()
        return data
    
    def get_totals(self) -> float:
        """It calculates the total price and amount of all the products and returns it"""
        products = session.query(Product).all()
        total = 0
        qnt = 0
        for product in products:
            total += float(product.total)
            qnt += int(product.amount)
        return {'total': total, 'qnt': qnt}

    def insert_product(self, name, price, amount, category) -> None:
        """It receives a details, turns it into an object and insert it in the database"""
        from datetime import datetime
        now = datetime.now()
        now = datetime.strftime(now, "%d/%m/%Y %H:%M")
        total = round(int(amount) * float(price), 2)
        product = Product(name=name,
                          price=price,
                          amount=amount,
                          total=total,
                          entry_date=now,
                          category_name=category)
        self.__add_data(product)

    def reduce_inventory(self, data) -> None:
        """It will reduce the product and recalculate the amount and the price.
        If the amount it is equal zero, the product will be removed"""
        from datetime import datetime
        now = datetime.now()
        now = datetime.strftime(now, "%d/%m/%Y %H:%M")
        items = self.__search_product(data["name"].title())
        qnt = int(data["amount"])
        for item in items:
            if item.amount >= qnt:
                item.amount -= qnt
                item.total = item.amount * item.price
                item.exit_date = now
                if item.amount == 0: session.delete(item)
                break
            else:
                if qnt == 0: break
                qnt -= item.amount
                session.delete(item)
        session.commit()

    def __search_product(self, name) -> object:
        """It seaches all the products with the given name, and returns them.
        If there is no product with the given name, it returns False"""
        products = session.query(Product).filter(Product.name == name).all()
        if len(products) != 0: return products
        return False
    
    def __search_category(self, name) -> object:
        """It seaches all the categories with the given name, and returns them.
        If there is no category with the given name, it returns False."""
        categories = session.query(Category).filter(Category.category_name == name).first()
        if categories != None: return categories
        return False

    def insert_category(self, name) -> None:
        """It receives a name and inserts it as a category"""
        category = Category(category_name=name)
        exists = self.__search_category(name)
        if not exists: self.__add_data(category)

    def __add_data(self, data) -> None:
        """It receives an object and inserts it in the database"""
        try:
            session.add(data)
        except:
            session.rollback()
        else:
            session.commit()

    def remove_product(self, name) -> None:
        """It receives a product's name and removes it from the database"""
        products = self.__search_product(name)
        try:
            for product in products:
                session.delete(product)
        except:
            session.rollback()
        else:
            session.commit()

    def remove_category(self, name) -> None:
        """It receives a category's name and removes it from the database."""
        category = self.__search_category(name)
        try:
            session.delete(category)
        except:
            session.rollback()
        else:
            session.commit()