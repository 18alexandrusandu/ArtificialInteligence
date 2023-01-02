;;
;; PDDL file for the AIPS2000 Planning Competition
;; based on the data generated by the airport simulator Astras.
;;

;; Author: Sebastian Trueg thisshouldbethecurrentdateandtime :(
;; Created with AdlDomainExporter 0.1 by Sebastian Trueg <trueg@informatik.uni-freiburg.de>
;;


(define (domain kitchen)
(:requirements :adl)

(:types egg tomato onion oil bacon salt peper knife fork salad cooker boal meal)

(:predicates
                (egg-fried ?e - egg)
                (tomato-choped ?t - tomato)
                (onion-choped ?o - onion)
                (knife-picked ?k - knife)
                (fork-picked ?f  - fork)
                (boal-salad-taken ?o - boal)
                (boal-eggs-taken ?o - boal)
                
                (knife-down ?k - knife)
                (oil-in-pan ?o - oil)
                (oil-on-salad ?o - oil  ?s - salad)
                (salad-salted ?s - salad)
                (salad-made ?s - salad)
                (bacon-is-frying)
                (bacon-fried)
                (cooker-started ?o - cooker)
                (cooker-stoped ?o - cooker)
                (eggs-made)
                (meal-made)
                (egg-picked ?e - egg)
                (eggs-are-frying)
                (waited_2_min)
                
                (all-onion-choped)
                (all-tomato-choped)
                (pan-part-made)
                (mixed-salad)
                (mixed-eggs)
                (eggs-condimented)
                (put-salt-on-eggs)
                (put-pepper-on-eggs)
                (put-egg-in-ball ?e)
                (put-tomato-in-boal ?t - tomato)
                (put-onion-in-boal ?o - onion)
                
                
)

(:action pick_knife
 :parameters
     (?k - knife)
 :precondition
    (not (knife-picked ?k))
               
 :effect
 (and (  not (knife-down ?k))
    
     (knife-picked ?k)
     )
               
)
(:action put_knife_down
 :parameters
     (?k - knife)
 :precondition
    (knife-picked  ?k)
               
 :effect
     (and 
     (not (knife-picked  ?k))
     (knife-down ?k)
     
               )
)

(:action pick_fork
 :parameters
     (?f - fork)
 :precondition
    (not (fork-picked ?f))
               
 :effect
 (and
     
      (fork-picked ?f)
     )
               
)
(:action put_fork_down
 :parameters
     (?f - fork)
 :precondition
     (fork-picked ?f)
               
 :effect
 (and
     (not (fork-picked ?f))
      
     )
               
)


(:action start-cooker
 :parameters
     (?k - knife  ?o - cooker ?f - fork)
 :precondition
 ( and
    (knife-down ?k)
    (not (fork-picked ?f))
    (cooker-stoped ?o)
   )
               
 :effect
     (and 
     (not (cooker-stoped ?o))
     (cooker-started ?o)
    
               )               
)

(:action stop-cooker
 :parameters
     (?o - cooker)
 :precondition
  
    (cooker-started ?o)
               
 :effect
     (and 
     (not (cooker-started ?o))
     (cooker-stoped ?o)
     
               )
)
(:action chop-onion
 :parameters
     (?ov - cooker ?o - onion ?k - knife)
 :precondition
  (and
    (knife-picked  ?k) 
    (cooker-stoped ?ov)
    (not (onion-choped ?o))
    )
               
 :effect
     (and 
     
     (onion-choped ?o)
               )
)

(:action chop-tomato
 :parameters
     (?t - tomato ?k - knife ?ov - cooker)
 :precondition
  ( and
    (knife-picked  ?k) (cooker-stoped ?ov)
    
    )
               
 :effect
     (and 
     (tomato-choped ?t)
               )
)



(:action mix-eggs
 :parameters
  ( ?f - fork)
 :precondition
  ( and
    
    (forall (?e - egg) (put-egg-in-ball ?e))
      (fork-picked ?f)
            )
              
 :effect
     (and 
     
     (mixed-eggs)
               )
)


(:action mix-salad
 :parameters
   (?f - fork)
 :precondition
  ( and
    
    (forall (?t - tomato) (put-tomato-in-boal ?t))
    (forall (?o - onion) (put-onion-in-boal ?o))
    (not  (mixed-salad))
    (fork-picked ?f)
            )
             
 :effect
     (and 
     (mixed-salad)
               )
)


(:action take_boal_eggs
 :parameters
   (?b - boal)
 :precondition
 (and 
  (not (boal-salad-taken ?b))
  (not  (boal-eggs-taken ?b))
)
 :effect
 (and 
  (boal-eggs-taken ?b)
  )
)

(:action take_boal_salad
 :parameters
   (?b - boal)
 :precondition
 (and 
  (not (boal-eggs-taken ?b))
  (not (boal-salad-taken ?b))
  )

 :effect
  (and 
  
  (boal-salad-taken ?b)
  )
)


(:action put_boal_salad_away
 :parameters
   (?b - boal)
 :precondition
 (and 
  (boal-salad-taken ?b)
  )
  

 :effect
  (and 
  
  ( not  (boal-salad-taken ?b))
  )
)

(:action put_boal_eggs_away
 :parameters
   (?b - boal)
 :precondition
 (and 
  (boal-eggs-taken ?b)
  )
  

 :effect
  (and 
  
  ( not  (boal-eggs-taken ?b))
  )
)


(:action puts-egg-in-boal
 :parameters
   (?b - boal ?e - egg)
 :precondition
 (and 
  (boal-eggs-taken ?b)
  (not (boal-salad-taken ?b))
  (not (put-egg-in-ball ?e))
  )
 :effect
 (and
  
  (put-egg-in-ball ?e)
  )
)

(:action puts-onion-in-boal
 :parameters
   (?b - boal ?o - onion)
 :precondition
 (and 
  (not (boal-eggs-taken ?b))
  (boal-salad-taken ?b)
  (not (put-onion-in-boal ?o))
  (onion-choped ?o)
  )
 :effect
  (and 
   
  (put-onion-in-boal ?o)
  )
)


(:action puts-tomato-in-boal
 :parameters
   (?b - boal ?t - tomato)
 :precondition
 (and 
  (not (boal-eggs-taken ?b))
  (boal-salad-taken ?b)
  (tomato-choped ?t)
  (not (put-tomato-in-boal ?t))
  )
 :effect
  (and 
  
  (put-tomato-in-boal ?t)
  )
)






(:action puts_salt_on_eggs
 :parameters
  ()
 :precondition
  ( and
      (not (put-salt-on-eggs))
      (mixed-eggs)
         
            )   
 :effect
     (and 
     
        (put-salt-on-eggs)
               )
)


(:action puts_pepper_on_eggs
 :parameters
  ()
 :precondition
  ( and
      (not (put-pepper-on-eggs))
      (mixed-eggs)
         
            )   
 :effect
     (and 
        (put-pepper-on-eggs)
               )
)

(:action have_eggs_condimented
 :parameters
   ()
 :precondition
  ( and
      (put-pepper-on-eggs)
      (put-salt-on-eggs)
         
            )   
 :effect
     (and 
     
       (eggs-condimented)
               )
)

(:action fry-eggs
 :parameters
     (?o - cooker ?k - knife ?oi - oil ?f - fork)
 :precondition
  ( and
    (cooker-started ?o)
    (knife-down ?k)
    (not (fork-picked ?f))
    (oil-in-pan ?oi)
    (mixed-eggs)
    (eggs-condimented)
            )   
 :effect
     (and 
      
     (eggs-are-frying)
               )
)

(:action fry-bacon
 :parameters
     (?o - cooker ?k - knife ?oi - oil)
 :precondition
  ( and
    (cooker-started ?o)
    (knife-down ?k)
    (not (fork-picked ?f))
    (oil-in-pan ?oi)
    (eggs-are-frying)
            )   
 :effect
     (and
      
     (bacon-is-frying)
               )
)


(:action wait_2_min
 :parameters
     (?o - cooker ?k - knife ?oi - oil )
 :precondition
  ( and
    (eggs-are-frying)
    (bacon-is-frying)
    (not (cooker-stoped ?o))
    (not (waited_2_min) )
            )   
 :effect
     (and 
   
      (waited_2_min)
     )



)


(:action stop_frying_eggs_and_bacon 
 :parameters
     (?o - cooker ?k - knife ?oi - oil )
 :precondition
  ( and
    (eggs-are-frying)
    (bacon-is-frying)
    (cooker-stoped ?o)
    (put-salt-on-eggs)
    (waited_2_min)
            )   
 :effect
     (and 
     (not (eggs-are-frying))
     (not (bacon-is-frying))
     (eggs-made)
     (bacon-fried)
     (pan-part-made)
     
               )
)

(:action put-oil-in-pan
:parameters
     ( ?o - oil  ?o2 - cooker)
     
 :precondition
 (cooker-started ?o2)
 
 :effect
 (and 
 
 (oil-in-pan ?o)
)

)

(:action put-oil-on-salad
:parameters
     ( ?o - oil ?s - salad )
     
 :precondition
 (mixed-salad)
 
 :effect
 ( oil-on-salad ?o  ?s)


)

(:action put-salt-on-salad
:parameters
     ( ?s - salad )
     
 :precondition
 (and (mixed-salad) (not (salad-salted ?s)))
 
 :effect
 (salad-salted ?s)


)

(:action finish-salad
:parameters
     ( ?s - salad ?o - oil)
     
 :precondition
 (and (mixed-salad) (salad-salted ?s)
 (oil-on-salad ?o  ?s)
 
 
 )
 
 :effect
 (and

 (salad-made ?s)
 )

)
(:action finish_meal
:parameters
  ( ?s - salad ?f - fork ?k - knife ?s - salad ?o - cooker )
     
 :precondition
 ( and (not (knife-picked ?k))
       (not (fork-picked ?f))
       (cooker-stoped ?o)
       (salad-made ?s)
       (pan-part-made)
       
 )
 
 :effect
 (meal-made)
 
 )

)
