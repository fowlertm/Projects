# recursive_factorial.py

def factR(n): # This would be a good place to maybe work with try/except
    
    try:
        n = int(n)
    except (ValueError, TypeError):
        x = "Your input must be an integer"
    else:
        if n < 0:
            return (f"You returned {n}, and factorial isn't defined for negative values")
        elif n == 1 or n == 0:
            return n
        else:
            return n * factR(n - 1)

print(factR('3.1')) # --> 120