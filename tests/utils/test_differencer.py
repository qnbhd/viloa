from viloa.utils.differencer import Differencer


def test_differencer():
    test_cases = [
        ("foo: 1, 2\n"
         "bar: 3, 4\n"
         "zoo: 5, 6\n",

         "foo: 1, 3\n"
         "bar: 3, 4\n"
         "yoo: 9, 8\n"
         "zoo: 5, 6"),

        ("foo: 1, 2\n",

         "foo: 1, 2\n"
         "bar: 1, 2")
    ]

    good = [
        [[1, '-', '- foo: 1, 2'],
         [1, '+', '+ foo: 1, 3'],
         [2, ' ', '  bar: 3, 4'],
         [3, '+', '+ yoo: 9, 8'],
         [4, ' ', '  zoo: 5, 6']],

        [[1, ' ', '  foo: 1, 2'],
         [2, '+', '+ bar: 1, 2']]

    ]

    for case, ans in zip(test_cases, good):
        old, new = case
        df = Differencer(old, new)
        diff = df.process()
        assert diff == ans
