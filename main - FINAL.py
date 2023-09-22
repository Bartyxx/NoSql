from neo4j import GraphDatabase

class Connection:
    def __init__(self, neo4j_uri, neo4j_username, neo4j_password):
        print(f"Connecting to the database {neo4j_uri}.")
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

    Menu of the programs.
    It's possible to choose 4 option, after the selection the users need to 
    insert the fiscal code of the interested person, the option are:
        a - To show the property of the interested person.
        b - To show the nearest parents in life of the interested person.
        c - To change the statust of the interested person from live to death.
            it also change the goods property to the parents shown in point b.
        any other key - to exit from the program.

    '''
    
    driver = connection.driver
    isfromc = False
    while True:
        print("_-" * 48 + "\n"
              'Welcome in the notaril support, choose an option:\n\t'
              '- Show the property of a live person                                   - a\n\t'
              '- Show the nearest parent in life of a person                          - b\n\t'
              '- Show the new property considering the departue of a person           - c\n\t'
              '- Exit                                                                 - every other key\n'
              + "_-" * 48)
        try:
            guess = str(input('Your choice:_'))
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
    query return name and value of the goods(a.nome, a.valore) and the 
    connection from the interested person to the goods(r.value).
    
    '''
    
    driver = connect.driver
    session = driver.session()
    
    person, counter, iterable_result, i, result = initialize_cf()
    control_cf(person, counter)            

    query_string = 'MATCH(p:p{cf:"' + i[0] + '"})-[r: Possiede]->(a) return a.nome, a.valore, r.value'
    query = session.run(query_string)
    query_iterable = iter(query)
    
    printobj = list()
    for item in query_iterable:
        printobj.append(item)
        
    if len(printobj):
        print(f'Items possessed by {i[1]} {i[2]}:\n'
              f'-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\
                  -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-')
        for item in printobj:
             print(f'Item name: {item["a.nome"]}\tValue of the item: \
                    {item["a.valore"]}€\n'
                  f'Percentage of item possession: {item["r.value"]}\t \
            Calculated value:{item["a.valore"]/100*item["r.value"]}')
    else:
        print(f"{i[1]} {i[2]} don't have any item")
    
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
    consort -> return name and surname of the consort (a.nome, a.cognome) and
               the name of the interested person (p.consort).
    sons    -> retunr name, surname, fiscal code off all the sons (a.nome, 
               a.cognome, a.cf) and the name of the interested person (p.consort)
    parbro -> return name, surname, fiscal code of the parents (a.nome, 
              a.cognome, a.cf), name, surname, fiscal code of the siblings 
              (b.nome, b.cognome, b.cf), name of the interested persone (p.nome).
              
    This function it's also used in the departure function to control the
    nearest ereditors in life. It's passed a variable name isfromc, if the 
    variable is True it means that the function it's used in the departure 
    function, if it's false the function it's called by the users in the menu.
    In the first case the variable person is the same of the c function.
        
    '''
        
    if isfromc == False:
        person, counter, iterable_result, i, result = initialize_cf()
        control_cf(person, counter)
        printv = True
    else: 
        person = person_fromc
        counter, iterable_result, i, result = initialize_cf_c(person)
        control_cf(person, counter)
        printv = False
        
    query_consort = "MATCH (p:p{cf:'"+ str(person)+"'})-[:SposatoCon]-(a) RETURN a.nome, a.cognome, p.nome"
    query_sons = "MATCH (p:p{cf:'"+ str(person)+"'})-[:Genera]->(a) RETURN a.nome, a.cognome, a.cf, p.nome"
    query_parbro = "MATCH(p:p{cf:'" + str(person)+"'})<-[:Genera]-(a:p)-[:Genera]->(b:p) RETURN a.nome, a.cognome, a.cf, p.nome,b.nome, b.cognome, b.cf"
    
    control = "consort"
    heirs = function_heirs(query_consort)
 
    if len(heirs):
        if printv == True:
            print(f" If {i[1]} where to be missing is good will go to \
                  {heirs[0][0]} {heirs[0][1]}, the cosort.")
        list_heirs = to_list(heirs, control, i)
    else:
        if printv == True:
            print(f"{i[1]} don't have a consort!")
        control = "sons"
        heirs = function_heirs(query_sons)
        list_heirs = to_list(heirs, control, i)
            
        if len(heirs):
            if printv == True:
                print(f"If {i[1]} where to be missing is good will go to \
                        they son/s: ")
            try:
                for i in heirs:
                    if printv == True:
                        print(f"----->{i['a.nome']}")
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
                    print(f"If{i[1]} where to be missing is good will go to\
                            parents and siblings: ")
                prec_gen=None
                prec_sons=None   
                try:
                    for i in heirs:
                        if i['a.nome']!=prec_gen:
                            if printv == True:
                                print(f"--parent--> {i['a.nome']}")
                            prec_gen = i['a.nome']
                        if i['b.nome']!=prec_sons:
                            if printv == True:
                                print(f"--siblings--> {i['b.nome']}")
                            prec_sons = i['b.nome']
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
    The cypher query return name, code and value of the goods (a.nome, a.codice, 
    a.valore), the value in percentage of the goods (r.value) and the name of
    the interested person(p.nome).
    
    If a person dosn't have any ereditor than the goods are assign to the 
    State.
    
    '''
    
    driver = connect.driver
    session = driver.session()

    person, counter, iterable_result, i, result = initialize_cf()
    control_cf(person, counter)
    

    query_string = 'MATCH(p:p{cf:"' + str(i[0]) + '"})-[r: Possiede]->(a) RETURN a.nome,a.codice, a.valore, r.value, p.nome'
    
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
                        query="create (" + str(heirs['cf']) + ":p)\
                            -[:Possiede{value:" + str(percent_own_ereditors) + "\
                                        }]->("+items['a.codice']+":b)"
                        session.run(query)
                        print(f"The goods{items['a.nome']} will be inherited by\
                              {heirs['nome']} {heirs['cognome']} for the \
                              {round(percent_own_ereditors, 2)}% of \
                            is value, so {items['a.valore']/len(heirs)}€")
                except KeyError:
                    print("")
        else:
            print(f"{i['p.nome']} did not have any heirs, the goods\
                    will go to the State")
            for items in possessions:
                query = "create (s:stato {nome:'italia'})-[:Possiede\
                {value:" + items['r.value'] + "}]->("+items['a.codice'] + ":b)"
                session.run(query)
                print(
                    f"The goods {items['a.nome']} will be inherit by the italian\
                      State, for the {items['r.value']}% correspond to,\
                      {items['a.valore']}€")

    else:
        print(f"{i['p.nome']} dind't have any goods")
    session.run("match(p: p {cf:'" + str(person) + "'}) set p.stato = 'morto'")

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
        l['p' + str(c)] = {'nome': line['p.nome'], 'cognome': line['p.cognome'], 'cf': line['p.cf'],'età':['p.eta']}
        c += 1
    return l

