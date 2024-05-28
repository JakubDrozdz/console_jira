# Jakub Drożdż, s24871

# Dokumentacja:

## Nawigacja
- [Ogólne informacje](#general)
- [Model danych](#model)
  * [Typy zadań (TaskType)](#task_type)
  * [Priorytety zadań (TaskPriority)](#task_priority)
  * [Statusy zadań (TaskStatus)](#task_status)
  * [Zadania (Task)](#task)
  * [Sprinty (Sprint)](#sprint)
- [Funkcjonalności aplikacji](#functionality)
  * [Trwałość danych](#data_persistance)
  * [Uruchomienie aplikacji](#application_start)
  * [Przetwarzanie akcji](#action_handling)
  * [Dodanie zadania](#add_task)
  * [Edycja zadania](#edit_task)
  * [Usuwanie zadania](#remove_task)
  * [Wyświetlenie zadań](#print_tasks)
  * [Wyświetlenie przefiltrowanych zadań](#print_filtered_tasks)
  * [Utworzenie sprint'u](#create_sprint)
  * [Wyświetlenie listy sprint'ów](#list_sprints)
  * [Wyświetlenie tablicy sprintu](#sprint_board)


<a name="general"></a>
## Ogólne informacje

Aplikacja służy do zarządzania zadaniami wzorując się na systemie Jira.

Do obsługi zadań udostępnione jest kilka funkcjonalnośći:
- dodanie zadań
- usuwanie zadań
- edycja zadań
- wyświetlenie wszystkich zadań
- wyświetlenie zadań z użyciem filtru

Oprócz obsługi zadań aplikacja zarządza sprint'ami, które jak w systemie Jira służa do grupowania zadań.
Do obsługi sprint'ów dostępne są następujące operacje:
- dodanie sprint'u
- wyświetlenie listy sprint'ów (podział na aktywne i nieaktywne)
- wyświetlenie tablicy zadań

<a name="model"></a>
## Model danych

W celu obsługi funkcjonalności aplikacji został wprowadzony następujący model danych

<a name="task_type"></a>
### Typy zadań (TaskType)

Enum zawierający dostępne typy zadań:

- Task
- Defect
- Story
- Epic

<a name="task_priority"></a>
### Priorytety zadań (TaskPriority)

Enum zawierający dostępne priorytety zadań:

- Low
- Medium
- High
- Critical

<a name="task_status"></a>
### Statusy zadań (TaskStatus)

Enum zawierający dostępne statusy zadań:

- Open
- In progress
- In review
- Closed

<a name="task"></a>
### Zadania (Task)

W celu obsługi zadań zdefiniowana została klasa `Task`, która stanowi definicję zadań oraz zapewnia metody
zarządzania zadaniami jak i serializację i deserializację danych.

#### Pola klasy

Dla obiektów zadań klasa definuje następujące pola:
- `task_number` - automatycznie generowany numer zadania (`int`)
- `task_title` - tutył zadania wprowadzany przez użytkownika (`str`)
- `task_description` - opis zadania wprowadzany przez użytkownika (`str`)
- `task_priority` - priorytet zadania wybierany przez użytkownika (`TaskPriority`)
- `task_type` - typ zadania wybierany przez użytkownika (`TaskType`)
- `sprint` - powiązanie ze sprint'em wybierane przez użytkownika (`Sprint`)
- `task_status` = status zadanie wybierany przez użytkownika (`TaskStatus`)

<a name="sprint"></a>
### Sprinty (Sprint)
W celu obsługi sprintów zdefiniowana została klasa `Sprint`, która stanowi definicję sprintu oraz zapewnia metody
zarządzania sprintami jak i serializację i deserializację danych.

#### Pola klasy
Dla obiektów sprint'u klasa definuje następujące pola:
- `sprint_number` - automatycznie generowany numer sprintu (`str`)
- `start_date` - data startu, generowana na podstawie daty zakończenia ostatniego sprintu lub dzisiejszej daty gdy pierwszy sprint (`date`)
- `end_date` - data zakończeniu, sprint może trwać max 2 - 4 tygodnie (`date`)

<a name="functionality"></a>
## Funkcjonalności aplikacji

<a name="data_persistance"></a>
### Trwałość danych
Klasy `Task` i `Sprint` przechowują informacje o swojej ekstensji w prywatnych listach statyczych: `__taskExtent` i `__sprintExtent` 
Przy każdym uruchomieniu aplikacji dane odczytywane są z plików .csv i obie ekstensje są wypełniane.
Podczas działania aplikacji wszelkie modyfikacje są aktualizowane w ekstensji i w momencie zamykania aplikacji obie ekstensje są zapisywane do plików.
Pozwala to zachować trwałość i aktualność danych.

#### Zapis ekstensji
W obu klasach za zapis odpowiadają metody `write_extent()`. Definiowane są pola klasy, które stanowią nagłówki w pliku .csv.
Do zapisu do pliku użytu został `DictWriter`, który inicjowany jest z nagłówkami w celu poprawnego zapisu.
Dla każdego elementu z ekstensji dane są zapisywane do pliku w nowej lini.

#### Odczyt ekstensji
W obu klasach za zapis odpowiadają metody `read_extent()`. Do odczytu użyty został `DictReader` który, czyta nagłówki i dzięki temu
możemy łatwo odwołać się do elemenetu po kluczu jakim jest nagłówek. Dla każdego wpisu używamy konstruktora klasy, który utworzy obiektu i doda je do ekstensji.
W przypadku wystąpienia błędu element nie zostanie dodany do ekstensji i informacja o błędzie zostanie wypisana na konsoli.

<a name="application_start"></a>
### Uruchomienie aplikacji
Po uruchomieniu wywołana zostaje metoda `console_jira.app()`, która w pętli prezentuje menu i reaguje na wybór użytkownika prezentując dalsze kroki.
Za wyświetlenie menu odpowiada `console_jira.show_menu()`. Po pobraniu akcji od użytkownika, wprowadzone dane są walidowane i w przypadku
błędu walidacji dane stosowny komunikat jest wyświetlany i aplikacja wyświetla ponownie menu. Gdy użytkownik wybierze opcję `0`, aplikacja kończy działanie.

<a name="action_handling"></a>
### Przetwarzanie akcji
Funkcja `console_jira.invoke_option()` jest odpowiedzialna za wywołanie odpowiedniej akcji.
Bazując na wyborze użytkownika używając instrukcji `match... case` wywoływana jest odpowiednia funkcja.
Niektóre operacje, mogące rzucić wyjątek otoczone są blokiem `try-except` i stosowne informacje są wyświetlane na konsoli w przypadku
wystąpienia błędu.

<a name="add_task"></a>
### Dodanie zadania
Za dodanie zadania odpowiedzialna jest funkcja `console_jira.add_task()`, która zbiera od użytkownika informacje potrzebne do utworzenia zadania.
Gdy użytkownik poda zły typ danych np. `int` zamiast `str` funkcja przechwyci wyjątek `ValueError` i wypisze informację o złych danych i powróci do menu.
Inne rodzaj wyjątków przetwarzanych przez funkcję to `InvalidTaskInputException` i `NoSprintPresentException`. `NoSprintPresentException` może być
rzucony przez `console_jira.choose_sprint()` gdy użytkownik poda numer nieistniejącego sprintu. `InvalidTaskInputException` może zostać rzucony podczas tworzeniu obiektu klasy `Task`
np. gdy podany zostanie pusty opis.

Wartość dla pól będących enum'em jest wybierana w następujący sposób.

```
for value in TaskPriority:
  print(f"\t{value}")
priority = TaskPriority(input("Enter task priority: "))
```
Najpierw użytkownik może zapoznać się z dostępnymi wartościami, a następnie podaje wartość. Ważne, aby wartość była podana dokładnie jak widnieje
na liście dostępnych wartości. W przeciwnym wypadku zostanie rzucony wyjątek `ValueError` i operacja zostanie przerwana.

#### Wybór sprint'u

<a name="edit_task"></a>
### Edycja zadania
Za edycję zadania odpowiedzialna jest funkcja `console_jira.edit_task()`, która pobiera od użytkownika numer zadania, a następnie pobiera zadanie
z ekstensji za pomocą `task.Task.Task.get_task()`. Jeśli podany zostanie zły numer funkcja `get_task()` rzuci wyjątek `InvalidTaskInputException`, który
zostanie przechwycony i stosowny komunikat zostanie wypisany, a operacja zostanie anulowana.

Po poprawnym pobraniu obiektu zadania zostaje wywołana funkcja `task.Task.Task.edit()`.
Funkcja wyświetli użytkownikowi aktualne dane dotyczące zadania oraz możliwość wybory, którą z wartości chce zmienić.
Po poprawnym wyborze wartości do zmiany funkcja pyta o nową wartość (ewentualnie wyświetla dostępne wartości dla enum'ów) i zmienia dane.

<a name="remove_task"></a>
### Usuwanie zadania

Funkcja odpowiedzialne za usunięcie zadania to `console_jira.remove_task()`. Funkcja pobiera numer zadania i w przypadku błędnych danych obsługuje `ValueError`.
Następnie funkcja ta woła statyczną metodę usuwającą zadanie z ekstensji `task.Task.Task.remove_from_extent()`. Gdy nie istnieje zadanie o danym numerze to funcja podniesie
`ValueError`. Zaktualizowana ekstensja zostanie zapisana przy zamykaniu programu.

<a name="print_tasks"></a>
### Wyświetlenie zadań

Za wyświetlanie wszystkich zadań odpowiada `task.Task.Task.print_extent()`, która w nowych liniach wyświetla informacje
o zadaniach przechowywanych aktualnie w ekstensji.

<a name="print_filtered_tasks"></a>
### Wyświetlenie przefiltrowanych zadań

Za wyświetlenie przefiltrowanych zadań odpowiada `task.Task.Task.print_filtered_extent()`. Możliwe do filtrowania właściwości to:
 
- priorytet
- typ
- status
- sprint

Użytkownik wybiera opcję po jakiej chce filtrować a następnie funkcja przy pomocy instrukcji `match... case` konstruuje 
odpowiednie wyrażenie lambda i używa funkcji `filter()` do wybrania z ekstensji jedynie pasujących zadań. Możliwe jest filtrowanie po jednym typie w danej chwili.
Po zebraniu listy przefiltrowanych zadań są one wyświetlone na konsoli.

Funkcja może rzucić wyjątek `NoSprintPresentException` oraz `ValueError`. Gdy wyjątek zostanie przechwycony stosowna informacja zostanie wyświetlona i nastąpi powrót do menu.

<a name="create_sprint"></a>
### Utworzenie sprint'u

Za utworzenie sprint'u odpowiada funkcja `console_jira.create_sprint()`, która najpeirw prezentuje obliczone wartości dla sprint'u: numer i datę początkową.

Do obliczeniu numer sprintu użyta jest funkcja `sprint.Sprint.Sprint.calculate_sprint_number()`, która wybiera aktualnie najwyższy numer w ekstensji sprint'ów 
(jeśli ekstensja jest pusta zwraca 0) i zwraca numer o 1 większy.

Do obliczenia daty startu sprint'u używana jest funkcja `sprint.Sprint.Sprint.calculate_start_date()`, która wybiera najpóźniejszą z dat zakończenia sprintu dostępnych
w ekstensji i zwiększa ją o jeden dzień

Następnie funkcja `create_sprint()` prosi użytkownika o podanie daty zakończenia sprint'u w formacie `(yyyy-mm-dd)` i używając funkcji `sprint.Sprint.Sprint.calculate_end_date()`
sprawdza czy długość sprintu wynosi 2 - 4 tygodnie. Jeśli sprint jest zbyt krótki zmienia datę zakończenia aby trwał 2 tygodnie. Jeśli sprint jest za długi zmienia datę zakończenia
aby wynosił 4 tygodnie.

Na końcu użytkownik proszony jest o potwierdzenie danych sprintu. Funkcja dodaje sprint po zatwierdzeniu danych i wyświetla komunikat. Jesli użytkownik nie zatwierdzi danych sprint
nie jest tworzony i stosowna informacja jest wyświetlana.

<a name="list_sprints"></a>
### Wyświetlenie listy sprint'ów

Za wyświetlenie listy sprintów odpowiedzialna jest funkcja `sprint.Sprint.Sprint.list_sprints()`, która wyświetla listę podzieloną na sprinty aktywne i nieaktywne.
Nieaktywny sprint to taki, którego data zakończenia jest późniejsza niż aktualna data.
Aktywne sprinty zwracane są przez funkcję `sprint.Sprint.Sprint.get_active_sprints()` natomiast nieaktywne prze 
`sprint.Sprint.Sprint.get_inactive_sprints()`. Obie funkcje korzystają z wyrażenia lambda wraz z metodą `filter()`. Wyrażenie lambda sprawdza datę zakończenia sprintu w porównaniu z aktualną datą.

Rezultaty obu funkcji są sortowane względem numeru sprintu od najnowszego do najstarszego.
Najpierw wyświetlane są sprintu aktywne, a następnie sptrintu nieaktywne.

<a name="sprint_board"></a>
### Wyświetlenie tablicy sprintu

Za wyświetlanide tablicy sprintu odpowiada funkcja `console_jira.show_sprint_board()`.

Najpierw pobierany jest numer sprint'u od użytkownika za pomocą funkcji `console_jira.choose_sprint()`, następnie ekstensja zadań jest filtrowana za pomocą wyrażenia lambda i metody `filter()`
w celu pobrania zadań posiadających wybrany numer sprint'u.
Tworzony jest słownik przechowujący pary `TaskStatus -> lista zadań` i w pętli przechodząc po wszystkich zadaniach słownik jest wypełniany.

Na końcu wyświetlana jest informacją w formacie

```
Typ_zadania:
Numer_zadania;Tytuł_zadania;Priorytet_zadania
...
```


