# Deployment of the Model

Um das Model nutzbar zu machen, muss lediglich der Python Flask Server gestartet werden.<br>
Dann ist eine API erreichbar die, Überschriften entgegennimmt und die Entwicklung des Aktienkurses vorhersagt.<br>

## Die API
Erreichen Sie die API durch einen HTTP-POST auf <b>/predict</b> um eine Vorhersage der Aktienpreisentwicklung auf Grundlage der übergebenen Überschrift einer Aktiennews zu erhalten.<br><br>
Übergeben Sie die Headline per <code>POST, application/json</code> in folgender Form: <br> <code>{<br/>'headlines': ['Dies ist eine Headline.', 'Dies ist noch eine Headline!']<br/>}</code><br/><br/>Die Antwort erfolgt ebenfalls per JSON in folgender Form: <br/> <code>{<br/>'prediction': -0.627, <br/>'stockChange': -1 <br/>}</code>

## Installations
### Docker
Simply run the following: <br>
<code>docker compose -f docker-compose.yml up</code>
The API runs on an Nginx-Server with uWSGI on Port 80.

#### CleanUp
To Shutdown and CleanUp simply run:<br>
<code>docker compose -f docker-compose.yml down</code>

### Local
If you prefer to run our API lokal, which is not recommended, you can do it also very easily.<br>
When the API runs local it only has the flask-development-server.<br>
* Change the path of the 'model.pkl' in the 'development.py' to your path.
* run <code>python deployment.py</code>
<br>
The Dev-Server is Running on http://127.0.0.1:80
<br>
You can also turn on Debugging by changing the '__develop__' variable to True. The Server will then Run on Port 8080.