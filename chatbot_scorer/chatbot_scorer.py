from termcolor import colored
import csv
import sys
import shutil

def print_blank_line():
    term_size = shutil.get_terminal_size()
    print(colored("_" * term_size.columns, "blue"), "\n")

def print_invalid_score_message():
    print(colored("ERROR: Please enter a number between 1 and 5, or q to quit", "red"))

def score_invalid(analysis_score):
    return not analysis_score.isnumeric() or (analysis_score.isnumeric() and (int(analysis_score) < 0 or int(analysis_score) > 5))

def write_row_to_csv(row, writer):
    writer.writerow(row)

def save_data(analysis_score, follow_up_score, row, writer):
    row.append(analysis_score)
    row.append(follow_up_score)
    write_row_to_csv(row, writer)

def check_quit(input, file):
    if input.lower() == "q":
        close_file(file)
        quit()

def check_validity(score):
    if score_invalid(score):
        print_invalid_score_message()

def score_row(row, writer, file):
    template = row[0]
    question = row[1]
    answer = row[2]
    analysis = row[3]
    follow_up_question = row[4]
    print(colored("Template: ", "green"), colored(template + "\n", "yellow"))
    print(colored("Question: ", "magenta"), colored(question + "\n", "cyan"))
    print(colored("Answer: ", "yellow"), colored(answer + "\n", "green"))

    # Analysis
    print(colored("Analysis: ", "cyan"), colored(analysis.split(":", 1)[1] + "\n", "magenta"))
    analysis_score = "Not set yet"
    while score_invalid(analysis_score):
        analysis_score = input(colored("Score this analysis (0-5): ", "red"))
        check_quit(analysis_score, file)
        check_validity(analysis_score)
    
    # Follow-Up Question
    print(colored("Follow-Up Question: ", "green"), colored(follow_up_question.split(":", 1)[1] + "\n", "cyan"))
    follow_up_score = "Not set yet"
    while score_invalid(follow_up_score):
        follow_up_score = input(colored("Score this follow-up-question (0-5): ", "red"))
        check_quit(follow_up_score, file)
        check_validity(follow_up_score)
    print_blank_line()
    save_data(analysis_score, follow_up_score, row, writer)

def score_rows(rows, writer, file):
    rows[0].append("Analysis Score")
    rows[0].append("Follow-Up Score")
    write_row_to_csv(rows[0], writer)
    # Row 1 is just the headers, so skip it.
    for row in rows[1:]:
        score_row(row, writer, file)

def get_csv_writer():
    file = open("scores.csv", "w")
    return csv.writer(file), file

def read_csv_file(csv_reader):
    rows = []
    for row in csv_reader:
        rows.append(row)
    return rows

def get_csv_reader(file_name):
    file = open(file_name)
    return csv.reader(file)

def close_file(file):
    file.close()

# Purpose: Scoring the chatbot using a specially formatted CSV with the exported data (generated from chatbot.py).
def run_scorer():
    print(colored("Welcome to the chatbot scorer! Type q to quit at any point.\n", "cyan", attrs=["bold"]))
    if len(sys.argv) > 1:
        # Alex: D:\\coding\\CS_673\\conversation_turns.csv
        file_name = str(sys.argv[1])
        csv_reader = get_csv_reader(file_name)
        rows = read_csv_file(csv_reader)
        writer, file = get_csv_writer()
        score_rows(rows, writer, file)
        close_file(file)
    else:
        print(colored("ERROR: Requires 1 CLI string argument (location of the CSV you want to open). Please try again.", "red"))
        quit()

run_scorer()