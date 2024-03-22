# json-to-graph
Trabalho de conclusão do curso de Sistemas de Informação

\subsection{Makefile}
Para facilitar a configuração do docker compose e possibilitar a correta comunicação entre os containers e o script, foi criado um Makefile na raiz do repositório com as configurações padrões para teste local, sendo elas possíveis de modificação por meio dos parâmetros. \par
As configurações são baseadas em variaveis de ambiente. Para garantir a separação das informações relevantes a aplicação, são criados diversos arquivos .env com as configurações que serão utilizadas. Para o MongoDB será criado o arquivo .env.mongodb, para o MongoExpress .env.mongo\_express, para o Mongo Seed, .env.mongo\_seed, para o Neo4J .env.neo4j. O arquivo na raiz são as configurações para o script de migração de dados.

Parametros:
\begin{itemize}

    \item \textbf{profile}: O perfil escolhido para rodar os scripts de infraestrutura. As opções são basic e full.

    \item \textbf{clean}: Caso verdadeiro irá apagar as configurações prévias nos arquivos de variáveis de ambiente e irá os recriar conforme as configurações especificadas.

    \item \textbf{mongodb\_root\_username}: Nome de usuário do administrador do MongoDB. (padrão: \texttt{root})

    \item \textbf{mongodb\_root\_password}: Senha do administrador do MongoDB. (padrão: \texttt{root})

    \item \textbf{mongodb\_database}: Nome do banco de dados. (padrão: \texttt{test})

    \item \textbf{mongodb\_collection}: Nome da coleção. (padrão: \texttt{nyt})

    \item \textbf{mongodb\_url}: URL de conexão com o MongoDB. (padrão: \texttt{mongodb://\$(mongodb\_root\_username):\$(mongodb\_root\_password)@mongodb:27017/\$(mongodb\_database)?authSource=admin})

    \item \textbf{neo4j\_user}: O nome de usuário do banco de dados Neo4j. (padrão: neo4j)

    \item \textbf{neo4j\_password}: A senha do banco de dados Neo4j. (padrão: neo4j)

\end{itemize}


Arquivo .env.mongodb
\begin{itemize}
    \item \textbf{MONGO\_INITDB\_ROOT\_USERNAME}: Nome de usuário root
    \item \textbf{MONGO\_INITDB\_ROOT\_PASSWORD}: Senha de usuário root
    \item \textbf{MONGO\_INITDB\_DATABASE}: Database
\end{itemize}

Arquivo .env.mongo\_express
\begin{itemize}
    \item \textbf{ME\_CONFIG\_MONGODB\_URL}: Url de conexão do MongoDB
    \item \textbf{ME\_CONFIG\_MONGODB\_ADMINUSERNAME}: Nome de usuário do administrador
    \item \textbf{ME\_CONFIG\_MONGODB\_ADMINPASSWORD}: Senha do administrador
\end{itemize}

Arquivo .env.neo4j
\begin{itemize}
    \item \textbf{NEO4J\_AUTH}: Usuário e senha do Neo4J
    \item \textbf{NEO4J\_dbms\_security\_auth\_\_minimum\_\_password\_\_length}: Configuração de tamanho mínimo da senha. Como essa configuração é para teste, não produção, então foi flexibilizado para tamanho 1 (mínimo).
\end{itemize}

Arquivo .env.mongo\_seed
\begin{itemize}
    \item \textbf{MONGO\_SEED\_MONGODB\_URL}: Url de conexão do MongoDB
    \item \textbf{MONGO\_SEED\_MONGODB\_COLLECTION}: Coleção a ser populada
\end{itemize}

Arquivo .env
\begin{itemize}
    \item \textbf{MONGODB\_DATA}: Pasta de dados do MongoDB
    \item \textbf{NEO4J\_DATA}: Pasta de dados do Neo4J
    \item \textbf{MONGODB\_URL}: Url de conexão do MongoDB
    \item \textbf{MONGODB\_COLLECTION}: Coleção a ser testada
    \item \textbf{MONGODB\_DATABASE}: Database
    \item \textbf{NEO4J\_URL}: Url de conexão do Neo4J
    \item \textbf{NEO4J\_USER}: Usuário do Neo4J
    \item \textbf{NEO4J\_PASSWORD}: Senha do Neo4J
\end{itemize}

Comandos:
\begin{itemize}
    \item \textbf{write\_env\_values}: Escreve os valores das variáveis de ambiente nos arquivos .env
    \item \textbf{setup\_env\_file}: Escreve os valores das variáveis de ambiente nos arquivos .env, apagando os arquivos .env antigos se clean = true
    \item \textbf{start\_infra}: Inicia a infraestrutura com o docker compose com as configurações definidas.
    \item \textbf{stop\_infra}: Para a infraestrutura com o docker compose.
    \item \textbf{run}: Inicia a execução do script de migração.
\end{itemize}

\subsection{Perfis}
No docker compose estão configurados dois perfis de execução: basic e full. No perfil basic estão configurados os containers do MongoDB Seed, MongoDB e o Neo4J. No perfil full estão todos os containers do basic, com a adição do MongoExpress para facilitar a visualização e depuração dos dados disponibilizados no MongoDB.

\subsection{Perfil basic}
O perfil basic tem a intenção de ser o básico para o teste local. Por conta disso apenas o essencial é configurado, sendo ele o banco de origem, destino e os dados para teste. \par
O MongoDB está disponível na porta 27017 e os seus dados são salvos na pasta local data/mongodb, assim permitindo a persistência mesmo depois do fim do container. \par
O MongoSeed utiliza de scripts para popular a instancia do MongoDB. Para isso ele utiliza uma imagem do próprio MongoDB, que possui a interface de comando. Os exemplos estão disponíveis na pasta local mongo-seed, junto com o script bash para popular o banco. \par
O Admin do Neo4J está disponível na porta 7474, sendo a porta do Bolt a padrão 7687. Seus dados são salvos na pasta local data/neo4j, assim permitindo a persistência mesmo depois do fim do container.

\subsection{Perfil full}
O perfil full tem a inteção de ser o necessário para depuração dos testes. Por conta disso foi disponibilizado o MongoExpress, já que por padrão a imagem do Mongo não possui interface web para administração.
O MongoExpress está disponível na porta 8081 e pode ser utilizado para visualizar o estado do banco, suas métricas e dados conforme o necessário.

\section{Interface de comando}
\section{Cliente do MongoDB}
O cliente do MongoDB é responsável por ler todas as linhas de uma coleção do banco.
