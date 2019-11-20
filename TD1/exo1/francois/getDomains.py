import os

domains = []

for name in os.listdir("D:/DocumentsHDD/M2/WebScraping/Corpus_detourage/html"):
    domain = name.split('/')[-1].split('_')[1].split('.')[-1]
    if domain not in domains:
        domains.append(domain)
    
for domain in sorted(domains):
    print(domain)