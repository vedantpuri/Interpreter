# 'Its' Interpreter

## Overview
This project implements an interpreter for a simple programming language, "Its", which is a subset of Python.
Makes use of the 'ast' Python library to perform lexing and parsing of the source code written in "Its". The primary goal is to traverse the abstract syntax tree, produced by the ast library, and execute the code
using an environment data structure to keep track of the variable bindings and function definitions.

## Project Requirements and Structure

The files that comprise this project are:
- interpreter.py – Contains the interpreter code. Defines the eval_tree function.
- env.py – Contains the class definitions for GlobalEnv and LocalEnv.
- interpreter_main.py – (provided) Creates the ast tree and runs the interpreter.
Some testing code is provided in interpreter_main. The interpreter module defines the following two functions:

**eval_tree (tree)** Takes the AST tree object, evaluates and executes the nodes in the tree and returns a result, the expressed value of the program that was executed. The default return is 0.

**eval_node (node, env)** Takes an ast Node object and an environment (GlobalEnv or LocalEnv) object. It returns both a numeric value and an environment object (GlobalEnv or LocalEnv).


## Evaluation and Grammar
Python's 'ast' library is used to do the work of the front end. The front-end work especially the parser, is quite complex and we gain much by using this library. However, the 'ast' parser uses Python grammar, so our defined language will have to be a subset of Python's grammar. The defining language will be Python.

The output of the ast parse function is an abstract syntax tree. Each node in the tree represents a function linked to productions in the grammar. The code traverses this tree to execute the program that was parsed by the front end. It uses a data structure to store variable/value bindings that are established by certain statements in the source code, namely assignment and function definitions.

The “Its” language will support expressions, assignment, arithmetic operations (add, subtract, multiply, divide, mod), function definitions, and function calls. Since we are adopting a subset of Python symbols and grammar, we’ll use the nodes in the AST tree described below as a way of realizing the grammar of our language.


### The AST Tree

After obtaining the abstract parse tree, the interpreter evaluates the nodes of the tree. The code processes each Node in the tree, extracts the relevant data, ands perform the relevant operation.

These are the types of ast nodes that have been evaluated. The relevant attributes are given in parentheses:
1. Expr (value) the “value” is an ast.Node object that represents the expression. An expression such as: 7 + 5 would be a BinOp object (see below).
2. Assign (targets, value) "targets" is a list. We will only use the first element, the variable that will be assigned to the "value".
3. BinOp (left, op, right) "op" is the operator, "left" and "right" are the operands. We'll just do binary operators in our language: operand1 op operand2. The operations implemented are: Add, Sub, Mult, Div, Mod.
4. FunctionDef (name, args, body) "name"- the function name. "args"- an ast.argument object, "body"- a list of objects representing statements in the function body. The last statement is an ast.Return object. Note: our language will assume all functions return a value. We are not going to enforce this programmatically, but we will assume this.
5. Call (func, args) "func"- the name of the function (an ast.Name node type), "args"- the values (or expressions) that will be bound to the formal params. The parameters and values are "positional" so they correspond to the order they appear in their lists. To execute the function, I create a local environment, add the bindings of params and arg values. Then use that environment to evaluate the body statements.
6. Return (value) the "value" is the expression to be evaluated and whose result is to be returned by the function.
7. Name (id) -- the "id" attribute is the variable’s name. Lookup the variable in the environment and return the value, env.
8. Num (n) -- a number literal such as 9 This code is provided.

### The Environment Data Structure

Another key part of this project is building the data structure for environments.Uses an immutable structure that stores variable-value pairs in lists. Each addition to the structure results in a new pair of lists, with a reference to the previous structure. Uses the "rib-cage" model.

#### GlobalEnv

An environment is a reference to a linked list of var-value pairs. This has been implemented as a GlobalEnv class in Python. Each instance of a GlobalEnv contains a bindings list, a values list, and a reference to a previous instance of a GlobalEnv object.

#### LocalEnv

A function call creates the need for a local environment. The function’s parameters get bound to values passed in in a local environment. Then, the body of the function is executed in the local environment. Note that a local environment keeps a pointer to a global environment.
A local environment object is created upon processing a function class node. The function arguments are bound to the values passed in in this environment and the body of the function, a list of statements, is executed in this environment. The only difference between a LocalEnv and a GlobalEnv is that the localEnv has a pointer to the GlobalEnv.

## Purpose
This was my submission for my Programming Methodology class assignment.
