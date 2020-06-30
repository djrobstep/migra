create type order_status as enum('pending', 'processing', 'complete', 'rejected');

create schema other;

create type other.otherenum1 as enum('a', 'b', 'c');

create type other.otherenum2 as enum('a', 'b', 'c');

create table orders(
  id serial primary key,
  status order_status default 'pending'::order_status,
  othercolumn other.otherenum2
);
