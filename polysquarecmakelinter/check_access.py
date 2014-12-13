# /polysquarecmakelinter/check_access.py
#
# Linter checks for access rights
#
# See LICENCE.md for Copyright information
"""Linter checks for access rights"""

from polysquarecmakelinter.types import LinterFailure
from polysquarecmakelinter import find_all
from polysquarecmakelinter import find_variables_in_scopes


def only_use_own_privates(abstract_syntax_tree):
    """Checks that all private definitions used are defined here"""

    calls, defs = find_all.private_calls_and_definitions(abstract_syntax_tree)

    errors = []

    for call, info in calls.items():
        if call not in defs.keys():
            for line in info:
                msg = "Used external private definition {0}".format(call)
                errors.append(LinterFailure(msg, line))

    return errors


def only_use_own_priv_vars(ast):
    """Checks that all private variables used are defined here"""

    errors = []

    global_set_vars = find_variables_in_scopes.set_in_tree(ast)
    global_used_vars = find_variables_in_scopes.used_in_tree(ast)

    # The big assumption here is that the "scopes" structure in both
    # trees are the same
    def _scope_visitor(set_vars_scope, used_vars_scope):
        """Visits scope's set vars and used vars.


        If a var was private and used, but not set in this scope or any
        parents, then report an error
        """

        assert len(set_vars_scope.scopes) == len(used_vars_scope.scopes)

        for index in range(0, len(set_vars_scope.scopes)):
            _scope_visitor(set_vars_scope.scopes[index],
                           used_vars_scope.scopes[index])

        for variable in used_vars_scope.used_vars:
            for use in find_all.variables_used_in_expr(variable.node):
                if use.startswith("_"):
                    # Used a private, check if it was set
                    private_var_was_set = False

                    traverse_scope = set_vars_scope
                    while traverse_scope is not None:
                        for set_var in traverse_scope.set_vars:
                            if (set_var.node.contents == use and
                                    (set_var.node.line,
                                     set_var.node.col) != variable):
                                private_var_was_set = True
                                break

                        traverse_scope = traverse_scope.parent

                    if not private_var_was_set:
                        msg = ("Referenced external private"
                               " variable {0}").format(use)
                        errors.append(LinterFailure(msg,
                                                    variable.node.line,
                                                    variable.node.col))

    _scope_visitor(global_set_vars, global_used_vars)

    return errors
