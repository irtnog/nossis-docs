;; nossis-docs, serverless hosting for static, private web sites that
;; works like GitHub Pages
;;
;; Copyright (C) 2024  Matthew X. Economou
;;
;; This program is free software: you can redistribute it and/or
;; modify it under the terms of the GNU Affero General Public License
;; as published by the Free Software Foundation, either version 3 of
;; the License, or (at your option) any later version.
;;
;; This program is distributed in the hope that it will be useful, but
;; WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
;; Affero General Public License for more details.
;;
;; You should have received a copy of the GNU Affero General Public
;; License along with this program.  If not, see
;; <https://www.gnu.org/licenses/>.

;; For more information, see (info "(emacs) Directory Variables").

((nil . ((eval . (progn
                   ;; install or activate the development environment
                   ;; (requires pyvenv-tracking-mode)
                   (set (make-local-variable 'my-project)
                        (locate-dominating-file default-directory ".dir-locals.el"))
                   (set (make-local-variable 'my-project-venv)
                        (concat my-project ".venv"))
                   (if (not (file-exists-p my-project-venv))
                       (let ((cwd default-directory)
                             (cmd "make setup"))
                         (cd my-project)
                         (async-shell-command cmd)
                         (cd cwd)
                         (message
                          (format "Please re-open this file/directory after the \"%s\" command finishes." cmd)))
                     ;; must be set project-wide for pre-commit to work
                     (set (make-local-variable 'pyvenv-activate)
                          my-project-venv))))))
 (python-mode . ((eval . (progn
                           ;; sort imports, then style code
                           (add-hook 'before-save-hook #'py-isort-before-save nil t)
                           (add-hook 'before-save-hook #'elpy-black-fix-code nil t))))))

;; Local Variables:
;; no-byte-compile: t
;; End:
