

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
            
            if len(elements) < 2 or len(elements) > 3:  # Ignoro le righe con meno di due valori o più di tre
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


    monthly_differences = [0] * 12 # Creo una lista di 12 mesi inizializzati a 0
    yearly_data = {} # Creo un dizionario vuoto che conterrà i dati raggruppati per anno

    # Raggruppo i dati per anno
    for data in time_series:
        date = data[0] # Estraggo la data
        year = int(date[:4]) # Estraggo l'anno
        month = int(date[5:]) # Estraggo il mese

        # Controllo che l'anno sia compreso tra first_year e last_year
        if first_year <= year <= last_year:
            # Se l'anno non è presente nel dizionario, lo aggiungo
            if year not in yearly_data:
                # Inizializzo la lista dei mesi per quell'anno a None 
                yearly_data[year] = [None] * 12
            # Inserisco il dato nella lista del mese corrispondente    
            yearly_data[year][month-1] = data[1]
            
    # Controllo che i dati siano presenti per tutti gli anni richiesti
    if first_year not in yearly_data or last_year not in yearly_data:
        raise ExamException(f'Errore, gli anni specificati non sono presenti nel file CSV.')
    
    # Calcolo la differenza tra i passeggeri di anno in anno
    for year in range(first_year, last_year):
        
        for month in range(12):
            # Controllo che i dati del mese corrente siano presenti per entrabi gli anni
            if yearly_data[year][month] is not None and yearly_data[year+1][month] is not None:
                # Calcolo la differenza tra i volori dei passeggeri 
                diff = yearly_data[year+1][month] - yearly_data[year][month]
                # Aggiungo la differenza al totale del mese
                monthly_differences[month] += diff

    # calcolo la media mensile
    avg_monthly_differences = []
    
    for month in range(12):
        # Calcolo il numero di anni per cui i dati sono presenti per il mese corrente
        count = sum([1 for year in range(first_year, last_year) if yearly_data[year][month] is not None and yearly_data[year+1][month] is not None])
        # Se il conteggio è 0, la media è 0
        if count == 0:
            avg_monthly_differences.append(0)
        else:
            # Altrimenti calcolo la media considerando il numero di anni per cui i dati sono presenti
            avg_monthly_differences.append(monthly_differences[month] / count)

    return avg_monthly_differences


