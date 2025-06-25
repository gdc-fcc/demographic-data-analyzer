import pandas as pd

def as_percent(num):
    return round(num * 100, 1)

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    #print(df.head(10))
    #print(df.shape)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df["race"].value_counts()

    # What is the average age of men?
    average_age_men = round(sum(df.query('sex == "Male"')['age'])/len(df.query('sex == "Male"')), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(sum(df['education'] == "Bachelors") / len(df) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = (df['education'] == 'Bachelors') | (df['education'] == 'Masters') | (df['education'] == 'Doctorate')
    lower_education = higher_education.apply(lambda x: not x)
    rich = df['salary'] == ">50K"

    # percentage with salary >50K
    higher_education_rich = as_percent(sum(higher_education & rich) / sum(higher_education))
    lower_education_rich = as_percent(sum(lower_education & rich) / sum(lower_education))

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = min(df['hours-per-week'])
    works_min = df['hours-per-week'] == min_work_hours

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = sum(works_min)

    rich_percentage = as_percent(sum(works_min & rich) / sum(works_min))

    # What country has the highest percentage of people that earn >50K?
    rich_by_c = df.query('salary==">50K"').groupby('native-country').size()
    all_by_c = df.groupby('native-country').size()
    highest_earning_country = (rich_by_c / all_by_c).sort_values(ascending = False)
    highest_earning_country_percentage = as_percent(highest_earning_country[0])
    highest_earning_country = highest_earning_country.index[0]


    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation =  df.query('salary==">50K"').rename(columns={"native-country": "nativeCountry"}).query('nativeCountry == "India"')["occupation"].mode()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
