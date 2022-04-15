import sys
# import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]
restart_sequence = "\nHuman: "

interviewers = {'Journalist': ['personal growth', 'career', 'career path', 'development', 'award', 'achievement', 'scandal', 'identity'],
                'Parent': ['family', 'friendship', 'kinship', 'love', 'growth', 'anger', 'education'],
                'Custom': []
                }

def selectInterviewer(interviewers):
    print('Please choose your interviewer\'s personality: ')
    personalities = list(interviewers.keys())
    for i in range(len(personalities)):
        print('\t', i, '--', personalities[i])

    interviewerSelectPrompt = "please type in the number you would like to choose: \n"

    personalityChoice = input(interviewerSelectPrompt)

    while int(personalityChoice) < 0 or int(personalityChoice) >= len(personalities):
        personalityChoice = input(interviewerSelectPrompt)
    
    if int(personalityChoice) == (len(interviewers) - 1):
        personality = input("please type in the name of your interviewer: \n")
        interest = ''
        interests = []
        while interest != 'exit':
            interest = input("please type in an interest of your interviewer (enter 'exit' to complete): \n")
            if len(interest) > 0 and interest != 'exit':
                interests.append(interest)
        return personality, interests

    return personalities[int(personalityChoice)], interviewers[personalities[int(personalityChoice)]]

def cleanResponse(response):
    r =''
    for c in response:
        if c != '\n':
            r = r + c
    return r


def startInterview(personality, interests):

    starterInfo = input("What is the most interesting thing about you?\n")
    print('\n')
    
    prompt = "The following is a conversation with a " + personality + ". The conversation is centered on "

    for i in range(len(interests)):
        if i != len(interests) - 1:
            prompt = prompt + interests[i] + ', '
        else:
            prompt = prompt + interests[i] + '. '

    # prompt = prompt + 'The ' + personality + ' leads the conversation. \n\nHuman: ' + starterInfo + '\n\n' + personality + ':'
    # prompt = prompt + 'The ' + personality + ' stir the conversation. \n\nHuman: ' + starterInfo + '\n\n' + personality + ':'
    prompt = prompt + '\n\nHuman: ' + starterInfo + '\n\n' + personality + ':'
    userResponse = ''
    
    i = 0
    while userResponse != 'exit' and i  < 10:
        # run through generator
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=1,
            max_tokens=100,
            top_p=1,
            frequency_penalty=2,
            presence_penalty=0.6,
            stop=["Human:"]
        )
        
        response = cleanResponse(response['choices'][0]['text'])
        userResponse = input('\n' + personality + ': ' + response + '\n\nYou (type \'exit\' to finish converstation): ')

        prompt = prompt + ' ' + response + '\nHuman: ' + userResponse + "\n\n" + personality + ':'
        i = i + 1
        
    return prompt



personality, interests = selectInterviewer(interviewers)

interviewScript = startInterview(personality, interests)

if len(sys.argv) > 1:
    print('save to' , './' ,sys.argv[1])
    f = open('./'  + sys.argv[1], 'w')
    f.write(interviewScript)
    f.close()


