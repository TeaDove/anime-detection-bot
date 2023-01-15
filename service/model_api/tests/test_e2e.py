from shared.container import init_combat_container

container = init_combat_container()


class TestClass:
    def test_get_weights(self):
        container.s3_supplier.safe_weights_file()

    # def predict(self):
    #     ml_service.predict(image, markup)

    # def test_predict(self, benchmark):
    #     benchmark.pedantic(self.predict, iterations=10, rounds=100)
