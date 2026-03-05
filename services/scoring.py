def age_score(age):
    if age <= 1: return 10
    elif age <= 2: return 8
    elif age <= 3: return 6
    elif age <= 4: return 4
    elif age <= 5: return 2
    else: return 1

def battery_score(battery):
    if battery >= 90: return 10
    elif battery >= 75: return 8
    elif battery >= 60: return 6
    elif battery >= 45: return 4
    elif battery >= 30: return 2
    else: return 1

def brand_score(brand):
    premium = ["apple", "samsung", "oneplus"]
    mid = ["vivo", "oppo", "realme"]
    budget = ["redmi", "poco", "motorola"]

    brand = brand.lower()

    if brand in premium: return 10
    elif brand in mid: return 8
    elif brand in budget: return 6
    else: return 3

def calculate_physical_score(age, battery, working, brand):
    a = age_score(age)
    b = battery_score(battery)
    br = brand_score(brand)
    return round((0.35*working)+(0.25*b)+(0.20*a)+(0.20*br),2)