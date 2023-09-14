import sqlite3

# Read the contents of the file into the list
with open("stephen_king_adaptations.txt", "r") as file:
    stephen_king_adaptations_list = file.readlines()

# Remove the newline character at the end of each line
stephen_king_adaptations_list = [line.rstrip('\n') for line in stephen_king_adaptations_list]

# Connect to the SQLite database or create a new one if it does not exist
conn = sqlite3.connect("stephen_king_adaptations.db")
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
             (movieID TEXT PRIMARY KEY ,
              movieName TEXT,
              movieYear INTEGER,
              imdbRating REAL)''')

# Insert the content into the database table
for line in stephen_king_adaptations_list:
    movie = line.split(",")
    print("INSERT INTO stephen_king_adaptations_table (movieID,movieName, movieYear, imdbRating) VALUES (?, ?, ?,?)",
              (movie[0],movie[1],int(movie[2]), float(movie[3])))
    c.execute("INSERT INTO stephen_king_adaptations_table (movieID,movieName, movieYear, imdbRating) VALUES (?, ?, ?,?)",
              (movie[0],movie[1],int(movie[2]), float(movie[3])))
    # insert_statement = f"INSERT INTO stephen_king_adaptations_table (movieID,movieName, movieYear, imdbRating) VALUES (?, ?, ?,?)"
    #
    # c.execute(insert_statement, (movie[0],movie[1],int(movie[2]),float(movie[3])))
# Commit the changes and close the database connection
conn.commit()
conn.close()

# Search movie function
def search_movies(option):
    conn = sqlite3.connect("stephen_king_adaptations.db")
    c = conn.cursor()

    if option == 1:
        movie_name = input("Please enter the name of the movie you want to search：")
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
    elif option == 2:
        movie_year = int(input("Please enter the year of the movie you want to search："))
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
    elif option == 3:
        rating = float(input("Please enter the movie rating you want to search for："))
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))

    movies = c.fetchall()

    if not movies:
        print("We couldn't find any movies in our database that fit the criteria.")
    else:
        for movie in movies:
            print("Title of movie：", movie[1])
            print("Year：", movie[2])
            print("Scoring：", movie[3])
            print()

    conn.close()


# 用户交互界面
while True:
    print("Please select parameters for searching movies：")
    print("1. Title of movie")
    print("2. Year")
    print("3. Scoring")
    print("4. Stop")
    option = int(input("Please enter options："))

    if option == 4:
        break

    search_movies(option)
