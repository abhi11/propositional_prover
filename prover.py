import itertools

# CONSTANTS
OR = 'OR'
IF = 'IF'
NOT = 'NOT'
AND = 'AND'
OPENING_BRACKET = '('
CLOSING_BRACKET = ')'
SPACE = ' '

VALID_OPS = [OR, NOT, IF, AND]

INVALID = 'E'
TAUTOLOGY = 'T'
UNSATISFIABLE = 'U'

def NOT_Expr(p):
    return '(not {0})'.format(p)


def IF_Expr(p, q):
    return '((not {0}) | {1})'.format(p, q)


def OR_Expr(p, q):
    return '({0} | {1})'.format(p, q)


def AND_Expr(p, q):
    return '({0} & {1})'.format(p, q)


def make_saner(s):
    '''
    Takes a string and removes unecessary spaces newline etc
    '''
    tokens = s.split()
    saner = ' '.join(tokens)
    return saner

def check_basic_sanity(F):
    '''
    Number of OPENING and CLOSING  brackets should be equal
    Returns False if not
    Also checks if there's any special character, if present returns False
    '''
    op = 0
    cl = 0
    for c in F:
        if c == ' ':
            continue

        # no special characters allowed
        if c != OPENING_BRACKET and c != CLOSING_BRACKET and (not c.isalnum()):
            return False

        if c == OPENING_BRACKET:
            op = op + 1

        if c == CLOSING_BRACKET:
            cl = cl + 1

    return (cl == op)

def isPure(p):
    '''
    Checks if the operand is pure or it is an indirection
    '''
    if 'OPERANDS' in p:
        return False
    return True

## it is important to use `OPERANDS` here
def handle_operation(op, stack_operands):
    if op not in VALID_OPS:
        return INVALID

    if len(stack_operands) < 1:
        return INVALID

    if op == NOT:
        p = stack_operands.pop()
        if len(stack_operands) < 1:
            return INVALID

        cl = stack_operands.pop()
        if cl != CLOSING_BRACKET:
            return INVALID

        var = ''
        if isPure(p):
            var = 'OPERANDS["{0}"]'.format(p)
        else:
            var = p
        return NOT_Expr(var)

    var1 = ''
    p = stack_operands.pop()
    if isPure(p):
        var1 = 'OPERANDS["{0}"]'.format(p)
    else:
        var1 = p

    if len(stack_operands) < 1:
        return INVALID

    var2= ''
    q = stack_operands.pop()
    if isPure(q):
        var2 = 'OPERANDS["{0}"]'.format(q)
    else:
        var2 = q

    if len(stack_operands) < 1:
        return INVALID

    cl = stack_operands.pop()
    if cl != CLOSING_BRACKET:
        return INVALID

    if op == IF:
        return IF_Expr(var1, var2)
    if op == OR:
        return OR_Expr(var1, var2)
    if op == AND:
        return AND_Expr(var1, var2)

def get_formula(F):
    stack_operands = []

    # dict to store operand names
    ## The name is important here it is used by the eval() mehtod
    operands = {}

    revF = reversed(F)
    # work on a list
    rev_characters = list(revF)

    buf = ''
    length = len(rev_characters)
    i = 0
    while i < length:
        c = rev_characters[i]
        i = i + 1

        if c == CLOSING_BRACKET:
            # Symbol here
            if buf != '':
                if not buf.islower():
                    return INVALID, operands
                stack_operands.append(buf)

            stack_operands.append(c)
            buf = ''
            continue

        if (c == SPACE) and (buf == ''):
            continue

        if c.isalnum():
            buf = c + buf
            continue

        ## Operation here
        if (c == OPENING_BRACKET) or ((c == SPACE) and (buf in VALID_OPS)):
            # if empty stack for braces then ill formed expression
            if len(stack_operands) < 1:
                return INVALID, operands

            # Now handle the operation
            expr = handle_operation(buf, stack_operands)
            if expr == INVALID:
                return INVALID, operands

            stack_operands.append(expr)
            buf = ''

            # if c was space just ignore the next opening bracket
            if c == SPACE:
                i = i + 1

            continue

        # We have a symbol
        if (c == SPACE) and (buf != ''):
            if not buf.islower():
                return INVALID, operands

            stack_operands.append(buf)
            operands[buf] = True
            buf = ''
            continue

        else:
            # invalid character unsupported
            return INVALID, operands

    ## buf should be empty for a valid formula
    if buf != "":
        return INVALID, operands

    if len(stack_operands) > 1:
        return INVALID, operands

    formula = stack_operands.pop()
    return formula, operands


def permutations_for_truth_values(n):
    '''
    Takes n as the number of bits and
    returns all possible permuations of bits
    as a matrix(list of list)
    '''
    bools = [True, False]
    perms = itertools.product(bools, repeat=n)
    perms = list(perms)

    return perms


def proveFormula(F):
    F = make_saner(F)

    ## Special case when just one literal
    tokens = F.split()
    if len(tokens) == 1 and tokens[0].isalnum() and tokens[0].islower() and tokens[0] not in VALID_OPS:
        return 1

    if not check_basic_sanity(F):
        return INVALID

    formula, OPERANDS = get_formula(F)
    if formula == INVALID:
        return INVALID

    number_of_operands = len(OPERANDS)
    permutations = permutations_for_truth_values(number_of_operands)

    ## Get all keys first as a list
    keys = list(OPERANDS.keys())

    ## Get Truth value for all combinations
    results = []
    for permutation in permutations:
        pointer = 0
        ## Put values in OPERANDS
        while pointer < number_of_operands:
            OPERANDS[keys[pointer]] = permutation[pointer]
            pointer = pointer + 1

        result = eval(formula)
        results.append(result)

    # count total
    total_trues = 0
    for x in results:
        if not x:
            continue
        total_trues = total_trues + 1

    if total_trues == 0:
        return UNSATISFIABLE

    if total_trues == len(permutations):
        return TAUTOLOGY

    return total_trues


problems = ['p',
        '(NOT (NOT (NOT (NOT not))  )           )',
        '(IF p p)',
        '(AND p (NOT p))']
answers = [1,
        1,
        'T',
        'U']
