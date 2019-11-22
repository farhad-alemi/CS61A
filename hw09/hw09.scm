; Tail recursion
(define (replicate x n)
  (define (helper x n lst)
    (if (= n 0)
        lst
        (helper x (- n 1) (append `(,x) lst))
    )
  )
  (helper x n ())
)

(define (accumulate combiner start n term)
  (if (= n 0)
      start
      (combiner (term n)
                (accumulate combiner start (- n 1) term)
      )
  )
)

(define (accumulate-tail combiner start n term)
  (if (= n 0)
      start
      (accumulate-tail combiner
                       (combiner start (term n))
                       (- n 1)
                       term
      )
  )
)

; Streams
(define (map-stream f s)
  (if (null? s)
      nil
      (cons-stream (f (car s))
                   (map-stream f (cdr-stream s))
      )
  )
)

(define multiples-of-three
        (cons-stream 3
                     (map-stream (lambda (n) (+ n 3))
                                 multiples-of-three
                     )
        )
)

(define (nondecreastream s)
  (cond 
    ((null? s)
     nil
    )
    ((null? (cdr-stream s))
     s
    )
    (else
     (if (<= (car s) (car (cdr-stream s)))
         ; (cons-stream (list (car s) (car (cdr-stream s)) (car (cdr-stream (cdr-stream s)))) (nondecreastream (cdr-stream (cdr-stream (cdr-stream s)))))
         ; (cons-stream (list (car s) (nondecreastream (cdr-stream s))) nil)
         (cons-stream (list (car s) (car (cdr-stream s)))
                      (nondecreastream (cdr-stream (cdr-stream s)))
         )
         (cons-stream (list (car s))
                      (nondecreastream (cdr-stream s))
         )
         ; (cons-stream (car s) (cons (nondecreastream (cdr-stream s))))
         ; (cons-stream (list (car s))
         ; (nondecreastream (cdr-stream s))
     )
    )
  )
)

(define finite-test-stream
        (cons-stream 1
                     (cons-stream 2
                                  (cons-stream 3
                                               (cons-stream 1
                                                            (cons-stream 2
                                                                         (cons-stream 2 (cons-stream 1 nil))
                                                            )
                                               )
                                  )
                     )
        )
)

(define infinite-test-stream
        (cons-stream 1
                     (cons-stream 2
                                  (cons-stream 2 infinite-test-stream)
                     )
        )
)
