# Number Analyzer Project

def is_even(n):
    return n % 2 == 0

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_palindrome(n):
    return str(n) == str(n)[::-1]

def main():
    print("Welcome to Number Analyzer!")
    numbers = input("Enter numbers separated by space: ").split()
    
    for num in numbers:
        if not num.isdigit():
            print(f"'{num}' is not a valid number!")
            continue
        
        n = int(num)
        print(f"\nAnalyzing {n}:")
        print(f"Even: {is_even(n)}")
        print(f"Prime: {is_prime(n)}")
        print(f"Palindrome: {is_palindrome(n)}")

if __name__ == "__main__":
    main()
