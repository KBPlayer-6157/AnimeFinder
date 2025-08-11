import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import io

anime_list = []

def search_anime():
    anime_name = entry.get().strip()
    if not anime_name:
        messagebox.showwarning("Input Error", "Please enter an anime name!")
        return

    url = f"https://kitsu.io/api/edge/anime?filter[text]={anime_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        anime_list.clear()
        result_list.delete(*result_list.get_children())

        if data["data"]:
            for anime in data["data"]:
                title = anime["attributes"].get("titles", {}).get("en_jp", "Unknown Title")
                anime_list.append(anime)
                result_list.insert("", tk.END, values=(title,))
        else:
            messagebox.showinfo("No Results", "No anime found with that name.")
    else:
        messagebox.showerror("Error", f"Failed to fetch data. Status Code: {response.status_code}")

def show_details(event):
    selected_item = result_list.selection()
    if not selected_item:
        return

    index = result_list.index(selected_item)
    anime = anime_list[index]["attributes"]

    title = anime.get("titles", {}).get("en_jp", "Unknown Title")
    synopsis = anime.get("synopsis", "No description available.")
    anime_type = anime.get("subtype", "Unknown")
    start_date = anime.get("startDate", "Unknown")
    episodes = anime.get("episodeCount", "Unknown")
    poster_url = anime.get("posterImage", {}).get("medium", "")

    details_text = (
        f"Title: {title}\n"
        f"Type: {anime_type}\n"
        f"Start Date: {start_date}\n"
        f"Episodes: {episodes}\n\n"
        f"Synopsis:\n{synopsis}"
    )

    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, details_text)
    output_box.config(state=tk.DISABLED)

    if poster_url:
        img_response = requests.get(poster_url)
        if img_response.status_code == 200:
            img_data = img_response.content
            pil_image = Image.open(io.BytesIO(img_data))
            pil_image = pil_image.resize((150, 220))
            img = ImageTk.PhotoImage(pil_image)
            poster_label.config(image=img)
            poster_label.image = img
        else:
            poster_label.config(image="", text="No Image Available")
    else:
        poster_label.config(image="", text="No Image Available")

win = tk.Tk()
win.title("Anime Finder App with Wallpaper")
win.geometry("900x650")

wallpaper = Image.open(r"C:\Users\relen\Documents\Anime.png")
wallpaper = wallpaper.resize((1550, 950))
bg_image = ImageTk.PhotoImage(wallpaper)
bg_label = tk.Label(win, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = tk.Label(win, text="Anime Finder", font=("Arial", 20, "bold"), fg="white", bg="#000000")
title_label.pack(pady=10)

search_frame = tk.Frame(win)
search_frame.pack(pady=5)

entry = tk.Entry(search_frame, font=("Arial", 14), width=40)
entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#ff4f5a", fg="white",
                       activebackground="#ff9999", command=search_anime)
search_btn.pack(side=tk.LEFT, padx=5)

result_frame = tk.Frame(win)
result_frame.pack(pady=10)

columns = ("Title",)
result_list = ttk.Treeview(result_frame, columns=columns, show="headings", height=10)
result_list.heading("Title", text="Search Results (Click to view details)")
result_list.column("Title", width=400)
result_list.bind("<<TreeviewSelect>>", show_details)
result_list.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_list.yview)
result_list.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

details_frame = tk.Frame(win)
details_frame.pack(pady=10)

poster_label = tk.Label(details_frame)
poster_label.pack(side=tk.LEFT, padx=10)

output_box = tk.Text(details_frame, wrap=tk.WORD, font=("Arial", 12), width=50, height=15, state=tk.DISABLED, bg="#f5f5f5")
output_box.pack(side=tk.LEFT, padx=10)

win.mainloop()