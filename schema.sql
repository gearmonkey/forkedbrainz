drop table if exists scores;
create table faceoffs (
  id integer primary key autoincrement,
  review_A_source text not null,
  review_A_id text not null,
  review_B_source text not null,
  review_B_id text not null,
  question int not null,
  winner char not null,
  time timestamp not null
);
drop table if exists scores;
create table questions (
  id integer primary key autoincrement,
  copy text not null
);
drop table if exists spotify_mbz;
create table spotify_mbz (
  id integer primary key autoincrement,
  spotify_id char(80) not null,
  mbz_id char(80) not null
);
CREATE INDEX mbidx on spotify_mbz (mbz_id);
CREATE INDEX spidx on spotify_mbz (spotify_id);