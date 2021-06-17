import re
import nltk
import math
import os 
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

TAGS_OF_INTEREST = ['a ',' a '] # memory or speed? shoud you use this or TAG_TO_PARAM.keys()?
TAG_TO_PARAM = {'a ':'href',' a ':'href'}
stop_words = set(nltk.corpus.stopwords.words('english'))
file_list = []

def file_to_string(file):
    # path = str(os.getcwd())
    # file = path + '\\searchengine\\templates\\searchengine\\Jan\\aol.html'
    # file = path
    f = open(file)
    s = f.read()
    f.close()
    # print(s)
    return s.lower() #moved lower here

def extract_params_from_tag(tag_w_params,tag):

    param_to_find = TAG_TO_PARAM[tag] #stores attribute we are looking for.. 'href'
    index = tag_w_params.find(param_to_find) #stores index location of attribute in tag
    left_quotation_mark = tag_w_params.find('"',index+len(param_to_find)) #looks for open quote next to href index location
    right_quotation_mark = tag_w_params.find('"',left_quotation_mark+1) #looks for closing quote index location

    if left_quotation_mark == -1 or right_quotation_mark == -1:
        print('\nERROR: There was an error while extracting the parameters of a tag.')
        print('tag:',tag,'\nfn input:',tag_w_params)
    
    
    return tag_w_params[left_quotation_mark+1:right_quotation_mark]



def process_left_tag(s,i,j): #checks if is tag of interest
    # print('count = ',count)
    tag_w_params = s[i+1:j] #stores string of opening tag minus the open carot
    offending_formats = ''
    
    for k,v in TAG_TO_PARAM.items():
        if v in tag_w_params:
          return extract_params_from_tag(tag_w_params,k) #initiates a param check on the tag
        else: 
          return ''


def parser(file):

    file_as_string = file_to_string(file) #get character data
    processed_text="" #initiate corpus variable
    
    #this is the first existing tag check 
    left_opening_tag_index = file_as_string.find('<',0) #locate first open carot index of opening tag
    left_closing_tag_index = file_as_string.find('>',left_opening_tag_index) #find closing carot index of opening tag
    if left_opening_tag_index == -1: #????
        pass # file is empty
    count = 0
    while True: #loop for extracting text from the document
        #this is the next tag, not closing tag ... threw me off
        right_opening_tag_index = file_as_string.find('<',left_closing_tag_index) #finds the open carot index for the next tag 
        right_closing_tag_index = file_as_string.find('>',right_opening_tag_index) #find closing carot index of next tag 

        if right_opening_tag_index == -1: #check if done
            break # file parsed completely
        

        close_tag_check = file_as_string[left_opening_tag_index+1:left_opening_tag_index+2]
        if close_tag_check != "/":
          processed_text += process_left_tag(file_as_string, left_opening_tag_index, left_closing_tag_index) + ' ' #processing all opening tags
          # count= count + 1
        else:
          pass
        

        processed_text += file_as_string[left_closing_tag_index+1:right_opening_tag_index] #adds all text between open and close tag to corpus

        left_opening_tag_index = right_opening_tag_index #sets preceding tag's open carot index to current tag index
        left_closing_tag_index = right_closing_tag_index #sets preceding tag's close carot index to current tag index

    #removes both symbols and digits. output result is the same
    processed_text = re.sub(r'([^a-zA-Z\s]+?)', ' ', processed_text)


    wordnet_lemmatizer = WordNetLemmatizer()

    ####Generates a dictionary of index locations/count WITHOUT stopwords
    hash_map = {}
    inverted_index = {}
    max_freq = 0

    for i, doc in enumerate(processed_text.split()):
      for term in doc.split():
        if term not in stop_words:
          lemma = wordnet_lemmatizer.lemmatize(term)
          if lemma in inverted_index:
            inverted_index[lemma].add(i)
            if len(inverted_index[lemma]) > max_freq:
              max_freq = len(inverted_index[lemma])
            else:
              pass
          else: inverted_index[lemma] = {i}
        else:
          pass
    doc_length = len(processed_text.split())
    hash_map['length'] = doc_length
    hash_map['max_frequency'] = max_freq
    hash_map['data'] = inverted_index


    # ####Generates a dictionary of index locations/count WITH stopwords
    # hash_map = {}
    # inverted_index = {}
    # max_freq = 0

    # for i, doc in enumerate(processed_text.split()):
    #   for term in doc.split():
    #     if term in inverted_index:
    #       inverted_index[term].add(i)
    #       if len(inverted_index[term]) > max_freq:
    #         max_freq = len(inverted_index[term])
    #       else:
    #         pass
    #     else: inverted_index[term] = {i}

    # doc_length = len(processed_text.split())
    # hash_map['length'] = doc_length
    # hash_map['max_frequency'] = max_freq
    # hash_map['data'] = inverted_index
    #### END dict WITH STOPWORDS ###


    return hash_map

