create type order_status as enum('pending', 'processing', 'complete', 'rejected');

create table orders(
  id serial primary key,
  status order_status default 'pending'::order_status
)
