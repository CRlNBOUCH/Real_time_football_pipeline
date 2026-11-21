
CREATE TABLE players (
    player_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    position VARCHAR(50),
    jersey_number INT,
    team VARCHAR(100)
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    player_id UUID REFERENCES players(player_id),
    session_id UUID,
    timestamp TIMESTAMP NOT NULL,
    heart_rate INT,
    distance FLOAT,
    acceleration FLOAT,
    speed FLOAT,
    calories FLOAT
);

INSERT INTO players (player_id, name, age, position, jersey_number, team)
VALUES
('11111111-1111-1111-1111-111111111111', 'Yassir Lagnaoui', 21, 'Midfielder', 8, 'FC Barcelona'),
('22222222-2222-2222-2222-222222222222', 'Player B', 27, 'Forward', 9, 'Team X'),
('33333333-3333-3333-3333-333333333333', 'Player C', 22, 'Defender', 5, 'Team Y');

CREATE VIEW player_dashboard AS
SELECT
   p.player_id,
   p.name,
   p.age,
   p.position, 
   p.jersey_number,
   p.team,
   e.session_id,

   DATE(e.timestamp) AS session_date,

   ROUND(AVG(e.heart_rate)::numeric,2) AS avg_heart_rate,
   ROUND(MAX(e.heart_rate)::numeric,2) AS max_heart_rate, 
   ROUND(SUM(e.distance)::numeric, 2) AS total_distance, 
   ROUND(MAX(e.speed)::numeric,2) AS max_speed, 
   ROUND(SUM(e.calories)::numeric ,2) AS calories_burnt, 
   ROUND(MAX(e.acceleration)::numeric,2) AS max_acceleration

FROM events e 
JOIN players p ON e.player_id = p.player_id

GROUP BY 
   p.player_id,
   p.name,
   p.age,
   p.position,
   p.jersey_number,
   p.team,
   e.session_id,
   DATE(e.timestamp);