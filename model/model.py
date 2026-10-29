from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito


'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        try:
            cnx = get_connection()

            cursore = cnx.cursor(dictionary=True)

            query = "SELECT * FROM strumento"
            cursore.execute(query)

            strumenti = []
            for riga in cursore:
                # Passi le singole chiavi del dizionario al costruttore
                strumento = Strumento(
                    codice=riga["codice"],
                    tipo=riga["tipo"],
                    marca=riga["marca"],
                    anno_acquisto=riga["anno_acquisto"],
                    valore=riga["valore"],
                    disponibile=riga["disponibile"]
                )
                strumenti.append(strumento)

            cursore.close()
            cnx.close()

            return strumenti
        except Exception as e:
            print(f"{e}")
            return None
        finally:
            if cnx and cnx.is_connected():
                cnx.close()


    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """

        try:
            cnx = get_connection()

            cursore = cnx.cursor(dictionary=True)

            query = f"""SELECT *
                        FROM strumento
                        WHERE tipo = %s"""
            cursore.execute(query,(tipo,))

            strumenti = []
            for riga in cursore:
                # Passi le singole chiavi del dizionario al costruttore
                strumento = Strumento(
                    codice=riga["codice"],
                    tipo=riga["tipo"],
                    marca=riga["marca"],
                    anno_acquisto=riga["anno_acquisto"],
                    valore=riga["valore"],
                    disponibile=riga["disponibile"]
                )
                strumenti.append(strumento)

            return strumenti
        except Exception as e:
            print(f"{e}")
        finally:
            if cnx and cnx.is_connected():
                cnx.close()




        '''     
        strumenti=self.get_strumenti()
        strumenti_per_tipo = []
        if strumenti is None :
            return None
        for strumento in strumenti:
            if strumento.tipo==tipo:
                strumenti_per_tipo.append(strumento)
        if not strumenti_per_tipo:
            return None
        return strumenti_per_tipo
        '''


