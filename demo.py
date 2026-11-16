"""별도 테스트 Supabase에서 회원/상품/주문 CRUD를 실제 실행하는 스크립트."""
import os
from pathlib import Path
from uuid import uuid4
from dotenv import load_dotenv
from supabase import create_client
from crud import Store

def main():
    load_dotenv(Path(__file__).with_name(".env"))
    names = ["SUPABASE_URL", "SUPABASE_PUBLISHABLE_KEY", "TEST_EMAIL", "TEST_PASSWORD"]
    if not all(os.getenv(name) for name in names):
        raise SystemExit(".env.example의 네 항목을 별도 테스트 프로젝트 값으로 설정하세요.")
    client = create_client(os.environ[names[0]], os.environ[names[1]])
    client.auth.sign_in_with_password({"email": os.environ["TEST_EMAIL"], "password": os.environ["TEST_PASSWORD"]})
    store = Store(client)
    created = []
    try:
        member = store.create("members", {"name": "실습 회원", "email": f"{uuid4().hex}@example.test"})[0]
        created.append(("members", member["id"]))
        product = store.create("products", {"title": "실습 상품", "price": 1000, "stock": 3})[0]
        created.append(("products", product["id"]))
        order = store.create("orders", {"member_id": member["id"], "product_id": product["id"], "quantity": 1})[0]
        created.append(("orders", order["id"]))
        for entity, row in [("members", member), ("products", product), ("orders", order)]:
            print(entity, "create:", row)
            result = store.read(entity, row["id"])
            assert len(result) == 1 and result[0]["id"] == row["id"]
            print(entity, "read by ID:", result)
        for entity, row, patch in [
            ("members", member, {"name": "수정 회원"}),
            ("products", product, {"price": 1200, "stock": 2}),
            ("orders", order, {"quantity": 2, "status": "paid"}),
        ]:
            updated = store.update(entity, row["id"], patch)
            assert len(updated) == 1 and all(updated[0][key] == value for key, value in patch.items())
            print(entity, "update:", updated)
    finally:
        # FK 때문에 주문부터 삭제. 이번 실행에서 만든 ID만 대상으로 삼는다.
        for entity, row_id in reversed(created):
            result = store.delete(entity, row_id)
            assert len(result) == 1
            assert store.read(entity, row_id) == []
            print(entity, "delete:", row_id, "confirmed")
        client.auth.sign_out()

if __name__ == "__main__":
    main()

