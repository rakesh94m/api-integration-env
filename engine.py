class MockDatabase:
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "Alice", "status": "active", "email": "alice@example.com"},
            2: {"id": 2, "name": "Bob", "status": "inactive", "email": "bob@example.com"},
            3: {"id": 3, "name": "Charlie", "status": "active", "email": "charlie@example.com"}
        }
        self.orders = []
        self.logs = []

    def get_user(self, user_id):
        return self.users.get(user_id, {"error": "User not found"})

    def create_order(self, data):
        if "user_id" not in data or "item" not in data:
            return {"error": "Missing fields: user_id and item are required"}, 400
        if data["user_id"] not in self.users:
            return {"error": "User not found"}, 404
        order = {"id": len(self.orders) + 1, "user_id": data["user_id"], "item": data["item"], "status": "pending"}
        self.orders.append(order)
        return {"status": "Order Created", "order": order}, 201
