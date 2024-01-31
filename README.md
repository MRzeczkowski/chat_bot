# Nietzsche bot

## Wstęp

To interaktywny agent konwersacyjny zaprojektowany, aby symulować dyskusje z filozofem Friedrichem Nietzsche. Ten prosty chatbot wykorzystuje przetwarzanie języka naturalnego do identyfikowania intencji użytkownika i odpowiadania na pytania dotyczące życia, filozofii i dzieł literackich Nietzschego, a także angażowania użytkowników w dialogi.

### Podstawowe funkcje

 - Rozmowy inspirowane filozofią Nietzschego.
 - Częściowo świadome kontekstu konwersacje.
 - Bot zadaje pytania, które kierują użytkownika do różnych tematów.
 - Gdy każda odpowiedź na temat została wyczerpana, użytkownik jest o tym informowany.

### Użycie
Bot został napisany w języku Python w wersji 3.11.6 i wykorzystuje biblioteki Numpy i Tensorflow.

W celu uruchomienia bot'a należy zainstalować zależności: `pip install -r requirements.txt`

Uruchomić skrypt: `python3 main.py`.

## Opis

Celem projektu było stowrzenie bot'a który będzie udzielał odpowiedzi związanych z wyrażonymi przez użytkownika intencjami. Odpowiedzi miały być różnorodne, bogate, powiązane z kontekstem rozmowy. Interakcje dynamiczne dzięki zadawaniu przez bot'a pytań, propozycji tematów do poruszenia i reakcji na odpowiedzi użytkownika - co jest szczególnie istotne ze względu na wybraną domenę (filozofię Nietzschego) która nie musi być dobrze znana użytkownikowi.

Pierwsza wersja bot'a powstała na podstawie artykułu ze strony Towards Data Science [1]. 

Bot składa się z trzech ogólnych części:
1. Bazy wiedzy `intents.json` która zawiera możliwe intencje użytkownika, wzorce wiadomości użytkownika i treści odpowiedzi bot'a. 

2. Sieci neuronowej która na podstawie zawartości `intents.json` uczy się przewidywać intencje użytkownika.

3. Kodu który pobiera dane z `intents.json`, konwertuje je na postać którą może przyjąć sieć neuronowa, tworzy i trenuje sieć neuronową, a następnie wchodzi w interakcje z użytkownikiem. Wykorzystuje sieć neuronową do zgadnięcia intencji użytkownika, a następnie na podstawie kontekstu rozmowy i treści `intents.json` odpowiada użytkownikowi.

Uruchomienie bot'a wyświetla informacje dot. tematów na które można rozmawiać z bot'em i jak będzie on reagował na intencje użytkownika w specjalnych przypadkach.

### Intencje użytkownika

Przewidziano 14 intencji użytkownika, każda intencja składa się z kilku elementów:
- `tag` - nazwa intencji, 
- `patterns` - lista wzroców wiadomości użytkownika, 
- `responses` - lista odpowiedzi bot'a, która zawiera treść odpowiedzi w polu `text` i może mieć dodatkowe pole `explanation` zawierające dodatkowe szczegóły dotyczące odpowiedzi
- `responses_exhausted` - lista odpowiedzi które są udzielane użytkownikowi kiedy wyczerpie on odpowiedzi z listy `responses`
- `followup_questions` - lista pytań które bot może zadać użytkownikowi po tym jak odpowie na jego wiadomość. Każde pytanie składa się z treści (`question`) i pola `proposed_intent` - czyli proponowanej intencji do której bot przejdzie jeśli użytkownik odpowie twierdząco na zadane pytanie

W celu osiągnięcia dużej różnorodności i jakości odpowiedzi oraz wzorców duża część pliku `intents.json` została wygenerowana za pomocą ChatGPT, a treść odpowiedzi na intencję `quote` została zaczerpnięta z artykułu na stronie The Collector [2].

### Reakcje bot'a

Większość intencji dotyczy zagadnień filozofii Nietzschego, ale kilka z nich ma dodatkowe funkcje poza samym dostarczeniem informacji.

Specjalne intencje to:
- `greeting` - przywitanie bot'a. Użytkownik może przywitać bot'a tylko raz i jeśli jego pierwszą intencją nie jest przywitanie, bot poza reakcją na intencje dodatkowo przywita użytkownika. W praktyce prawie każda pierwsza wiadomość wysłana do bot'a zaczyna się od przywitania z jego strony.
- `interest` - wyrażenie tej intencji jest sygnałem dla bot'a, że ma udzielić dodatkowego wyjaśnienia dla swojej odpowiedzi (pole `explanation`) lub w przypadku pytania (pole `question`) przejść do intencji z nim związanego (pole `proposed_intent`)
- `disinterest` - wyrażenie tej intencji jest sygnałem dla bot'a, że ma **nie** udzielić dodatkowego wyjaśnienia dla swojej odpowiedzi (pole `explanation`) lub w przypadku pytania (pole `question`) **nie** przejść do intencji z nim związanego (pole `proposed_intent`)
- `goodbye` - pożegnanie bot'a na które bot reaguje wyświetleniem odpowiedzi i zakończenie działania programu

