(define (problem Move_balls) (:domain Shakey)
(:objects 
    room_a room_b room_c - room
    ball_1 ball_2 ball_3 ball_4 - small_object 
    gripper_left gripper_right - gripper
    s - shakey
    door1 door2 - big_door
    door3 - small_door
    our_box - box
    light_switch_a light_switch_b light_switch_c - light_switch
)

(:init
    (in_room s room_a)
    (so_in_room ball_1 room_a)
    (so_in_room ball_2 room_a)
    (so_in_room ball_3 room_b)
    (so_in_room ball_4 room_a)
    (empty gripper_left)
    (empty gripper_right)
    (box_in_room our_box room_c)    

    ;setup light 
    (light_in_room light_switch_a room_a)
    (light_in_room light_switch_b room_b)
    (light_in_room light_switch_c room_c)
    (light_off light_switch_a room_a)
    (light_off light_switch_b room_b)
    (light_off light_switch_c room_c)


    ;setup doors
    (door_between room_a room_b door1)
    (door_between room_b room_c door2)
    (door_between room_b room_c door3)
    ;
    (door_between room_b room_a door1)
    (door_between room_c room_b door2)
    (door_between room_c room_b door3)
    ;
    (is_big_door door1)
    (is_big_door door2)
)

(:goal (and
    (so_in_room ball_1 room_c)
    (so_in_room ball_2 room_c)
    (so_in_room ball_3 room_c)
    (so_in_room ball_4 room_c)
    (box_in_room our_box room_c)
    (light_off light_switch_a room_a)
    (light_off light_switch_b room_b)
    (light_off light_switch_c room_c)

))


)

