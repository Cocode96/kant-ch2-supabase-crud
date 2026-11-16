# Supabase 회원, 상품, 주문 CRUD

Python과 Supabase SDK로 쇼핑몰의 회원, 상품, 주문을 생성, 조회, 수정, 삭제하는 CH2 과제다. uv로 의존성을 고정하고 데이터 무결성은 PostgreSQL 제약조건, 사용자별 접근은 RLS로 관리한다.

**검증 상태:** SDK 호출 테스트 4개와 격리된 로컬 PGlite의 CRUD, 제약조건, RLS, COMMIT/ROLLBACK 검증을 통과했다. 실제 Supabase 프로젝트의 SDK 실행 및 CRUD 캡처는 아직 확보하지 않았다. 아래 로컬 검증을 원격 실행 증거로 보지 않는다.

## 실행

Python 3.13 이상과 uv가 필요하다.

```sh
uv sync --locked
uv run --locked python -m unittest -v
```

실제 연동은 전용 실습 프로젝트에 [schema.sql](schema.sql)을 한 번 적용하고, `.env.example`을 `.env`로 복사하여 아래 값을 설정한 다음 실행한다.

| 이름 | 용도 |
| --- | --- |
| SUPABASE_URL | 실습 프로젝트 URL |
| SUPABASE_PUBLISHABLE_KEY | 공개 클라이언트 키 |
| TEST_EMAIL | 가입과 이메일 확인을 마친 실습 계정 |
| TEST_PASSWORD | 해당 계정 비밀번호 |

```sh
uv run --locked python demo.py
```

키와 비밀번호는 Git에 포함하지 않는다. 로그인된 사용자 권한으로 검증하므로 service-role 키를 사용하지 않는다. 생성 SQL은 기존 테이블을 덮어쓰는 마이그레이션이 아니며 같은 프로젝트에서 중복 실행하지 않는다.

## 테이블과 관계

| 테이블 | PK | 데이터 | FK / 제약조건 |
| --- | --- | --- | --- |
| practice_members | id, bigint identity | name, email, owner_id | owner_id → auth.users.id, 사용자별 email 유일, 이름 1~80자 |
| practice_products | id, bigint identity | title, price, stock, owner_id | owner_id → auth.users.id, 제목 1~100자, 가격과 재고 0 이상 |
| practice_orders | id, bigint identity | member_id, product_id, quantity, status, created_at, owner_id | (member_id, owner_id) → practice_members(id, owner_id), (product_id, owner_id) → practice_products(id, owner_id), 수량 양수 |

주문 상태는 `pending / paid / cancelled`로 제한한다. 주문이 참조하는 회원과 상품은 먼저 삭제할 수 없다(`ON DELETE RESTRICT`). 삭제 시에는 주문을 먼저 지운다.

회원과 상품의 속성을 주문에 중복 저장하지 않고 FK로 연결한다. 이 실습의 주문 한 행은 상품 한 종류를 뜻한다. 여러 상품으로 구성되는 주문과 결제 시점의 가격 보존은 별도 주문 상세 모델이 필요한 확장 범위다.

테이블은 `practice_` 접두사, 컬럼은 snake_case로 통일했다. PK 인덱스와 별도로 주문의 두 복합 FK에 인덱스를 두었다.

## CRUD와 권한 설계

| 동작 | 구현 | 확인할 결과 |
| --- | --- | --- |
| 생성 | Store.create → insert → execute | DB가 생성한 ID와 저장된 행 반환 |
| 조회 | Store.read → select → eq → order | 전체 목록 또는 지정한 ID |
| 수정 | Store.update → update → eq | 지정 ID의 허용 필드만 변경 |
| 삭제 | Store.delete → delete → eq | 지정 ID 삭제 후 조회 결과가 빈 목록 |

[crud.py](crud.py)는 엔티티별 필드 목록과 필수값 검사를 공유한다. `id`, `owner_id`를 입력으로 덮어쓸 수 없고, 수정/삭제에는 양의 정수 ID만 허용한다. DB 오류는 호출자에게 전달하여 실패를 성공으로 처리하지 않는다.

RLS의 `USING`은 조회/수정/삭제할 기존 행을, `WITH CHECK`는 생성/수정 후 행의 소유자를 검사한다. 두 조건 모두 `auth.uid() = owner_id`다. 주문의 복합 FK는 다른 사용자의 회원이나 상품을 연결하는 것도 차단한다. 익명 역할에는 테이블 권한이 없다.

[demo.py](demo.py)는 세 테이블의 생성, ID 조회, 수정 결과를 검증한 뒤 자신이 만든 ID만 역순으로 삭제한다. 여러 SDK 요청은 하나의 DB 트랜잭션이 아니므로, 아래 SQL 트랜잭션 실습과 구분한다.

## 트랜잭션과 실패 재현

[transactions.sql](transactions.sql)은 같은 DB 세션에서 임시 테이블만 사용한다.

1. 재고 10 → 8 변경 후 COMMIT: 조회 결과 8.
2. 다음 트랜잭션에서 8 → 5 변경.
3. 재고 -1 변경으로 CHECK 위반을 의도적으로 발생.
4. ROLLBACK 후 재조회: 앞서 변경한 5도 취소되어 8.

실패 구문과 ROLLBACK은 같은 세션에서 구분해서 실행한다. 연결을 교체하면 임시 테이블과 진행 중인 트랜잭션 상태를 이어받을 수 없다.

## 확인 결과와 제출 증거

2026-11-16 확인:

| 검증 | 결과와 범위 |
| --- | --- |
| Python unittest | 4개 통과. 세 엔티티의 SDK 호출, ID 필터, 소유자 필드 주입 차단, 잘못된 ID와 필수값 검사 |
| 로컬 PGlite | 세 테이블 CRUD, FK 삭제 제한, 수량 CHECK, A/B 사용자 격리 통과 |
| SQL 실패 시나리오 | COMMIT 뒤 8, 실패 트랜잭션 내부 5, ROLLBACK 뒤 8 확인 |
| 실제 Supabase Auth / SDK | 미검증 |
| 실제 CRUD 화면 캡처 | 미확보 |

발제의 캡처 요건을 완료하려면 실제 실습 프로젝트에서 테이블 PK/FK 화면과 세 테이블의 생성/조회/수정/삭제 결과를 촬영하여 이 README에 연결해야 한다. 현재 없는 캡처를 링크하거나 로컬 결과를 Supabase 실행 화면으로 표시하지 않는다.
