# Add new user
python src/utils/db_manager.py --add-user "new_admin" "securepass123" "admin2@company.com"

# View database stats
python src/utils/db_manager.py --stats

# Reset database
python src/utils/db_manager.py --reset

# Export logs
python src/utils/db_manager.py --export 