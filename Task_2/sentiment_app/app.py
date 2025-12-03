from flask import Flask,render_template, request
from textblob import TextBlob
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io,base64

app=Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c=conn.cursor()
    c.execute("""
CREATE TABLE IF NOT EXISTS analysis (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              text TEXT,
              sentiment TEXT,
              polarity REAL,
              subjectivity REAL
              )"""
        )
    conn.commit()
    conn.close()

init_db()

def save_analysis(text,sentiment,polarity,subjectivity):
    conn=sqlite3.connect("database.db")
    c=conn.cursor()
    c.execute("""
        INSERT INTO analysis(text, sentiment, polarity, subjectivity)
        VALUES (?, ?, ?, ?)
    """,(text,sentiment,polarity,subjectivity))
    conn.commit()
    conn.close()

def generate_plot(polarity,subjectivity):
    plt.figure(figsize=(4,3))
    plt.bar(["Polarity","Subjectivity"],[polarity,subjectivity])
    plt.title("Sentiment Metrics")
    plt.tight_layout()

    img  = io.BytesIO()
    plt.savefig(img,format="png",bbox_inches="tight")
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/analyze",methods=["POST"])
def analyze():
    text=request.form["user_text"]

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment = "Positive 😊"
    elif polarity < 0:
        sentiment = "Negative 😞"
    else:
        sentiment = "Neutral 😐"
    
    save_analysis(text,sentiment,polarity,subjectivity)

    graph = generate_plot(polarity,subjectivity)

    return render_template("result.html",
                           text=text,
                           sentiment=sentiment,
                           polarity=polarity,
                           subjectivity=subjectivity,
                           graph=graph)
if __name__=="__main__":
    app.run(debug=True)


