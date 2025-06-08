import flwr as fl
import numpy as np
from sklearn.linear_model import SGDRegressor

# Данные клиента
X = np.random.rand(20, 1)
y = 3 * X.squeeze() + np.random.normal(0, 0.1, 20)

# Модель линейной регрессии
model = SGDRegressor(max_iter=1, learning_rate='constant', eta0=0.01)

# Инициализируется модель одной тренировкой, чтобы появились coef_ и intercept_
model.partial_fit(np.array([[0.0]]), np.array([0.0]))

# Клиент Flower
class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return [model.coef_, np.array([model.intercept_])]

    def fit(self, parameters, config):
        model.coef_ = parameters[0]
        model.intercept_ = parameters[1]
        model.partial_fit(X, y)
        return self.get_parameters(config), len(X), {}

    def evaluate(self, parameters, config):
        model.coef_ = parameters[0]
        model.intercept_ = parameters[1]
        loss = np.mean((model.predict(X) - y) ** 2)
        return float(loss), len(X), {}

if __name__ == "__main__":
    fl.client.start_numpy_client(server_address="localhost:8080", client=FlowerClient())