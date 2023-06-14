import time
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from textblob import TextBlob

def clean_text(text):
    # Metin temizleme işlemlerini burada gerçekleştirin
    # Örneğin, noktalama işaretlerini kaldırabilir, küçük harfe çevirebilirsiniz
    # İsteğe bağlı olarak stop-words'leri kaldırabilir ve stemming işlemi yapabilirsiniz
    cleaned_text = text.lower().strip()
    return cleaned_text

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

url = 'https://www.cbc.ca/news'

# Selenium WebDriver'ı başlatma
driver = webdriver.Chrome()

# Sayfayı açma
driver.get(url)

# Sayfanın en altına kadar kaydırma işlemi
scroll_counter = 0
while scroll_counter < 8:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(4)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # Load More button'unun var olup olmadığını kontrol etme
        load_more_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'loadMore')]")
        if load_more_button:
            load_more_button[0].click()
            time.sleep(2)
            scroll_counter += 1
            continue
        else:
            break
    last_height = new_height

# Sayfanın kaynak kodunu alın
page_source = driver.page_source

# WebDriver'ı kapatma
driver.quit()

# BeautifulSoup ile işlem yapma
soup = BeautifulSoup(page_source, 'html.parser')
headlines = soup.find_all('h3', class_='headline')

# Başlıkları bir liste olarak saklama
headline_list = [headline.text.strip() for headline in headlines]

# Başlıkların duygu analizini yapma
results = []
for headline in headline_list:
    cleaned_headline = clean_text(headline)
    sentiment = analyze_sentiment(cleaned_headline)
    if sentiment > 0:
        tone = 'Positive'
    elif sentiment < 0:
        tone = 'Negative'
    else:
        tone = 'Neutral'
    results.append([headline, sentiment, tone])

# Sonuçları Excel dosyasına kaydetme
df = pd.DataFrame(results, columns=['Headline', 'Sentiment', 'Tone'])
df.to_excel('headline_sentiment_analysis.xlsx', index=False)

# Duygu analizi sonuçlarını görüntüleme
tone_counts = df['Tone'].value_counts()

# Çubuk grafik oluşturma
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.bar(tone_counts.index, tone_counts.values, color=['green', 'red', 'blue'])
plt.title('Haber Başlıklarının Duygu Analizi (Çubuk Grafik)')
plt.xlabel('Duygu Tonu')
plt.ylabel('Başlık Sayısı')

# Pasta grafik oluşturma
plt.subplot(1, 2, 2)
plt.pie(tone_counts.values, labels=tone_counts.index, autopct='%1.1f%%', colors=['green', 'red', 'blue'])
plt.title('Haber Başlıklarının Duygu Analizi (Pasta Grafik)')

# Grafikleri gösterme
plt.tight_layout()
plt.show()


# Başlık uzunluğu ve duygu ilişkisini analiz etme
headline_lengths = []
sentiments = []

for headline in headline_list:
    cleaned_headline = clean_text(headline)
    sentiment = analyze_sentiment(cleaned_headline)
    headline_lengths.append(len(cleaned_headline))
    sentiments.append(sentiment)

# Başlık uzunluğu ve duygu ilişkisini gösteren bir scatter plot oluşturme
plt.figure(figsize=(8, 6))
plt.scatter(headline_lengths, sentiments, alpha=0.5)
plt.title('Başlık Uzunluğu ve Duygu İlişkisi')
plt.xlabel('Başlık Uzunluğu')
plt.ylabel('Duygu Değerlendirmesi')
plt.show()






