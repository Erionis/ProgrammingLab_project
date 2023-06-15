

class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    """
    Classe che permette di leggere un file contenente una serie temporale di valori separati da virgola.
    """
    def __init__(self, name):
        self.name = name
    
    def get_data(self):
        """
        Metodo che permette di leggere i dati dal file.
        """
        # Controllo che il file esista e che sia leggibile
        try: 
            with open(self.name, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            raise ExamException(f'Errore, il file "{self.name}" non esiste.')
        
        data_list = []

        # Leggo le righe del file
        for line in enumerate(lines[1:], start=2):  # Parto dalla seconda riga
            elements = line.strip().split(',') # Separo i valori della riga e rimuovo gli spazi
            
            if len(elements) < 2 or len(elements) > 3:  # Ignoro le righe con meno di due valori o più di tre
                continue

            date = elements[0] # Estraggo la data

            passengers = elements[1] # Estraggo il numero di passeggeri
            # Controllo che il numero di passeggeri sia un intero positivo
            if not passengers.isdigit() or int(passengers) < 0:
                continue  # Ignoro le righe con valori non validi
            
            # Aggiungo i dati alla lista
            data_list.append([date, int(passengers)])

        return data_list
    
    
def compute_avg_monthly_difference(time_series, first_year, last_year):
    """
    Funzione che calcola la media delle differenze tra i passeggeri di anno in anno per ogni mese.
    """
    pass




time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
differences = compute_avg_monthly_difference(time_series, 1949, 1951)
print(differences)