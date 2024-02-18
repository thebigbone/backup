if [ ! -d "server-backup" ]; then
	restic -r server-backup init
fi

if [ ! -d "server-backup-copy" ]; then
	restic -r server-backup-copy init
fi

restic -r server-backup backup . --exclude-file=excludes.txt
restic copy -r server-backup --repo2 server-backup-copy --password-command2="echo $RESTIC_PASSWORD2"
restic -r server-backup forget --keep-daily 5

