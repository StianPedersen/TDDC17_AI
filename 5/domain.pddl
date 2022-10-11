;Header and description

(define (domain Shakey)

;remove requirements that are not needed
(:requirements :strips :equality :typing :adl)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    box
    light_switch
    door_small
    door_wide
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

    ;(light_on ?l - light_switch)
    (so_in_room ?x - small_object ?y - room)
    (in_room  ?s - shakey ?y - room)

    ; Predicates
    ; ROOM(?r - room)
    ; BALL(?x - small_object)


)

;define actions here
(:action move 
    :parameters (?x - room ?y - room ?s - shakey)
    :precondition (and (in_room ?s ?x))
    :effect (and (in_room ?s ?y)
                ( not (in_room ?s ?x)))
)

(:action pick_up 
    :parameters (?x - small_object ?y - room ?z - gripper ?s - shakey) ; x = ball, y = room, z = gripper, s = shakey
    :precondition (and (so_in_room ?x ?y) (in_room ?s ?y) (empty ?z))
    :effect (and (carry ?x ?z)
            (not (so_in_room ?x ?y))
            (not (empty ?z)))
)

(:action drop 
    :parameters (?x - small_object ?y - room ?z - gripper ?s - shakey) ; x = ball, y = room, z = gripper, s = shakey
    :precondition (and (carry ?x ?z) (in_room ?s ?y))
    :effect (and (so_in_room ?x ?y)
            (empty ?z)
            (not (carry ?x ?z)))
)



)