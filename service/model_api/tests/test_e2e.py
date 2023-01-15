from pathlib import Path

from shared.container import init_combat_container

container = init_combat_container()


class TestClass:
    def test_get_weights(self):
        container.s3_supplier.safe_weights_file()

    def test_predict(self):
        print()
        for file in Path("tests/images").iterdir():
            print(f"{file}: {container.ml_service.predict(str(file.absolute()))}")