def create_file_list(): #function to generate list of files
    path = str(os.getcwd()) + '\\searchengine\\templates\\searchengine\\Jan\\'
    #Creating a list 'html_files' to use as index values
    print(path)
    html_files = []
    for root, dirs, files in os.walk(path):
        print('in loop')
        for file in files:
            if file.endswith('.html'):
                use = path + file
                html_files.append(use)
                # html_files.append('\\searchengine\\templates\\searchengine\\Jan\\'+file)
    return html_files

def create_document_list_hash_map(): #indexes the parsed data with the associated file.
    document_list = {}
    global file_list
    
    file_list = create_file_list()
    for document in file_list:
        data = parser(document) 
        document_list[document] = data
        # print(document,':',document_list[document])
    return document_list

dl_hash = create_document_list_hash_map()

def compute_tf_idf(inverted_index):
  global dl_hash
  global file_list

  for k,v in inverted_index.items():
    for pk,p in v['posting_list'].items():
      tf = p['tf']
      mf = dl_hash[pk]['max_frequency']
      N = len(file_list)
      df = v['df']

      p['tf-idf'] = (tf/mf) * math.log2(N/df)

def create_inverted_index():
    global file_list
    index=[]
    inverted_index = {}
    count = 0
    for file in file_list:
      doc = count+1
      for k,v in dl_hash[file]['data'].items():

        if k not in index:
          index.append(k)
          inverted_index[k] = {'index':len(index)-1}
          inverted_index[k]['df'] = 1
          inverted_index[k]['posting_list'] = {file: {'tf':len(v),'tf-idf':0.0, 'locations':v }}
          
        else:
          inverted_index[k]['df'] += 1
          inverted_index[k]['posting_list'][file] = {'tf':len(v),'tf-idf':0.0, 'locations':v }

          pass

    compute_tf_idf(inverted_index)

    return inverted_index

ii_hashmap = create_inverted_index()
# print(ii_hashmap)

def compute_doc_vector_length():
  global ii_hashmap
  global dl_hash
  doc_vectors = {}
  for k,v in dl_hash.items():
    tfidf_store = set()
    for i in v['data']:
      tfidf = ii_hashmap[i]['posting_list'][k]['tf-idf']
      tfidf_store.add(tfidf)
    dvl = 0.0
    for ti in tfidf_store:
      dvl = dvl + (ti*ti)
    doc_vectors[k] = dvl
  
  return doc_vectors

dv = compute_doc_vector_length()


