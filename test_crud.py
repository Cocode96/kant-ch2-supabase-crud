"""SDK 호출 경로 회귀 테스트. 실제 Supabase 실행을 대신하지 않는다."""
import unittest
from unittest.mock import MagicMock
from crud import Store

class CrudTests(unittest.TestCase):
    def setUp(self):
        self.client = MagicMock()
        self.query = self.client.table.return_value
        for name in ["select", "insert", "update", "delete", "eq", "order"]:
            getattr(self.query, name).return_value = self.query
        self.query.execute.return_value.data = [{"id": 7}]
        self.store = Store(self.client)

    def test_all_entities_have_four_executed_operations(self):
        examples = {
            "members": {"name": "회원", "email": "a@example.test"},
            "products": {"title": "상품", "price": 100},
            "orders": {"member_id": 1, "product_id": 1, "quantity": 1},
        }
        for entity, data in examples.items():
            with self.subTest(entity=entity):
                self.store.create(entity, data)
                self.store.read(entity, 7)
                self.store.update(entity, 7, data)
                self.store.delete(entity, 7)
                self.client.table.assert_called_with("practice_" + entity)
        self.assertEqual(self.query.execute.call_count, 12)

    def test_order_read_uses_columns_then_id_filter(self):
        self.store.read("orders", 42)
        self.query.select.assert_called_once_with("*")
        self.query.eq.assert_called_once_with("id", 42)

    def test_id_and_owner_mass_assignment_blocked(self):
        for patch in [{"owner_id": "someone"}, {"id": 3}, {}]:
            with self.assertRaises(ValueError):
                self.store.update("members", 1, patch)
        for row_id in [None, 0, -1, True, False, '1', 1.5]:
            with self.assertRaises(ValueError):
                self.store.delete("orders", row_id)
            with self.assertRaises(ValueError):
                self.store.update("orders", row_id, {"quantity": 1})

    def test_missing_member_fields_rejected(self):
        with self.assertRaises(ValueError):
            self.store.create("members", {"name": "회원"})

if __name__ == "__main__":
    unittest.main()
