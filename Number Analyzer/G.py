

from colorama import Fore, Style, init
init(autoreset=True)

def is_even(n): return n % 2 == 0
def is_odd(n): return n % 2 != 0
def is_prime(n): return n > 1 and all(n % i for i in range(2, int(n**0.5) + 1))
def is_palindrome(n): return str(n) == str(n)[::-1]
def is_perfect_square(n): return int(n**0.5)**2 == n
def is_armstrong(n): return n == sum(int(d)**len(str(n)) for d in str(n))
def is_perfect(n): return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def analyze_number(n):
    print(Fore.CYAN + f"\n🔍 Analyzing {n}:" + Style.RESET_ALL)
    print(f"Even: {is_even(n)}")
    print(f"Odd: {is_odd(n)}")
    print(f"Prime: {is_prime(n)}")
    print(f"Palindrome: {is_palindrome(n)}")
    print(f"Perfect Square: {is_perfect_square(n)}")
    print(f"Armstrong: {is_armstrong(n)}")
    print(f"Perfect Number: {is_perfect(n)}")

def main():
    print(Fore.GREEN + "===============================")
    print("     🧮 Number Analyzer ")
    print("===============================" + Style.RESET_ALL)
    
    numbers = input("Enter numbers separated by space: ").split()
    nums = []

    for num in numbers:
        if not num.isdigit():
            print(Fore.RED + f"⚠️ '{num}' is not a valid integer!" + Style.RESET_ALL)
            continue
        n = int(num)
        nums.append(n)
        analyze_number(n)

    if nums:
        print(Fore.YELLOW + "\n📊 --- Summary ---" + Style.RESET_ALL)
        print(f"Total numbers: {len(nums)}")
        print(f"Even numbers: {sum(is_even(x) for x in nums)}")
        print(f"Prime numbers: {sum(is_prime(x) for x in nums)}")
        print(f"Palindromes: {sum(is_palindrome(x) for x in nums)}")
        print(f"Perfect Numbers: {sum(is_perfect(x) for x in nums)}")

        with open("number_report.txt", "w") as f:
            f.write("=== Number Analyzer Pro Report ===\n\n")
            for n in nums:
                f.write(f"Number: {n}\n")
                f.write(f"  Even: {is_even(n)}\n")
                f.write(f"  Odd: {is_odd(n)}\n")
                f.write(f"  Prime: {is_prime(n)}\n")
                f.write(f"  Palindrome: {is_palindrome(n)}\n")
                f.write(f"  Perfect Square: {is_perfect_square(n)}\n")
                f.write(f"  Armstrong: {is_armstrong(n)}\n")
                f.write(f"  Perfect Number: {is_perfect(n)}\n\n")
            f.write("=== End of Report ===\n")

        print(Fore.BLUE + "\n💾 Report saved as 'number_report.txt'" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo valid numbers to analyze." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
