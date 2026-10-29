import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    # TODO
    def handle_get_strumenti(self,e):
        strumenti = self._model.get_strumenti() #viene richiamata la funzione get_strumenti() su model e
                                                #veuen riportata la lista degli strumenti creata in quella def
        # Pulisce la ListView nella View prima di aggiungere i nuovi dati, sennò si accumulerebbero degi strumenti duplicati
        self._view.lista_strumenti.controls.clear()  # ogni volta che si clicca

        # Se non ci sono strumenti o c'è un errore
        if strumenti is None:
            self._view.show_alert("Nessuno strumento trovato nel database!") #funzione nella view che richiede di mettere un messaggio
            return        # di avvertenza
        elif len(strumenti)==0:
            self._view.show_alert('errore:database strumeti vuoto')
            return

        # Popola la ListView con i dati restituiti dal Model
        for s in strumenti:
            self._view.lista_strumenti.controls.append(ft.Text(str(s))) #trasformo ogni strumento in un testo di flet con ft.Text(str(s))

        # Aggiorna l'interfaccia grafica
        self._view.update()
    def handle_cerca_tipo(self,e):
        tipo_cercato=self._view.input_tipo_strumento.value.strip()

        if not tipo_cercato:
            self._view.show_alert("Errore:inserisci un tipo da cercare")
            return
        if tipo_cercato.isdigit():
            self._view.show_alert("Errore:tipo non valido")
            return
        strumenti=self._model.cerca_strumenti_per_tipo(tipo_cercato)
        self._view.lista_strumenti_ricerca.controls.clear()

        if strumenti is None:
            self._view.show_alert("Errore.impossibile collegarsi al database")
            return
        elif len(strumenti)==0:
            self._view.show_alert(f"Errore:il tipo {tipo_cercato} non esiste")
        else:
            for s in strumenti:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(s)))
        self._view.update()

