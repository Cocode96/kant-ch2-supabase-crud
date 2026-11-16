-- 새 개인 테스트 프로젝트에서만 실행. 기존 팀 테이블과 이름을 분리한다.
create table public.practice_members (
    id bigint generated always as identity primary key,
    owner_id uuid not null default auth.uid() references auth.users(id),
    name text not null check (length(trim(name)) between 1 and 80),
    email text not null check (position('@' in email) > 1),
    unique (owner_id, email),
    unique (id, owner_id)
);
create table public.practice_products (
    id bigint generated always as identity primary key,
    owner_id uuid not null default auth.uid() references auth.users(id),
    title text not null check (length(trim(title)) between 1 and 100),
    price numeric(12,2) not null check (price >= 0),
    stock integer not null default 0 check (stock >= 0),
    unique (id, owner_id)
);
-- 최소 예제: 주문 한 건은 상품 한 종류를 주문한다.
create table public.practice_orders (
    id bigint generated always as identity primary key,
    owner_id uuid not null default auth.uid() references auth.users(id),
    member_id bigint not null,
    product_id bigint not null,
    quantity integer not null check (quantity > 0),
    status text not null default 'pending' check (status in ('pending','paid','cancelled')),
    created_at timestamptz not null default now(),
    foreign key (member_id, owner_id) references public.practice_members(id, owner_id) on delete restrict,
    foreign key (product_id, owner_id) references public.practice_products(id, owner_id) on delete restrict
);
create index on public.practice_orders(member_id, owner_id);
create index on public.practice_orders(product_id, owner_id);
alter table public.practice_members enable row level security;
alter table public.practice_products enable row level security;
alter table public.practice_orders enable row level security;
create policy own_members on public.practice_members for all to authenticated
    using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
create policy own_products on public.practice_products for all to authenticated
    using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
create policy own_orders on public.practice_orders for all to authenticated
    using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
revoke all on public.practice_members, public.practice_products, public.practice_orders from anon;
grant select, insert, update, delete on public.practice_members, public.practice_products, public.practice_orders to authenticated;
grant usage, select on sequence public.practice_members_id_seq, public.practice_products_id_seq, public.practice_orders_id_seq to authenticated;