Intencje `interest` i `disinterest` są akceptowane przez bot'a tylko jeśli zadał użytkownikowi pytanie o bardziej szczegółową odpowiedź lub o to czy jest zainteresowany zaproponowanym tematem. Jeśli te intencje zostaną wyrażone w innych sytuacjach bot zwróci losową odpowiedź informującą użytkownika o tym, że jest zdezorientowany.

Bot przechowuje kontekst konwersacji z użytkownikiem który zawiera listę udzielonych odpowiedzi związanych z daną intencją. Zastosowanie kontekstu umożliwia uniknięcie wielokrotnych powitań użytkownika i zwracanie tylko tych odpowiedzi które nie zostały już udzielone. Jeśli wszystkie odpowiedzi zostały już wykorzystane, bot wylosuje odpowiedź z listy `responses_exhausted` które informują użytkownika o wyczerpaniu odpowiedzi i proszą o zmianę tematu.

#### Przykład interakcji
```
You: hello

Nietzsche bot: Hello, free spirit! Are you ready to embark on a journey beyond good and evil?

You: yes, tell me about some of your concepts

Nietzsche bot: Behold the pillars of my thought: The Will to Power, the essence of our driving force; The Übermensch, a beacon of self-overcoming; Eternal Recurrence, the cyclical nature of existence; Master-Slave Morality, a critique of ethical standards; and the profound proclamation that God is Dead, heralding a new era of philosophical inquiry.

Nietzsche bot: Interested in hearing more?

You: yes

Nietzsche bot: Ah, a mind eager for knowledge! Let's continue our exploration.

Nietzsche bot: Each concept represents a cornerstone of my philosophy. The Will to Power is the primary driving force in humans, the Übermensch symbolizes the ideal individual who transcends traditional values, Eternal Recurrence challenges us to live life as if it would repeat eternally, Master-Slave Morality critiques traditional ethics, and 'God is Dead' reflects the decline of religious authority.

You: god is dead?

Nietzsche bot: The declaration 'God is Dead' reflects the erosion of metaphysical and religious foundations in the modern world.

Nietzsche bot: Are you interested in more details?

You: yes

Nietzsche bot: Very well, let us delve deeper into this topic.

Nietzsche bot: It signifies a profound shift where traditional morals and beliefs lose their power, paving the way for new values. This phrase is not a celebration but a recognition of a significant cultural and philosophical transformation.

```

### Sieć neuronowa

Zastosowano architekturę zoptymalizowaną do rozpoznawania intencji w czatach na podstawie artykułu "Intent recognition using Trensorflow" [3].

Do trenowania sieci neuronowej zastosowano dane z `intents.json`. Wejściem do sieci są wzorce `patterns` poddane tokenizacji, a oczekiwanym wyjściem `tag` poddany kodowaniu One-hot. 

Sieć neuronowa składa się z następujących warstw:
1. **Embedding**: Konwertuje indeks słów występujących we wzorach `patterns` na gęste wektory cech o stałym rozmiarze.
Pozwala sieci lepiej zrozumieć zależności i kontekst w danych tekstowych.
2. **Bidirectional LSTM**: Dwukierunkowa sieć rekurencyjna LSTM, przetwarzająca sekwencje danych z obu kierunków.
LSTM jest skuteczna w przechwytywaniu zależności w danych sekwencyjnych, takich jak tekst. 
Dwukierunkowość pozwala sieci przetwarzać dane w obu kierunkach (do przodu i do tyłu), co poprawia zrozumienie kontekstu sekwencji.
Zastosowano parametr dropout.
3. **Dense**: Warstwa gęsta z aktywacją 'relu', przetwarzająca cechy z poprzednich warstw. 
Zastosowano regularyzację L2 do zapobiegania nadmiernemu dopasowaniu przez nałożenie kary na zbyt duże wagi.
4. **BatchNormalization**: Normalizuje aktywacje poprzedniej warstwy, stabilizując proces uczenia.
5. **Dropout**: Redukuje ryzyko przeuczenia przez losowe wyłączanie części neuronów.
6. **Dense (wyjściowa)**: Warstwa wyjściowa z funkcją aktywacji 'softmax', przekształcająca wyniki na prawdopodobieństwa klas.

Użyto optymalizatora Adam z niewielkim tempem uczenia i regulacją wagi.
Model jest kompilowany z funkcją straty categorical_crossentropy, oraz metryką 'accuracy' (dokładność).

#### Możliwe usprawnienia

Czasami występuje problem przeuczenia i nie poprawna identyfikacja intencji. Temu problemowi mogą zaradzić następujące zmiany:
- zwiększenie ilości wzorców i ich różnorodności
- wyrównanie ilości wzorców dla każdej intencji
- zmniejszenie podobieństwa wzorców
- podział danych zbiory: trenujący, walidacyjny i testowy. Bieżąca implementacja nie dokonuje tego podziału po cześci ze względu na niewystarczającą ilość wzorców wiadomości użytkownika
- zapisywanie najlepszego modelu zmiast tworzenia nowego podczas każdego uruchomienia bot'a

## Żródła:
[1] https://towardsdatascience.com/a-simple-chatbot-in-python-with-deep-learning-3e8669997758

[2] https://www.thecollector.com/what-are-nietzsche-most-famous-quotes/

[3] https://www.geeksforgeeks.org/intent-recognition-using-tensorflow/
