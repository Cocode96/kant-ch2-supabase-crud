# Supabase ȸ��, ��ǰ, �ֹ� CRUD

FastAPI ���� Supabase Python SDK�� ����� ȸ��, ��ǰ, �ֹ��� ����ϰ� ��ȸ, ����, �����մϴ�. �ֹ��� ������ ��ϵ� ȸ���� ��ǰ�� �����մϴ�.

| ���̺� | PK | FK�� ���� |
| --- | --- | --- |
| `practice_members` | `id` | `owner_id` �� `auth.users.id`. ����ں� �̸��� �ߺ� ���� |
| `practice_products` | `id` | `owner_id` �� `auth.users.id`. ����, ����� 0 �̻� |
| `practice_orders` | `id` | `owner_id` �� `auth.users.id`. `(member_id, owner_id)`�� `(product_id, owner_id)`�� ���� ȸ��, ��ǰ ���� FK. ������ 0 �ʰ� |

RLS�� �α����� ����ڰ� �ڱ� �ุ �����ϵ��� �����մϴ�. ���� FK�� �ٸ� ������� ȸ���̳� ��ǰ�� �ֹ��� ������� �ʰ� �����ϴ�.

## ����

1. �ǽ��� Supabase ������Ʈ���� `schema.sql`�� �����մϴ�.
2. �׽�Ʈ ������ �غ��ϰ� `.env.example`�� ������ `.env`�� ������Ʈ URL, publishable key�� �׽�Ʈ ���� ������ �ֽ��ϴ�.
3. �Ʒ� �������� ȸ��, ��ǰ, �ֹ� CRUD�� �����մϴ�. ��ũ��Ʈ�� �ڽ��� ���� ���� ���� �ֹ����� �������� �����մϴ�.

```sh
uv sync --locked
uv run python demo.py
uv run python -m unittest -v
```

`transactions.sql`�� �ӽ� ���̺����� ��� ������ Ŀ���� ��, ���� ����� CHECK ���࿡ �ɸ��� �� Ʈ������� ������ �ѹ��ϴ� �����Դϴ�.
