
Create a Python Environment and activate it:
```bash 
    virtualenv spacy --python=python3
    cd ./scpay
    source bin/activate
```

Install the required dependencies.
```bash
pip install -r requirements.txt
```

Download spacy model:
```bash
python -m spacy download es_core_news_lg
```

Download wordnet in spanish:
```bash
wget -O anotar.zip "https://drive.google.com/uc?export=download&id=1iqq8MGOx7WwaBEHNM2ZvC7zRTFaP4dlh"
unzip anotar.zip
co anotar data
rm anotar.zip
```

Download wordnet in spanish:


### Contacts:
If you have any questions please contact the authors.   
  * Robiert Sepúlveda Torres rsepulveda911112@gmail.com 

  
### License:
  * Apache License Version 2.0 