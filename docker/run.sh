# this command should work as long as pccfs2 is mounted onto the machine. If running somewhere else, change the volume mount to the partisan brain directory
docker run --gpus all -it \
	-v /mnt/pccfs2/backed_up/crytting/cs673:/cs673 \
	dockercc:latest