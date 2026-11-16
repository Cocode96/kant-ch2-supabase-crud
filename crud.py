"""ȸ��/��ǰ/�ֹ��� ������ CRUD �� ����. Supabase SDK ȣ���� �� ������ �д´�."""
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
            raise ValueError("members, products, orders �� �����ϼ���.")
        return self.client.table("practice_" + entity)

    def validate(self, entity, data, creating=False):
        if entity not in FIELDS or not data or set(data) - FIELDS[entity]:
            raise ValueError("��� �ְų� ������� ���� �ʵ��Դϴ�.")
        if creating and REQUIRED[entity] - set(data):
            raise ValueError("�ʼ� �ʵ尡 �����ϴ�.")

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
            raise ValueError("���� ��� ID�� �ʿ��մϴ�.")
        self.validate(entity, data)
        return self.table(entity).update(data).eq("id", row_id).execute().data

    def delete(self, entity, row_id):
        if not isinstance(row_id, int) or row_id <= 0:
            raise ValueError("���� ��� ID�� �ʿ��մϴ�.")
        return self.table(entity).delete().eq("id", row_id).execute().data

