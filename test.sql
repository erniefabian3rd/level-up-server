SELECT
    gr.id,
    u.first_name || ' ' || u.last_name AS full_name,
    g.*
FROM levelupapi_game g
JOIN levelupapi_gamer gr
    ON g.gamer_id = gr.id
JOIN auth_user u
    ON gr.user_id = u.id      

SELECT
    gr.id AS gamer_id,
    u.first_name || ' ' || u.last_name AS full_name,
    e.*,
    g.title
FROM levelupapi_event e
JOIN levelupapi_gamer gr
    ON e.organizer_id = gr.id
JOIN auth_user u
    ON gr.user_id = u.id
JOIN levelupapi_game g
    ON e.game_id = g.id

SELECT
    gr.id AS gamer_id,
    u.first_name || ' ' || u.last_name AS full_name,
    e.*,
    g.title
FROM levelupapi_event e
JOIN levelupapi_event_attendees ea
    ON ea.event_id = e.id
JOIN levelupapi_gamer gr
    ON ea.gamer_id = gr.id
JOIN auth_user u
    ON gr.user_id = u.id
JOIN levelupapi_game g
    ON g.id = e.game_id