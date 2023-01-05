# Endpoint update

https://github.com/yassineaouam/matrix-docker-ansible-deploy/roles/custom/matrix-synapse/templates/synapse/ext/s3-storage-provider/env.j2

    {% if matrix_synapse_ext_synapse_s3_storage_provider_config_endpoint_url %}
    ENDPOINT={{ matrix_synapse_ext_synapse_s3_storage_provider_config_endpoint_url }}
    {% endif %}

- there is a condition on the matrix_synapse_ext_synapse_s3_storage_provider_config_endpoint_url variable so that if we set a value in the vars file, it's going to be affected to it.
If not, there won't be any need for the variable endpoints_url: '' to be shown with an empty field. 


# Serching users update

https://github.com/yassineaouam/matrix-docker-ansible-deploy/roles/custom/matrix-synapse/templates/synapse/homeserver.yaml.j2

    {% if matrix_synapse_config_search_all_users %}
    search_all_users: {{ matrix_synapse_config_search_all_users  }}
    {% endif %}

- This parameter allows us to search for users with only the first characters of the user's names.
Once you write the first character, options starting with that character begin to appear.


# log drive update

https://github.com/yassineaouam/matrix-docker-ansible-deploy/roles/custom/matrix-synapse/templates/synapse/systemd/matrix-synapse-worker.service.j2

https://github.com/yassineaouam/matrix-docker-ansible-deploy/roles/custom/matrix-synapse/templates/goofys/systemd/matrix-goofys.service.j2

	{% if matrix_synapse_log_driver %}
	--log-driver={{ matrix_synapse_log_driver }} \
	{% else %}
	--log-driver=none \
	{% endif %}
    
- I applied another condition on the --log-drive. If matrix_synapse_log_driver has a specific value, it should automatically be affected to the --log-drive. Else, it will get a none.