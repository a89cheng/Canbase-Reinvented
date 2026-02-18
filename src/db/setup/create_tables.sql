-- Canbase_Reinvented avoids having to use quotes
CREATE DATABASE Canbase_Reinvented;

-- The required fields: ID and Name
CREATE TABLE Player (
    Id INTEGER NOT NULL AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Rating INTEGER,
    Federation VARCHAR(60),
    PRIMARY KEY (Id)
);

-- The required fields: ID, Name and Starting Date
CREATE TABLE Tournament (
    Id INTEGER NOT NULL AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Location VARCHAR(60),
    Start_date DATE,
    Rounds INTEGER,
    PRIMARY KEY (Id)
);

-- The required fields: Id of the game, player Ids, tournament Id and result
-- Change the date from VARCHAR back to date at a later time
CREATE TABLE Game (
    Id INTEGER NOT NULL AUTO_INCREMENT ,
    White_player_id INTEGER NOT NULL,
    Black_player_id INTEGER NOT NULL,
    Tournament_id INTEGER NOT NULL,
    Moves VARCHAR(5000),
    Result VARCHAR(7),
    Played_Date VARCHAR(25),
    Eco VARCHAR(50),
    PRIMARY KEY (Id),
    FOREIGN KEY (White_player_id) REFERENCES Player(Id),
    FOREIGN KEY (Black_player_id) REFERENCES Player(Id),
    FOREIGN KEY (Tournament_id) REFERENCES Tournament(Id)
);

-- Sidenote, the other way to declare primary and foreign keys was to include them
-- in the line that "created" the table column

