class RiskManagement:
    def __init__(self, max_drawdown, max_position_size):
        self.max_drawdown = max_drawdown
        self.max_position_size = max_position_size

    def check_drawdown(self, portfolio_value):
        if portfolio_value < (1 - self.max_drawdown):
            raise ValueError("Drawdown limit exceeded")

    def check_position_size(self, position_size):
        if position_size > self.max_position_size:
            raise ValueError("Position size exceeds maximum allowed")
