import random
import csv

# ---------- SCORING FUNCTIONS ----------

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

    if brand in premium: return 10
    elif brand in mid: return 8
    elif brand in budget: return 6
    else: return 3

# ---------- PHYSICAL SCORE ----------
def physical_score(age, battery, working, brand):
    a = age_score(age)
    b = battery_score(battery)
    w = working
    br = brand_score(brand)

    score = (0.35*w) + (0.25*b) + (0.20*a) + (0.20*br)
    return round(score, 2)

# ---------- REFURBISH VALUE ----------
def refurbish_value(p_score, d_score):
    # good physical & low damage = high value
    value = (0.6*p_score) + (0.4*(10-d_score))
    return round(max(0, min(10, value)), 2)

# ---------- DATASET GENERATION ----------
brands = ["apple","samsung","oneplus","vivo","oppo","realme","redmi","poco","motorola","local"]

rows = []

for _ in range(350):  # number of records
    age = round(random.uniform(0.5,6),1)
    battery = random.randint(20,100)
    working = random.randint(0,10)
    brand = random.choice(brands)

    damage_score = round(random.uniform(0,10),2)

    p_score = physical_score(age,battery,working,brand)
    r_value = refurbish_value(p_score,damage_score)

    rows.append([p_score,damage_score,r_value])

# ---------- SAVE CSV ----------
with open("dataset.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["physical_score","damage_score","refurbish_value"])
    writer.writerows(rows)

print("Dataset created successfully: dataset.csv")
