-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
drop table if exists matches;
drop table if exists players;
drop database if exists tournament;

create database tournament;

create table players (
    id serial primary key,
    name text,
    match int
);

create table matches (
    id serial primary key,
    winner int references players(id),
    loser int references players(id)
);