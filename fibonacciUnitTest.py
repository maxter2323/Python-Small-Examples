import unittest
numbersAmount = 10

def FibonnaciSequence():
    numbers = [0]
    for i in range(numbersAmount):
        if numbers[i] == 0:
            numbers.append(1)
        else:
            num = numbers[i] + numbers[i-1]
            numbers.append(num)
    return  numbers

def FibonnaciSequenceWrong():
    numbers = [0]
    for i in range(numbersAmount):
        if numbers[i] == 0:
            numbers.append(1)
        else:
            numbers.append(numbers[i] + numbers[i])
            numbers.append(num)
    return numbers

class FibonacciTest(unittest.TestCase):

    def setUp(self):
        self.fibonacciList = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_fib(self):
        testSequence = FibonnaciSequence()
        for i in range(len(self.fibonacciList)):
            original = self.fibonacciList[i]
            obtained = (testSequence[i])
            self.assertEqual(original, obtained)

    def test_wrongfib(self):
        testSequence = FibonnaciSequenceWrong()
        for i in range(len(self.fibonacciList)):
            original = self.fibonacciList[i]
            obtained = testSequence[i]
            self.assertEqual(original, obtained)


if __name__ == '__main__':
    unittest.main()