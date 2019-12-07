; Lab 14: Final Review
(define (compose-all funcs)
  (define (helper1 x)
    (define (helper2 x functions)
      (cond 
        ((null? functions)
         x
        )
        ((null? (cdr functions))
         ((car functions) x)
        )
        (else
         (helper2 ((car funcs) x) (cdr functions))
        )
      )
    )
    (helper2 x funcs)
  )
  helper1
)

(define (has-cycle? s)
  (define (pair-tracker seen-so-far curr)
    (cond 
      ((null? curr)
       #f
      )
      ((contains? seen-so-far (car curr))
       #t
      )
      (else
       (pair-tracker (cons (car curr) seen-so-far)
                     (cdr-stream curr)
       )
      )
    )
  )
  (pair-tracker (list) s)
)

(define (contains? lst s)
  (cond 
    ((null? lst)       #f)
    ((eq? (car lst) s) #t)
    (else              (contains? (cdr lst) s))
  )
)
