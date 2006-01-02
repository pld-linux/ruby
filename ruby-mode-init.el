;; ruby-mode-init.el
;; Created: 2002-02-01
;;
(if (featurep 'xemacs)
    (setq load-path (cons "/usr/lib/xemacs/xemacs-packages/lisp/ruby-mode" load-path))
  (setq load-path (cons "/usr/share/emacs/site-lisp/ruby-mode" load-path)))
     

(autoload 'ruby-mode "ruby-mode" "Mode for editing ruby source files" t)
(setq auto-mode-alist
      (cons '("\\.rb$" . ruby-mode) auto-mode-alist))
(setq interpreter-mode-alist
      (cons '("ruby" . ruby-mode) interpreter-mode-alist))

(autoload 'run-ruby "inf-ruby" "Run an inferior Ruby process")
(autoload 'inf-ruby-keys "inf-ruby" "Set local key defs for inf-ruby in ruby-mode")

(add-hook 'ruby-mode-hook
	  '(lambda ()
	     (inf-ruby-keys)))
