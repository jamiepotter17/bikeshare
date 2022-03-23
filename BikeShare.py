import PySimpleGUI as sg
import pandas as pd

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (list[int]) months - list of months to filter by, 1 = Jan, ... 6 = Jul.
        (list[int]) days - list of days to filter by, 0 = Mon, etc.
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    ## Dictionary for loading the correct data
    city_file_dict = {
        'Chicago': 'chicago.csv',
        'New York': 'new_york_city.csv',
        'Washington': 'washington.csv'}

    # load data file into a dataframe
    df = pd.read_csv(city_file_dict[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # filter by month to create the new dataframe
    df = df[df['Start Time'].dt.month.isin(month)]

    # filter by day of week if applicable
    df = df[df['Start Time'].dt.dayofweek.isin(day)]

    return df

def getfilters():
    """
    Uses PySimpleGUI interface to get filters from user and return this info.
    Args:
        -
    Returns:
        (tuple) with elements:
            (str) city - name of the city to analyze
            (list[int]) months - list of months to filter by, 1 = Jan, ... 6 = Jul.
            (list[int]) days - list of days to filter by, 0 = Mon, etc.
    """
    ## Creates layout for select data and filters menu
    select_data_layout = [
        [sg.Text("Select the location for which you'd like information:", pad=(0,10))],
        [sg.Combo(["Chicago", "New York", "Washington"], size=(40,50), key='-CITY-',
        default_value="Chicago")],
        [sg.Text("Select the months for which you'd like information:", pad=(0,10))],
        [sg.Checkbox('January', key='Jan', default=True, size = (10,2)),
        sg.Checkbox('February', key='Feb', default=True, size = (10,2)),
        sg.Checkbox('March', key='Mar', default=True, size = (10,2))],
        [sg.Checkbox('April', key='Apr', default=True, size = (10,2)),
        sg.Checkbox('May', key='May', default=True, size = (10,2)),
        sg.Checkbox('June', key='Jun', default=True, size = (10,2))],
        [sg.Text("Select the days for which you'd like information:", pad=(0,10))],
        [sg.Checkbox('Monday', key='Mon', default=True, size = (10,2)),
        sg.Checkbox('Tuesday', key='Tue', default=True, size = (10,2)),
        sg.Checkbox('Wednesday', key='Wed', default=True, size = (10,2))],
        [sg.Checkbox('Thursday', key='Thu', default=True, size = (10,2)),
        sg.Checkbox('Friday', key='Fri', default=True, size = (10,2))],
        [sg.Checkbox('Saturday', key='Sat', default=True, size = (10,2)),
        sg.Checkbox('Sunday', key='Sun', default=True, size = (10,2))],
        [sg.Text("Select any information packages you require:", pad=(0,10))],
        [sg.Checkbox('Times', key='Times', default=True, size = (10,2)),
        sg.Checkbox('Stations', key='Stations', default=True, size = (10,2))],
        [sg.Checkbox('Trips', key='Trips', default=True, size = (10,2)),
        sg.Checkbox('Users', key='Users', default=True, size = (10,2))],
        [sg.Button('OK', pad=([120,10],10), size=(10,2)),
        sg.Button('Exit', pad=([10,120],10), size=(10,2))]]

    ## Read from select_data_window for filters the user wants.
    select_data_window = sg.Window('Select Data', select_data_layout)

    # Loop that keeps you in the window until a button is pressed:
    while True:
        event, values = select_data_window.read(close=True)
        if event in (None, 'Exit'):
            exit()
            break
        if event == "OK":

            # Produce a list of months required from values taken from user menu.
            months_req = []
            if values['Jan']:
                months_req.append(1)
            if values['Feb']:
                months_req.append(2)
            if values['Mar']:
                months_req.append(3)
            if values['Apr']:
                months_req.append(4)
            if values['May']:
                months_req.append(5)
            if values['Jun']:
                months_req.append(6)

            # Produce a list of days required from values taken from user menu.
            days_req = []
            if values['Mon']:
                days_req.append(0)
            if values['Tue']:
                days_req.append(1)
            if values['Wed']:
                days_req.append(2)
            if values['Thu']:
                days_req.append(3)
            if values['Fri']:
                days_req.append(4)
            if values['Sat']:
                days_req.append(5)
            if values['Sun']:
                days_req.append(6)

            info_req = []
            if values['Times']:
                info_req.append('Times')
            if values['Stations']:
                info_req.append('Stations')
            if values['Trips']:
                info_req.append('Trips')
            if values['Users']:
                info_req.append('Users')

            break

    return values['-CITY-'], months_req, days_req, info_req

def times(filt_df):
    """
    Takes input of pd dataframe and calculates times descriptive stats.
    Args:
        (pd.dataframe) filt_df
    Returns:
        (str) output - string output from the information package.
    """

    # Uses list of Months (up to July) to return modal month as a string.
    monlist = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    mon = monlist[int(filt_df['Start Time'].dt.month.mode().values) - 1]

    # Uses list of days to return modal dayofweek as a string.
    daylist = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
    'Saturday', 'Sunday']
    day = daylist[int(filt_df['Start Time'].dt.dayofweek.mode().values)]

    # Finds modal hour
    hour = filt_df['Start Time'].dt.hour.mode().values

    # Puts everything together as a string
    output = (
        'Times Information:\n\n'
        +'The most common month of travel is {}.\n'
        +'The most common day of the week of travel is {}.\n'
        +'The most common hour of the day to travel is {:02d}:00.\n\n'
        ).format(mon, day, hour[0])

    return output

def stations(filt_df):
    """
    Takes input of pd dataframe and calculates stations descriptive stats.
    Args:
        (pd.dataframe) filt_df
    Returns:
        (str) output - string output from the information package.
    """

    # Creates a pandas series, df_start, of counts of Start Station
    df_start = filt_df.groupby(['Start Station'])['Start Time'].count()

    # Creates a pandas series, df_end, of counts of End Station
    df_end = filt_df.groupby(['End Station'])['Start Time'].count()

    # Creates a pandas series, df_startemd, of counts of combinations of
    # start and end stations
    df_startend = filt_df.groupby(
    ['Start Station', 'End Station'])['Start Time'].count()

    # Returns a string with all the relevant information for the info package.
    output = (
        'Stations Information:\n\n'
        +'The most common start station is {}, which was used {} times.\n'
        +'The most common end station is {}, which was used {} times.\n'
        +'The most common trip is {} to {}, which occurred {} times.\n\n'
        ).format(df_start.idxmax(), df_start.max(), df_end.idxmax(),
        df_end.max(), df_startend.idxmax()[0], df_startend.idxmax()[1],
        df_startend.max())

    return output

def trips(filt_df):
    """
    Takes input of pd dataframe and calculates trips descriptive stats.
    Args:
        (pd.dataframe) filt_df
    Returns:
        (str) output - string output from the information package.
    """
    # Gets the total trip duration in seconds from the dataframe:
    total = filt_df['Trip Duration'].sum()

    # Lots of horrendous remainder calculations to convert trip duration from
    # the dataframe into a digestible string. Could have used
    # datetime.timedelta() here instead.
    tyears = total // 31557600
    tdays = (total % 31557600) // 86400
    thours = ((total % 31557600) % 86400) // 3600

    # Gets the average trip duration in seconds from the dataframe by using
    # a count of the number of unique trips (counting the first column as it's
    # an implicit ID for each trip.)
    average = total/filt_df.iloc[:,0].nunique()

    # Again with the remainder calculations.
    aminutes = average // 60
    aseconds = average % 60

    # Produces a string with all the information in it.
    output = (
        'Trips Information:\n\n'
        +'The total travel time is {} years, {} days, and {:02d} hours.\n'
        +'The average travel time is {:02d} minutes and {:02d} seconds.\n\n'
        ).format(int(tyears), int(tdays), int(thours),
        int(aminutes), int(aseconds))

    return output

def users(filt_df, is_washington):
    """
    Takes input of pd dataframe and calculates users descriptive stats.
    Args:
        (pd.dataframe) filt_df
    Returns:
        (str) output - string output from the information package.
    """
    output = "User Information:\n\n"

    # Create pandas series giving counts of user types
    df_user_types = filt_df.groupby(['User Type'])['Start Time'].count()

    # Iterates on user types to create string with user type counts included.
    for user in df_user_types.index:
        output += ('The number of {}s is {}.\n'.format
        (str(user).lower(), str(df_user_types[user]).lower()))

    # Since Washington does not have gender or birth count, we use if statement:
    if not is_washington:

        output +='\n'

        # Creates a pandas series giving counts of user sex:
        df_sex = filt_df.groupby(['Gender'])['Start Time'].count()

        # Iterates on user sex to update output string for the counts.
        for user in df_sex.index:
            output += ('The number of {} users is {}.\n'.format
            (str(user).lower(), str(df_sex[user]).lower()))

        # Finds the earliest, latest and modal birth year of users:
        earliest = int(min(filt_df['Birth Year']))
        latest = int(max(filt_df['Birth Year']))
        mode_birth_year = int(filt_df['Birth Year'].mode())

        # Updates string output with info on birth year.
        output += ('\n'
            +'The earliest user birth year is {}.\n'
            +'The most recent user birth year is {}.\n'
            +'The most common user birth year is {}.\n'
            ).format(earliest, latest, mode_birth_year)

    return output

def showinfo(info, df):

    """
    Args:
        (str) info is a long string with the output from the Information
        packages.
        (pd.dataframe) df is the database in case we need to send it to be
        itemised.
    Returns:
        -
    """
    # Creating a PySimpeGUI window to display string output.
    show_info_layout = [
    [sg.Multiline('{}'.format(info), key='OutputBox', size = (60,25))],
    [sg.Text("To see an itemised list of journeys, in order of their start time"
    +", select \'Itemise\'.")],
    [sg.Button('Itemise', pad=([170,10],10), size=(10,2)),
    sg.Button('Exit', pad=([10,170],10), size=(10,2))]
    ]
    show_info_window = sg.Window('Information Requests', show_info_layout)

    # Loop that keeps you in the window until a button is pressed:
    while True:
        event, values = show_info_window.read(close=True)
        if event in (None, 'Exit'):
            #exit()
            break
        if event == "Itemise":
            itemise(df)

    return

def itemise(df):
    """
    Shows PySimpleGUI table with dataframe displayed five lines at a time.
    Drops the first column and sorts by 'Start Date'.

    Args:
        (pd.dataframe)
    Returns:
        -
    """
    # Preparing the dataframe for displaying in a table
    table_df = df.drop(df.columns[0], axis = 1)
    head_list = list(table_df.columns)
    table_df = table_df.sort_values(by=['Start Time'])
    data = table_df.iloc[1:6].values.tolist()

    ## Window for showing table of values
    table_layout = [
        [sg.Table(headings = head_list, values = data,
        auto_size_columns=True, key='table')],
        [sg.Text('To see the next 5 items, select \'Next 5\' or press Enter.')],
        [sg.Button('Next 5', pad=([400,0],[10,10]),bind_return_key=True, size=(10,2)),
        sg.Button('Exit', pad=([10,400],[10,10]), size=(10,2))],
        ]
    table_window = sg.Window('Table', table_layout)

    # Iterator that shows next five lines of spreadsheet
    for i in five_line_it(table_df):
        events, values = table_window.read()
        if events in [None, 'Exit']:
            exit()
            break
        elif events == 'Next 5':
            data = i.values.tolist()
            table_window['table'].Update(values=data)
            continue

    return

def five_line_it (df):
    """Generator yields next 5 lines of dataframe each time it's called.
    Args:
        (pd.dataframe) df - pandas dataframe
    Returns:
        (pd.dataframe) df slice, next five rows.
    """
    for i in range(6, len(df), 5):
        yield df[i:i+5]

def main():
    # Set overall theme for PySimpleGUI
    sg.theme('SystemDefault')
    sg.SetOptions(font = ('Cambria', 12))

    # Get filters and information packages required:
    fcity, fmonth, fday, info_req = getfilters()

    # Checks month and day are non-empty.
    if fmonth == []:
        sg.popup('No months were selected. Exiting...')
        return
    if fday == []:
        sg.popup('No days were selected. Exiting...')
        return

    # Load the data and apply filter:
    filt_df = load_data(fcity, fmonth, fday)

    # Gets string of info from the appropriate information packages.
    # Note that you can proceed without selecting any information packages.
    output_str = ""
    if 'Times' in info_req:
        output_str += times(filt_df)
    if 'Stations' in info_req:
        output_str += stations(filt_df)
    if 'Trips' in info_req:
        output_str += trips(filt_df)
    if 'Users' in info_req:
        output_str += users(filt_df, fcity == 'Washington')
    else:
        output_str += 'No information packages were selected.\n'

    # Show information (with option to then show itemised list)
    showinfo(output_str, filt_df)

    return

main()
