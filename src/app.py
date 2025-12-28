
"""
OLD CODE
from src.db.Connection_Manager import create_db_connection
from analytics.queries import total_games, top_openings

def main():
    conn = create_db_connection(1,2,3,4)

    print("Total games:", total_games(conn))

    for row in top_openings(conn)[:5]:
        print(row)

    conn.close()

    # Check if it’s closed
    if not conn.is_connected():
        print("Connection successfully closed.")
    else:
        print("Connection is still open!")

if __name__ == "__main__":
    main()
"""
