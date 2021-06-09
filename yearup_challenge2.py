import glob
import os
import json
import re
import csv
import pprint
from datetime import datetime

TWEET_LOG_DIR_NAME = 'data/yearup_challenge/'


# EXAMPLE METRICS FUNCTION
def get_weekday_metrics_for_all_tweets(tweet_data_list):
    weekday_metrics = {}

    for tweet_data in tweet_data_list:
        weekday = tweet_data['date_weekday']

        # Check to see if we've already added this weekday before, otherwise we'll need to initialize it
        if weekday in weekday_metrics: # this means we've already initialized this weekday, so we can just update it
            # += 1 is a short way to say add one to the previous number
            weekday_metrics[weekday] += 1
        else: #initialize metrics for the new weekday
            weekday_metrics[weekday] = 1

    return weekday_metrics


# EXAMPLE METRICS FUNCTION
def get_weekday_metrics_for_by_cve(tweet_data_list):
    weekday_metrics = {}

    # Note: well need to make a nested dictionary like this:
    #  weekday_metrics[cve][weekday]
    # or
    #  { "cve1": {"weekday1: 13, "weekday2": 24...} ,
    #    "cve2": {"weekday1: 54, "weekday2": 12...} ... }

    for tweet_data in tweet_data_list:
        cve = tweet_data['cve']
        weekday = tweet_data['date_weekday']

        # Check to see if we've already added this cve before, otherwise we'll need to initialize it
        if cve not in weekday_metrics: # this means we've haven't initialized this cve yet so we'll need to
            # initialize cve with an empty dictionary for the weekday metrics
            weekday_metrics[cve] = {}

        # Check to see if we've already added this weekday before, otherwise we'll need to initialize it
        if weekday in weekday_metrics[cve]: # this means we've already initialized this weekday, so we can just update it
            # += 1 is a short way to say add one to the previous number
            weekday_metrics[cve][weekday] += 1
        else: # initialize metrics for the new weekday
            weekday_metrics[cve][weekday] = 1

    return weekday_metrics


# EXAMPLE METRICS FUNCTION
def get_tweet_user_count(tweet_data_list):
    user_count_metrics = {}

    for tweet_data in tweet_data_list:
        username = tweet_data['user_screen_name']

        # Check to see if we've already added this weekday before, otherwise we'll need to initialize it
        if username in user_count_metrics: # this means we've already initialized this weekday, so we can just update it
            # += 1 is a short way to say add one to the previous number
            user_count_metrics[username] += 1
        else: #initialize metrics for the new weekday
            user_count_metrics[username] = 1

    return user_count_metrics


# TODO: Update print_tweet_data_metrics to include each of the requested challenge metrics
def print_tweet_data_metrics(tweet_data_list):

    # ----- EXAMPLES -------#

    # call your function that computes the metric (you'll need to write the function above)
    weekday_metrics = get_weekday_metrics_for_all_tweets(tweet_data_list)
    # print the metric name/headline
    print("DAY OF THE WEEK METRICS (total tweet count for each day")
    # print the metric file
    pretty_print(weekday_metrics)

    # call your function that computes the metric (you'll need to write the function above)
    weekday_metrics_per_tweet = get_weekday_metrics_for_by_cve(tweet_data_list)
    # print the metric name/headline
    print("DAY OF THE WEEK METRICS (count per tweet")
    # print the metric file
    pretty_print(weekday_metrics_per_tweet)

    # call your function that computes the metric (you'll need to write the function above)
    tweeter_count = get_tweet_user_count(tweet_data_list)
    # print the metric name/headline
    print("USER COUNT METRICS (number of tweets by user)")
    # print the metric file
    pretty_print(tweeter_count)

    # ----- END EXAMPLES -------#

    # TODO: insert your code to fill out the metrics report, use the examples above for inspiration


# TODO: remove tweets from the list that have cve set to '' (empty), because they didn't have a valid CVE
# see extract_data_from_tweet_json where cve was extracted from text for reference
def filter_tweet_data(tweet_data_list):
    filtered_list = []

    for tweet in tweet_data_list:
        tweet_cve = tweet['cve']
        # "append" tweet to filtered_list if tweet_cve is not equal to '' (blank)
        # TODO: add your code here to "append" ONLY valid _tweets_ to the filtered_list
        #       (be sure to append the full tweet, not tweet_cve)


    return filtered_list


# NO NEED TO EDIT BELOW THIS LINE, FEEL FREE TO MAKE CHANGES BUT BE CAREFUL
# Any "INFO" below this line marks areas where you can uncomment print statements for debugging (feel free to add your own)

