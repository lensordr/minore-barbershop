import sqlite3

def verify_database():
    conn = sqlite3.connect('barbershop.db')
    cursor = conn.cursor()
    
    # Check all main tables
    tables = ['barbers', 'services', 'appointments', 'daily_revenue', 'monthly_revenue']
    
    print("🔍 Database Status Check:")
    print("-" * 30)
    
    all_empty = True
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        status = "✅ Empty" if count == 0 else f"❌ Has {count} records"
        print(f"{table.capitalize()}: {status}")
        if count > 0:
            all_empty = False
    
    print("-" * 30)
    if all_empty:
        print("✅ Database is completely clean and ready for manual data entry!")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Go to: http://localhost:8000/admin/login")
        print("3. Login with: admin / minore123")
        print("4. Use Staff Management to add barbers and services")
    else:
        print("❌ Database still contains data. Run clear_database.py again.")
    
    conn.close()

if __name__ == "__main__":
    verify_database()