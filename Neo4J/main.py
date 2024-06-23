from neo4j import GraphDatabase

class Connection:
    def __init__(self, neo4j_uri, neo4j_username, neo4j_password):
        print(f"Connecting to the database {neo4j_uri}....")
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, \
                                                            neo4j_password))
        print(f"Connect to the database {neo4j_uri}.")

    def close(self):
        if self.driver:
            self.driver.close()
            print(f"Sconnected to the database {self.driver}.")

# ============================================================================
def menu(connection:Connection):
    '''

    Menu of the program.
    It's possible to choose 4 option, after the selection the user need to 
    insert the id of the interested person, the option are:
        a - To show the property of the interested person.
        b - To show the nearest parents in life of the interested person.
        c - To change the status of the interested person from live to death.
            it also change the goods property to the parents shown in point b.
        any other key - to exit from the program.

    '''
    
    driver = connection.driver
    isfromc = False
    while True:
        print("=" * 100 + "\n"
              'Menu\n\t'
              'Welcome to the notarial support. Please choose an option:\n\t'
              '- Show the property of a living person.                                 - a\n\t'
              '- Show the nearest living relative of a person.                         - b\n\t'
              '- Show the new property considering the departure of a person.          - c\n\t'
              '- Exit                                                                  - every other key\n'
              + "=" * 100)
        try:
            guess = str(input('Your choice: > '))
            break
        except Exception as e:
            print(f'Something went wrong:{e}')
    if guess.lower() == 'a':
        possessions(connection)
    elif guess.lower() == 'b':
        relatives("", isfromc)
    elif guess.lower() == 'c':
        departure()
    else:
        print('Thank for choosing us!')
        driver.close()

# ============================================================================
def possessions(connect:Connection):
    '''
    
    This function show all the property of the iterested person. The cypher 
    query return name and value of the goods(a.name, a.value) and the 
    connection from the interested person to the goods(r.value).
    
    '''
    
    driver = connect.driver
    session = driver.session()
    
    person, counter, iterable_result, i, result = initialize_id()
    control_id(person, counter)            

    query_string = 'MATCH(p:p{id:"' + i[0] + '"})-[r: Owns]->(a) return a.name, a.value, r.value'
    query = session.run(query_string)
    query_iterable = iter(query)
    
    printobj = list()
    for item in query_iterable:
        printobj.append(item)
        
    if len(printobj):
        print(f'\n Items possessed by {i[1]} {i[2]}:\n')
        print("=" * 100 + "\n")
        for item in printobj:
             print(f'--------------------------------------\n'
                   f'Item name: {item["a.name"]}\n'
                   f'--------------------------------------\n'
                   f'Value of the item: {item["a.value"]}€\n'
                   f'Percentage of item possession: {item["r.value"]}\n'
                   f'Calculated value:{item["a.value"]/100*item["r.value"]}\n')
    else:
        print(f'--------------------------------------\n'
              f"{i[1]} {i[2]} don't have any items\n"
              f'--------------------------------------\n')
    
    final_control()
        
        
# ============================================================================
def relatives(person_fromc, isfromc):
    '''
    
    This function show the nearest parents alive parents of the interested 
    person, the parents shown are the one who are going to inherit the goods
    if the person pass away.
    It's possible to look at the succession rules in the file:
    'Regole di successione con query cypher.txt'
    
    The cypher query used are 3:
    consort -> return name and surname of the consort (a.name, a.surname) and
               the name of the interested person (p.consort).
    sons    -> retunr name, surname, id off all the sons (a.name, 
               a.surname, a.id) and the name of the interested person (p.consort)
    parbro -> return name, surname, id of the parents (a.name, 
              a.surname, a.id), name, surname, id of the siblings 
              (b.name, b.surname, b.id), name of the interested persone (p.name).
              
    This function it's also used in the departure function to control the
    nearest ereditors in life. It's passed a variable name isfromc, if the 
    variable is True it means that the function it's used in the departure 
    function, if it's false the function it's called by the users in the menu.
    In the first case the variable person is the same of the c function.
        
    '''
        
    if isfromc == False:
        person, counter, iterable_result, i, result = initialize_id()
        control_id(person, counter)
        printv = True
    else: 
        person = person_fromc
        counter, iterable_result, i, result = initialize_id_c(person)
        control_id(person, counter)
        printv = False
        
    query_consort = "MATCH (p:p{id:'"+ str(person)+"'})-[:SposatoCon]-(a) RETURN a.name, a.surname, p.name"
    query_sons = "MATCH (p:p{id:'"+ str(person)+"'})-[:Generate]->(a) RETURN a.name, a.surname, a.id, p.name"
    query_parbro = "MATCH(p:p{id:'" + str(person)+"'})<-[:Generate]-(a:p)-[:Generate]->(b:p) RETURN a.name, a.surname, a.id, p.name,b.name, b.surname, b.id"
    
    control = "consort"
    heirs = function_heirs(query_consort)
 
    if len(heirs):
        if printv == True:
            print(f"If {i[1]} where to be missing the good will go to "
                  f'{heirs[0][0]} {heirs[0][1]}, the consort.')
        list_heirs = to_list(heirs, control, i)
    else:
        if printv == True:
            print(f"{i[1]} don't have a consort!")
        control = "sons"
        heirs = function_heirs(query_sons)
        list_heirs = to_list(heirs, control, i)
            
        if len(heirs):
            if printv == True:
                print(f"If {i[1]} where to be missing is good will go to "
                      f"his son/s: ")
            try:
                for i in heirs:
                    if printv == True:
                        print(f"-----> {i['a.name']}")
            except KeyError:
                print("")
        else:
            if printv == True:
                print(f"{i[1]} don't have sons!")
            control = "parbro"
            heirs = function_heirs(query_parbro)
            list_heirs = to_list(heirs, control, i)
            if len(heirs):
                if printv == True:
                    print(f"If {i[1]} where to be missing is good will go to " 
                          f"parents and siblings: "
                          f'{"=" * 100}')
                prec_gen=None
                prec_sons=None   
                try:
                    for i in heirs:
                        if i['a.name']!=prec_gen:
                            if printv == True:
                                print(f"--parent--> {i['a.name']}")
                            prec_gen = i['a.name']
                        if i['b.name']!=prec_sons:
                            if printv == True:
                                print(f"--siblings--> {i['b.name']}")
                            prec_sons = i['b.name']
                except KeyError:
                    print("")
            else:
                if printv == True:
                    print(f"{i[1]} don't have parents or brothers so \
                          is good will pass to the State ")
    if printv == True:
        final_control()
    return list_heirs
    
