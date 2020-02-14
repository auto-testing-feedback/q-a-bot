import os, time, json, pprint, math
import piazza_api
import matcher

def update(bot, erase=False):
    piazza = piazza_api.Piazza()
    piazza.user_login(bot['login']['email'], bot['login']['password'])

    data_file = open(bot['link'].replace('.json', '') + '-data.json', 'r+') # get the data file
    data = json.loads(data_file.read())

    if erase:
        # erase question data
        data['questions'] = {}
        # erase folder data
        data['folders'] = {}
        # erase total data
        for key in data['total']:
            data['total'][key] = 0
        # erase nlp data
        data['df'] = {}
        data['idf'] = {}

    try:
        for term in bot['terms']:
            piazza_term = piazza.network(term) # get the piazza term
            term_stats = piazza_term.get_statistics()['total']

            # only update if there are new posts or responses--otherwise skip this course
            if term_stats['questions'] != data['total']['posts']:
                # pop the entries we don't care about
                for x in ['response_time', 'anon_pool', 'net_time']:
                    term_stats.pop(x)
                term_stats['posts'] = term_stats.pop('questions')
                term_stats['answers'] = term_stats.pop('i_answers') + term_stats.pop('s_answers')

                data['total'] = term_stats

                update_term_data(data, piazza_term)
            else:
                print('nothing to update for ' + term)
    except:
        traceback.print_exc()
        print("error writing to file--making no changes")
        data_file.close()

    data_file.seek(0) # erase the contents of the file
    data_file.truncate()
    json.dump(data, data_file, indent=4) # write new data to file

    # pass two, NLP data
    for question_id in data['questions']:
        question = data['questions'][question_id]
        for i in [question['content'], question['title']]:
            for word in i.split(' '):
                if len(word) < 2: # skip single character and empty strings
                    continue
                # update df for each word
                if word not in data['df']:
                    data['df'][word] = 0
                data['df'][word] += 1
        # update tf table
        question['tf'] = matcher.get_tf_table(question['content'])

    # calculate idf for each word in corpus
    unique_words = len(data['df'])
    for word in data['df']:
        data['idf'][word] = math.log(unique_words / (data['df'][word] + 1))

    # barf, check if there are any matching questions in the corpus
    keys = list(int(i) for i in data['questions'].keys())
    k1 = len(keys) - 1
    while k1 > 0:
        q1 = data['questions'][str(keys[k1])]
        q2 = data['questions'][str(keys[k1 - 1])]
        if matcher.questions_match(data['idf'], q1, q2):
            print('questions %d and %d match!' % (keys[k1], keys[k1 - 1]))
        k1 -= 1

    data_file.seek(0) # erase the contents of the file
    data_file.truncate()
    json.dump(data, data_file, indent=4) # write new data to file

def update_term_data(data, piazza_term):
    term_stats = piazza_term.get_statistics()

    current_id = 1
    if len(data['questions']) > 1: # if there is question data, start at the latest post
        int(data['question_ids'].keys()[-1])
    limit = term_stats['total']['questions']
    wait_time = 0.1
    timeout_wait_time = 30
    while current_id < limit:
        # keep trying to get post until we succeed
        success = False
        while not success:
            try:
                piazza_post = piazza_term.get_post(current_id)

                # if we get to this point we didn't time out, otherwise go to request error exception block
                success = True
                current_id += 1
                time.sleep(wait_time)

                # we only care about questions
                if piazza_post['type'] != 'question': break

                responses = get_piazza_responses(piazza_post)
                answered = False
                for response in responses: 
                    if response['is_answer']:
                        answered = True

                post = {
                    'id': piazza_post['nr'],
                    'folders': piazza_post['folders'],
                    'answered': answered,
                    'title': matcher.clean(piazza_post['history'][0]['subject']),
                    'content': matcher.clean(piazza_post['history'][0]['content']),
                    'responses': responses
                }

                data['questions'][str(post['id'])] = post

                # increment number of questions in each folder
                for folder in piazza_post['folders']:
                    if not folder in data['folders']:
                        data['folders'][folder] = 0
                    data['folders'][folder] += 1
            except piazza_api.exceptions.RequestError:
                # if we get a request error, wait and print to console
                print('too fast, waiting %d... ' % timeout_wait_time)
                for i in range(timeout_wait_time):
                    print(i + 1, end=' ', flush=True); time.sleep(1)
                # increment the timeout wait time for next time we get a request error
                print(); timeout_wait_time += 30

def get_piazza_responses(post):
    responses = []
    for child in post['children']:
        if child['type'] in ['i_answer', 's_answer']:
            response = {
                'content': matcher.clean(child['subject'] if 'history' not in child else child['history'][0]['content']),
                'is_answer': child['type'] == 'i_answer' or len(child['tag_endorse']) > 0 # not sure if students can change this
            }
            responses.append(response)
    return responses