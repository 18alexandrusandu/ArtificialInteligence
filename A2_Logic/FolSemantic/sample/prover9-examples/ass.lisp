(defun ass (l v)
  (cond ((null l) nil)
        ((< v 1)  l)
        ((>= (length (car (cdr (car l)))) v) (cons (car (car l)) (ass (cdr l) v)))
        (T (ass (cdr l) v))
  )
) 


(defun ass2 (l v acc)
  (cond ((null l) acc)
        ((< v 1)  acc)
        ((>= (length (car (cdr (car l)))) v)  (ass2 (cdr l) v (cons (car (car l)) acc)))
        (T (ass2 (cdr l) v acc))
  )
) 

(print (ass2 '((georhe (a vb x s)) (ana (a z d))) 4 nil))

(defun zip2 (f b)
  (do (      
       (auxf f (cdr auxf))
       (auxb b (cdr auxb))
       (rez nil)
      )
      ((or (endp auxf) (endp auxb)) (print 'Yuuopp) (reverse rez))
       (setq f1 (car auxf))
       (setq b1 (car auxb))
       (setq rez (cons (cons f1 (list b1)) rez))
   )
) 

(defun zip3 (f b)
    (mapcar #'(lambda (x y) (cons x (list y))) f b)
) 


(print (car (zip2 '(monica rachel phoebe) '(chandler ross joe))))
(print (zip3 '(monica rachel phoebe) '(chandler ross joe)))