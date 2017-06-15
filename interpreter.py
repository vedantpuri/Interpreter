from env import GlobalEnv, LocalEnv

genv = GlobalEnv.empty_env()
result = 0


def eval_tree(tree):
    """ The top level function.
        Args:
            tree (ast.Module): The ast abstract syntax tree- the root is a Module node object. The children are contained in a list.
        Returns:
            integer or float: the result of any value returned by the program, 0 by default.
    """
    global genv
    global result
    # Here, get the list of children nodes. Iterate over that list, calling eval_node on each node.
    list_nodes = tree.body
    env = genv
    for node in list_nodes:
        evaluated_node = eval_node(node, env)
        env = evaluated_node[1]
        result = evaluated_node[0]
    return result


def node_name(node):
    return type(node).__name__


def eval_node(node, env):
    """ Evaluates a Node object in the abstract syntax tree.
        Args:
            node (ast.Node): The node to evaluate.
            env (GlobalEnv | LocalEnv): An environment data type.
        Returns:
            (integer or float, environment): A tuple, where the first element is the result of any
            value computed at this node, and the second value is either a GlobalEnv or LocalEnv object.
    """
    global genv
    global result
    node_type = node_name(node)
    if node_type == 'Expr':
        return eval_node(node.value, env)
    elif node_type == 'Assign':
        # extract the variable name, evaluate the RHS, then extend the environment.
        var_name = node.targets[0].id
        val = eval_node(node.value, env)[0]
        env = env.extend([var_name], [val])
        return None, env
    elif node_type == 'BinOp':
        # get the left and right operands (we use only single operands) and the operator.
        # evaluate the operands and apply the operator. return the number, env.
        left_operand = eval_node(node.left, env)[0]
        right_operand = eval_node(node.right, env)[0]
        res = 0
        operator = node_name(node.op)
        if operator == "Add":
            res = left_operand + right_operand
        elif operator == "Sub":
            res = left_operand - right_operand
        elif operator == "Mult":
            res = left_operand * right_operand
        elif operator == "Div":
            res = left_operand / right_operand
        elif operator == "Mod":
            res = left_operand % right_operand
        return res, env
    elif node_type == 'FunctionDef':
        # need the function id (name), args, and body. Extend the environment.
        # you can leave the args wrapped in the ast class and the body and unpack them
        # when the function is called.
        env = env.extend([node.name], [[node.args, node.body]])
        return None, env
    elif node_type == 'Call':
        # get any values passed in to the function from the Call object.
        # get the fxn name and look up its parameters, if any, and body from the env.
        # get lists for parameter names and values and extend a LocalEnv with those bindings.
        # evaluate the body in the local env, return the value, env.

        fxn_at_hand = node.func
        if node_name(fxn_at_hand) == 'Name':
            fxn_at_hand = env.lookup(node.func.id)
        else:
            fxn_at_hand = eval_node(fxn_at_hand, env)[0]
        body = fxn_at_hand[1]
        params_objects = fxn_at_hand[0].args

        local_environment = LocalEnv(None, genv)
        arg_vals = []
        params = []
        for arg in node.args:
            arg_vals += [eval_node(arg, env)[0]]
        for par in params_objects:
            params += [par.arg]
        local_environment = local_environment.extend(params, arg_vals)

        res = 0
        for statement in body:
            res_tuple = eval_node(statement, local_environment)
            local_environment = res_tuple[1]
            res = res_tuple[0]
        return res, env
    elif node_type == 'Return':
        # evaluate the node, return the value, env.
        return eval_node(node.value, env)[0], env
    elif node_type == 'Name':
        # Name(identifier id)- lookup the value binding in the env
        return env.lookup(node.id), env
    # Num(object n) -- a number, return the number, env.
    elif node_type == 'Num':
        return node.n, env
