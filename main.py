import json
from datetime import datetime, timedelta

FILE_NAME = 'shopping_list.json'

# JSON 

def save_items(items):
    with open(FILE_NAME, 'w') as f:
        json.dump(items, f, indent=4)

def load_items():
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
            if not all(isinstance(item, dict) and {'name', 'expiry', 'quantity', 'category'} <= item.keys() for item in data): # Ja kaut kas nav ar JSON failu, tad outputo tālak redzamo message.
                print("❗ Kļūda: JSON fails satur nederīgus ierakstus. Tiek ielādēts tukšs saraksts.")
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ JSON fails nav atrasts vai ir bojāts. Tiek ielādēts tukšs saraksts.")
        return []


# INPUT PARBAUDE

def input_integer(prompt):
    while True:
        value = input(prompt)
        if value.isdigit(): #parbaude vai value ir cipars
            return int(value)
        else:
            print("❗ Jāievada skaitlis!")

def input_date():
    while True:
        try:
            day = input_integer("Ievadi dienu (1–31): ")
            month = input_integer("Ievadi mēnesi (1–12): ")
            year = input_integer("Ievadi gadu (piem. 2025): ")
            return datetime(year, month, day).date()
        except ValueError:
            print("❗ Nederīgs datums. Mēģini vēlreiz.")

def input_category():
    categories = load_categories()
    print("Pieejamās kategorijas:")
    for i, categorija in enumerate(categories, 1): #katram elementam piešķir kārtas nummuru (i), enumerate sāk ar 1. locekli
        print(f"{i}. {categorija}")
    print(f"{len(categories)+1}. Jauna kategorija")

    choice = input_integer("Izvēlies kategoriju: ")
    if 1 <= choice <= len(categories): #pārbaude vai choice ir lielāks vai vienāds ar 1 un mazāk vai vienāds ar categories
        return categories[choice-1]
    elif choice == len(categories) + 1: #ja pirmais if nosacījums neizpildas, tad
        new_category = input("Ievadi jauno kategoriju: ")
        categories.append(new_category)
        save_categories(categories)
        return new_category
    else:
        print("❗ Nederīga izvēle. Izvēlēta noklusējuma kategorija 'Cits'.")
        return "Cits"

CATEGORY_FILE = 'categories.json'

def save_categories(categories):
    with open(CATEGORY_FILE, 'w') as f:
        json.dump(categories, f, indent=4)

