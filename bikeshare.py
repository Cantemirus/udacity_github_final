

### File name: bikeshare.py
### Author: Liviu Marian Albu
### Date created: 20/09/2024
### Date last modified: 25/09/2024
### Python Version: 3.11.4


import time
import pandas as pd
import numpy as np
import os  # Import os to handle directory paths

# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the city data dictionary with the absolute paths
CITY_DATA = {
    'chicago': os.path.join(current_dir, 'chicago.csv'),
    'new york': os.path.join(current_dir, 'new_york_city.csv'),
    'washington': os.path.join(current_dir, 'washington.csv')
}

# Cities, months, and days lists
cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """Asks user to specify a city, month, and day to analyze."""
    print("Hello! I will be your virtual assistant today. Let's explore some US bikeshare data, shall we?")

    # Get user input for city
    while True:
        city = input("Please tell me for which of the following cities you want to see data:\n Chicago, New York, or Washington\n").lower()
        if city in cities:
            break
        else:
            print('I do not have any info on that. Please enter a valid city.')

    # Get user input to filter by month, day, or none
    while True:
        choice = input("Would you like to filter the data by month, day, or none?\n").lower()
        if choice == 'month':
            month = input("Please enter the month you want to explore. If you do not want a month filter, enter 'all'. \nChoices: All, January, February, March, April, May, June\n").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Please enter a valid month.')
        elif choice == 'day':
            day = input("Please enter the day of the week you want to explore. If you do not want to apply a day filter, enter 'all'. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()
            month = 'all'
            if day in days:
                break
            else:
                print('Please enter a valid day.')
        elif choice == 'none':
            month = 'all'
            day = 'all'
            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()  # Use day_name() instead of weekday_name

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['month'].mode()[0]
    month_names = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Common Month:', month_names[popular_month - 1])

    # Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day of the Week:', popular_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    if popular_hour < 12:
        print('Most Common Start Hour:', popular_hour, 'AM')
    else:
        print('Most Common Start Hour:', (popular_hour - 12) if popular_hour > 12 else 12, 'PM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station:", popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station:", popular_end_station)

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print("Most Common Trip from Start to End:", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("Total Travel Time: {} Hours, {} Minutes, and {} Seconds.".format(hour, minute, second))

    # Display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(average_duration, 60)
    if minute > 60:
        hour, minute = divmod(minute, 60)
        print('Average Travel Time: {} Hours, {} Minutes, and {} Seconds.'.format(hour, minute, second))
    else:
        print('Average Trip Duration: {} Minutes and {} Seconds.'.format(minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of Each User Type:\n", user_types)

    # Display counts of gender if available
    try:
        gender = df['Gender'].value_counts()
        print("\nCounts of Each User Gender:\n", gender)
    except KeyError:
        print('Gender data is not available for {}'.format(city.title()))

    # Display earliest, most recent, and most common year of birth if available
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nEarliest Birth Year:", earliest)
        print("Most Recent Birth Year:", most_recent)
        print("Most Common Birth Year:", most_common)
    except KeyError:
        print('Birth year data is not available for {}'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_data(df):
    """Displays individual trip data upon request."""
    start_data = 0
    end_data = 5
    df_length = len(df.index)

    while start_data < df_length:
        raw_data = input("\nWould you like to see 5 rows of individual trip data? Enter 'yes' or 'no'.\n")
        if raw_data.lower() == 'yes':
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        print("You selected {}, {}, and {}.".format(city.title(), month.title(), day.title()))

        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\n")
        if restart.lower() != 'yes':
            print("\nThank you for your time! It was fun exploring the bikeshare data with you. Have a great day!\n")
            break

if __name__ == "__main__":
    main()