# ============================================================================
def departure():
    '''
    
    This function calculate the ereditor in case of the departure of a person.
    The succession rule are the same of the parents function, so the parent
    function it's called to decide the ereditors and the variable isfromc is
    passed.
    The cypher query return name, code and value of the goods (a.name, a.code, 
    a.value), the value in percentage of the goods (r.value) and the name of
    the interested person(p.name).
    
    If a person dosn't have any ereditor than the goods are assign to the 
    State.
    
    '''
    
    driver = connect.driver
    session = driver.session()

    person, counter, iterable_result, i, result = initialize_id()
    control_id(person, counter)
    

    query_string = 'MATCH(p:p{id:"' + str(i[0]) + '"})-[r: Owns]->(a) RETURN a.name,a.code, a.value, r.value, p.name'
    
    result_possession = session.run(query_string)
    iter_possession = iter(result_possession)
    possessions = list()
    
    for i in iter_possession:
        possessions.append(i)

    if len(possessions):
        isfromc = True
        heirs = relatives(person, isfromc)
        if len(heirs)!=0:
            for items in possessions:
                percent_own_ereditors = round(items['r.value'] / len(heirs),2)
                try:
                    for heirs in heirs:
                        query="create (" + str(heirs['id']) + ":p)\
                              -[:Owns{value:" + str(percent_own_ereditors) + "\
                               }]->("+items['a.code']+":b)"
                        session.run(query)
                        print(f"The goods {items['a.name']} will be inherited " 
                              f"by {heirs['name']} {heirs['surname']} for the " 
                              f"{round(percent_own_ereditors, 2)}% of "
                              f"is value, so {items['a.value']/len(heirs)}€")
                except KeyError:
                    print("")
        else:
            print(f"{i['p.name']} did not have any heirs, the goods "
                  f"will go to the State")
            for items in possessions:
                query = "create (s:country {name:'italy'})-[:Owns\
                {value:" + items['r.value'] + "}]->("+items['a.code'] + ":b)"
                session.run(query)
                print(
                    f"The goods {items['a.name']} will be inherit by the italian "
                    f"State, for the {items['r.value']}% correspond to,"
                    f"{items['a.value']}€")

    else:
        print(f"{i['p.name']} Didn't have any goods")
    session.run("match(p: p {id:'" + str(person) + "'}) set p.status = 'dead'")

# ============================================================================
def arrange_query_person(a: iter) -> dict:
    '''
       :param a:iter(result of a neo4j query)
       :return: dict of person
       
    Given a neo4j object in return a dict.
    '''
    
    l = {}
    c = 0
    print(a)
    for line in a:
        l['p' + str(c)] = {'name': line['p.name'], 'surname': line['p.surname'], 'id': line['p.id'],'età':['p.age']}
        c += 1
    return l

# ============================================================================
def control_id(person, counter):
    '''
    
    This function is used in the three main function to control(when the fiscal
    code is asked):
    - id len.
    - existence of the id.
    - presente of equal id.
    
    Then in case of Error gives to possibility at the users to exit from the
    progrm or of return to the menu.
    
    '''
    
    if len(person) != 16:
        print("The id must be of length 16.")
        error = True
    elif counter == 0:
        print("There are no alive person with this id in our databases.")
        error = True
    elif counter > 1:
        print("There are more person with the same id in our databases!")
        print("There have been some mistake, the id should be unique!")
        error = True

    try:
        error
    except NameError:
        error = False
        
    if error == True:
        print('Press 1 if you want to go to the menu\nEvery other key to exit')
        try:
            guess=str(input('_'))
        except Exception as e:
            print(f'Something went wrong: {e}')
        if guess=='1':
            menu(connect)
        else:
            return 
    return 