# ============================================================================
def control_cf(person, counter):
    '''
    
    This function is used in the three main function to control(when the fiscal
    code is asked):
    - cf len.
    - existence of the cf.
    - presente of equal cf.
    
    Then in case of Error gives to possibility at the users to exit from the
    progrm or of return to the menu.
    
    '''
    
    if len(person) != 16:
        print("The fiscal code must be of length 16.")
        error = True
    elif counter == 0:
        print("There are no alive person with this fiscal code in our databases.")
        error = True
    elif counter > 1:
        print("There are more person with the same fiscal code in our databases!")
        print("There have been some mistake, the fiscal code should be unique!")
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
def initialize_cf():
    '''
    
    This function is used in the three main function for asking the fiscal code.
    After the insertion of the fiscal code it's checkd with the control_cf
    function.
    
    RETURN:
        - cf               -> fiscal code inserted
        - counter          -> in case there is more than one persone with the 
                              same cf.
        - iterable_results -> the iteration of the query.
        - i                -> the last value in iterable_result, if the query
                              is empty i is assigned to 0.
        - result -         > the cypher query.
    
    '''
    
    driver = connect.driver
    session = driver.session()
    try:
        person = str(input('Insert the fiscal code\n_'))
    except Exception as e:
        print(f'Something went wrong: {e}')
    
    session = driver.session()
    result = session.run("match (p:p{cf:'"+str(person)+"',stato:'vivo'})\
                         return p.cf,p.nome,p.cognome,p.stato,p.eta")
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
def initialize_cf_c(person):
    '''
    
    Same of the initialize_cf function but dosn't return person.
    It's not possibile to use initialize_cf because ask for the cf, but the 
    function initialize_cf as been already called when the users choose the c
    function so another fuction for initialize the cf is needed without to ask
    for the cf.

    '''
    
    driver = connect.driver
    session = driver.session()
    
    session = driver.session()
    result = session.run("match (p:p{cf:'"+str(person)+"',stato:'vivo'})\
                         return p.cf,p.nome,p.cognome,p.stato,p.eta")
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
        initialize_cf.

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
            heirs.append({'nome': i[0], 'cognome': i[1], 'relazione': 'coniuge'})
    if control == "sons":
        for i in sons:
            heirs.append({'nome': i[0], 'cognome': i[1], 'cf': i[2], 'relazione': 'figlio/a'})
    if control == "parbro":
        prec_gen = None
        prec_bro = None
        for i in parbro:
            if i['a.nome'] != prec_gen:
                heirs.append({'nome': i['a.nome'], 'cognome': i['a.cognome'], 'cf': i['a.cf'], 'relazione': 'genitore'})
                prec_gen = i['a.nome']
            if i['b.nome'] != prec_bro:
                heirs.append({'nome': i['b.nome'], 'cognome': i['b.cognome'], 'cf': i['b.cf'],'relazione': 'fratello/sorella'})
                prec_bro = i['b.nome']
    list_heirs = list(heirs)
    return list_heirs

# ============================================================================
def final_control():
    '''
    
    The final message of the program, if 0 is pressed the program return in
    the menu, if any others key is pressed exit the program.

    '''
    
    print("-_" * 48)
    print("Press 0 for exit or every other key to reach the menu")
    
    try:
        guess = str(input('_'))
    except Exception as e:
        print(f'Something went wrong: {e}')
    if guess!= "0":
        menu(connect)
    


if __name__ == '__main__':
    neo4j_uri = "bolt://localhost:7687"
    neo4j_username = "neo4j"
    neo4j_password = "hellohello"
    connect=Connection(neo4j_uri,neo4j_username,neo4j_password)
    menu(connect)

