;Header and description

(define (domain Shakey)

;remove requirements that are not needed
(:requirements :strips :equality :typing :adl)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    box
    light_switch
    small_door big_door - door
    shakey
    small_object
    gripper
    room
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (carry ?x - small_object ?z - gripper )
    (empty ?z - gripper)

    (so_in_room ?x - small_object ?y - room)
    (in_room  ?s - shakey ?y - room)

    (door_between ?r1 - room ?r2 - room ?d - door)
    (is_big_door ?d - door)

    (box_in_room ?b - box ?y - room)

    (light_in_room ?l - light_switch ?r - room)
    (light_on ?l ?r)
    (light_off ?l ?r)
)

;define actions here
(:action I_like_to_move_it_move_it ; moves shakey
    :parameters (?x - room ?y - room ?s - shakey ?d - door)
    :precondition (and (in_room ?s ?x) (door_between ?x ?y ?d))
    :effect (and (in_room ?s ?y)
                ( not (in_room ?s ?x)))
)

(:action Push_me_and_then_touch_me_until_i_can_get_my_satisfaction ; pushes box through big_door
    :parameters (?x - room ?y - room ?s - shakey ?d - door ?b - box)
    :precondition (and (in_room ?s ?x) (door_between ?x ?y ?d) (is_big_door ?d) (box_in_room ?b ?x))
    :effect (and (in_room ?s ?y) (box_in_room ?b ?y)
                ( not (in_room ?s ?x)) 
                ( not (box_in_room ?b ?x)))
)

(:action Pick_it_up_pick_ut_up_pick_it_up_up_up_never_say_never ; picks up small object
    :parameters (?x - small_object ?y - room ?z - gripper ?s - shakey ?l - light_switch)
    :precondition (and (so_in_room ?x ?y) (in_room ?s ?y) (empty ?z) (light_on ?l ?y))
    :effect (and (carry ?x ?z)
            (not (so_in_room ?x ?y))
            (not (empty ?z)))
)

(:action Drop_it_like_its_hot ; drops small object
    :parameters (?x - small_object ?y - room ?z - gripper ?s - shakey) 
    :precondition (and (carry ?x ?z) (in_room ?s ?y))
    :effect (and (so_in_room ?x ?y)
            (empty ?z)
            (not (carry ?x ?z)))
)

(:action Turn_all_the_lights_on ; turns light on
    :parameters (?l - light_switch ?y - room  ?s - shakey ?b - box) 
    :precondition (and (light_in_room ?l ?y) (in_room  ?s ?y) (box_in_room ?b ?y) (light_off ?l ?y))
    :effect (and (light_on ?l ?y))
)
)