;Header and description

(define (domain Shakey)

    ;remove requirements that are not needed
    (:requirements :strips :equality :typing :adl)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        box light_switch small_door big_door - door
        shakey small_object gripper room
    )

    ; un-comment following line if constants are needed
    ;(:constants )

    (:predicates
        (carry ?x - small_object ?z - gripper) ; needed to represent carrying an object
        (empty ?z - gripper) ;Needed to check if gripper is empty

        (so_in_room ?x - small_object ?y - room) ; Needeed to represent of small object is in room
        (in_room ?s - shakey ?y - room) ; Represents which room shakey is in

        (door_between ?r1 - room ?r2 - room ?d - door) ; Between which rooms are the doors
        (is_big_door ?d - door) ; Only big doors can have boxes pushed through them

        (box_in_room ?b - box ?y - room) ; checks if box is in room

        (light_in_room ?l - light_switch ?r - room) ; checks if light is i room
        (light_on ?l ?r) ; is light on?
        (light_off ?l ?r) ; is light off?
    )

    ;define actions here
    (:action Move ; moves shakey
        :parameters (?x - room ?y - room ?s - shakey ?d - door)
        :precondition (and (in_room ?s ?x) (door_between ?x ?y ?d))
        :effect (and (in_room ?s ?y)
            ( not (in_room ?s ?x)))
    )

    (:action Push ; pushes box through big_door
        :parameters (?x - room ?y - room ?s - shakey ?d - door ?b - box)
        :precondition (and (in_room ?s ?x) (door_between ?x ?y ?d) (is_big_door ?d) (box_in_room ?b ?x))
        :effect (and (in_room ?s ?y) (box_in_room ?b ?y)
            ( not (in_room ?s ?x))
            ( not (box_in_room ?b ?x)))
    )

    (:action Pick_up ; picks up small object
        :parameters (?x - small_object ?y - room ?z - gripper ?s - shakey ?l - light_switch)
        :precondition (and (so_in_room ?x ?y) (in_room ?s ?y) (empty ?z) (light_on ?l ?y))
        :effect (and (carry ?x ?z)
            (not (so_in_room ?x ?y))
            (not (empty ?z)))
    )

    (:action Drop ; drops small object
        :parameters (?x - small_object ?y - room ?z - gripper ?s - shakey)
        :precondition (and (carry ?x ?z) (in_room ?s ?y))
        :effect (and (so_in_room ?x ?y)
            (empty ?z)
            (not (carry ?x ?z)))
    )

    (:action Turn_on ; turns light on
        :parameters (?l - light_switch ?y - room ?s - shakey ?b - box)
        :precondition (and (light_in_room ?l ?y) (in_room ?s ?y) (box_in_room ?b ?y) (light_off ?l ?y))
        :effect (and (light_on ?l ?y))
    )
)