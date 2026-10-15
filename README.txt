SKILLPATH BLACK + YELLOW — WINDOWS SETUP
========================================
1. Extract this ZIP into your existing project folder:
   C:\Users\imru\Videos\Desktop\courserecommder
   Allow it to replace app.py, templates and static files with these new versions.
2. Keep your .env in the same folder as app.py. It should contain:
   SECRET_KEY=some-long-random-secret
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=skillapp
   MYSQL_PASSWORD=the exact password that successfully connected for skillapp
   MYSQL_DB=skill_course_db
   Do not add quotes. Do not share your .env file.
3. Open VS Code in that folder. PowerShell:
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
4. Open MySQL Workbench, connect to local MySQL, open schema.sql, press the lightning bolt Run button.
5. Stop the old Flask server in VS Code terminal with Ctrl+C.
6. Run: python app.py
7. Open one browser tab at: http://127.0.0.1:5000
   Keep the terminal running while using the site.
Pages: Home -> Register -> Login -> Dashboard; Dashboard -> Courses / Analytics.
All links are normal Flask routes and navigate in the same tab.
Do not open HTML files by double-clicking; Flask renders templates.
If port is already used, stop the old server with Ctrl+C.
If Google Fonts are blocked, the site uses fallback fonts.