def pretty_print(data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


def convert_weekday_num_to_string(weekday_num):
    weekday_string = ""
    if weekday_num == 0:
        weekday_string = 'Monday'
    elif  weekday_num == 1:
        weekday_string = 'Tuesday'
    elif weekday_num == 2:
        weekday_string = 'Wednesday'
    elif  weekday_num == 3:
        weekday_string = 'Thursday'
    elif weekday_num == 4:
        weekday_string = 'Friday'
    elif  weekday_num == 5:
        weekday_string = 'Saturday'
    elif weekday_num == 6:
        weekday_string = 'Sunday'
    return weekday_string


#   extract_data_from_tweet_json returns a dict (dictionary) object with the extracted values
#
#   EXAMPLE:
#
#  {  'cve': 'CVE-2020-16971',
#     'date': '2020/12/10',
#     'date_day': 10,
#     'date_month': 12,
#     'date_weekday': Wednesday,
#     'date_year': 2020,
#     'id': 1336872395802632203,
#     'text': 'One night, CVE-2020-16971 wished upon a star, and today that wish '
#             'has been granted. It now has a name, like a real,… '
#             'https://t.co/6MZm4ARBzg',
#     'user_followers_count': 953,
#     'user_friends_count': 0,
#     'user_screen_name': 'vulnonym',
#     'user_statuses_count': 18257
#  }
def extract_data_from_tweet_json(tweet_json):
    extracted_tweet_data = {}
    extracted_tweet_data['id'] = tweet_json['id']

    # Convert create_at string format to our desired format YEAR/MONTH/DAY
    # date_str = datetime.today().strftime('%Y-%m-%d')
    # "created_at": "Wed Oct 10 20:19:24 +0000 2018"
    created_at_datetime = datetime.strptime(tweet_json['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    created_at_date = created_at_datetime.date()
    date_str = datetime.strftime(created_at_datetime, '%Y/%m/%d')
    extracted_tweet_data['date'] = date_str
    extracted_tweet_data['date_year'] = created_at_date.year
    extracted_tweet_data['date_month'] = created_at_date.month
    extracted_tweet_data['date_day'] = created_at_date.day
    # Monday is 0 and Sunday is 6 - ref: https://docs.python.org/3/library/datetime.html
    extracted_tweet_data['date_weekday'] = convert_weekday_num_to_string(created_at_date.weekday())

    extracted_tweet_data['text'] = tweet_json['text']
    # extract first CVE from text (note: there may be multiple, but to simplify we'll only take the first)
    # ref: https://stackoverflow.com/questions/60178826/extracting-cve-info-with-a-python-3-regular-expression

    # CVE regular expression
    cve_pattern = r'CVE-\d{4}-\d{4,7}'

    # search for CVE references using RegEx
    cves = re.findall(cve_pattern, tweet_json['text'])
    # if no CVEs are found in the text then set it as '' or empty string
    # there are at least two cases where we may not have a CVE:
    #  1) the search function includes anything with "cve" so we need to filter tweets with 'cve' but not the full with year and cve id
    #  2) tweets are currently truncated, so long tweets that matched might not have the cve included in the truncated text
    if len(cves) > 0:
        first_cve = cves[0]
        extracted_tweet_data['cve'] = first_cve
    else:
        extracted_tweet_data['cve'] = ''

    extracted_tweet_data['user_screen_name'] = tweet_json['user']['screen_name']
    extracted_tweet_data['user_followers_count'] = tweet_json['user']['followers_count']
    extracted_tweet_data['user_friends_count'] = tweet_json['user']['friends_count']
    extracted_tweet_data['user_statuses_count'] = tweet_json['user']['statuses_count']

    return extracted_tweet_data


# process_tweet_log_file will process a single tweet log file and
#     return a list of dicts in the format that's returned by extract_data_from_tweet_json
# see notes above extract_data_from_tweet_json for an example of the tweet data format
def process_tweet_log_file(tweet_filepath):
    processed_tweet_data = []
    tweet_log_file = open(tweet_filepath, 'r')
    # Note: tweets are stored in the log as one line per tweet, so this for loop will let us process
    #       each tweet one by one by processing each line of the file
    for tweet_line in tweet_log_file.readlines():
        tweet_json = json.loads(tweet_line)
        extracted_tweet_data = extract_data_from_tweet_json(tweet_json)
        processed_tweet_data.append(extracted_tweet_data)
        # INFO: uncomment below if you want to see the original tweets that were processed (good for debugging)
        # pretty_print(extracted_tweet_data)
    tweet_log_file.close()
    return processed_tweet_data


# process_tweet_log_files will process a list of tweet log files
#    and filter out tweet data that doesn't contain a valid CVE
def process_tweet_log_files(list_of_tweet_log_paths):
    clean_and_processed_tweet_data = []

    for tweet_log_file_path in list_of_tweet_log_paths:
        processed_tweet_data = process_tweet_log_file(tweet_log_file_path)
        filtered_tweet_data = filter_tweet_data(processed_tweet_data)
        # INFO: uncomment below if you want to see the filtered tweets that were processed (good for debugging)
        # for tweet_data in filtered_tweet_data:
        #     pretty_print(tweet_data)
        # INFO: uncomment below if you want to see the size difference between the original and filtered lists (good for debugging)
        # print("{file}: size of original tweet data: {size}".format(file=tweet_log_file_path, size=len(processed_tweet_data)))
        # print("{file}: size of filtered tweet data: {size}".format(file=tweet_log_file_path, size=len(filtered_tweet_data)))
        clean_and_processed_tweet_data.extend(filtered_tweet_data)
    return clean_and_processed_tweet_data


def save_filtered_tweets_to_csv(tweet_data_list):
    # get header (column names) - using the keys of the first in the list as an example
    column_names = tweet_data_list[0].keys()

    with open("twitter_data.csv", 'w', encoding='utf-8') as csv_output_file:
        csv_writer = csv.DictWriter(csv_output_file, fieldnames=column_names, quoting=csv.QUOTE_NONNUMERIC)

        # write header
        csv_writer.writeheader()

        # write tweet data as rows
        for tweet_data in tweet_data_list:
            # remove newlines from tweet text, replace double quotes with single quotes
            tweet_data['text'] = tweet_data['text'].replace('\n', ' ').replace('"', '\'')
            csv_writer.writerow(tweet_data)


def main():
    tweet_logs_path = os.path.join(TWEET_LOG_DIR_NAME, '*.log')
    list_of_tweet_log_paths = glob.glob(tweet_logs_path)

    # process all tweet logs in tweet log directory
    tweet_data_list = process_tweet_log_files(list_of_tweet_log_paths)
    print_tweet_data_metrics(tweet_data_list)

    # for extra SQL challenge, feel free to comment this out if you don't need the CSV file
    save_filtered_tweets_to_csv(tweet_data_list)

if __name__ == '__main__':
    main()
