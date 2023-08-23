import re
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

text = """
VAL CHIAVENNA:
Baita del Capriolo - Bertacchi - Brasca - Bresciadega - Cà Bianca - Camanin - Carlo Emilio - Castellaccio - Chianova - Chiara e Walter - Chiavenna - Circul di Uschione - Curti - Forcola - Frasnedo - Garzonedo - Il Biondo - Lavorerio - La Locanda di Codera - Mai Tardi - Manco - Notaro - Osteria Alpina - Passo del Servizio - Pian del Nido - Primalpia - Savogno - Scarlonzöö - Stuetta - Suretta - Uschione - Val Capra - Valli - Val Loga - Volta

VALTELLINA:
Ai Fop - Allievi Bonacossa - Alpe Colina - Alpe Granda (rifugio) - Alpe Granda (bivacco) - Alpini Santo Stefano - Anghileri Rusconi - Baita del Sole - Barchi - Bignami - Bosio - Bottani Cornaggia - Brusada - Campomoro - Carate - Ca Runcasch - Cederna Maffina - Cometti - Cristina - De Dosso - Del Grande Camerini - Desio - Erler - Gianetti - Gugiatti Sertorelli - La Casermetta - Lagazzuolo - Longoni - Luna Nascente - Marinella - Marinelli Bombardieri - Mello - Mitta - Montirolo - Motta - Musella - Omio - Palù - Pioda - Ponte - Ponti - Porro Gerli - Poschiavino - Rasega - Scermendone - Scotti - Sufrina - Tartaglione - Valditogno - Ventina - Vetta di Rhon - Zoia
"""

split_parts = re.split(r'\n\n*', text)
split_parts.pop(0)
# Extracting regions
regions = [split_parts[0], split_parts[2]]
regions = [re.sub(r'\:$', '', region) for region in regions]

# Extracting hikes
hikes = [split_parts[1], split_parts[3]]
hikes_list = [hike.strip() for e in hikes for hike in re.split(r'\-', e)]
hikes_pages = [re.sub(r'\s+', '', hike) for hike in hikes_list]
with open("CorrectNames.txt", "r") as file:
    for line in file:
        hikes_pages.append(line.strip())
print(hikes_pages)
# Step 1: Web Scraping
base_url = "https://www.diska.it/"

hikes_info = []
URLErr = []
DataErr = []

for page in hikes_pages:
    dec_page = unidecode(page)
    url = base_url + 'rif' + dec_page + '.asp'

    response = requests.get(url)
    if response.status_code == 404:
        URLErr.append(url)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract hike name, description, rating, etc.
        hike_name = soup.title.string
        hike_description = str(soup.body)
        hike_info = hike_description.split("Tempo impiegato")
        hike_time = re.findall(r"Tempo impiegato:?\s*ore (\d+(?:\.\d+)?)", hike_description)
        hike_elgain = re.findall(r"Dislivello:? m\. ?([+-]?\d+ ?[+-]?\d+)",hike_description)

        hike_time = [(float(time)) for time in hike_time]
        if len(hike_elgain) == 0:
            DataErr.append(hike_name)
        else:
            print(hike_name +':')
            print(hike_elgain)

        hikes_info.append({
            "name": hike_name,
            "hike elevation gain": hike_elgain,
            "hike duration": hike_time
        })

# output the errors
with open("URLerrors.txt", "w") as file:
    for error in URLErr:
        file.write(str(error)+'\n')
with open("TimeErrors.txt", "w") as file:
    for error in DataErr:
        file.write(str(error)+'\n')

print('URL Errors:', len(URLErr))
print('Data Errors:', len(DataErr))
# Now you have the hikes information in the hikes_info list

# Step 2: Text Summarization (using a hypothetical summarization function)
def summarize_text(text):
    # Implement your text summarization logic here
    # For example, you could use Gensim's summarization module
    summarized_text = your_summarization_function(text)
    return summarized_text


for hike in hikes_info:
    hike["summary"] = summarize_text(hike["description"])

# Step 3: Data Structuring (using Pandas)
import pandas as pd

hikes_df = pd.DataFrame(hikes_info)


# Step 4: Ranking
def custom_sorting_key(hike):
    # Define your ranking criteria here
    return hike["rating"]  # Change this to your preferred ranking criteria


sorted_hikes = sorted(hikes_info, key=custom_sorting_key, reverse=True)

# Step 5: Displaying Results
for rank, hike in enumerate(sorted_hikes, start=1):
    print(f"Rank {rank}: {hike['name']} - Rating: {hike['rating']:.2f}")

# You can further enhance and customize each step as per your needs.

