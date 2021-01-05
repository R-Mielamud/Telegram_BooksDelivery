from api.call_api import BaseAPI

class UsersAPI(BaseAPI):
    def __init__(self):
        super().__init__("users")

    def get_by_messenger_id(self, messenger_id):
        return self.requester.get("by_messenger_id/%s/" % messenger_id)

class OrdersAPI(BaseAPI):
    def __init__(self):
        super().__init__("orders")

class RequisitesAPI(BaseAPI):
    def __init__(self):
        super().__init__("requisites")

class BillsAPI(BaseAPI):
    def __init__(self):
        super().__init__("bills")