# ============================================================================
def initialize_id():
    '''
    
    This function is used in the three main function for asking the id.
    After the insertion of the id it's checkd with the control_id
    function.
    
    RETURN:
        - id               -> id inserted
        - counter          -> in case there is more than one persone with the 
                              same id.
        - iterable_results -> the iteration of the query.
        - i                -> the last value in iterable_result, if the query
                              is empty i is assigned to 0.
        - result -         > the cypher query.
    
    '''
    
    driver = connect.driver
    session = driver.session()
    try:
        person = str(input('Insert the id\n> '))
    except Exception as e:
        print(f'Something went wrong: {e}')
    
    session = driver.session()
    result = session.run("match (p:p{id:'"+str(person)+"',status:'alive'})\
                         return p.id,p.name,p.surname,p.status,p.age")
    iterable_result = iter(result)
    counter = 0
    
    for i in iterable_result:
        counter += 1
    
    try:
        i
    except NameError:
        i = 0
        
    return person, counter, iterable_result, i, result
  
# ============================================================================      
def initialize_id_c(person):
    '''
    
    Same of the initialize_id function but dosn't return person.
    It's not possibile to use initialize_id because ask for the id, but the 
    function initialize_id as been already called when the users choose the c
    function so another fuction for initialize the id is needed without to ask
    for the id.

    '''
    
    driver = connect.driver
    session = driver.session()
    
    session = driver.session()
    result = session.run("match (p:p{id:'"+str(person)+"',status:'alive'})\
                         return p.id,p.name,p.surname,p.status,p.age")
    iterable_result = iter(result)
    counter = 0
    
    for i in iterable_result:
        counter+=1
    try:
        i
    except NameError:
        i = 0
        
    return counter, iterable_result, i, result

# ============================================================================
def function_heirs(query):
    '''
    
    It's used in the relatives function for iterate the list of the heirs.
    
    RETURN a list with the heirs.

    '''
    
    driver = connect.driver
    session = driver.session()
    
    heirs = session.run(query)
    iterable_heirs = iter(heirs)
    
    listheirs = list()
    for i in iterable_heirs:
        listheirs.append(i)
    return listheirs

# ============================================================================
def to_list(f_heirs, control, i):
    '''
    
    Parameters
    ----------
    f_heirs : list
        The list contain the heirs, it's transformed from a neo4j object to a 
        list in the function_heirs function.
    control : str
        A string with the type of control we are checking at, it can be consrot,
        sons and parbro.
    i : value
        The actual value of the iteration in iterable_result in the function 
        initialize_id.

    Returns
    -------
    list_heirs : list
        A list with the heirs.

    '''    

    if control == "consort":
        iterable_heirs = iter(f_heirs)
        consort = list()
        for i in iterable_heirs:
            consort.append(i)
    if control == "sons":
        iterable_heirs = iter(f_heirs)
        sons = []
        for i in iterable_heirs:
            sons.append(i)
    if control == "parbro":
        iterable_heirs = iter(f_heirs)
        parbro = list()
        for i in iterable_heirs:
            parbro.append(i)
        
    heirs = list()
    if control == "consort":
        for i in consort:
            heirs.append({'name': i[0], 'surname': i[1], 'relationship': 'spouse'})
    if control == "sons":
        for i in sons:
            heirs.append({'name': i[0], 'surname': i[1], 'id': i[2], 'relationship': 'son/daughter'})
    if control == "parbro":
        prec_gen = None
        prec_bro = None
        for i in parbro:
            if i['a.name'] != prec_gen:
                heirs.append({'name': i['a.name'], 'surname': i['a.surname'], 'id': i['a.id'], 'relationship': 'parent'})
                prec_gen = i['a.name']
            if i['b.name'] != prec_bro:
                heirs.append({'name': i['b.name'], 'surname': i['b.surname'], 'id': i['b.id'],'relationship': 'brother/sister'})
                prec_bro = i['b.name']
    list_heirs = list(heirs)
    return list_heirs

# ============================================================================
def final_control():
    '''
    
    The final message of the program, if 0 is pressed the program return in
    the menu, if any others key is pressed exit the program.

    '''
    print("\t")
    print("=" * 100)
    print("Press 0 for exit or every other key to reach the menu")
    
    try:
        guess = str(input(' >'))
    except Exception as e:
        print(f'Something went wrong: {e}')
    if guess!= "0":
        menu(connect)
    


if __name__ == '__main__':
    neo4j_uri = "bolt://localhost:7687"
    neo4j_username = "neo4j"
    neo4j_password = "AlfaAlfa"
    connect=Connection(neo4j_uri,neo4j_username,neo4j_password)
    menu(connect)

