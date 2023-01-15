from dataclasses import dataclass

from service.ml_service import MlService
from supplier.s3_supplier import S3Supplier


@dataclass
class Container:
    s3_supplier: S3Supplier
    ml_service: MlService


def init_combat_container() -> Container:
    s3_supplier = S3Supplier()

    ml_service = MlService(s3_supplier=s3_supplier)
    return Container(s3_supplier=s3_supplier, ml_service=ml_service)
