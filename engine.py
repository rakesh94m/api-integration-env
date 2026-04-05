class MockDatabase:
    def __init__(self):
        # Initial data for the AI to interact with
        self.users = {1: {"name": "Alice", "status": "active"}, 2: {"name": "Bob", "status": "inactive"}}
        self.orders = []
        self.logs = []

    def get_user(self, user_id):
        return self.users.get(user_id, {"error": "User not found"})

    def create_order(self, data):
        if "user_id" not in data or "item" not in data:
            return {"error": "Missing fields"}, 400
        self.orders.append(data)
        return {"status": "Order Created", "id": len(self.orders)}, 201