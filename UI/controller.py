import flet as ft

from database.DB_connect import get_connection
from model.corso import Corso
from model.studente import Studente


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.corsi = []
        self.studenti = {}

    def cercaIscritti(self, e):

        c = self._view.ddCorsi.value

        if c is None:
            self._view.create_alert("Seleziona un corso!")
            self._view.update_page()
            return

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM STUDENTE")

        self.studenti.clear()

        for s in cursor:
            x = Studente(**s)
            self.studenti[x.matricola] = x

        cursor.execute("SELECT * FROM ISCRIZIONE")

        for q in cursor:

            if q["codins"] == c:
                stringa = ""
                stringa = "Nome: " + self.studenti[q["matricola"]].nome + " | Cognome: " + self.studenti[q["matricola"]].cognome + " | Matricola: " + str(self.studenti[q["matricola"]].matricola)

                self._view.lV.controls.append(ft.Text(stringa))
                self._view.update_page()

        db.close()

    def cercaStudente(self, e):

        mat = self._view.matricola.value

        if mat == "":
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        elif mat is None:
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        elif mat.isdigit():
            db = get_connection()
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM STUDENTE")
            self.studenti.clear()

            for s in cursor:
                x = Studente(**s)
                self.studenti[x.matricola] = x

            db.close()
            if self.studenti.__contains__(int(mat)):

                nome = self.studenti[int(mat)].nome
                cognome = self.studenti[int(mat)].cognome

                #self._view.cognome.value(cognome)
                self._view.update_page()
            else:
                self._view.create_alert("La matricola che hai inserito non esiste!")
                self._view.update_page()
                return


    def cercaCorsi(self, e):

        mat = self._view.matricola.value

        if mat == "":
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        elif mat is None:
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        elif mat.isdigit():
            db = get_connection()
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM ISCRIZIONE")
            trovato = 0
            for c in cursor:

                if c["matricola"] == int(mat):
                    trovato = 1
                    stringa = ""
                    stringa = "Codice corso: " + c["codins"]
                    self._view.lV.controls.append(ft.Text(stringa))
                    self._view.update_page()

            if trovato == 0:
                self._view.create_alert("Matricola non trovata!")
                self._view.update_page()
                return

            db.close()


    def iscriviti(self, e):
        mat = self._view.matricola.value

        if mat == "":
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        elif mat is None:
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        elif mat.isdigit():
            c = self._view.ddCorsi.value
            if c is None:
                self._view.create_alert("Seleziona un corso!")
                self._view.update_page()
                return

            db = get_connection()
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM STUDENTE")
            self.studenti.clear()

            for s in cursor:
                x = Studente(**s)
                self.studenti[x.matricola] = x

            if self.studenti.__contains__(int(mat)):
                cursor.execute("SELECT * FROM ISCRIZIONE")

                for q in cursor:
                    if q["matricola"] == int(mat) and q["codins"] == c:
                        self._view.create_alert("Lo studente è già iscritto a questo corso!")
                        self._view.update_page()
                        return

                query = "INSERT INTO iscrizione (matricola, codins) VALUES (%s, %s)"
                dati= (mat, c)

                cursor.execute(query, dati)
                db.close()


    def fillCorsi(self):

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM CORSO")
        self.corsi.clear()

        for c in cursor:
            x = Corso(**c)
            self.corsi.append(x)
            self._view.ddCorsi.options.append(ft.dropdown.Option(key=x.codins, text=x.nome))

        db.close()