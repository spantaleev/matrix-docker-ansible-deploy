# Setting up postgres backup (optional)

The playbook can install and configure [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) for you.

## Adjusting the playbook configuration

| Name                              | Default value                | Description                                                      |
| :-------------------------------- | :--------------------------- | :--------------------------------------------------------------- |
|matrix_postgres_backaup_enabled|false|Set to true to use [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) to create automatic database backups|
|matrix_postgres_backup_schedule| '@daily' |Cron-schedule specifying the interval between postgres backups.|
|matrix_postgres_backup_keep_days|"7"|Number of daily backups to keep|
|matrix_postgres_backup_keep_weeks|"4"|Number of weekly backups to keep|
|matrix_postgres_backup_keep_months|"12"|Number of monthly backups to keep|
|matrix_postgres_backup_path | "{{ matrix_base_data_path }}/postgres-backup" | Storagepath for the database backups|
|matrix_postgres_backup_matrix_reminder_bot_enabled| false | Set to true to backup matrix_reminder_bot database. Per default matrix-reminder-bot uses an sqlite database. Only use this if you are using a postgres database for matrix-reminder-bot. |
|matrix_postgres_backup_matrix_appservice_discord_enabled| false | Set to true to backup matrix_appservice_discord database. Per default matrix_appservice_discord uses an sqlite database. Only use this if you are using a postgres database for matrix_appservice_discord. |
|matrix_postgres_backup_matrix_appservice_irc_enabled| false | Set to true to backup matrix_appservice_irc database. Per default matrix_appservice_irc uses an nedb database. Only use this if you are using a postgres database for matrix_appservice_irc. |
|matrix_postgres_backup_matrix_appservice_slack_enabled| false | Set to true to backup matrix_appservice_slack database. Per default matrix_appservice_slack uses an nedb database. Only use this if you are using a postgres database for matrix_appservice_slack. |
|matrix_postgres_backup_matrix_mautrix_facebook_enabled| false | Set to true to backup matrix_mautrix_facebook database. Per default matrix_mautrix_facebook uses an postgresned database. |
|matrix_postgres_backup_matrix_mautrix_hangouts_enabled| false | Set to true to backup _matrix_mautrix_hangouts database. Per default _matrix_mautrix_hangouts uses an sqlite database. Only use this if you are using a postgres database for _matrix_mautrix_hangouts. |
|matrix_postgres_backup_matrix_mautrix_signal_enabled| false | Set to true to backup matrix_mautrix_signal database. Per default matrix_mautrix_signal uses an postgres database.  |
|matrix_postgres_backup_matrix_mautrix_telegram_enabled| false | Set to true to backup matrix_mautrix_telegram database. Per default matrix_mautrix_telegram uses an sqlite database. Only use this if you are using a postgres database for matrix_mautrix_telegram. |
|matrix_postgres_backup_matrix_mautrix_whatsapp_enabled| false | Set to true to backup matrix_mautrix_whatsapp database. Per default matrix_mautrix_whatsapp uses an sqlite database. Only use this if you are using a postgres database for matrix_mautrix_whatsapp. |
|matrix_postgres_backup_matrix_mx_puppet_discord_enabled| false | Set to true to backup matrix_mx_puppet_discord database. Per default matrix_mx_puppet_discord uses an sqlite database. Only use this if you are using a postgres database for matrix_mx_puppet_discord. |
|matrix_postgres_backup_matrix_mx_puppet_instagram_enabled| false | Set to true to backup matrix_mx_puppet_instagram database. Per default matrix_mx_puppet_instagram uses an sqlite database. Only use this if you are using a postgres database for matrix_mx_puppet_instagram. |
|matrix_postgres_backup_matrix_mx_puppet_skype_enabled| false | Set to true to backup matrix_mx_puppet_skype database. Per default matrix_mx_puppet_skype uses an sqlite database. Only use this if you are using a postgres database for matrix_mx_puppet_skype. |
|matrix_postgres_backup_matrix_mx_puppet_slack_enabled| false | Set to true to backup matrix_mx_puppet_slack database. Per default matrix_mx_puppet_slack uses an sqlite database. Only use this if you 
|matrix_postgres_backup_matrix_mx_puppet_steam_enabled| false | Set to true to backup matrix_mx_puppet_steam database. Per default matrix_mx_puppet_steam uses an sqlite database. Only use this if you are using a postgres database for matrix_mx_puppet_steam. |
|matrix_postgres_backup_matrix_mx_puppet_twitter_enabled| false | Set to true to backup matrix_mx_puppet_twitter database. Per default matrix_mx_puppet_twitter uses an sqlite database. Only use this if you are using a postgres database for matrix_mx_puppet_twitter. |
|matrix_postgres_backup_matrix_dimension_enabled| false | Set to true to backup matrix_dimension database. Per default matrix_dimension uses an sqlite database. Only use this if you are using a postgres database for matrix_dimension. |
|matrix_postgres_backup_matrix_etherpad_enabled| false | Set to true to backup matrix_etherpad database. Per default matrix_etherpad uses an sqlite database. Only use this if you are using a postgres database for matrix_etherpad. |
|matrix_postgres_backup_matrix_ma1sd_enabled| false | Set to true to backup matrix_ma1sd database. Per default matrix_ma1sd uses an sqlite database. Only use this if you are using a postgres database for matrix_ma1sd. |
|matrix_postgres_backup_matrix_registration_enabled| false | Set to true to backup matrix_registration database. Per default matrix_registration uses an sqlite database. Only use this if you are using a postgres database for matrix_registration. |
|matrix_postgres_backup_matrix_synapse_enabled| true | Set to false to disabble backup of matrix_synapse database. |

## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```