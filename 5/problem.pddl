(define (problem Move_bals) (:domain Shakey)
(:objects 
    room_A, room_B - room
    ball_1, ball_2, ball_3, ball_4 - small_object 
    gripper_left, gripper_right - gripper
    s - shakey
)

(:init
    (in_room s Room_A)
    (so_in_room ball_1 room_A)
    (so_in_room ball_2 room_A)
    (so_in_room ball_3 room_A)
    (so_in_room ball_4 room_A)
    (empty gripper_left)
    (empty gripper_right)

)

(:goal (and
    (so_in_room ball_1 room_B)
    (so_in_room ball_2 room_B)
    (so_in_room ball_3 room_B)
    (so_in_room ball_4 room_B)
))


)

