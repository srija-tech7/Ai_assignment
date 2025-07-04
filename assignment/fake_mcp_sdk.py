class MCPServer:
    def __init__(self):
        self.tools = {}
        self.resources = {}

    def tool(self, name):
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

    def resource(self, name):
        def decorator(func):
            self.resources[name] = func
            return func
        return decorator

    def run(self):
        print("🛠️ [Mock Server Running] MCPServer started on http://localhost:5000")
        print("Available tools:", list(self.tools.keys()))
        print("Available resources:", list(self.resources.keys()))
