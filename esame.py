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
        except IOError:
            raise ExamException(f'Errore durante l\'apertura del file "{self.name}".')

        data_list = []
        last_year = None # Variabile per l'anno per controllare l'ordine dei timestamp
        last_month = None # Variabile per il mese per controllare l'ordine dei timestamp

        # Leggo le righe del file
        for line_num, line in enumerate(lines[1:], start=2):  # Parto dalla seconda riga
            elements = line.strip().split(',') # Separo i valori della riga e rimuovo gli spazi
            
            if len(elements) < 2: # Ignoro le righe con meno di due valori 
                continue

            date = elements[0] # Estraggo la data
            
            # Controllo che la data sia nel formato corretto
            try:
                year = int(date[:4])  # Estraggo l'anno
                month = int(date[5:])  # Estraggo il mese
            except ValueError:
                continue  # Ignoro le righe con date non valide

            # Controllo l'ordine dei timestamp
            if last_year is not None and last_month is not None and (year < last_year or (year == last_year and month <= last_month)):
                raise ExamException(f'Errore, timestamp fuori ordine o duplicato nella riga {line_num}.')

            last_year = year # Aggiorno l'anno
            last_month = month # Aggiorno il mese

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
    # Controllo che first_year e last_year siano anni validi
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    except ValueError:
        raise ExamException('Errore, gli anni specificati devono essere numeri.')
    
    # Controllo che first_year e last_year siano numeri di quattro cifre
    if first_year < 1000 or first_year > 9999 or last_year < 1000 or last_year > 9999:
        raise ExamException('Errore, gli anni specificati devono essere numeri di quattro cifre.')

    # Controllo che last_year sia maggiore di first_year
    if last_year <= first_year:
        raise ExamException('Errore, last_year deve essere maggiore di first_year.')

    monthly_differences = [0] * 12 # Creo una lista di 12 mesi inizializzati a 0
    dictionary = {} # Creo un dizionario vuoto che conterrà i dati raggruppati per anno

    # Costriusco il dizionario dei dati raggruppati per anno
    for data in time_series:
        date = data[0] # Estraggo la data
        year = int(date[:4]) # Estraggo l'anno
        month = int(date[5:]) # Estraggo il mese

        # Controllo che l'anno sia compreso tra first_year e last_year
        if first_year <= year <= last_year:
            # Se l'anno non è presente nel dizionario, lo aggiungo
            if year not in dictionary:
                # Inizializzo la lista dei mesi per quell'anno a None 
                dictionary[year] = [None] * 12
            # Inserisco il dato dei passeggeri nella lista del mese corrispondente    
            dictionary[year][month-1] = data[1]
            
    # Controllo che i dati siano presenti per tutti gli anni richiesti
    if first_year not in dictionary or last_year not in dictionary:
        raise ExamException(f'Errore, gli anni specificati non sono presenti nel file CSV.')
    
    # Calcolo la differenza tra i passeggeri di anno in anno
    for year in range(first_year, last_year):
        
        for month in range(12):
            # Controllo che i dati del mese corrente siano presenti per entrabi gli anni
            if dictionary[year][month] is not None and dictionary[year+1][month] is not None:
                # Calcolo la differenza tra i volori dei passeggeri 
                difference = dictionary[year+1][month] - dictionary[year][month]
                # Aggiungo la differenza al totale del mese
                monthly_differences[month] += difference

    # calcolo la media mensile
    avg_monthly_differences = []
    
    for month in range(12):
        # Calcolo il numero di anni per cui i dati sono presenti per il mese corrente
        count = sum([1 for year in range(first_year, last_year) if dictionary[year][month] is not None and dictionary[year+1][month] is not None])
        # Se il conteggio è 0, la media è 0
        if count < 1:
            avg_monthly_differences.append(0)
        else:
            # Altrimenti calcolo la media considerando il numero di anni per cui i dati sono presenti
            avg_monthly_differences.append(monthly_differences[month] / count)

    return avg_monthly_differences



# time_series_file = CSVTimeSeriesFile(name='data.csv')
# time_series = time_series_file.get_data()
# differences = compute_avg_monthly_difference(time_series, 1949, 1951)
# print(time_series)
# print(differences)

