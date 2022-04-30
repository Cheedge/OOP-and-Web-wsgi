This is a mini Web Server use WSGI protocol
1. mini_oop_wsgi_server_v**:
	only use for communication with Browser and static/dynamic source
2. dynamic/wsgi_app_frame_v**:
	when Brower request for dynamic case, here means *.py(later will change)
	then Server will turn for help here.
	Let wsgi_app_frame to make the response BODY and return to Server
3. server_source_path.conf:
	store the static/dynamic source path to make Server to read
4. run.sh:
	run Server
5. 	
