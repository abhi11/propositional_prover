from prover import prove_formula


def main():
    problems = ['p',
                '(NOT (NOT (NOT (NOT not))  )           )',
                '(IF p p)',
                '(AND p (NOT p))']
    answers = [1, 1, 'T', 'U']

    for i in range(0, len(problems)):
        ans = prove_formula(problems[i])
        print('For: ', problems[i], '\nAns: {0}, Expected: {1}\n'.format(ans, answers[i]))


if __name__ == '__main__':
    main()
