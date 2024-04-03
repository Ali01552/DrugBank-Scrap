from syn import syn
import asyncio
from pandas import DataFrame
from bs4 import BeautifulSoup as bs
import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


f = os.path.abspath(__file__)
pp = os.path.dirname(f)

root = tk.Tk()
root.title("Data Scraper")

style = ThemedStyle(root)
style.set_theme("arc")  # You can change the theme here

# Create a frame for the log textbox and progress bar
frame = ttk.Frame(root)
frame.pack(expand=True, fill='both')

# Create a frame for the log textbox
log_frame = ttk.Frame(frame)
log_frame.pack(side='top', fill='both', expand=True)

log_label = ttk.Label(log_frame, text="Log:")
log_label.pack(pady=(10,0))

logbox = tk.Text(log_frame, width=40, height=5)
logbox.pack(fill='both', expand=True)

# Create a frame for the progress bar
progress_frame = ttk.Frame(frame)
progress_frame.pack(side='bottom', fill='x', padx=10, pady=10)

progress_label = ttk.Label(progress_frame, text="Scraping...")
progress_label.pack(side='left')

progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=220, mode='determinate')
progress.pack(side='left', padx=10, fill='x', expand=True)

data = {
    "Link": [],
    "GName": [],
    "Structure": [],
    "Description": []
    }


def log(msg, color=None):
    if color:
        logbox.tag_config(color, foreground=color)
        logbox.insert(tk.END, msg + '\n', color)
    else:
        logbox.insert(tk.END, msg + '\n')
    logbox.see(tk.END)
    root.update()


pages = []
l = "https://go.drugbank.com/drugs?approved=1&c=name&d=up&page="
for i in range(1,111):
    pages.append(l+str(i))

log("Downloading Data...","blue")
scr = syn(pages)
scr.main()
res = scr.results
log("OK..","green")    

async def pars_(r, p):                
    log(f"Parsing : {p}","blue")
    soup = bs(r, 'html.parser')
    links = ["https://go.drugbank.com"+l['href'] for l in soup.select('#drugs-table > tbody > tr > td.name-value.text-sm-center.drug-name > strong > a')]
    data["Link"]+=links
    strucs = ["https://go.drugbank.com"+l['href'] for l in soup.select('#drugs-table > tbody > tr > td.structure-value > a')]
    data["Structure"]+=strucs
    GNames = [l.text for l in soup.select('#drugs-table > tbody > tr > td.name-value.text-sm-center.drug-name > strong > a')]
    data["GName"]+=GNames
    desc = [l.text for l in soup.select('#drugs-table > tbody > tr > td.description-value')]
    data["Description"]+=desc
    progress['value'] += 1
    root.update()
    await asyncio.sleep(1)
    
async def main():
    tasks = [asyncio.create_task(pars_(r,p)) for r,p in zip(res,pages)]
    await asyncio.gather(*tasks)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
    
df = DataFrame(data)
df.to_csv(f"{pp}/basic_data.csv", index=False)
log(f"Data saved to {pp}/basic_data.csv", "green")
progress.destroy()
progress_label.config(text="Finished!")
root.quit()


root.mainloop()