def compute_cosine_similarity(q):
  global dv
  global ii_hashmap
  global dl_hash
  query_hash_map = {}
  docs = set()
  doc_list = []
  for word in q:
    if word in ii_hashmap:   
      for i in ii_hashmap[word]['posting_list']:

        if i not in doc_list:
          doc_list.append(i)
          query_hash_map[i] = {word: set({ii_hashmap[word]['posting_list'][i]['tf-idf']})}
        else:
          query_hash_map[i] = {word: set({ii_hashmap[word]['posting_list'][i]['tf-idf']})}
          pass
  for d in doc_list:
    for word in q:
      if word in dl_hash[d]['data']:
        loc = ii_hashmap[word]['posting_list'][d]['locations']
        ti = ii_hashmap[word]['posting_list'][d]['tf-idf']

        query_hash_map[d][word] = {'location':loc}
        query_hash_map[d][word]['tf-idf'] = ti

  cos_tups = []
  for k,v in query_hash_map.items():
    sum_of_tfi_sqrd = 0.0

    for j,b in v.items():

      sum_of_tfi_sqrd += (b['tf-idf']**2)

    dvl = dv[k]
    ql = len(q)
    cossim = (1/math.sqrt(dvl))*(1/math.sqrt(ql))*sum_of_tfi_sqrd

    cos_tups.append((k,cossim,))

  ####ADDING PROXIMITY CHECK####

  wordnet_lemmatizer = WordNetLemmatizer()
  tokens = list( map( wordnet_lemmatizer.lemmatize, q ) )
  list_of_IDsets = list(map(map_keyword,tokens))
  docIDs = intersect_all(list_of_IDsets)

  docs_containing_phrase =[]
  for doc in docIDs:
    current_token_locs = list(ii_hashmap[tokens[0]]['posting_list'][doc]['locations'])
    current_token_locs.sort()

    for k in range(1,len(tokens)):
      next_token = tokens[k]
      next_token_locs = list(ii_hashmap[next_token]['posting_list'][doc]['locations'])
      next_token_locs.sort()
      t = []
      
      i = 0
      j = 0
      while i < len(current_token_locs) and j < len(next_token_locs):
        if next_token_locs[j] < current_token_locs[i]:
          j += 1
        elif current_token_locs[i] + 1 == next_token_locs[j]:
          t.append(next_token_locs[j])
          i += 1
          j += 1
        else:
          i += 1

      current_token_locs = t
    if len(current_token_locs) != 0:
      docs_containing_phrase.append(doc)

  ####PROXIMITY CHECK ENDING####

  for doc in docs_containing_phrase:
    index = 0
    for doc_cos in cos_tups:
      if doc_cos[0] == doc:
        new_doc = doc_cos[0]
        new_cos = doc_cos[1] + 10
        cos_tups.pop(index)
        cos_tups.append((new_doc, new_cos,),)
      index+=1

  return cos_tups

def phrasal_query(q):
  q = q.lower()
  ql = q.split()
  pqresult = compute_cosine_similarity(ql)
  return pqresult

def map_keyword(key):
  global ii_hashmap
  url_list = []
  key_hashmap = set()
  if key in ii_hashmap:
    for k in ii_hashmap[key]['posting_list']:
      url_list.append(k)
    for i in url_list:
      key_hashmap.add(i)

  return key_hashmap

def extract_next_query_token(q,i):
    j = q.find(' ',i)
    return (q[i:j],j+1)

def d_or(x,y):
    return x.union(y)

def d_and(x,y):
    return x.intersection(y)

def d_but(x,y):
    return x.difference(y)

def handle_bool_query(q,arg1,i):

    global T
    op, i = extract_next_query_token(q, i)
    arg2, i = extract_next_query_token(q, i)
    
    if op == '':
        return list(arg1)
    else:
        if op == 'and':
            return handle_bool_query(q,d_and(arg1, map_keyword(arg2)), i)
        elif op == 'or':
            return handle_bool_query(q,d_or(arg1, map_keyword(arg2)), i)
        elif op == 'but':
            return handle_bool_query(q,d_but(arg1, map_keyword(arg2)), i)
        else:
            print('Error: >{0}<is not a valid boolean operation.'.format(op))


def bool_query(q):
    q += ' '
    if len(q) != 0:
        arg1,i = extract_next_query_token(q,0)
        return handle_bool_query(q,map_keyword(arg1),i)
    else:
        print('Error: empty boolean query.')
        return ['No Results']

def intersect_all(list_of_sets):
  if len(list_of_sets) == 0:
    return {} # return empty set

  r = list_of_sets[0]
  
  for s in list_of_sets:
    r = r.intersection(s)
    
  return r



def main():
    bools = ['and', 'or', 'but']
    # q = 'cat and html or dog or good'
    is_bool_query = True
    while True:
      query = input("Enter a search query=> ")
      print('Query = ',query)
      for i in bools:
        if i in query:
          t = bool_query(query)
          for result in t:
            print(result[0])
          is_bool_query = True
        else:
          is_bool_query = False
          pass
      if is_bool_query == False:
        if query != None and query.isnumeric() != True:
          t = phrasal_query(query)
          t.sort(key=lambda x:x[1], reverse=True)
          for result in t:
            print(result[0])
        else:
          print('invalid search')
      if query == None or query == '':
       print('goooooodbye')
       break


# main()





