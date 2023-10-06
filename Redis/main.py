'''
    SCHOOL ELECTION.

    Creation of a program which purpose is to control the vote for various
    proposal in a school.

    The student have to insert:
                                - Name
                                - Surname
                                - ID

    When the fields are inserted the studen can choose between this action:
                                - Create a new proposal.
                                - Vote for an existing proposal.
                                - View the proposal, who created it and the
                                  number of votes. A proposal can be created
                                  by two student.
                                - Terminate the program.

    A student can insert an unlimeted quantity of proposal.
    A student can vote for every proposal, but only one time for every proposal.

    The python client have to use a REDIS server for managing the data from
    the election.

    Data structure used:
                                - ZSET for insert the election results.
                                  In this way every proposal have a number
                                  related and is possibile to automatically
                                  order the proposal.
                                - HSET for the proposal and the information.
                                  The hset will contain.
                                                - Number of the proposal.
                                                - Description of the proposal.
                                                - Creators.
                                                - Numbers of vote.


    #########################################################################
    ATTENTION.
    What we have to control:
    - It's impossibile to insert two identical proposal. If a student insert
      an existing proposal the program have to react consequetially.
    - The initial vote of every proposal have to be set on 0.

'''

import redis
import sys


class Proposte:
    '''
        Redis initialization.
    '''

    def __init__(self):
        self.redis = redis.Redis(host             = 'localhost',
                                 port             = 6379,
                                 db               = 0,
                                 charset          = 'utf-8',
                                 decode_responses = True)

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def home(self):
        '''

            _______
           !      !
           ! HOME !
           !______!


            -----------------------------------------------------------------
            Student log and show the possible action to the users.
            -----------------------------------------------------------------
        '''

        print('Immetti i tuoi dati per votare e visualizzare le proposte.\n')
        print('\n')
        while True:
            while True:
                try:
                    print("-" * 90)
                    self.alunno_nome    = str(input('Inserisci il tuo nome:\t').title())
                    self.alunno_cognome = str(input('Inserisci il tuo cognome:\t').title())
                    self.alunno_ID      = int(input("Inserisci il tuo ID studente:\t"))
                    print("-" * 90)
                    self.inserisci_studente(self.alunno_nome, self.alunno_cognome)
                    break
                except ValueError:
                    print('Inserisci un id numerico')
                except TypeError as e:
                    print(e)

            while True:
                try:
                    print('Che cosa vuoi fare?\n\n\n'
                          'n = Nuova proposta\n'
                          'v = Vota una proposta\n'
                          'd = Descrizione delle proposte\n'
                          'e = Exit')
                    scelta = str(input())

                    n_option = ['n', 'N']
                    v_option = ['v', 'V']
                    d_option = ['d', 'D']
                    e_option = ['e', 'E']
                    if scelta in n_option or \
                            scelta in v_option or \
                            scelta in d_option or \
                            scelta in e_option:
                        pass
                    else:
                        raise ValueError('Non hai inserito nessuna delle possibili scelte')
                except ValueError as err:
                    print(err)

                if scelta in n_option:
                    prop = input('Inserisci la tua proposta\n')
                    self.inserisci_proposta(prop)
                elif scelta in v_option:
                    print('Vota una proposta\n')
                    self.vota_proposta()
                elif scelta in d_option:
                    if [key for key in self.redis.scan_iter('proposta:*')]:
                        self.leggi_proposte()
                    else:
                        print('non sono ancora state inserite proposte\n')
                elif scelta in e_option:
                    sys.exit("Grazie! A presto.")
                else:
                    print('\n Non sono ancora state inserite proposte')

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def leggi_proposte(self):
        '''

            _______________________
           !                       !
           ! READ PROPOSAL SECTION !
           !_______________________!


        ----------------------------------------------------------------------
            Read the keys in Redis wich correspond to 'proposta:*'
            The student see on the screen all the proposal with:
                 - The creator
                 - Number of vote
                 - Description.

        ---------------------------------------------------------------------

        '''

        print('')

        for key in self.redis.zrange('voti:proposte', 0, -1, desc=True):

            print(key.title() + '\t\t' + 'Proposta da ' +
                  str(self.redis.hget(key, "proponente")) + '\n' +
                  'Descrizione: ' + str(self.redis.hget(key, 'desc')) +
                  '\t\t' + str(self.redis.hget(key, 'voti')) + ' voti'
                  + '\n' + '-' * 95)

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def inserisci_studente(self, nome, cognome):
        '''
        Parameters
        ----------
        nome : str
            Name of the student.
        cognome : str
            Surname of the student.

        ---------------------------------------------------------------------

        The funciton insert name and surname in a Redis set.
        The key of the set is student:student_ID

        ----------------------------------------------------------------------

        '''
        if f'studente:{self.alunno_ID}' in self.redis.scan_iter('studente:*'):
            if self.redis.get(f'studente:{self.alunno_ID}') == f'{nome} {cognome}':
                pass
            else:
                raise TypeError('inserisci delle credenziali valide')
        self.redis.set(f'studente:{str(self.alunno_ID)}', f'{nome} {cognome}')

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def inserisci_proposta(self, sugg):
        '''

            _________________________
           !                         !
           ! INSERT PROPOSAL SECTION !
           !_________________________!


        ---------------------------------------------------------------------
        Parameters
        ----------
        sugg : str
            The propose insert in the home function.

        ---------------------------------------------------------------------

        The function initialize the proposal of the student. It's inserted in
        Redis in a hset with key "proposta:n_proposta"
                The hset contain:
                            - desc -> description of the proposal.
                            - proponente -> who have create the proposal?
                            - voti -> numbers of vote of the proposal.
        ---------------------------------------------------------------------

        '''
        proposte = [key for key in self.redis.scan_iter('proposta:*')]
        proposte.sort()

        if sugg in [self.redis.hget(key, 'desc') for key in proposte]:
            print('La proposta esiste già')
        elif len(proposte) == 0:

            self.redis.hset(f'proposta:1', 'desc', f'{sugg}')
            self.redis.hset(f'proposta:1', 'proponente',
                            str(self.redis.get(f'studente:{str(self.alunno_ID)}')))
            self.redis.hset(f'proposta:1', 'voti', 0)
            self.redis.lpush(f'proponenti:proposta:1', str(self.alunno_ID))
            self.redis.zadd('voti:proposte', {'proposta:1': 0})
            print('proposta inserita correttamente')
            # creo lista redis con proponenti:1  ID
        else:
            ultima_proposta = int(proposte[-1][proposte[-1].find(':') + 1:])
            self.redis.hset(f"proposta:{ultima_proposta + 1}", 'desc', f'{sugg}')
            self.redis.hset(f"proposta:{ultima_proposta + 1}", 'proponente',
                            str(self.redis.get(f'studente:{self.alunno_ID}')))
            self.redis.hset(f"proposta:{ultima_proposta + 1}", 'voti', 0)
            # creo lista con proponenti:ultima_proposta+1  ID
            self.redis.zadd('voti:proposte', {f'proposta:{ultima_proposta + 1}': 0})
            print('Proposta inserita correttamente')

    # ========================================================================
    # ========================================================================
    # ========================================================================

    def vota_proposta(self):
        '''

            _______________
           !              !
           ! VOTE SECTION !
           !______________!


            -----------------------------------------------------------------
            In this section is possible to vote for a proposal.
            Insert the nuber correspondant to a proposal ex. proposta:5, I
            need to insert 5.
            Every student can vote one time for one proposal but he can vote
            for every proposal.
            -----------------------------------------------------------------
        '''

        proposte = [key for key in self.redis.scan_iter('proposta:*')]
        proposte.sort()

        if len(proposte) == 0:
            print("Nessuno ha ancora proposta qualcosa! Visitare la sezione " +
                  "Nuova proposta per essere il primo!")
        else:
            print('Vota una delle seguenti proposte:')
            self.leggi_proposte()
            lista_proposte = [int(key[key.find(':') + 1:]) for key in
                              self.redis.scan_iter('proposta:*')]
            while True:
                try:
                    scelta = int(input('scrivi il numero della proposta che vuoi votare\n'))
                    if scelta in lista_proposte:
                        lista_votanti = self.redis.lrange(f'votanti:proposta:{scelta}', 0, -1)
                        if str(self.alunno_ID) not in lista_votanti:
                            self.redis.lpush(f'votanti:proposta:{scelta}',
                                             self.alunno_ID)
                            self.redis.hincrby(f'proposta:{scelta}', 'voti', 1)
                            self.redis.zincrby('voti:proposte', 1, f'proposta:{scelta}')
                            print('\ngrazie per aver votato\n')
                        else:
                            print("hai già votato per questa proposta, votane un' altra")
                            break
                    else:
                        raise ValueError('inserisci il numero di una proposta esistente')
                    break
                except ValueError:
                    print('inserisci un numero intero')


if __name__ == '__main__':
    a = Proposte()
    a.home()
