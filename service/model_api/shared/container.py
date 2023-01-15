from dataclasses import dataclass

from supplier.s3_supplier import S3Supplier


@dataclass
class Container:
    s3_supplier: S3Supplier


def init_combat_container() -> Container:
    s3_supplier = S3Supplier()
    return Container(s3_supplier=s3_supplier)
