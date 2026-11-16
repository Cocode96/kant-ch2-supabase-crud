# Supabase 회원, 상품, 주문 CRUD

FastAPI 없이 Supabase Python SDK를 사용해 회원, 상품, 주문을 등록하고 조회, 수정, 삭제합니다. 주문은 실제로 등록된 회원과 상품을 참조합니다.

| 테이블 | PK | FK와 제약 |
| --- | --- | --- |
| `practice_members` | `id` | `owner_id` → `auth.users.id`. 사용자별 이메일 중복 방지 |
| `practice_products` | `id` | `owner_id` → `auth.users.id`. 가격, 재고는 0 이상 |
| `practice_orders` | `id` | `owner_id` → `auth.users.id`. `(member_id, owner_id)`와 `(product_id, owner_id)`는 각각 회원, 상품 복합 FK. 수량은 0 초과 |

RLS는 로그인한 사용자가 자기 행만 관리하도록 제한합니다. 복합 FK는 다른 사용자의 회원이나 상품이 주문에 연결되지 않게 막습니다.

## 실행

1. 실습용 Supabase 프로젝트에서 `schema.sql`을 실행합니다.
2. 테스트 계정을 준비하고 `.env.example`을 복사해 `.env`에 프로젝트 URL, publishable key와 테스트 계정 정보를 넣습니다.
3. 아래 명령으로 회원, 상품, 주문 CRUD를 실행합니다. 스크립트는 자신이 만든 샘플 행을 주문부터 역순으로 정리합니다.

```sh
uv sync --locked
uv run python demo.py
uv run python -m unittest -v
```

`transactions.sql`은 임시 테이블에서 재고 변경을 커밋한 뒤, 음수 재고가 CHECK 제약에 걸리면 그 트랜잭션의 변경을 롤백하는 예제입니다.
