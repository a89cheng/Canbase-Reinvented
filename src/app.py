from db.connection import create_db_connection
from analytics.queries import total_games, top_openings

def main():
    conn = create_db_connection(1,2,3,4)

    print("Total games:", total_games(conn))

    for row in top_openings(conn)[:5]:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()
