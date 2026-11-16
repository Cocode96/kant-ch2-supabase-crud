"""회원/상품/주문에 공통인 CRUD 네 동작. Supabase SDK 호출을 한 곳에서 읽는다."""
FIELDS = {
    "members": {"name", "email"},
    "products": {"title", "price", "stock"},
    "orders": {"member_id", "product_id", "quantity", "status"},
}
REQUIRED = {
    "members": {"name", "email"},
    "products": {"title", "price"},
    "orders": {"member_id", "product_id", "quantity"},
}

class Store:
    def __init__(self, client):
        self.client = client

    def table(self, entity):
        if entity not in FIELDS:
            raise ValueError("members, products, orders 중 선택하세요.")
        return self.client.table("practice_" + entity)

    def validate(self, entity, data, creating=False):
        if entity not in FIELDS or not data or set(data) - FIELDS[entity]:
            raise ValueError("비어 있거나 허용하지 않은 필드입니다.")
        if creating and REQUIRED[entity] - set(data):
            raise ValueError("필수 필드가 없습니다.")

    def create(self, entity, data):
        self.validate(entity, data, creating=True)
        return self.table(entity).insert(data).execute().data

    def read(self, entity, row_id=None):
        query = self.table(entity).select("*")
        if row_id is not None:
            query = query.eq("id", row_id)
        return query.order("id").execute().data

    def update(self, entity, row_id, data):
        if not isinstance(row_id, int) or row_id <= 0:
            raise ValueError("수정 대상 ID가 필요합니다.")
        self.validate(entity, data)
        return self.table(entity).update(data).eq("id", row_id).execute().data

    def delete(self, entity, row_id):
        if not isinstance(row_id, int) or row_id <= 0:
            raise ValueError("삭제 대상 ID가 필요합니다.")
        return self.table(entity).delete().eq("id", row_id).execute().data

