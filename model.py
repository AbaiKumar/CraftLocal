from tkinter import Image
from bson import ObjectId
from pymongo import MongoClient


class Data:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client["CraftLocal"]
        self.userCollection = self.database["Users"]
        self.productCollection = self.database["Products"]

    def createAccount(self, mail, password):
        user_document = {
            "mail": mail,
            "password": password
        }
        if (self.userCollection.find_one({"mail": mail}) == None):
            self.userCollection.insert_one(user_document)
            return True
        else:
            return False

    def loginAccount(self, mail, pwd):
        query = {"mail": mail}
        result = self.userCollection.find_one(query)

        if result:
            if result.get("password") == pwd:
                return True
        return False

    def getData(self, indx):
        try:
            start = indx * 10
            end = start + 10
            data = list(self.productCollection.find(
                {}, {'_id': 1, 'Name': 1, 'Price': 1, 'Discount': 1}).skip(start).limit(end))
            for item in data:
                item['_id'] = str(item['_id'])
            return [True, data]
        except Exception as e:
            return [False, []]

    def getSingle(self, pid):
        obj_pid = ObjectId(pid)
        try:
            data = list(self.productCollection.find({"_id": obj_pid}))
            data[0]['_id'] = str(data[0]['_id'])
            return [True, data[0]]
        except:
            return [False, []]

    def addItemToCart(self, itemID, mail):
        user_document = {"mail": mail}
        user_result = self.userCollection.find_one(user_document)

        if user_result is None:
            return False
        else:
            update_result = self.userCollection.update_one(
                {"mail": mail},
                {"$set": {f"checkout.{itemID}": 1, "placed": {}}},
                upsert=True
            )

            if update_result.modified_count > 0 or update_result.upserted_id is not None:
                return True
            else:
                return False

    def getItemFromCart(self, mail):
        user_document = {"mail": mail}
        user_result = self.userCollection.find_one(user_document)
        productList = []

        if user_result is None:
            return {"data": productList, "msg": False}
        else:
            for id, quantity in user_result["checkout"].items():
                data = self.productCollection.find_one({"_id": ObjectId(id)})
                product = {"id": str(data["_id"]), "Name": data["Name"], "Price": data["Price"],
                           "Discount": data["Discount"], "Quantity": quantity}
                productList.append(product)
            return {"data": productList, "msg": True}

    def updateCheckoutData(self, record, mail):
        user_document = {"mail": mail}
        user_result = self.userCollection.find_one(user_document)
        if user_result is None:
            return False
        else:
            for i in record:
                if user_result['checkout'][i['id']] != i["Quantity"]:
                    print("hi")
                    update_result = self.userCollection.update_one(
                        {"mail": mail},
                        {"$set": {f"checkout.{i['id']}": int(i["Quantity"])}},
                        upsert=True
                    )

                    if update_result.modified_count > 0 or update_result.upserted_id is not None:
                        continue
                    else:
                        return False
        return True


data = Data()
