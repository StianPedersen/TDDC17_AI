;Header and description

(define (domain Felix_Nyrfors)

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
    (carry ?g - gripper ?c - small_object)
    (empty ?g - gripper)

    (light_on ?l - light_switch)
    (so_in_room ?s - small_object ?r - room)
    (in_room ?r - room ?s - shakey)


)

;define actions here
(:action sug_min_rov
    :parameters ()
    :precondition (and )
    :effect (and )
)


)