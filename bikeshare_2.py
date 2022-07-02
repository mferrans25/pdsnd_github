import time
import pandas as pd
import tabulate as tb

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

WEEKDAY_DATA = ('monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
                )


MONTH_DATA = ('january',
              'february',
              'march',
              'april',
              'may',
              'june',
              'july',
              'august',
              'september',
              'october',
              'november',
              'december'
              )

'''Function that returns a valid input by validating inputs against a tuple of 
allowed values. A default value can be set if a user tries enters nothing or
tries to break out of the code'''
def get_valid_input(input_name, validation_tuple, default_value=''):
    while True:
        try:
            input_string = str(input ("Enter a {}: ".format(input_name))).lower()
            if input_string in validation_tuple:
                return input_string
            elif input_string == '':
                print("Using default value of {}".format(
                    default_value))
                return default_value
            else:
                print("Invalid {}, valid inputs are:\n{}".format(
                    input_name, "\n".join(validation_tuple)))
        except (EOFError, KeyboardInterrupt):
            print("Keyboard interrupt detected, using default value of {}".format(
                default_value))
            return default_value
        except:
           print("Invalid {}, valid inputs are:\n{}".format(
               input_name, "\n".join(validation_tuple)))
         

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    city = get_valid_input('city', valid_cities, default_value='chicago')
    # get user input for month (all, january, february, ... , june)
    valid_months = MONTH_DATA + ('all',)
    month = get_valid_input('month', valid_months, default_value='all')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = WEEKDAY_DATA + ('all',)
    day = get_valid_input('day', valid_days, default_value='all')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # Convert data to appropriate data types
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='seconds')
    if month != 'all':
        print("Filtering to events in {}".format(month))
        df = df[df['Start Time'].dt.month == MONTH_DATA.index(month) + 1]
    if day != 'all':
        print("Filtering to events on {}".format(day))
        df = df[df['Start Time'].dt.weekday == WEEKDAY_DATA.index(day)]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: {}".format(
        MONTH_DATA[df['Start Time'].dt.month.mode()[0] - 1].title()))

    # display the most common day of week
    print("Most common day of the week: {}".format(
        WEEKDAY_DATA[df['Start Time'].dt.weekday.mode()[0]].title()))

    # display the most common start hour
    print("Most common start hour: {}:00".format(
        df['Start Time'].dt.hour.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common starting station: {}".format(
        df['Start Station'].mode()[0]))
    # display most commonly used end station
    print("Most common end station: {}".format(
        df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    trip_series = df['Start Station'] + ' to ' + df['End Station']
    print("Most common trip: {}".format(
        trip_series.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel time: {}".format(
        df['Trip Duration'].sum()))

    # display mean travel time
    print("Mean Travel time: {}".format(
        df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Types: \n")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if ('Gender' in df.columns):
        print("Gender Counts: \n")
        print(df['Gender'].value_counts())
    else:
        print("Gender information not available in this data set")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Youngest Customer Birth Year: {}\n".format(
            int(df['Birth Year'].min())))
        print("Oldest Customer Birth Year: {}\n".format(
            int(df['Birth Year'].max())))
        print("Most common customer birth year: {}\n".format(
            int(df['Birth Year'].mode()[0])))
    else:
        print("Birth Information not available in this data set")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

'''Function for displaying the data frame results individually. Uses the 
   tabulate library to stylize the outputs.'''
def view_dataframe(df):
    try:
        response = input("Would you like to view the tabular data? (y/n): ")
    except:
        return
    if response.lower() == 'y':
        print(tb.tabulate(df.head(5), headers = 'keys', tablefmt = 'psql'))
        table_index = 6
        while True:
            try:
                response = input("Would you like to view additional rows? (y/n): ")
            except EOFError:
                break
            if response.lower() == 'y':
                print(tb.tabulate(df.iloc[table_index:table_index + 5], headers = 'keys', tablefmt = 'psql'))
                table_index += 5
                if table_index + 5 > len(df.index):
                    break;
            else:
                break

'''The main program function'''
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if len(df) != 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            view_dataframe(df)
        else:
            print("No data found with your search criteria")
        try:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except:
            break


if __name__ == "__main__":
	main()
