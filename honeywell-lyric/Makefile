DEFAULT_MATS_DIR = $(HOME)/Documents/mats
WHO_AM_I = $(USER)

install:
	if [ -d "$(DEFAULT_MATS_DIR)" ]; then \
		echo "OK"; \
		if [ ! -f "$(DEFAULT_MATS_DIR)/android_ipython_honeywell_lyric.py" ]; then \
			cat ./mats/android_ipython_honeywell_lyric.py | sed -e 's/whoami/$(WHO_AM_I)/g' > $(DEFAULT_MATS_DIR)/android_ipython_honeywell_lyric.py; \
		fi; \
		if [ ! -f "$(DEFAULT_MATS_DIR)/ios_ipython_honeywell_lyric.py" ]; then \
			cat ./mats/ios_ipython_honeywell_lyric.py | sed -e 's/whoami/$(WHO_AM_I)/g' > $(DEFAULT_MATS_DIR)/ios_ipython_honeywell_lyric.py; \
		fi; \
		if [ ! -f "$(DEFAULT_MATS_DIR)/etc/projects/honeywell_lyric.json" ]; then \
			cat ./mats/honeywell_lyric.json | sed -e 's/whoami/$(WHO_AM_I)/g' > $(DEFAULT_MATS_DIR)/etc/projects/honeywell_lyric.json; \
		fi; \
		echo "Usage: go to your mats folder and start ipython. Type in:"; \
		echo "    from android_ipython_honeywell_lyric import *; flow, device, data=get_flow(); f=self=flow; d=device"; \
		echo "        or: "; \
		echo "    from ios_ipython_honeywell_lyric import *; flow, device, data=get_flow(); f=self=flow; d=device"; \
	fi
