<!-- ---------------------------------------------------------------------- -->
<h1>Notaril support in Neo4J</h1>
<!-- ---------------------------------------------------------------------- -->
<h2>Dataset</h2>
<i>Neo_DB.txt</i> --> Dataset used for the notaril support. The dataset is 
                      created by the work team.<br/><br/>


<h3>Element description</h3>
<table>
<caption>The dataset is composed by five type of data</caption>
<tr><td><b>ID</b></td><td><b>Type</b>       </td></tr>
<tr><td>p        </td><td>Person            </td></tr>
<tr><td>bi       </td><td>Immobiliar goods </td></tr>
<tr><td>bm       </td><td>Mobiliar goods    </td></tr>
<tr><td>cc       </td><td>Bank Account      </td></tr>
<tr><td>s        </td><td>Contry            </td></tr>
</table>

-------------------------------------------------------------------------------
<h4>Person(p)</h4>
-------------------------------------------------------------------------------
An example of person is:

CREATE(ROSIL01ISOLD09OL:p {name:"astolfo",
    surname: "rossi",
    id: "ROSIL01ISOLD09OL",
    status: "alive",
    age: 90 })

Where ROSIL01ISOLD09OL is the unique key that identify the person, is the same
of the id.

<table>
<caption>Person attribute</caption>
<tr><td><b>ID</b></td><td><b>Description</b>                </td></tr>
<tr><td>name     </td><td>Name of the persone               </td></tr>
<tr><td>surname  </td><td>Surname of the person             </td></tr>
<tr><td>id       </td><td>Identification code of the person </td></tr>
<tr><td>status   </td><td>Alive or deceased                 </td></tr>
<tr><td>age      </td><td>Age                               </td></tr>
</table>
     
-------------------------------------------------------------------------------
<h4>Immobial good(bi)</h4><br/>
-------------------------------------------------------------------------------
CREATE(bi0:b {name: "house in the Alps",
                value: 500000,
				code:'bi0'})

Where bi0 id the unique identification of the immobiar good

<table>
<caption>Immobiliar good attribute</caption>
<tr><td><b>ID</b></td><td><b>Description</b>                     </td></tr>
<tr><td>name     </td><td>Name of the goods                      </td></tr>
<tr><td>value    </td><td>Value in euro                          </td></tr>
<tr><td>code     </td><td>Same code as the unique identification </td></tr>
</table>

-------------------------------------------------------------------------------
<h4>Mobiliar good(bm)</h4><br/>
-------------------------------------------------------------------------------

CREATE(bm0:b {name: "alfa giulia",
                value: 40000,
				code:'bm0'})


Where bm0 id the unique identification of the mobiliar good

<table>
<caption>Immobiliar good attribute</caption>
<tr><td><b>ID</b></td><td><b>Description</b>                     </td></tr>
<tr><td>name     </td><td>Name of the goods                      </td></tr>
<tr><td>value    </td><td>Value in euro                          </td></tr>
<tr><td>code     </td><td>Same code as the unique identification </td></tr>
</table>


-------------------------------------------------------------------------------
<h4>Bank account(cc)</h4><br/>
-------------------------------------------------------------------------------
CREATE(cc0:b {name: "bank account intesa",
                value: 4000,
				code:'cc0'})

Where cc0 id the unique identification of the bank account

<table>
<caption>Immobiliar good attribute</caption>
<tr><td><b>ID</b></td><td><b>Description</b>                     </td></tr>
<tr><td>name     </td><td>Name of bank account                   </td></tr>
<tr><td>value    </td><td>Money in the bank account              </td></tr>
<tr><td>code     </td><td>Same code as the unique identification </td></tr>
</table>


-------------------------------------------------------------------------------
<h4>Country(s)</h4><br/>
-------------------------------------------------------------------------------
There is one country, if a person die and don't have any parents, siblings or
sons the goods of the person became property of the country.
CREATE(s:country {name:"italy"})

<!-- ---------------------------------------------------------------------- -->
<h3>Relationship description</h3><br/>
<!-- ---------------------------------------------------------------------- -->
<h4>Person to person</h4><br/>
<!-- ---------------------------------------------------------------------- -->

There are two type of relationship:
Generate : Relationship between parents and son/daughter.
CREATE(ROSIL01ISOLD09OL)-[g1:Generate {value: 1}]->(ROSIL11ISOLD09OL)

MarriesdWith: Marriage between two person
CREATE(ROSIL11ISOLD09OL)-[s1:MarriedWith {value: 0}]->(ROSILA1ISOLD09OL)

<!-- ---------------------------------------------------------------------- -->
<h4>Person to goods</h4><br/>
<!-- ---------------------------------------------------------------------- -->
There is one type of relationship:
Own: The goods is own by a person.
CREATE(ROSIL01ISOLD09OL)-[:Owns {value: 100.00}]->(bi0)

<br/>
<br/>
<h2>Graph</h2><br/>















<h2>Decease family member</h2><br/>


- Descrizione del database
- Descrizione dei grafi (con immagini)
- Mostrare cosa succede quando uno dei parenti muore e come vengono distribuite le proprieta
- Capire perche comando non funziona.
- Correggere i commenti.
- Capire come aggiustare i commit
