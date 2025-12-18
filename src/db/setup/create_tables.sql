--Canbase_Reinvented avoids having to use quotes
CREATE DATABASE Canbase_Reinvented;

--The required fields: ID and Name
CREATE TABLE Player (
    Id INTEGER NOT NULL,
    Name VARCHAR NOT NULL,
    Rating INTEGER,
    Federation VARCHAR,
    PRIMARY KEY (Id)
);

--The required fields: ID, Name and Starting Date
CREATE TABLE Tournament (
    Id INTEGER NOT NULL,
    Name VARCHAR NOT NULL,
    Location VARCHAR,
    Start_date DATE NOT NULL,
    Rounds INTEGER,
    PRIMARY KEY (Id)
);

--The required fields: Id of the game, player Ids, tournament Id and result
CREATE TABLE Game(
    Id INTEGER,
    White_player_id INTEGER NOT NULL,
    Black_player_id INTEGER NOT NULL,
    Tournament_id INTEGER NOT NULL,
    Moves CHAR,
    Result VARCHAR(7) NOT NULL,
    Played_date DATE,
    Eco VARCHAR,
    --Id is always the primary key
    PRIMARY KEY (Id),
    --White and Black are referenced in player table, tournament is referenced in tournament table
    FOREIGN KEY (White_player_id) REFERENCES Player(Id),
    FOREIGN KEY (Black_player_id) REFERENCES Player(Id)
    FOREIGN KEY (Tournament_id) REFERENCES Tournament(Id)
);