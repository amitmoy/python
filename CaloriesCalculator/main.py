womenCoeffs = {"general": 655.1, "weight": 9.563, "height": 1.850, "age": 4.676}  # coefficients to calculate women BMR
menCoeffs = {"general": 66.47, "weight": 13.75, "height": 5.003, "age": 6.755}  # coefficients to calculate men BMR
activityCoeffs = [1.2, 1.375, 1.55, 1.725, 1.9]


def calculate_bmr(weight, height, age, male, activity=2):
    if male:
        currentCoeffs = menCoeffs
    else:
        currentCoeffs = womenCoeffs

    answer = currentCoeffs["general"]
    answer += weight*currentCoeffs["weight"]
    answer += height*currentCoeffs["height"]
    answer -= age*currentCoeffs["age"]
    answer *= activityCoeffs[activity-1]
    return answer


validGender = False
while not validGender:
    print("Please choose your gender:")
    print("1.Male")
    print("2.Female")
    gender = input("Your choice: ")
    if gender == '1':
        isMale = True
        validGender = True
    elif gender == '2':
        isMale = False
        validGender = True

userWeight = float(input("Please enter your weight in kg: "))
userHeight = float(input("Please enter your height in cm: "))
userAge = float(input("Please enter your age in years: "))
print("Please choose your activity level")
print("1.Sedentary (little or no exercise a week)")
print("2.Lightly (exercise 1-3 days a week)")
print("3.Moderate (exercise 3-5 days a week)")
print("4.Active (exercise 6-7 days a week)")
print("5.Very Active (hard exercise 6-7 days a week)")
userActivity = int(input("Your choice: "))
print("Your daily calories intake is:", calculate_bmr(userWeight, userHeight, userAge, isMale, userActivity))
