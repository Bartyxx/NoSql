<!-- ---------------------------------------------------------------------- -->
<h1>Notaril support in Neo4J</h1>
<!-- ---------------------------------------------------------------------- -->
<hr>
<h2>Dataset</h2>
<i>Neo_DB.txt</i> --> Dataset used for the notaril support. The dataset is 
                      created by the work team.<br/><br/>


<h3>Element description</h3>
<table>
<caption>The dataset is composed by five type of data</caption>
<tr><td>p        </td><td>Person            </td></tr>
<tr><td>bi       </td><td>Immobiliar goods </td></tr>
<tr><td>bm       </td><td>Mobiliar goods    </td></tr>
<tr><td>cc       </td><td>Bank Account      </td></tr>
<tr><td>s        </td><td>Contry            </td></tr>
</table>

<br/>
-------------------------------------------------------------------------------
<h4>Person(p)</h4>
-------------------------------------------------------------------------------
<br/>

An example of person is:<br/>

<pre><i>CREATE(ROSIL01ISOLD09OL:p {name:"astolfo",
       surname: "rossi",   
       id: "ROSIL01ISOLD09OL",   
       status: "alive",
       age: 90 })</i></pre><br/>

Where <i>ROSIL01ISOLD09OL</i> is the unique key that identify the person, is the same
of the id.<br/>

<table>
<caption>Person attribute</caption>
<tr><td>name     </td><td>Name of the persone               </td></tr>
<tr><td>surname  </td><td>Surname of the person             </td></tr>
<tr><td>id       </td><td>Identification code of the person </td></tr>
<tr><td>status   </td><td>Alive or deceased                 </td></tr>
<tr><td>age      </td><td>Age                               </td></tr>
</table>
   
<br/>  
-------------------------------------------------------------------------------
<h4>Immobiliar good(bi)</h4>
-------------------------------------------------------------------------------
<br/>

<pre><i>CREATE(bi0:b {name: "house in the Alps",
                value: 500000,
				code:'bi0'})</i></pre><br/>

Where <i>bi0</i> id the unique identification of the immobiar good<br/>

<table>
<caption>Immobiliar good attribute</caption>
<tr><td>name     </td><td>Name of the goods                      </td></tr>
<tr><td>value    </td><td>Value in euro                          </td></tr>
<tr><td>code     </td><td>Same code as the unique identification </td></tr>
</table>

<br/>
-------------------------------------------------------------------------------
<h4>Mobiliar good(bm)</h4>
-------------------------------------------------------------------------------
<br/>

<pre><i>CREATE(bm0:b {name: "alfa giulia",
                value: 40000,
				code:'bm0'})</i></pre><br/>


Where <i>bm0</i> id the unique identification of the mobiliar good<br/>

<table>
<caption>Immobiliar good attribute</caption>
<tr><td>name     </td><td>Name of the goods                      </td></tr>
<tr><td>value    </td><td>Value in euro                          </td></tr>
<tr><td>code     </td><td>Same code as the unique identification </td></tr>
</table>

<br/>
-------------------------------------------------------------------------------
<h4>Bank account(cc)</h4>
-------------------------------------------------------------------------------
<br/>


<pre><i>CREATE(cc0:b {name: "bank account intesa",
                value: 4000,
				code:'cc0'})</i></pre><br/>

Where <i>cc0</i> id the unique identification of the bank account<br/>

<table>
<caption>Immobiliar good attribute</caption>
<tr><td>name     </td><td>Name of bank account                   </td></tr>
<tr><td>value    </td><td>Money in the bank account              </td></tr>
<tr><td>code     </td><td>Same code as the unique identification </td></tr>
</table>

<br/>
-------------------------------------------------------------------------------
<h4>Country(s)</h4>
-------------------------------------------------------------------------------
<br/>

There is one country, if a person die and don't have any parents, siblings or
sons the goods of the person became property of the country.<br/>
<pre><i>CREATE(s:country {name:"italy"})</i></pre><br/>

<!-- ---------------------------------------------------------------------- -->
<h3>Relationship description</h3><br/>
-------------------------------------------------------------------------------
<h4>Person to person</h4>
-------------------------------------------------------------------------------
<br/>

There are two type of relationship:<br/>
<ul>
    <li><b>Generate</b> : Relationship between parents and son/daughter</li>
</ul>

<pre><i>CREATE(ROSIL01ISOLD09OL)-[g1:Generate {value: 1}]->(ROSIL11ISOLD09OL)</i></pre><br/>
<ul>
    <li><b>MarriedWith</b> : Marriage between two person</li>
</ul>

<pre><i>CREATE(ROSIL11ISOLD09OL)-[s1:MarriedWith {value: 0}]->(ROSILA1ISOLD09OL)</i></pre><br/>


<br/>
-------------------------------------------------------------------------------
<h4>Person to goods</h4><br/>
-------------------------------------------------------------------------------
<br/>

There is one type of relationship:<br/>
<ul>
    <li><b>Own</b> : The goods is own by a person, the value field is the % of
                      the good own by the person.</li>
</ul>

<pre><i>CREATE(ROSIL01ISOLD09OL)-[:Owns {value: 100.00}]->(bi0)</i></pre><br/>

<br/>
<br/>
<hr>
<h2>Graph</h2><br/>

An example of the graph created: <br/>
<p><img src = "https://github.com/Bartyxx/NoSql/blob/main/Neo4J/img/completeGraph.png"/></p>
<ul>
    <li><b>Blue nodes </b> : Person </li>
    <li><b>Red nodes  </b> : Goods  </li>
    <li><b>Green nodes</b> : Country</li>
</ul>

<br/>







<h2>Decease family member</h2><br/>

- Mostrare cosa succede quando uno dei parenti muore e come vengono distribuite le proprieta
- Capire perche comando non funziona.
