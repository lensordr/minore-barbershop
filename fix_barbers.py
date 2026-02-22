from database_postgres import get_db
import models

db = next(get_db())

# Fix Cristian's trailing space
cristian = db.query(models.Barber).filter(models.Barber.name.like('Cristian%')).first()
if cristian:
    print(f"Found: '{cristian.name}' (id={cristian.id})")
    cristian.name = cristian.name.strip()
    db.commit()
    print(f"Fixed to: '{cristian.name}'")

# Check Luca's early access settings
luca = db.query(models.Barber).filter(models.Barber.name == 'Luca').first()
if luca:
    print(f"\nLuca (id={luca.id}):")
    print(f"  early_access_enabled: {luca.early_access_enabled}")
    print(f"  early_access_price_add: {luca.early_access_price_add}")
    if not luca.early_access_enabled:
        print("  WARNING: Early access is DISABLED for Luca!")

# List all barbers with early access
print("\n=== All Barbers with Early Access ===")
barbers = db.query(models.Barber).filter(models.Barber.early_access_enabled == 1).all()
for b in barbers:
    print(f"  {b.name}: +€{b.early_access_price_add}")

db.close()
