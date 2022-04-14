from termcolor import colored
import csv
import sys
import shutil

def print_blank_line():
    term_size = shutil.get_terminal_size()
    print(colored("_" * term_size.columns, "blue"), "\n")

def print_new_line():
    print("\n")

def print_invalid_score_message():
    print(colored("ERROR: Please enter a number between 0 and 5, or q to quit", "red"))

def score_invalid(analysis_score):
    return not analysis_score.isnumeric() or (analysis_score.isnumeric() and (int(analysis_score) < 0 or int(analysis_score) > 5))

def write_row_to_csv(row, writer):
    writer.writerow(row)

def save_data(analysis_score_novelty, analysis_score_relevance, analysis_score_understanding, 
        analysis_score_thought_provocation, follow_up_score_novelty, follow_up_score_relevance, 
        follow_up_score_understanding, follow_up_score_thought_provocation, row, writer):
    row.append(analysis_score_novelty)
    row.append(analysis_score_relevance)
    row.append(analysis_score_understanding)
    row.append(analysis_score_thought_provocation)
    row.append(follow_up_score_novelty)
    row.append(follow_up_score_relevance)
    row.append(follow_up_score_understanding)
    row.append(follow_up_score_thought_provocation)
    write_row_to_csv(row, writer)

def check_quit(input, file):
    if input.lower() == "q":
        close_file(file)
        quit()

def check_validity(score):
    if score_invalid(score):
        print_invalid_score_message()

def score_section(file, prompt, color="red"):
    score = "Not set yet"
    while score_invalid(score):
        score = input(colored(prompt, color))
        check_quit(score, file)
        check_validity(score)
    return score

def score_analysis_novelty(file):
    return score_section(file, "Score this analysis along the dimension of NOVELTY (0-5): ")

def score_analysis_relevance(file):
    return score_section(file, "Score this analysis along the dimension of RELEVANCE (0-5): ", "cyan")

def score_analysis_understanding(file):
    return score_section(file, "Score this analysis along the dimension of UNDERSTANDING (0-5): ")

def score_analysis_thought_provocation(file):
    return score_section(file, "Score this analysis along the dimension of THOUGHT-PROVOCATION (0-5): ", "cyan")

def score_follow_up_novelty(file):
    return score_section(file, "Score this follow-up question along the dimension of NOVELTY (0-5): ")

def score_follow_up_relevance(file):
    return score_section(file, "Score this follow-up question along the dimension of RELEVANCE (0-5): ", "cyan")

def score_follow_up_understanding(file):
    return score_section(file, "Score this follow-up question along the dimension of UNDERSTANDING (0-5): ")

def score_follow_up_thought_provocation(file):
    return score_section(file, "Score this follow-up question along the dimension of THOUGHT-PROVOCATION (0-5): ", "cyan")

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
    analysis_score_novelty = score_analysis_novelty(file)
    analysis_score_relevance = score_analysis_relevance(file)
    analysis_score_understanding = score_analysis_understanding(file)
    analysis_score_thought_provocation = score_analysis_thought_provocation(file)
    print_new_line()
    
    # Follow-Up Question
    print(colored("Follow-Up Question: ", "green"), colored(follow_up_question.split(":", 1)[1] + "\n", "cyan"))
    follow_up_score_novelty = score_follow_up_novelty(file)
    follow_up_score_relevance = score_follow_up_relevance(file)
    follow_up_score_understanding = score_follow_up_understanding(file)
    follow_up_score_thought_provocation = score_follow_up_thought_provocation(file)
    
    # Post-Process
    print_blank_line()
    save_data(analysis_score_novelty, analysis_score_relevance, analysis_score_understanding, 
        analysis_score_thought_provocation, follow_up_score_novelty, follow_up_score_relevance, 
        follow_up_score_understanding, follow_up_score_thought_provocation, row, writer)

# Append the sub-category scores for analyses and follow-up scores as part of the title row in the CSV.
def append_sub_category_scores(rows):
    rows[0].append("Analysis Score: Novelty")
    rows[0].append("Analysis Score: Relevance")
    rows[0].append("Analysis Score: Understanding")
    rows[0].append("Analysis Score: Thought-Provocation")
    rows[0].append("Follow-Up Score: Novelty")
    rows[0].append("Follow-Up Score: Relevance")
    rows[0].append("Follow-Up Score: Understanding")
    rows[0].append("Follow-Up Score: Thought-Provocation")
    return rows

def score_rows(rows, writer, file):
    rows = append_sub_category_scores(rows)
    write_row_to_csv(rows[0], writer)
    # Row 1 is just the headers, so skip it.
    for row in rows[1:]:
        score_row(row, writer, file)

def get_csv_writer():
    file = open("scores.csv", "w", newline="")
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

def print_cli_error():
    print(colored("ERROR: Requires 1 CLI string argument (location of the CSV you want to open). Please try again.", "red"))

# Purpose: Scoring the chatbot using a specially formatted CSV with the exported data (generated from chatbot.py).
def run_scorer():
    print(colored("Welcome to the chatbot scorer! Type q to quit at any point.\n", "cyan", attrs=["bold"]))
    if len(sys.argv) > 1:
        # Example CLI input:
        # python chatbot_scorer.py D:\\coding\\CS_673\\conversation_turns.csv
        file_name = str(sys.argv[1])
        csv_reader = get_csv_reader(file_name)
        rows = read_csv_file(csv_reader)
        writer, file = get_csv_writer()
        score_rows(rows, writer, file)
        # Cleanup
        close_file(file)
    else:
        print_cli_error()
        quit()

run_scorer()