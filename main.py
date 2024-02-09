import requests
import random
import os

def download_all_comments(video_id):
    api_key = "YOUR_YOUTUBE_API_KEY"  # Replace this with your own YouTube API key
    comments = []
    next_page_token = None

    while True:
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100"
        if next_page_token:
            url += f"&pageToken={next_page_token}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            comments += [(item['snippet']['topLevelComment']['snippet']['textDisplay'], item['snippet']['topLevelComment']['snippet']['authorDisplayName']) for item in data['items']]
            if 'nextPageToken' in data:
                next_page_token = data['nextPageToken']
            else:
                break
        else:
            print("Failed to download comments.")
            return []

    return comments

def filter_comments(comments, filter_text):
    filtered_comments = [(comment, username) for comment, username in comments if filter_text.lower() in comment.lower()]
    return filtered_comments

def select_random_comments(comments, num_comments):
    random_comments = random.sample(comments, min(num_comments, len(comments)))
    return random_comments

def save_comments_to_file(comments, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for comment, username in comments:
            file.write(f"{username}: {comment}\n")

def load_blacklist(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r', encoding='utf-8') as file:
        return set(file.read().splitlines())

def save_to_blacklist(username, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(username + '\n')

def main():
    video_link = input("Podaj link do filmu na YouTube: ")
    video_id = video_link.split("v=")[1]

    comments = download_all_comments(video_id)
    if not comments:
        print("Nie udało się pobrać żadnych komentarzy.")
        return

    print(f"Liczba pobranych komentarzy: {len(comments)}")

    filter_option = input("Czy chcesz filtrować komentarze? (T/N): ")
    if filter_option.lower() == 't':
        filter_text = input("Podaj tekst do filtrowania komentarzy: ")
        comments = filter_comments(comments, filter_text)
        print(f"Liczba komentarzy po filtrowaniu: {len(comments)}")

    num_comments_to_select = int(input("Podaj ilość komentarzy do wylosowania: "))

    blacklist_filename = "bialalista.txt"
    blacklist = load_blacklist(blacklist_filename)

    selected_comments = select_random_comments(comments, num_comments_to_select)
    for comment, username in selected_comments:
        if username not in blacklist:
            print(f"Użytkownik: {username}")
            print(f"Komentarz: {comment}\n")
            save_to_blacklist(username, blacklist_filename)

    print("Pomyślnie zapisano wylosowanych użytkowników do pliku.")

if __name__ == "__main__":
    main()
