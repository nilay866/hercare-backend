#!/bin/bash
# Add this to crontab: 0 2 * * * /home/ec2-user/backup_db.sh

BACKUP_DIR="/home/ec2-user/backups"
DB_HOST="hercare-db.cnwui00o4gn8.ap-south-1.rds.amazonaws.com"
DB_USER="postgres"
DB_NAME="postgres"
export PGPASSWORD="XeSHMfBOkK0cM4js" # In production, use .pgpass file

mkdir -p $BACKUP_DIR

# Create backup
FILENAME="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
echo "Backing up database to $FILENAME..."
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $FILENAME

# Keep only last 7 days
find $BACKUP_DIR -type f -name "*.sql" -mtime +7 -delete

echo "Backup complete."