def load_categories():
    try:
        with open(CATEGORY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return ["Saldētava", "Ledusskapis", "Skapītis"]


# MENU FUNKCIJAS

def add_item():
    name = input("Produkta nosaukums: ")
    expiry = input_date()

    if expiry < datetime.today().date(): #pārbauda vai derīguma termiņš nav jau beidzies
        print("❌ Produkta derīguma termiņš jau ir pagājis! Šo produktu vajadzētu izmest.\n")
        return

    quantity = input_integer("Daudzums: ")
    category = input_category()

    items = load_items()
    items.append({"name": name, "expiry": expiry.isoformat(), "quantity": quantity, "category": category})
    save_items(items)
    print("✅ Produkts pievienots!\n")

def view_items():
    items = load_items()
    if not items: #Ja nav ko rādīt printē sekojošo message
        print("📭 Saraksts ir tukšs.\n")
        return

    print("\n🧾 Produktu saraksts:")
    for i, item in enumerate(items, 1): #piešķir katram loceklim savu kārtas nr (i), enumerate nodrošina ka sākas ar 1.
        print(f"{i}. {item['name']} – Derīguma termiņš: {item['expiry']} – Daudzums: {item['quantity']} – Kategorija: {item['category']}")
    print()

def remove_item():
    items = load_items()
    if not items: #Ja saraksts ir tukšs returno sekojošo message
        print("📭 Nav ko izņemt.\n")
        return

    print("\nIzvēlies produktu ko izņemt:")
    for i, item in enumerate(items, 1): #piešķir katram loceklim savu kārtas nr (i), enumerate nodrošina ka sākas ar 1.
        print(f"{i}. {item['name']} (x{item['quantity']}) – {item['category']}")

    index = input_integer("Ievadi produkta numuru: ") - 1

    if 0 <= index < len(items): #pārbaude vai index ir derīgs saraksta items indekss
        selected_item = items[index]

        print("1. Noņemt no konkrētās kategorijas")
        print("2. Dzēst pilnībā")
        option = input_integer("Izvēlies darbību: ")

        if option == 1 and selected_item['quantity'] > 1: #ja izvēlas opciju 1 
            to_remove = input_integer(f"Cik daudz no '{selected_item['name']}' izņemt? (1–{selected_item['quantity']}): ")
            if to_remove < selected_item['quantity']: #pārbauda vai negrib noņemt vairāk nekā ir
                items[index]['quantity'] -= to_remove
            else:
                items.pop(index)
        elif option == 2: #ja izvelas 2 opciju
            items.pop(index)
        else:
            print("❗ Nederīga izvēle vai daudzums. Produkts netika izņemts.")
            return

        save_items(items)
        print("🗑️ Produkts izņemts.\n")
    else:
        print("❗ Nederīgs produkta numurs.\n")

def manage_categories():
    categories = load_categories()
    print("\nKategoriju saraksts:")
    for i, cat in enumerate(categories, 1): #piešķir katram loceklim savu kārtas nr (i), enumerate nodrošina ka sākas ar 1.
        print(f"{i}. {cat}")
    print("a. Pievienot kategoriju")
    print("b. Dzēst kategoriju")

    choice = input("Izvēlies darbību: ")
    if choice == 'a': #ja ir izveleta opcija a
        new_category = input("Ievadi jaunas kategorijas nosaukumu: ")
        if new_category not in categories: #ja jauna kategorija nav kategoriju sraksta
            categories.append(new_category) #pievieno to
            save_categories(categories) #saglaba
            print("✅ Kategorija pievienota.\n")
    elif choice == 'b': #ja ir izveleta opcija b
        index = input_integer("Ievadi dzēšamās kategorijas numuru: ") - 1
        if 0 <= index < len(categories): #parbauda vai indekss nav mazaks, vienads ar 0, ja ir tad dara sekojošo
            cat_to_remove = categories[index]
            categories.pop(index)
            save_categories(categories)
            print(f"❌ Kategorija '{cat_to_remove}' dzēsta.\n")
        else:
            print("❗ Nederīgs kategorijas numurs.\n")
    else:
        print("❗ Nederīga izvēle.\n")

def remind_items():
    today = datetime.today().date()
    items = load_items()
    reminders = []

    for item in items: #visos items kopumā items mēģināt sekojošo
        try:
            expiry = datetime.strptime(item['expiry'], "%Y-%m-%d").date()
            days_left = (expiry - today).days
            if days_left <= 2: #parbauda vai deriguma termins ir mazaks, vienads ar 2
                reminders.append((item['name'], item['quantity'], expiry, days_left))
        except ValueError:
            print(f"⚠️ Nederīgs derīguma termiņš produktam: {item.get('name', 'nezināms')}")

    if reminders: #ja ir atgadinajums tad izprinte sekojoso
        print("\n⏰ Produkti ar tuvojošos vai nokavētu derīguma termiņu:")
        for name, quantity, expiry, days_left in reminders: #norāda ar kuriem elementiem tiks strādāts, lai kods saprastu ar ko tiek veiktas darbības.
            status = "NOKAVĒTS" if days_left < 0 else f"{days_left} dienas palikušas"
            print(f"- {name} (x{quantity}) – Derīguma termiņš: {expiry} ({status})")
        print()
    else:
        print("✅ Visiem produktiem derīguma termiņš ir kārtībā.\n")

def check_today_date():
    print("📅 Šodienas datums ir:", datetime.today().strftime("%Y-%m-%d"), "\n")


# INTERFEIS

def home_screen():
    while True:
        print("✨ Izvēlies darbību:")
        print("◾ 1. Pievienot produktu")
        print("◾ 2. Apskatīt produktus")
        print("◾ 3. Noņemt produktu")
        print("◾ 4. Atgādināt par produktiem ar tuvojošos derīguma termiņu")
        print("◾ 5. Pārbaudīt šodienas datumu")
        print("◾ 6. Pārvaldīt kategorijas")
        print("◾ 7. Iziet")

        choice = input("Ievadi izvēles numuru: ")

        if choice == "1": #ja ir izveleta dota opcija, tad dara sekojoso
            add_item()
        elif choice == "2": #ja ir izveleta dota opcija, tad dara sekojoso
            view_items()
        elif choice == "3": #ja ir izveleta dota opcija, tad dara sekojoso
            remove_item()
        elif choice == "4": #ja ir izveleta dota opcija, tad dara sekojoso
            remind_items()
        elif choice == "5": #ja ir izveleta dota opcija, tad dara sekojoso
            check_today_date()
        elif choice == "6": #ja ir izveleta dota opcija, tad dara sekojoso
            manage_categories()
        elif choice == "7": #ja ir izveleta dota opcija, tad dara sekojoso
            print("👋 Uz redzēšanos!")
            break
        else:
            print("❗ Nederīga izvēle. Mēģini vēlreiz.\n")

if __name__ == "__main__": #iesledz kodu
    home_screen()

